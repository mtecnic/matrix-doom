"""Pygame font loading and width calculation."""

import pygame
from typing import Final

from config import Config


class FontManager:
    """Manages font loading and character width calculation."""

    def __init__(self, font_path: str, size: int):
        self._font = pygame.font.Font(font_path, size)
        self._char_cache: dict[str, int] = {}

    def get_width(self, char: str) -> int:
        """Return the pixel width of a single character."""
        if char not in self._char_cache:
            self._char_cache[char] = self._font.size(char)[0]
        return self._char_cache[char]


# Initialize font lazily to avoid issues during module import
FONT: Final[FontManager] = None  # Will be initialized by GameEngine
