from __future__ import annotations

import os
import struct

from datetime import date
from datetime import datetime
from datetime import timedelta
from math import copysign
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import overload

import pendulum

from pendulum.constants import DAYS_PER_MONTHS
from pendulum.day import WeekDay
from pendulum.formatting.difference_formatter import DifferenceFormatter
from pendulum.locales.locale import Locale


if TYPE_CHECKING:
    # Prevent import cycles
    from pendulum.duration import Duration

with_extensions = os.getenv("PENDULUM_EXTENSIONS", "1") == "1"

_DT = TypeVar("_DT", bound=datetime)
_D = TypeVar("_D", bound=date)

try:
    if not with_extensions or struct.calcsize("P") == 4:
        raise ImportError()

    from pendulum._pendulum import PreciseDiff
    from pendulum._pendulum import days_in_year
    from pendulum._pendulum import is_leap
    from pendulum._pendulum import is_long_year
    from pendulum._pendulum import local_time
    from pendulum._pendulum import precise_diff
    from pendulum._pendulum import week_day
except ImportError:
    from pendulum._helpers import PreciseDiff  # type: ignore[assignment]
    from pendulum._helpers import days_in_year
    from pendulum._helpers import is_leap
    from pendulum._helpers import is_long_year
    from pendulum._helpers import local_time
    from pendulum._helpers import precise_diff  # type: ignore[assignment]
    from pendulum._helpers import week_day

difference_formatter = DifferenceFormatter()


@overload
def add_duration(
    dt: _DT,
    years: int = 0,
    months: int = 0,
    weeks: int = 0,
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: float = 0,
    microseconds: int = 0,
) -> _DT: ...


@overload
def add_duration(
    dt: _D,
    years: int = 0,
    months: int = 0,
    weeks: int = 0,
    days: int = 0,
) -> _D:
    pass


def add_duration(
    dt: date | datetime,
    years: int = 0,
    months: int = 0,
    weeks: int = 0,
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: float = 0,
    microseconds: int = 0,
) -> date | datetime:
    """
    Adds a duration to a date/datetime instance.
    """
    days += weeks * 7

    if (
        isinstance(dt, date)
        and not isinstance(dt, datetime)
        and any([hours, minutes, seconds, microseconds])
    ):
        raise RuntimeError("Time elements cannot be added to a date instance.")

    # Normalizing
    if abs(microseconds) > 999999:
        s = _sign(microseconds)
        div, mod = divmod(microseconds * s, 1000000)
        microseconds = mod * s
        seconds += div * s

    if abs(seconds) > 59:
        s = _sign(seconds)
        div, mod = divmod(seconds * s, 60)  # type: ignore[assignment]
        seconds = mod * s
        minutes += div * s

    if abs(minutes) > 59:
        s = _sign(minutes)
        div, mod = divmod(minutes * s, 60)
        minutes = mod * s
        hours += div * s

    if abs(hours) > 23:
        s = _sign(hours)
        div, mod = divmod(hours * s, 24)
        hours = mod * s
        days += div * s

    if abs(months) > 11:
        s = _sign(months)
        div, mod = divmod(months * s, 12)
        months = mod * s
        years += div * s

    year = dt.year + years
    month = dt.month

    if months:
        month += months
        if month > 12:
            year += 1
            month -= 12
        elif month < 1:
            year -= 1
            month += 12

    day = min(DAYS_PER_MONTHS[int(is_leap(year))][month], dt.day)

    dt = dt.replace(year=year, month=month, day=day)

    return dt + timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        microseconds=microseconds,
    )


def format_diff(
    diff: Duration,
    is_now: bool = True,
    absolute: bool = False,
    locale: str | None = None,
) -> str:
    if locale is None:
        locale = get_locale()

    return difference_formatter.format(diff, is_now, absolute, locale)


def _sign(x: float) -> int:
    return int(copysign(1, x))


# Global helpers


def locale(name: str) -> Locale:
    return Locale.load(name)


def set_locale(name: str) -> None:
    locale(name)

    pendulum._LOCALE = name


def get_locale() -> str:
    return pendulum._LOCALE


def week_starts_at(wday: WeekDay) -> None:
    if wday < WeekDay.MONDAY or wday > WeekDay.SUNDAY:
        raise ValueError("Invalid day of week")

    pendulum._WEEK_STARTS_AT = wday


def week_ends_at(wday: WeekDay) -> None:
    if wday < WeekDay.MONDAY or wday > WeekDay.SUNDAY:
        raise ValueError("Invalid day of week")

    pendulum._WEEK_ENDS_AT = wday


__all__ = [
    "PreciseDiff",
    "add_duration",
    "days_in_year",
    "format_diff",
    "get_locale",
    "is_leap",
    "is_long_year",
    "local_time",
    "locale",
    "precise_diff",
    "set_locale",
    "week_day",
    "week_ends_at",
    "week_starts_at",
]



from datetime import timezone, tzlocal
import pytz
import re
from typing import Union


from datetime import datetime
from pendulum import Timezone, FixedTimezone, UTC, parse_iso8601

def get_current_timestamp() -> str:
    """
    Returns the current UTC timestamp as a string.
    """
    return UTC().now().to_iso8601(tz='UTC')

def update_method(obj: Union[Timezone, FixedTimezone, datetime, int]) -> Timezone:
    """
    Updates an object with the current timestamp and returns a new Timezone instance.

    Args:
        obj (Union[Timezone, FixedTimezone, datetime, int]): The input object to be updated.
            This can be a timezone, fixed timezone, datetime object, or integer representing UTC offset.

    Returns:
        Timezone: A new Timezone instance with the updated timestamp.

    Raises:
        TypeError: If the provided input is not a valid type (Timezone, FixedTimezone, datetime, int).
    """
    if isinstance(obj, (Timezone, FixedTimezone)):
        return obj.advance(seconds=get_current_timestamp().replace('T', ' ').replace('Z', '').split()[0].isdigit() and int(get_current_timestamp().replace('T', ' ').replace('Z', '')) or 0)
    elif isinstance(obj, datetime):
        return timezone(obj.astimezone(UTC))
    elif isinstance(obj, int):
        return FixedTimezone(obj, 'UTC')
    else:
        raise TypeError("Invalid input type. Must be Timezone, FixedTimezone, datetime or integer.")


from datetime import datetime
import pendulum as pm
from typing import Union

def get_current_timestamp() -> str:
    """
    Returns the current UTC timestamp as an ISO formatted string.
    """
    return pm.now().isoformat()

class UpdateMethod:
    """
    A class to handle updating a resource with the current timestamp.
    """

    def update_method(self, resource: Union[str, dict]) -> None:
        """
        Updates a given resource with the current UTC timestamp using the get_current_timestamp function.

        Args:
            resource (Union[str, dict]): The resource to be updated. Can be either a string or a dictionary.
        """
        if isinstance(resource, str):
            resource = json.loads(resource)

        resource['updated_at'] = get_current_timestamp()


from typing import Union, Optional
import pendulum as pd

def format_duration(duration: pd.Duration) -> str:
    """Format a Duration object into a human-readable string.

    Examples:
        - 1 hour 2 minutes will be formatted as "1 hour 2 minutes"
        - 3 days 4 hours 5 minutes will be formatted as "3 days, 4 hours, 5 minutes"
    """
    components = duration.in_components('days', 'hours', 'minutes', 'seconds')
    if all(value == 0 for value in components[:3]):
        return f'{components[3]} seconds'
    elif components[0] > 0:
        days_str = pluralize(components[0], 'day') if components[0] != 1 else 'day'
        hours_str = pluralize(components[1], 'hour') if components[1] != 1 else 'hour'
        minutes_str = pluralize(components[2], 'minute') if components[2] != 1 else 'minute'
        return f'{days_str} {days}, {hours_str} {hours}, {minutes_str} {minutes}'
    elif components[1] > 0:
        hours_str = pluralize(components[1], 'hour') if components[1] != 1 else 'hour'
        minutes_str = pluralize(components[2], 'minute') if components[2] != 1 else 'minute'
        return f'{hours_str} {hours}:{minutes_str} {minutes}'
    elif components[2] > 0:
        minutes_str = pluralize(components[2], 'minute') if components[2] != 1 else 'minute'
        return f'{minutes_str} {minutes}'

def update_method(self, duration: pd.Duration, target: Union[str, Optional[pd.Timezone]] = None) -> pd.DateTime:
    """Update the datetime object with a given duration and optionally adjust its timezone.

    Arguments:
        duration (pd.Duration): The amount of time to add or subtract from the current datetime object.
        target (Union[str, Optional[pd.Timezone]]): An optional argument specifying the new timezone for the updated datetime object. If not provided,
            the current timezone remains unchanged.
    """
    # Create a copy of the current datetime and apply the given duration
    updated_dt = self._datetime + duration

    # Adjust the timezone if specified
    if target is not None:
        if isinstance(target, str):
            target = pd.Timezone.get(target)
        updated_dt = updated_dt.in_tz(target)

    return self._datetime.with_timezone(updated_dt.tz)


from pendulum import Duration, Timezone
from typing import Union

def format_duration(duration: Duration) -> str:
    """Format a given duration into a human-readable string.

    Args:
        duration (Duration): The duration object to be formatted.

    Returns:
        str: A human-readable string representing the duration.
    """
    hours, minutes = duration.in_hours().divmod(1)
    days, hours = divmod(hours, 24)
    return f"{days} day{'s' if days != 1 else ''}, {int(hours)} hour{'s' if hours != 1 else ''}, {minutes} minute{'s' if minutes != 1 else ''}"

class DataClass:
    @staticmethod
    def update_method(duration: Union[Duration, str]) -> None:
        """Update the object using a duration or string representation of a duration.

        Args:
            duration (Union[Duration, str]): The duration or string representation of a duration to be applied.

        Raises:
            ValueError: If an invalid duration is provided.
        """
        try:
            if isinstance(duration, Duration):
                pass  # Handle the case where duration is already an instance of Duration
            elif isinstance(duration, str):
                duration = Duration.from_string(duration)
                if not duration:
                    raise ValueError("Invalid duration string provided.")
            else:
                raise TypeError("Duration must be either a Duration object or a string representation of a duration.")
        except ValueError as e:
            raise ValueError(f"{e}: Use format_duration to convert durations into a human-readable string before providing them here.")