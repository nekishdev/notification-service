import logging.config

DEBUG = True

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DEFAULT_HANDLERS = [
    "console",
]

level = "NOTSET" if DEBUG else "WARNING"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(name)s %(lineno)d " "%(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "%(message)s",
        },
    },
    "handlers": {
        "logfile": {
            "formatter": "default",
            "level": level,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "working.log",
            "backupCount": 7,
            "maxBytes": 5_242_880,
        },
        "verbose_output": {
            "formatter": "simple",
            "level": level,
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "load_data": {
            "level": level,
            "handlers": [
                "verbose_output",
            ],
        },
    },
    "root": {"level": level, "handlers": ["logfile", "verbose_output"]},
}

logging.config.dictConfig(LOGGING)

app_logger = logging.getLogger(__name__)
