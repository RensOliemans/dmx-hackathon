from dataclasses import dataclass





@dataclass
class Color:
    r: int = 0
    g: int = 0
    b: int = 0

    def to_hex(self):
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

    @staticmethod
    def to_rgb(hex_code: str):
        color = hex_code.lstrip('#')
        r, g, b = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        return Color(r, g, b)

    def __add__(self, other):
        return Color(int(self.r + other.r), int(self.g + other.g), int(self.b + other.b))

    def __sub__(self, other):
        return Color(int(self.r - other.r), int(self.g - other.g), int(self.b - other.b))

    def __mul__(self, other):
        return Color(int(self.r * other), int(self.g * other), int(self.b * other))

    __rmul__ = __mul__
