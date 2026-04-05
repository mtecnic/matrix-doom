"""Weapon definitions: PulseRifle, Shotgun, PlasmaCannon."""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from enum import Enum

from config import Config
from particle import ParticleEngine, ParticleEffect


class WeaponType(Enum):
    PULSE_RIFLE = "pulse_rifle"
    SHOTGUN = "shotgun"
    PLASMA_CANNON = "plasma_cannon"


@dataclass
class WeaponConfig:
    """Configuration for a weapon including fire rate, damage, and projectile settings."""
    name: str
    weapon_type: WeaponType
    damage: int
    fire_rate: float  # seconds between shots
    spread: float  # degrees
    projectile_speed: float
    projectile_lifetime: float  # seconds
    projectile_range: float  # max distance projectile can travel
    particle_effect: ParticleEffect
    pellets_per_shot: int = 1
    recoil: float = 0.0


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

        return True


class WeaponRegistry:
    """Registry of weapon configurations."""

    _weapons: Dict[str, WeaponConfig] = {}

    @classmethod
    def register(cls, config: WeaponConfig) -> None:
        """Register a weapon configuration."""
        cls._weapons[config.name] = config

    @classmethod
    def get(cls, name: str) -> WeaponConfig:
        """Get a weapon configuration by name."""
        if name not in cls._weapons:
            raise ValueError(f"Weapon '{name}' not found")
        return cls._weapons[name]

    @classmethod
    def initialize(cls) -> None:
        """Initialize default weapons."""
        cls._weapons.clear()

        pulse_config = WeaponConfig(
            name="pulse_rifle",
            weapon_type=WeaponType.PULSE_RIFLE,
            damage=25,
            fire_rate=0.15,
            spread=2.0,
            projectile_speed=400.0,
            projectile_lifetime=1.5,
            projectile_range=20.0,
            particle_effect=ParticleEffect.PULSE_BEAM,
            recoil=2.0,
        )

        shotgun_config = WeaponConfig(
            name="shotgun",
            weapon_type=WeaponType.SHOTGUN,
            damage=15,
            fire_rate=0.8,
            spread=15.0,
            projectile_speed=350.0,
            projectile_lifetime=0.8,
            projectile_range=10.0,
            particle_effect=ParticleEffect.SHOTGUN_SPREAD,
            pellets_per_shot=6,
            recoil=8.0,
        )

        plasma_config = WeaponConfig(
            name="plasma_cannon",
            weapon_type=WeaponType.PLASMA_CANNON,
            damage=60,
            fire_rate=0.5,
            spread=0.5,
            projectile_speed=250.0,
            projectile_lifetime=2.0,
            projectile_range=25.0,
            particle_effect=ParticleEffect.PLASMA_EXPLOSION,
            recoil=5.0,
        )

        cls.register(pulse_config)
        cls.register(shotgun_config)
        cls.register(plasma_config)

    @classmethod
    def list_all(cls) -> List[str]:
        """Return list of registered weapon names."""
        return list(cls._weapons.keys())


# Initialize default weapons on module load
WeaponRegistry.initialize()
