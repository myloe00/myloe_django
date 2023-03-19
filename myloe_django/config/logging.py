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
    },
    'handlers': { #日志处理方式，日志实例,向哪里输出
        'console': { #在控制台输出时的实例
            'level': 'DEBUG', #日志等级；debug是最低等级，那么只要比它高等级的信息都会被记录
            'filters': ['require_debug_true'], #在debug=True下才会打印在控制台
            'class': 'logging.StreamHandler', #使用的python的logging模块中的StreamHandler来进行输出
            'formatter': 'simple'
        },
    },
    # 日志对象
    'loggers': {
        'django': {  #和django结合起来使用，将django中之前的日志输出内容的时候，按照我们的日志配置进行输出，
            'handlers': ['console'], #将来项目上线，把console去掉
            'propagate': True, #冒泡：是否将日志信息记录冒泡给其他的日志处理系统，工作中都是True，不然django这个日志系统捕获到日志信息之后，其他模块中可能也有日志记录功能的模块，就获取不到这个日志信息了
        },
    }
}