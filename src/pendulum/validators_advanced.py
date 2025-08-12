"""
Advanced validator functions for Pendulum library.

This module provides additional validation functions that build upon the basic ones found in pendulum.validators.
These functions handle edge cases and provide more advanced validation scenarios.
"""

from typing import Union
from datetime import datetime, timedelta
from . import constants as p_consts
from .utils import is_datetime_valid

def validate_date_in_range(date: datetime, start: Union[datetime, str], end: Union[datetime, str]) -> bool:
    """
    Validates if a given date falls within the provided start and end dates (inclusive).

    Args:
        date (datetime or str): The date to validate. If it is a string, it should be in the format "YYYY-MM-DD".
        start (datetime or str): The inclusive start date for validation.
        end (datetime or str): The inclusive end date for validation.

    Returns:
        bool: True if the given date falls within the provided start and end dates, False otherwise.

    Raises:
        ValueError: If either start or end is not a datetime object or a valid string representation of a date.
    """
    # Convert all input to datetime objects
    start_date = p_consts.parse_date(start)
    end_date = p_consts.parse_date(end)

    if not is_datetime_valid(start_date):
        raise ValueError(f"Invalid start date: {start}")

    if not is_datetime_valid(end_date):
        raise ValueError(f"Invalid end date: {end}")

    return start_date <= date <= end_date

def validate_time_between(time: datetime, start: Union[datetime, str], end: Union[datetime, str]) -> bool:
    """
    Validates if a given time falls between the provided start and end times (inclusive).

    Args:
        time (datetime or str): The time to validate. If it is a string, it should be in the format "HH:MM:SS".
        start (datetime or str): The inclusive start time for validation.
        end (datetime or str): The inclusive end time for validation.

    Returns:
        bool: True if the given time falls between the provided start and end times, False otherwise.

    Raises:
        ValueError: If either start or end is not a datetime object or a valid string representation of a time.
    """
    # Convert all input to datetime objects
    start_time = p_consts.parse_time(start)
    end_time = p_consts.parse_time(end)

    if not is_datetime_valid(start_time):
        raise ValueError(f"Invalid start time: {start}")

    if not is_datetime_valid(end_time):
        raise ValueError(f"Invalid end time: {end}")

    return start_time <= time <= end_time