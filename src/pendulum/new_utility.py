"""
Pendulum - Utility for performing some common calculations.

This module contains a new utility function that performs a specific calculation useful within the pendulum package.
"""

from typing import Union

from math import radians, sin, cos, atan2, sqrt, pi

class PendulumUtility:
    """
    Class for handling various pendulum-related calculations.
    """

    @staticmethod
    def angle_between(angle1: float, angle2: float) -> Union[float, None]:
        """
        Calculates the angle between two angles in radians.

        Args:
            angle1 (float): First angle in radians.
            angle2 (float): Second angle in radians.

        Returns:
            The difference between the two angles in radians, or None if the angles are equal.
        """
        diff = atan2(sin(angle1 - angle2), cos(angle1) * cos(angle2))
        if abs(diff) > pi:
            return (diff + 2 * pi) % (2 * pi)
        return diff

    @staticmethod
    def simple_pendulum(angle: float, length: float, gravity: float) -> Union[float, None]:
        """
        Calculates the angular acceleration of a simple pendulum.

        Args:
            angle (float): Angle of the pendulum in radians.
            length (float): Length of the pendulum in meters.
            gravity (float): Gravitational constant in m/s².

        Returns:
            The angular acceleration of the pendulum in rad/s², or None if the angle is equal to 0.
        """
        if abs(angle) < 1e-6:
            return None

        return -gravity * sin(angle) / length