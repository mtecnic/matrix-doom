"""Player controller: movement and shooting logic."""

from typing import Dict, List, Tuple

from config import Config
from input import InputHandler, KEY_MAP
from weapon import WeaponRegistry, Projectile
from world import World, CollisionManager


class PlayerController:
    """Handles player movement, shooting, and input processing."""

    def __init__(
        self,
        x: float,
        y: float,
        stats,
        weapon_registry: WeaponRegistry,
        world: World,
        collision_manager: CollisionManager,
        input_handler: InputHandler,
    ):
        """
        Initialize player controller.

        Args:
            x: Initial X position
            y: Initial Y position
            stats: PlayerStats instance
            weapon_registry: WeaponRegistry for weapon lookup
            world: World instance for entity management
            collision_manager: CollisionManager for collision detection
            input_handler: InputHandler for input processing
        """
        self.x = x
        self.y = y
        self.stats = stats
        self.weapon_registry = weapon_registry
        self.world = world
        self.collision_manager = collision_manager
        self.input_handler = input_handler
        self.facing: Tuple[float, float] = (1.0, 0.0)  # Default facing right
        self.last_shoot_time: float = 0.0
        self.current_weapon_name: str = "pulse_rifle"

    def move(self, dx: float, dy: float) -> None:
        """
        Move player by given delta.

        Args:
            dx: Change in X position
            dy: Change in Y position
        """
        if dx == 0.0 and dy == 0.0:
            return

        # Normalize diagonal movement
        if dx != 0.0 and dy != 0.0:
            length = (dx**2 + dy**2) ** 0.5
            dx /= length
            dy /= length

        # Update facing direction
        if dx != 0.0 or dy != 0.0:
            length = (dx**2 + dy**2) ** 0.5
            self.facing = (dx / length, dy / length)

        # Apply movement with collision detection
        success = self.world.update_entity_pos(self, dx, dy)
        if success:
            self.x += dx * Config.CHAR_SIZE
            self.y += dy * Config.CHAR_SIZE

    def update(self, dt: float) -> None:
        """
        Update player state each frame.

        Args:
            dt: Delta time since last frame
        """
        # Handle movement from input
        axis = self.input_handler.get_axis()
        dx, dy = axis
        if dx != 0.0 or dy != 0.0:
            # Scale movement by character size and dt
            speed = Config.CHAR_SIZE * dt * 2.0
            self.move(dx * speed, dy * speed)

        # Handle shooting
        keys = self.input_handler.update()
        if keys.get(KEY_MAP["action"], False):
            self._handle_shooting(dt)

    def _handle_shooting(self, dt: float) -> None:
        """Process shooting input."""
        # Check fire rate limit
        fire_rate = self.weapon_registry.get(self.current_weapon_name).fire_rate
        if dt < (1.0 / fire_rate) - self.last_shoot_time:
            return

        projectiles = self.shoot()
        if projectiles:
            self.last_shoot_time += dt

    def shoot(self) -> List[Projectile]:
        """
        Shoot current weapon.

        Returns:
            List of projectiles created
        """
        # Check ammo
        if not self.stats.use_ammo():
            return []

        weapon_config = self.weapon_registry.get(self.current_weapon_name)

        # Calculate projectile direction
        start_x = self.x + self.facing[0] * Config.CHAR_SIZE
        start_y = self.y + self.facing[1] * Config.CHAR_SIZE
        start = (start_x, start_y)

        # Normalize facing vector
        length = (self.facing[0] ** 2 + self.facing[1] ** 2) ** 0.5
        direction = (
            self.facing[0] / length,
            self.facing[1] / length,
        )

        # Create projectile
        # Calculate velocity from direction and speed
        dx, dy = direction
        speed = weapon_config.projectile_speed
        velocity = (dx * speed, dy * speed)

        projectile = Projectile(
            pos=start,
            velocity=velocity,
            damage=weapon_config.damage,
            lifetime=weapon_config.projectile_lifetime,
            effect=weapon_config.particle_effect,
        )

        # Check for collisions along the ray
        blocked, distance = self.collision_manager.raycast(start, direction)
        if blocked and distance < weapon_config.projectile_range:
            # Adjust projectile to stop at collision point
            end_x = start[0] + direction[0] * distance * Config.CHAR_SIZE
            end_y = start[1] + direction[1] * distance * Config.CHAR_SIZE
            projectile.end_point = (end_x, end_y)

        return [projectile]

    def set_current_weapon(self, name: str) -> bool:
        """
        Set current weapon by name.

        Args:
            name: Weapon name

        Returns:
            True if weapon exists, False otherwise
        """
        if name in self.weapon_registry.weapons:
            self.current_weapon_name = name
            return True
        return False

    def get_position(self) -> Tuple[float, float]:
        """Get current player position."""
        return (self.x, self.y)
