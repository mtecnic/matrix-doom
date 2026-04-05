"""Vector and interpolation utilities."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Vec2:
    """Immutable 2D vector with basic operations."""

    x: float
    y: float

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vec2":
        return Vec2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> "Vec2":
        return Vec2(self.x / scalar, self.y / scalar)

    def dot(self, other: "Vec2") -> float:
        return self.x * other.x + self.y * other.y

    def length(self) -> float:
        return (self.x * self.x + self.y * self.y) ** 0.5

    def distance(self, other: "Vec2") -> float:
        return (self - other).length()

    def normalize(self) -> "Vec2":
        length = self.length()
        if length == 0:
            return Vec2(0, 0)
        return self / length

    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)


def clamp(x: float, lo: float, hi: float) -> float:
    """Clamp a value between lo and hi."""
    return max(lo, min(x, hi))


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b by factor t (0 <= t <= 1)."""
    t = clamp(t, 0.0, 1.0)
    return a + (b - a) * t
