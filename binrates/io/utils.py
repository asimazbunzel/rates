"""Module to load YAML configuration files"""

import errno
import logging
import os

import yaml

logger = logging.getLogger(__name__)


def safe_makedirs(path: str) -> None:
    """A safe function for creating a directory tree."""
    try:
        os.makedirs(path)
    except OSError as err:
        if err.errno == errno.EEXIST:
            if not os.path.isdir(path):
                raise
        else:
            raise


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
