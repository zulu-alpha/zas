import pytest
from environment.helpers import (
    get_bool_env,
    get_int_env,
    get_str_env,
)


class TestGetBoolEnv:
    """Test get_bool_env"""

    envar_name = "TEST_VAR"

    @pytest.mark.parametrize(
        "environment_value",
        [
            "1",
            "TRUE",
            "true",
            "YES",
            "yes",
        ],
    )
    def test_trythy_bools(
        self,
        monkeypatch,
        environment_value,
    ):
        """Correctly gets the truthy booleans from strings."""
        monkeypatch.setenv(
            self.envar_name,
            environment_value,
        )
        assert (
            get_bool_env(
                self.envar_name,
                False,
            )
            is True
        )

    @pytest.mark.parametrize(
        "environment_value",
        [
            "0",
            "FALSE",
            "false",
            "NO",
            "no",
        ],
    )
    def test_falsy_bools(
        self,
        monkeypatch,
        environment_value,
    ):
        """Correctly gets the falsy booleans from strings."""
        monkeypatch.setenv(
            self.envar_name,
            environment_value,
        )
        assert (
            get_bool_env(
                self.envar_name,
                False,
            )
            is False
        )

    @pytest.mark.parametrize(
        "environment_value",
        [
            "11",
            "junk",
        ],
    )
    def test_invalid(
        self,
        monkeypatch,
        environment_value,
    ):
        """Test that a value error is raised for non convertable values."""
        monkeypatch.setenv(
            self.envar_name,
            environment_value,
        )
        with pytest.raises(ValueError):
            get_bool_env(self.envar_name)

    def test_defaults(
        self,
    ):
        """Correctly gives default values if they do not exist."""
        assert (
            get_bool_env(
                "NOT_EXISTING",
                True,
            )
            is True
        ), "Tried setting default to True"
        assert (
            get_bool_env(
                "NOT_EXISTING",
                False,
            )
            is False
        ), "Tried setting default to False"
        assert (
            get_bool_env("NOT_EXISTING") is False
        ), "Using default default, which should be False"


class TestGetIntEnv:
    """Test get_int_env"""

    envar_name = "TEST_VAR"

    @pytest.mark.parametrize(
        "environment_value, expected_value",
        [
            (
                "55",
                55,
            ),
            (
                "1",
                1,
            ),
        ],
    )
    def test_converts_integers(
        self,
        monkeypatch,
        environment_value,
        expected_value,
    ):
        """Test the simple case of a series of numbers."""
        monkeypatch.setenv(
            self.envar_name,
            environment_value,
        )
        assert get_int_env(self.envar_name) == expected_value

    def test_non_existent(
        self,
    ):
        """Check that an assertion error is raised when fetching a non existent"""
        with pytest.raises(AssertionError):
            get_int_env(self.envar_name)


class TestGetstrEnv:
    """Test get_str_env"""

    envar_name = "TEST_VAR"

    @pytest.mark.parametrize(
        "environment_value",
        [
            "HelloWorld",
            "654623456",
            "With Spaces",
        ],
    )
    def test_converts_integers(
        self,
        monkeypatch,
        environment_value,
    ):
        """Test the simple case of a series of numbers."""
        monkeypatch.setenv(
            self.envar_name,
            environment_value,
        )
        assert get_str_env(self.envar_name) == environment_value

    def test_non_existent(
        self,
    ):
        """Check that an assertion error is raised when fetching a non existent"""
        with pytest.raises(AssertionError):
            get_int_env(self.envar_name)
