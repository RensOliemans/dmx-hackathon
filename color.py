"""
Module containing the Color dataclass
"""
from dataclasses import dataclass


@dataclass
class Color:
    """Color object, having r, g, b, and a to_hex method."""
    r: int = 0
    g: int = 0
    b: int = 0

    def to_hex(self):
        """Converts this object to a hex representation"""
        return "#{:02X}{:02X}{:02X}".format(self.r, self.g, self.b)

    @staticmethod
    def to_rgb(hex_code: str):
        """Converts a given hex code to a Color object with proper rgb values.

        :param: hex_code, color code in hex (with or without '#' to convert)
        """
        color = hex_code.lstrip('#')
        return Color(*tuple(int(color[i:i + 2], 16) for i in (0, 2, 4)))

    def __add__(self, other):
        return Color(int(self.r + other.r), int(self.g + other.g), int(self.b + other.b))

    def __sub__(self, other):
        return Color(int(self.r - other.r), int(self.g - other.g), int(self.b - other.b))

    def __mul__(self, other):
        return Color(int(self.r * other), int(self.g * other), int(self.b * other))

    __rmul__ = __mul__
