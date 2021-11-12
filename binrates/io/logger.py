import getpass
import logging
import logging.config
import os
import sys
import tempfile

from .utils import safe_makedirs

# a really nice way to handle logging: save .log in $HOME/.local/share/bin2dcomngr (if possible)
# else in /tmp/bin2dcomngr
if "HOME" in os.environ:
    _XDG_CACHE_HOME = os.path.join(os.environ["HOME"], ".local", "share")
else:
    _XDG_CACHE_HOME = ""
# Define the glances log file
if (
    "XDG_CACHE_HOME" in os.environ
    and os.path.isdir(os.environ["XDG_CACHE_HOME"])
    and os.access(os.environ["XDG_CACHE_HOME"], os.W_OK)
):
    safe_makedirs(os.path.join(os.environ["XDG_CACHE_HOME"], "bin2dcomngr"))
    LOG_FILENAME = os.path.join(
        os.environ["XDG_CACHE_HOME"], "bin2dcomngr", "bin2dcomngr.log"
    )
elif os.path.isdir(_XDG_CACHE_HOME) and os.access(_XDG_CACHE_HOME, os.W_OK):
    safe_makedirs(os.path.join(_XDG_CACHE_HOME, "bin2dcomngr"))
    LOG_FILENAME = os.path.join(
        _XDG_CACHE_HOME, "bin2dcomngr", "bin2dcomngr.log"
    )
else:
    LOG_FILENAME = os.path.join(
        tempfile.gettempdir(), "bin2dcomngr-{}.log".format(getpass.getuser())
    )

LOGGING_CFG = {
    "version": 1,
    "disable_existing_loggers": "False",
    "root": {"level": "INFO", "handlers": ["file", "console"]},
    "formatters": {
        "standard": {"format": "%(asctime)s -- %(levelname)s -- %(message)s"},
        "short": {"format": "%(levelname)s -- %(message)s"},
        "long": {
            "format": "%(asctime)s -- %(levelname)s -- %(message)s (%(funcName)s in %(filename)s)"
        },
        "free": {"format": "%(message)s"},
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1000000,
            "backupCount": 3,
            "formatter": "standard",
            "filename": LOG_FILENAME,
        },
        "console": {
            "level": "CRITICAL",
            "class": "logging.StreamHandler",
            "formatter": "free",
        },
    },
    "loggers": {
        "debug": {"handlers": ["file", "console"], "level": "DEBUG"},
        "verbose": {"handlers": ["file", "console"], "level": "INFO"},
        "standard": {"handlers": ["file"], "level": "INFO"},
        "requests": {"handlers": ["file", "console"], "level": "ERROR"},
        "elasticsearch": {"handlers": ["file", "console"], "level": "ERROR"},
        "elasticsearch.trace": {
            "handlers": ["file", "console"],
            "level": "ERROR",
        },
    },
}


def set_logger():
    """build and return a logger

    Returns
    -------
    logger : `Logger instance`
    """

    _logger = logging.getLogger()

    config = LOGGING_CFG

    # Load the configuration
    logging.config.dictConfig(config)

    return _logger


binrates_logger = set_logger()
