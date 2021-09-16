"""A collection of utility functions
"""

from typing import Union

import numpy as np
from binrates.utils import constants as const


__all_ = ["P_to_a", "a_to_P", "a_to_f"]


def P_to_a(
    period: Union[float, np.ndarray],
    m1: Union[float, np.ndarray],
    m2: Union[float, np.ndarray],
) -> Union[float, np.ndarray]:
    """Binary separation from a known period

    Parameters
    ----------
    period : `float/array`
       Binary period in days

    m1 : `float/array`
       Mass of primary star in Msun

    m2 : `flota/array`
       Mass of secondary star in Msun

    Returns
    -------
    a : `float/array`
       Binary separation in Rsun
    """

    period = period * 24e0 * 3600e0  # in sec
    m1 = m1 * const.Msun
    m2 = m2 * const.Msun  # in g

    separation = np.power(
        const.standard_cgrav * (m1 + m2) * np.square(period / (2 * const.pi)),
        const.one_third,
    )

    return separation / const.Rsun


def a_to_P(
    separation: Union[float, np.ndarray],
    m1: Union[float, np.ndarray],
    m2: Union[float, np.ndarray],
) -> Union[float, np.ndarray]:
    """Orbital period from a known separation

    Parameters
    ----------
    a : `float/array`
       Binary separation in Rsun

    m1: `float/array`
       Mass of primary star in Msun

    m2: `float/array`
       Mass of secondary star in Msun

    Returns
    -------
    P : `float/array`
       Binary period in days
    """

    separation = separation * const.Rsun  # in cm
    m1 = m1 * const.Msun
    m2 = m2 * const.Msun  # in g

    period = np.power(
        separation
        * separation
        * separation
        / (const.standard_cgrav * (m1 + m2)),
        0.5e0,
    )
    period = (2 * const.pi) * period

    return period / (24e0 * 3600e0)


def a_to_f(
    separation: Union[float, np.ndarray],
    m1: Union[float, np.ndarray],
    m2: Union[float, np.ndarray],
) -> Union[float, np.ndarray]:
    """Converts semi-major axis to orbital frequency

    Parameters
    ----------
    separation : `float/array`
       Semi-major axis

    m1 : `float/array`
       Primary mass

    m2 : `float/array`
       Secondary mass

    Returns
    -------
    f_orb : `float/array`
       Orbital frequency
    """

    separation = separation * const.Rsun  # in cm
    m1 = m1 * const.Msun
    m2 = m2 * const.Msun  # in g

    f_orb = np.power(
        const.standard_cgrav * (m1 + m2) / separation ** 3, 0.5
    ) / (2 * const.pi)

    return f_orb
