"""population

Module containing stuff related to binary populations
"""

import logging

import numpy as np

from binrates.statistics.rvs import (
    sample_from_powerlaw,
    sample_from_uniform,
    set_seed,
)

logger = logging.getLogger(__name__)


class Population(object):
    """Object containing a random sample population of binaries characterized
    by masses and orbital periods

    Parameters
    ----------
    number : `float`
        Number of random binaries in the population.

    seed : `integer`
        Seed for pseudo-random draws.

    Config : `dictionary`
        Dictionary with configs for the PDFs of initial binary conditions.
    """

    DEFAULT_BINARIESNO = 100000

    def __init__(
        self, number: float = 0, seed: int = None, Config: dict = None
    ):

        logger.debug("generating binary population")

        try:
            number = int(number)
        except ValueError:
            msg = "The `number` of random binaries must be an integer or a "
            msg += f"float. Setting its default value of: `{number}`"
            logger.error(msg)
            number = self.DEFAULT_BINARIESNO

        if seed is not None:
            try:
                seed = int(seed)
            except ValueError:
                msg = "The `seed` for random draws must be an integer or a "
                msg += "float. Setting its default value of `None`"
                logger.error(msg)
                seed = None

        self.number = number
        self.seed = seed
        args = {
            "Primary": {
                "pdf": "Salpeter",
                "min_mass": 1,
                "max_mass": 150,
            },
            "MassRatio": {
                "pdf": "Uniform",
                "min_mass_ratio": 1e-2,
                "max_mass_ratio": 1,
            },
            "OrbitalPeriod": {
                "pdf": "Sana",
                "min_period": 1.412537545e0,
                "max_period": 316227.766e0,
            },
        }

        for key, value in Config.items():

            if key == "Primary":
                for subkey, subval in Config[key].items():
                    if subkey in Config[key]:
                        if subval is not None:
                            args[key][subkey] = subval

            if key == "MassRatio":
                for subkey, subval in Config[key].items():
                    if subkey in Config[key]:
                        if subval is not None:
                            args[key][subkey] = subval

            if key == "OrbitalPeriod":
                for subkey, subval in Config[key].items():
                    if subkey in Config[key]:
                        if subval is not None:
                            args[key][subkey] = subval

        logger.debug(f"Arguments to use: `{args}`")

        # for reproduction of results
        if self.seed is not None:
            set_seed(self.seed)

        self.primaries = self.generate_primaries(args["Primary"])
        self.mass_ratios = self.generate_companions(args["MassRatio"])
        self.periods = self.generate_periods(args["OrbitalPeriod"])

    def generate_primaries(self, args):
        """Method to generate a set of initial primary masses"""

        min_mass = float(args["min_mass"])
        max_mass = float(args["max_mass"])

        if args["pdf"] == "Salpeter":
            slope = -2.35
            m1 = sample_from_powerlaw(slope, min_mass, max_mass, self.number)
        else:
            m1 = None

        return m1

    def generate_companions(self, args):
        """Method to generate a set of initial mass-ratios

        Companion masses are defined as m1 * q
        """

        min_mass_ratio = float(args["min_mass_ratio"])
        max_mass_ratio = float(args["max_mass_ratio"])

        if args["pdf"] == "Uniform":
            q = sample_from_uniform(
                min_mass_ratio, max_mass_ratio, self.number
            )
        else:
            q = None

        return q

    def generate_periods(self, args):
        """Method to generate a set of initial orbital periods"""

        min_log_period = np.log10(float(args["min_period"]))
        max_log_period = np.log10(float(args["max_period"]))

        if args["pdf"] == "Sana":
            slope = -0.55
            logp = sample_from_powerlaw(
                slope, min_log_period, max_log_period, self.number
            )
            p = np.power(10, logp)
        else:
            p = None

        return p
