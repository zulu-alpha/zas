"""
Project wide common utilities.
Must not depend on anything else in the project.
"""

from distutils.util import strtobool
import os
from typing import Optional


def get_bool_env(environ_var: str, default: Optional[bool] = False) -> bool:
    """Somewhat reliably returns a boolean value based on various kinds of `truthy` or
    `falsy` string values in the environment.
    """
    return bool(strtobool(os.getenv(environ_var, str(default))))
