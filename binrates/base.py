import logging
import sys

from binrates.io.logger import set_logging
from binrates.io.utils import load_config


logger = logging.getLogger(__name__)


def eval_rates(config_fname: str = "", log_level: str = None, **kwargs):

    set_logging(log_level)

    logger.debug("loading configuration in YAML file")
    if isinstance(config_fname, str):
        try:
            Config = load_config(config_fname)
        except Exception:
            logger.error("cannot load YAML file with configuration")
    else:
        logger.error(
            "`config_fname` must be either a string or a pathlib object"
        )
        raise TypeError(
            "`config_fname` must be either a string or a pathlib object"
        )

    if not isinstance(log_level, str):
        raise TypeError("`log_level` must be a string")

    return None
