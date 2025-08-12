"""
Advanced validator functions for handling complex data validation in Pendulum.
"""

from typing import Any, Callable, Union

from pendulum import InvalidDate, Timezone
from .constants import ADVANCED_VALIDATORS

def is_valid_date(value: Union[str, int], timezone: Timezone = None) -> bool:
    """
    Validates if a given value is a valid date.

    Args:
        value (Union[str, int]): The value to validate as either a string or an integer.
        timezone (Timezone, optional): The timezone to use for validation if the value is an integer. Defaults to None.

    Returns:
        bool: True if the value is valid date, False otherwise.

    Raises:
        ValueError: If the given value cannot be converted to a datetime object or is not a supported type.
    """
    try:
        if isinstance(value, str):
            pendulum_obj = Pendulum().from_string(value)
        elif timezone:
            pendulum_obj = Pendulum().from_timestamp(value, in_tz=timezone)
        else:
            raise ValueError("Value must be either a string or an integer with a valid Timezone object.")

        # Handle edge cases such as non-existing dates (e.g., Feb 30) and invalid timezones
        if pendulum_obj.in_tz(timezone) and not pendulum_obj.is_valid():
            raise InvalidDate("The provided value is not a valid date.")

        return True
    except (ValueError, InvalidDate):
        return False

def advanced_validator(custom_validator: Callable[[Any], bool]) -> Callable[[Union[str, int]], bool]:
    """
    Decorator function to create an advanced validator for custom logic.

    Args:
        custom_validator (Callable[[Any], bool]): The custom validation function to be used.

    Returns:
        Callable[[Union[str, int]], bool]: A new validator function that wraps the given custom_validator function.

    Raises:
        TypeError: If the provided custom_validator is not a callable or does not accept a single argument.
    """

    if not callable(custom_validator) or len(inspect.signature(custom_validator).parameters) != 1:
        raise TypeError("custom_validator must be a callable function accepting one argument.")

    def advanced_validator_wrapper(value: Union[str, int]) -> bool:
        return custom_validator(value)

    ADVANCED_VALIDATORS.append((advanced_validator_wrapper.__name__, advanced_validator_wrapper))

    return advanced_validator_wrapper