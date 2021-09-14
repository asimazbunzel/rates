"""rvs

Module with functions to compute random values from different distributions
"""

import logging

import numpy as np
from scipy.stats import uniform

logger = logging.getLogger(__name__)


def set_seed(seed=None):
    """Set a seed for reproduction of results found

    Parameters
    ----------
    seed : `integer`
        Number to use for the pseudo-random number generator. Default is None
    """

    if seed is None:
        logger.warning("seed is None. Return without calling the seed method")
        return

    np.random.seed(seed)


def sample_from_powerlaw(
    alpha: float = None, xi: float = None, xf: float = None, N: int = 10000
):
    """Draw a sample of N values distributed according to a powerlaw pdf

    The sample will be constraint between [xi, xf]

    Parameters
    ----------
    alpha : `float`
        Slope of the powerlaw function.

    xi : `float`
        Minimum possible value for the random number interval.

    xf : `float`
        Maximum possible value for the random number interval.

    N : `integer`
        Number of random numbers to sample.

    Returns
    -------
    x : `np.ndarray`
        Array with the drawn values from the powerlaw.
    """

    if not isinstance(alpha, float):
        raise TypeError("`alpha` must be a float")
    if not isinstance(xi, float):
        raise TypeError("`xi` must be a float")
    if not isinstance(xf, float):
        raise TypeError("`xf` must be a float")
    if not isinstance(N, int):
        raise TypeError("`N` must be an integer")

    # min & max values
    pdf_i = np.power(xi, alpha + 1)
    pdf_f = np.power(xf, alpha + 1)

    # random numbers in the interval (pdf_i, pdf_f)
    cpd = np.random.uniform(pdf_i, pdf_f, N)

    return np.power(cpd, 1.0 / (alpha + 1))


def sample_from_uniform(xi: float = None, xf: float = None, N: int = 10000):
    """Draw a sample of N values uniformely distributed

    The sample will be constraint between [xi, xf]

    Parameters
    ----------
    xi : `float`
        Minimum possible value for the random number interval.

    xf : `float`
        Maximum possible value for the random number interval.

    N : `integer`
        Number of random numbers to sample.

    Returns
    -------
    x : `np.ndarray`
        Array with the drawn values from the uniform pdf.
    """

    if not isinstance(xi, float):
        raise TypeError("`xi` must be a float")
    if not isinstance(xf, float):
        raise TypeError("`xf` must be a float")
    if not isinstance(N, int):
        raise TypeError("`N` must be an integer")

    # first, draw random values in the [0, 1] interval
    u = uniform.rvs(size=N)

    # convert to proper range [xi, xf]
    x = xi + u * (xf - xi)

    return x
