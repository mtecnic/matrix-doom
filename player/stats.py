"""Player stats tracking: health, ammo, and related metrics."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PlayerStats:
    """Tracks player health, ammo, and basic combat stats."""

    max_health: int = 100
    health: int = 100
    max_ammo: int = 30
    ammo: int = 30
    score: int = 0
    kills: int = 0
    deaths: int = 0

    def take_damage(self, amount: int) -> bool:
        """Apply damage to player. Returns True if player is still alive."""
        self.health = max(0, self.health - amount)
        return self.health > 0

    def heal(self, amount: int) -> int:
        """Heal player by amount. Returns actual healing done."""
        before = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - before

    def use_ammo(self, amount: int = 1) -> bool:
        """Try to consume ammo. Returns True if successful."""
        if self.ammo >= amount:
            self.ammo -= amount
            return True
        return False

    def reload(self) -> None:
        """Refill ammo to maximum."""
        self.ammo = self.max_ammo

    def add_score(self, points: int) -> None:
        """Add points to player score."""
        self.score += points

    def record_kill(self) -> None:
        """Record a kill and add score."""
        self.kills += 1
        self.add_score(100)

    def record_death(self) -> None:
        """Record a death."""
        self.deaths += 1

    def is_alive(self) -> bool:
        """Check if player is still alive."""
        return self.health > 0

    def is_low_ammo(self) -> bool:
        """Check if ammo is critically low (≤20%)."""
        return self.ammo <= int(self.max_ammo * 0.2)

    def get_health_percent(self) -> float:
        """Return health as percentage (0.0–1.0)."""
        return self.health / self.max_health

    def get_ammo_percent(self) -> float:
        """Return ammo as percentage (0.0–1.0)."""
        return self.ammo / self.max_ammo
