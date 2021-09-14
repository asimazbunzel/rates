"""Module to load YAML configuration files"""

import logging

import yaml

logger = logging.getLogger(__name__)


def load_config(fname):
    """Load configuration file with YAML format

    Parameters
    ----------
    fname

    Returns
    -------
    """
    with open(fname, "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)
