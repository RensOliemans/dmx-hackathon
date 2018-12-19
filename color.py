from dataclasses import dataclass


@dataclass
class Color:
    r: int = 0
    g: int = 0
    b: int = 0

    def __add__(self, other):
        return Color(int(self.r + other.r), int(self.g + other.g), int(self.b + other.b))

    def __sub__(self, other):
        return Color(int(self.r - other.r), int(self.g - other.g), int(self.b - other.b))

    def __mul__(self, other):
        return Color(int(self.r * other), int(self.g * other), int(self.b * other))

    __rmul__ = __mul__
