"""Projectile and particle effects for weapons."""

from typing import Tuple, List
from dataclasses import dataclass
from enum import Enum

from config import Config
from particle import ParticleEngine, ParticleEffect


@dataclass
class Projectile:
    """A projectile fired from a weapon."""
    pos: Tuple[float, float]
    velocity: Tuple[float, float]
    damage: int
    lifetime: float
    effect: ParticleEffect
    active: bool = True

    def update(self, dt: float) -> bool:
        """Update projectile position and lifetime. Returns False when expired."""
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.active = False
            return False

        x, y = self.pos
        vx, vy = self.velocity
        self.pos = (x + vx * dt, y + vy * dt)

        # Check screen bounds
        if (
            x < 0
            or x > Config.SCREEN_WIDTH
            or y < 0
            or y > Config.SCREEN_HEIGHT
        ):
            self.active = False
            return False

        # Spawn trail particles
        ParticleEngine.spawn(self.pos, self.effect)

        return True


def spawn_explosion(pos: Tuple[float, float], effect: ParticleEffect) -> None:
    """Spawn an explosion effect at the given position."""
    ParticleEngine.spawn(pos, effect)


def create_projectile_from_weapon(
    pos: Tuple[float, float],
    direction: Tuple[float, float],
    weapon_name: str,
) -> Projectile:
    """Create a projectile based on a weapon configuration."""
    from .types import WeaponRegistry

    config = WeaponRegistry.get(weapon_name)
    speed = config.projectile_speed

    # Normalize direction
    dx, dy = direction
    length = (dx**2 + dy**2) ** 0.5
    if length > 0:
        dx, dy = dx / length, dy / length

    velocity = (dx * speed, dy * speed)

    return Projectile(
        pos=pos,
        velocity=velocity,
        damage=config.damage,
        lifetime=config.projectile_lifetime,
        effect=config.particle_effect,
    )


def create_shotgun_projectiles(
    pos: Tuple[float, float],
    direction: Tuple[float, float],
    weapon_name: str,
) -> List[Projectile]:
    """Create multiple projectiles for shotgun spread."""
    from .types import WeaponRegistry
    import math

    config = WeaponRegistry.get(weapon_name)
    speed = config.projectile_speed
    spread_deg = config.spread

    # Normalize direction
    dx, dy = direction
    length = (dx**2 + dy**2) ** 0.5
    if length > 0:
        dx, dy = dx / length, dy / length

    base_angle = math.atan2(dy, dx)
    projectiles = []

    for i in range(config.pellets_per_shot):
        # Calculate angle offset for this pellet
        offset = (i - config.pellets_per_shot // 2) * math.radians(spread_deg)
        angle = base_angle + offset

        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed

        projectiles.append(
            Projectile(
                pos=pos,
                velocity=(vx, vy),
                damage=config.damage,
                lifetime=config.projectile_lifetime,
                effect=config.particle_effect,
            )
        )

    return projectiles
