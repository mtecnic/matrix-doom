"""ASCII renderer for rendering game world as text."""

import pygame
from typing import List, Tuple
from config import Config
from levelgen.map_data import MapData, CellType


class ASCIIRenderer:
    """Renders the game world using ASCII characters on a pygame surface."""

    def __init__(self):
        """Initialize the ASCII renderer."""
        self.screen_width = Config.SCREEN_WIDTH
        self.char_size = Config.CHAR_SIZE
        self.colors = {
            'wall': (0, 255, 0),      # Matrix green
            'floor': (0, 50, 0),      # Dark green
            'empty': (0, 0, 0),       # Black background
            'player': (255, 255, 255), # White
            'enemy': (255, 0, 0),     # Red for enemies
            'ammo': (255, 255, 0),    # Yellow for ammo
            'health': (0, 255, 0),    # Green for health
        }

    def draw_frame(self, map_data: MapData, player_x: float, player_y: float) -> None:
        """
        Draw the current frame using ASCII characters.

        Args:
            map_data: The map data to render
            player_x: Player X position
            player_y: Player Y position
        """
        # This would render to a pygame surface in a real implementation
        # For now, we'll just validate the rendering logic works
        pass

    def render_text(self, text: str, x: int, y: int, color: Tuple[int, int, int] = None) -> None:
        """
        Render text at the given position.

        Args:
            text: Text to render
            x: X position
            y: Y position
            color: RGB color tuple (default: matrix green)
        """
        pass

    def clear(self) -> None:
        """Clear the screen."""
        pass
