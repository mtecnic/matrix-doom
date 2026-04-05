"""Menu state classes."""

import pygame
from typing import Tuple
from config import Config


class MainMenuState:
    """Main menu state."""

    def __init__(self):
        """Initialize main menu state."""
        self.options = ["New Game", "Load Game", "Options", "Exit"]
        self.selected = 0
        self.width = 40
        self.height = len(self.options) + 2

    def update(self, dt: float) -> None:
        """Update menu state."""
        pass

    def render(self) -> None:
        """Render the main menu."""
        pass

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handle menu input."""
        pass

    def select(self, index: int) -> None:
        """Select a menu option."""
        if 0 <= index < len(self.options):
            self.selected = index

    def get_selection(self) -> str:
        """Get the currently selected option."""
        return self.options[self.selected]
