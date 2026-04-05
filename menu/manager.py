"""Menu manager for handling game menus."""

import pygame
from typing import Dict, Any
from config import Config
from menu.state import MainMenuState


class MenuManager:
    """Manages game menus and UI states."""

    def __init__(self):
        """Initialize the menu manager."""
        self.current_state = MainMenuState()
        self.states: Dict[str, Any] = {}
        self.active = True

    def update(self, dt: float) -> None:
        """Update menu state."""
        if self.current_state:
            self.current_state.update(dt)

    def render(self) -> None:
        """Render the current menu."""
        if self.current_state:
            self.current_state.render()

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handle menu input events."""
        if self.current_state:
            self.current_state.handle_input(event)

    def set_state(self, state_name: str) -> None:
        """Set the current menu state."""
        if state_name in self.states:
            self.current_state = self.states[state_name]
