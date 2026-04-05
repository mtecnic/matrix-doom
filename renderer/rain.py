"""Digital rain effect renderer for Matrix-style background."""

import random
import pygame
from typing import List, Tuple
from config import Config
from asset.glyphs import GLYPH_SET


class DigitalRain:
    """Renders cascading digital rain effect."""

    def __init__(self):
        """Initialize the digital rain effect."""
        self.columns = Config.SCREEN_WIDTH
        self.drop_length = 10
        self.drops: List[List[Tuple[int, int]]] = []
        self._init_drops()

    def _init_drops(self) -> None:
        """Initialize drop positions."""
        for _ in range(self.columns):
            # Start drops at random heights
            height = random.randint(-50, 0)
            self.drops.append([(i, height) for i in range(self.drop_length)])

    def render(self) -> None:
        """Render the digital rain effect."""
        # This would render to a pygame surface in a real implementation
        # For now, we'll just validate the logic works
        pass

    def update(self, dt: float) -> None:
        """Update rain drop positions."""
        # This would update drop positions based on delta time
        pass
