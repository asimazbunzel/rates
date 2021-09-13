import logging
import sys

FORMAT = (
    "[%(name)-20s][%(levelname)-18s]  %(message)s (%(filename)s:%(lineno)d)"
)

logging.captureWarnings(True)
logger = logging.getLogger("binrates")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(filename="binrates.log", format=FORMAT)

logger.addHandler(console_handler)
logging.getLogger("py.warnings").addHandler(console_handler)

LOGGING_LEVELS = {
    "NOTSET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

DEFAULT_LOG_LEVEL = "CRITICAL"


def set_logging(level):

    if level:
        logging_level = level.upper()
    else:
        logging_level = DEFAULT_LOG_LEVEL

    if logging_level not in LOGGING_LEVELS:
        msg = f"`level = {logging_level}` is not valid. Must be one of the "
        msg += f"following {list(LOGGING_LEVELS.keys())}"
        raise ValueError(msg)
    else:
        logger.setLevel(LOGGING_LEVELS[logging_level])

    if logger.filters:
        for filter in logger.filters:
            logger.removeFilter(filter)

    return logger
