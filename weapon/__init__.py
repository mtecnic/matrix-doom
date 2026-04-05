"""Weapon module: weapon logic, projectile types, particle effects per weapon."""

from .types import WeaponRegistry
from .fx import Projectile

__all__ = ["WeaponRegistry", "Projectile"]
