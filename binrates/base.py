"""base

Module with methods to compute rates comparing simulations from a detailed
stellar evolutionary code and random binary populations following certain
P.D.F.s
"""

import logging

from binrates.io.logger import set_logging
from binrates.io.utils import load_config
from binrates.population import Population


logger = logging.getLogger(__name__)


def init_binaries(BinPopConfig):
    """Function to initialize binary populations"""

    msg = "instantiating Population object for random population from "
    msg += "probability density functions"
    logger.debug(msg)

    # get some really important values
    number = BinPopConfig["number"]
    seed = BinPopConfig["seed"]

    BinPop = Population(number=number, seed=seed, Config=BinPopConfig)

    return BinPop


def eval_rates(config_fname: str = "", log_level: str = None, **kwargs):
    """Main function to evaluate rates"""

    if not isinstance(log_level, str):
        raise TypeError("`log_level` must be a string")

    # set logging configuration
    set_logging(log_level)

    # load configuration file
    logger.info("loading configuration in YAML file")
    if isinstance(config_fname, str):
        try:
            Config = load_config(config_fname)
        except Exception:
            logger.error("cannot load YAML file with configuration")
    else:
        raise TypeError(
            "`config_fname` must be either a string or a pathlib object"
        )

    # create binary population
    logger.info("initializing binary populations")
    BinPop = init_binaries(Config["BinaryPopulation"])
    logger.info(f"Population succesfully computed in `{BinPop}`")

    return None
