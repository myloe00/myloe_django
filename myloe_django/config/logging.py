import os
import sys
import time
import logging
from logging.handlers import TimedRotatingFileHandler


class CommonTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
        多进程的支持
    """
    @property
    def dfn(self):
        currentTime = int(time.time())
        # get the time that this sequence started at and make it a TimeTuple
        dstNow = time.localtime(currentTime)[-1]
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
    def filter(self, record):
        print("xxxx")
        return True

LOG_PATH = "./logs/"
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)
LOGGING = {
    'version': 1,  #使用的python内置的logging模块，那么python可能会对它进行升级，所以需要写一个版本号，目前就是1版本
    'disable_existing_loggers': False, #是否去掉目前项目中其他地方中以及使用的日志功能，但是将来我们可能会引入第三方的模块，里面可能内置了日志功能，所以尽量不要关闭。
    'formatters': { #日志记录格式
        'standard': { #levelname等级，asctime记录时间，module表示日志发生的文件名称，lineno行号，message错误信息
            'format': '%(process)d %(processName)s %(thread)d %(threadName)s %(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            # 'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
            'format': '%(process)d %(processName)s %(thread)d %(threadName)s %(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': { #过滤器：可以对日志进行输出时的过滤用的
        'require_debug_true': { #在debug=True下产生的一些日志信息，要不要记录日志，需要的话就在handlers中加上这个过滤器，不需要就不加
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': { #和上面相反
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'filter_path':{
            'filter_path': PathFilter
        }
    },
    'handlers': { #日志处理方式，日志实例,向哪里输出
        'console': {  # 流处理器(控制台)，所有的高于(包括)debug的消息会被传到stderr，使用的是simple格式器
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'info': {
            'level': 'INFO',
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
            'filters': [],# 注意过滤器要写全，不要遗漏
            'when': 'midnight',
            'interval': 1,
            'backupCount': 60,
            'formatter': 'standard',
        }
    },
    # 日志对象
    'loggers': {
        'django': {  #和django结合起来使用，将django中之前的日志输出内容的时候，按照我们的日志配置进行输出，
            'handlers': ['console', 'info', 'error'], #将来项目上线，把console去掉
            'propagate': True, #冒泡：是否将日志信息记录冒泡给其他的日志处理系统，工作中都是True，不然django这个日志系统捕获到日志信息之后，其他模块中可能也有日志记录功能的模块，就获取不到这个日志信息了
        },
        'root': {  # 和django结合起来使用，将django中之前的日志输出内容的时候，按照我们的日志配置进行输出，
            'handlers': ['console', 'info', 'error'],  # 将来项目上线，把console去掉
            'propagate': True,
            # 冒泡：是否将日志信息记录冒泡给其他的日志处理系统，工作中都是True，不然django这个日志系统捕获到日志信息之后，其他模块中可能也有日志记录功能的模块，就获取不到这个日志信息了
        },
    }
}