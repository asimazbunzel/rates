"""base

Module with methods to compute rates comparing simulations from a detailed
stellar evolutionary code and random binary populations following certain
P.D.F.s
"""

import logging

from binrates.io.logger import set_logger
from binrates.io.utils import load_config
from binrates.population import Population, TargetRegion


logger = logging.getLogger(__name__)


def init_random_binaries(BinPopConfig):
    """Function to initialize binary populations"""

    msg = "instantiating Population object for random population from "
    msg += "probability density functions"
    logger.debug(msg)

    # get some really important values
    number = BinPopConfig["number"]
    seed = BinPopConfig["seed"]

    # define the random binary pop.
    BinPop = Population(number=number, seed=seed, Config=BinPopConfig)

    return BinPop


def load_target_region(TargetRegionConfig):
    """Function that loads a target region to which rates will be evaluated"""

    # get some stuff
    load_from_file = TargetRegionConfig["load_from_file"]
    fname = ""
    if load_from_file:
        fname = TargetRegionConfig["fname"]
    make_test = TargetRegionConfig["make_test_with_figure"]
    shape = ""
    if make_test:
        shape = TargetRegionConfig["shape_of_figure"]

    Region = TargetRegion(load_from_file, fname, make_test, shape)

    return Region


def eval_rates(config_fname: str = "", log_level: str = None, **kwargs):
    """Main function to evaluate rates"""

    if not isinstance(log_level, str):
        raise TypeError("`log_level` must be a string")

    # set logging configuration
    set_logger()

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
    logger.info("initializing random binary population")
    BinPop = init_random_binaries(Config["BinaryPopulation"])
    logger.info(f"Population succesfully computed in `{BinPop}`")

    # now get region of binary parameter space to which rates will be eval
    logger.info("loading target region of binary parameter space")
    BinPop = load_target_region(Config["TargetRegion"])
    logger.info("target region succesfully loaded")

    return None
