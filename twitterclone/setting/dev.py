from base import *

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(funcName)s() %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(module)s.%(filename)s::%(funcName)s() (%(lineno)d) %(message)s'
        },
    },
    'handlers': {
        'file_accounts': {
            'level': 'DEBUG',
            'formatter': 'simple',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'accounts.log'),
            'maxBytes': 100*1024,
            'backupCount': 5
        },
        'file_tweet': {
            'level': 'DEBUG',
            'formatter': 'simple',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'tweet.log'),
            'maxBytes': 100*1024,
            'backupCount': 5
        },
    },
    'loggers': {
        'logview.accounts': {
            'handlers': ['file_accounts'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'logview.accounts': {
            'handlers': ['file_tweet'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
