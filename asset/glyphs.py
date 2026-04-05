"""Matrix rain character cache for rendering."""

import random
from typing import Final, List

from config import Config


class GlyphSet:
    """Cache of characters used in Matrix rain effect."""

    def __init__(self):
        # Katakana + Latin + numbers + symbols
        base_chars = [
            "アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "0123456789",
            "αβγδεζηθικλμνξοπρστυφχψω",
            "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
        ]
        self._chars = "".join(base_chars)
        self._cache: List[str] = []

    def load_rain_chars(self) -> List[str]:
        """Return a shuffled list of characters for rain effect."""
        if not self._cache:
            self._cache = list(self._chars)
            random.shuffle(self._cache)
        return self._cache


GLYPH_SET: Final[GlyphSet] = GlyphSet()
