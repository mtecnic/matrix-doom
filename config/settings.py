"""Global configuration constants and settings."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """Global configuration constants and settings."""

    SCREEN_WIDTH: int = 80
    CHAR_SIZE: int = 12
    FPS: int = 60
