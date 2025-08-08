"""Timezone Validator module for handling validating IANA timezones.

This module provides a TimezoneValidator class which validates if a given string represents a valid IANA timezone.
It also handles edge cases and errors appropriately.

Example usage:
    >>> from timezone_validator import TimezoneValidator
    >>> validator = TimezoneValidator()
    >>> validator.is_valid("America/Los_Angeles")  # Valid IANA timezone
    True
    >>> validator.is_valid("InvalidTimeZone")  # Invalid IANA timezone
    False
"""

from typing import Union, Callable, Any
import pytz

class TimezoneValidator:
    """Validates if a given string represents a valid IANA timezone."""

    def __init__(self, timezone_list: Union[str, list] = None) -> None:
        """Initialize the TimezoneValidator with an optional list of valid timezones.

        Args:
            timezone_list (Union[str, list], optional): A list of IANA timezones to validate against. Defaults to None.
        """
        self._valid_timezones = pytz.all_timezones.copy() if timezone_list is None else _normalize_timezones(timezone_list)

    def _is_valid(self, timezone: str) -> bool:
        """Checks if the given timezone is in the list of valid timezones.

        Args:
            timezone (str): The IANA timezone to check.

        Returns:
            bool: True if the timezone is valid, False otherwise.
        """
        return timezone in self._valid_timezones

    def is_valid(self, timezone: str) -> bool:
        """Checks if the given string represents a valid IANA timezone.

        Args:
            timezone (str): The string to validate.

        Returns:
            bool: True if the string represents a valid IANA timezone, False otherwise.
        """
        try:
            pytz.timezone(timezone)
            return self._is_valid(timezone)
        except ValueError as e:
            raise ValueError(f"Invalid timezone '{timezone}': {str(e)}")

def _normalize_timezones(timezones: Union[str, list]) -> list:
    """Normalizes the given timezones to a list of strings.

    Args:
        timezones (Union[str, list]): The timezones to normalize.

    Returns:
        list: A list of normalized timezone strings.
    """
    if isinstance(timezones, str):
        return [timezones]
    elif isinstance(timezones, list):
        return [tz.strip() for tz in timezones]
    else:
        raise TypeError("Timezones must be a string or a list.")