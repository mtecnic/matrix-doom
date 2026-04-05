"""Input state management for keyboard/mouse handling."""

from typing import Dict, Tuple

import pygame

from config import Config
from input.keys import MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT, MOUSE_X1, MOUSE_X2


class InputHandler:
    """Handles keyboard and mouse input state."""

    def __init__(self) -> None:
        self._keys: Dict[str, bool] = {}
        self._mouse_buttons: Dict[int, bool] = {}
        self._mouse_pos: Tuple[int, int] = (0, 0)
        self._mouse_rel: Tuple[int, int] = (0, 0)

        # Initialize key states
        for key_name in ["up", "down", "left", "right", "action", "cancel"]:
            self._keys[key_name] = False

        # Initialize mouse button states
        for btn in [MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT, MOUSE_X1, MOUSE_X2]:
            self._mouse_buttons[btn] = False

    def update(self) -> Dict[str, bool]:
        """Update input state from pygame events and return key states."""
        # Reset key states
        for key_name in self._keys:
            self._keys[key_name] = False

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._keys["cancel"] = True
            elif event.type == pygame.KEYDOWN:
                self._handle_key_down(event.key)
            elif event.type == pygame.KEYUP:
                self._handle_key_up(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_buttons[event.button] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_buttons[event.button] = False
            elif event.type == pygame.MOUSEMOTION:
                self._mouse_pos = event.pos
                self._mouse_rel = event.rel

        return dict(self._keys)

    def get_axis(self) -> Tuple[float, float]:
        """Get normalized input axis from keyboard."""
        x, y = 0.0, 0.0

        if self._keys.get("left", False):
            x -= 1.0
        if self._keys.get("right", False):
            x += 1.0
        if self._keys.get("up", False):
            y -= 1.0
        if self._keys.get("down", False):
            y += 1.0

        # Normalize diagonal movement
        if x != 0.0 and y != 0.0:
            factor = 1.0 / (2 ** 0.5)
            x *= factor
            y *= factor

        return (x, y)

    def is_key_pressed(self, key_name: str) -> bool:
        """Check if a named key is currently pressed."""
        return self._keys.get(key_name, False)

    def is_mouse_button_pressed(self, button: int) -> bool:
        """Check if a mouse button is currently pressed."""
        return self._mouse_buttons.get(button, False)

    def get_mouse_pos(self) -> Tuple[int, int]:
        """Get current mouse position relative to screen."""
        return self._mouse_pos

    def get_mouse_rel(self) -> Tuple[int, int]:
        """Get relative mouse movement since last frame."""
        return self._mouse_rel

    def _handle_key_down(self, key: int) -> None:
        """Handle key down event."""
        if key == KEY_MAP["up"]:
            self._keys["up"] = True
        elif key == KEY_MAP["down"]:
            self._keys["down"] = True
        elif key == KEY_MAP["left"]:
            self._keys["left"] = True
        elif key == KEY_MAP["right"]:
            self._keys["right"] = True
        elif key == KEY_MAP["action"]:
            self._keys["action"] = True
        elif key == KEY_MAP["cancel"]:
            self._keys["cancel"] = True

    def _handle_key_up(self, key: int) -> None:
        """Handle key up event."""
        if key == KEY_MAP["up"]:
            self._keys["up"] = False
        elif key == KEY_MAP["down"]:
            self._keys["down"] = False
        elif key == KEY_MAP["left"]:
            self._keys["left"] = False
        elif key == KEY_MAP["right"]:
            self._keys["right"] = False
        elif key == KEY_MAP["action"]:
            self._keys["action"] = False
        elif key == KEY_MAP["cancel"]:
            self._keys["cancel"] = False
