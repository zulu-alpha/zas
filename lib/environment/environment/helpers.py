import os
from distutils.util import strtobool
from typing import Optional


def get_bool_env(
    environ_var: str,
    default: Optional[bool] = False,
) -> bool:
    """Somewhat reliably returns a boolean value based on various kinds of `truthy` or
    `falsy` string values in the environment.
    """
    value = os.getenv(
        environ_var,
        str(default),
    )
    return bool(strtobool(value))


def get_int_env(
    env_name: str,
) -> int:
    """Get the given integer envar or raise an assertion error"""
    value = int(
        os.getenv(
            env_name,
            "0",
        )
    )
    assert value, f"The environmental variable {env_name} was not found!"
    return value


def get_str_env(
    env_name: str,
) -> str:
    """Get the given envar or raise an assertion error"""
    value = os.getenv(env_name)
    assert value, f"The environmental variable {env_name} was not found!"
    return value
