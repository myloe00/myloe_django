import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import getLogger


def myloe_logger(name=None):
    name = name or 'myloe_django'
    return getLogger(name)


# todo 针对非本应用的默认logger也会使用myloe_django的logger, 其他方案？
logging.getLogger = myloe_logger


class CommonTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
        多进程的支持
    """
    @property
    def dfn(self):
        current_time = int(time.time())
        # get the time that this sequence started at and make it a TimeTuple
        dstNow = time.localtime(current_time)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.rotation_filename(self.baseFilename + "." + time.strftime(self.suffix, timeTuple))
        return dfn

    def shouldRollover(self, record):
        """
        是否应该执行日志滚动操作：
        1、存档文件已存在时，执行滚动操作
        2、当前时间 >= 滚动时间点时，执行滚动操作
        """
        dfn = self.dfn
        t = int(time.time())
        if t >= self.rolloverAt or os.path.exists(dfn):
            return 1
        return 0

    def doRollover(self):
        """
        执行滚动操作
        1、文件句柄更新
        2、存在文件处理
        3、备份数处理
        4、下次滚动时间点更新
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        dfn = self.dfn
        # 存档log 已存在处理
        if not os.path.exists(dfn):
            self.rotate(self.baseFilename, dfn)
        # 备份数控制
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        # 延迟处理
        if not self.delay:
            self.stream = self._open()
        # 更新滚动时间点
        currentTime = int(time.time())
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            dstNow = time.localtime(currentTime)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt


class PathFilter(logging.Filter):
    PATH = ['/system/login']

    def filter(self, record):
        if record.filename == 'basehttp.py':
            for path in self.PATH:
                if path in record.args[0]:
                    return False
        return True


LOG_PATH = "./logs/"
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(name)s|%(process)d %(processName)s %(thread)d %(threadName)s %(levelname)s %(asctime)s %(pathname)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'filter_path': {
            '()': PathFilter
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'filters': ['filter_path'],
        },
        'info': {
            'level': 'DEBUG',
            'class': 'myloe_django.config.logging.CommonTimedRotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'info.log'),
            'filters': ['filter_path'],
            'when': 'midnight',
            'interval': 1,
            'backupCount': 60,
            'formatter': 'standard',
        },
        'error': {
            'level': 'ERROR',
            'class': 'myloe_django.config.logging.CommonTimedRotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'error.log'),
            'filters': [],
            'when': 'midnight',
            'interval': 1,
            'backupCount': 60,
            'formatter': 'standard',
        }
    },
    # 日志对象
    'loggers': {
        'django': {
            'handlers': ['console', 'info', 'error'],
            'propagate': True,
        },
        'myloe_django': {
            'handlers': ['console', 'info', 'error'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console', 'info', 'error'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
