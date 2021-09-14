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

    kwargs : `dictionary`
        Dictionary with configs for the PDFs of initial binary conditions.
    """

    DEFAULT_BINARIESNO = 100000

    def __init__(self, number: float = 0, seed: int = None, **kwargs):

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
            "PDF_m1": "Salpeter",
            "min_m1": 1,
            "max_m1": 150,
            "PDF_q": "Uniform",
            "min_q": 1e-2,
            "max_q": 1,
            "PDF_p": "Sana",
            "min_p": 1.412537545e0,
            "max_p": 316227.766e0,
        }

        for key, value in kwargs.items():
            if key in args:
                args[key] = value
            else:
                msg = f"keyword argument `{key}` not recognised and will be "
                msg += f"ignored. Available options are: {list(args.keys())}"
                logging.warning(msg)

        # for reproduction of results
        if self.seed is not None:
            set_seed(self.seed)

        self.generate_primaries(args)
        self.generate_companions()
        self.generate_periods()

    def generate_primaries(self, args):
        """Method to generate a set of initial primary masses"""

        if args["PDF_m1"] == "Salpeter":
            slope = -2.7
            m1 = sample_from_powerlaw(
                slope, args["min_m1"], args["max_m1"], self.number
            )

        return m1

    def generate_companions(self, args):
        """Method to generate a set of initial mass-ratios

        Companion masses are defined as m1 * q
        """

        if args["PDF_q"] == "Uniform":
            q = sample_from_uniform(args["min_q"], args["max_q"], self.number)

        return q

    def generate_periods(self, args):
        """Method to generate a set of initial orbital periods"""

        if args["PDF_p"] == "Sana":
            slope = -0.5
            logp = sample_from_powerlaw(
                slope, args["min_p"], args["max_p"], self.number
            )
            p = np.power(10, logp)

        return p
