from app.core import settings
import logging
import logging.config
import sys


def setup_logging():

    selected_formatter = "json" if settings.is_production else "standard"
    selected_level = "INFO" if settings.is_production else "DEBUG"

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "": {  # root logger
                "handlers": ["default"],
                "level": "INFO",
            },
            "app": {  # app logger
                "handlers": ["default"],
                "level": selected_level,
                "propagate": False,
            },
            "uvicorn": {  # uvicorn logger
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": selected_formatter,
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
            }
        },
        "formatters": {
            "standard": {  # Development
                "format": "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%SZ",  # Format output to 2026[year]-07[month]-21[day]T17[hour]:05[minute]:10[second]Z[UTC stamp]
            },
            "json": {  # production
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
    }
    logging.config.dictConfig(logging_config)
