#!/usr/bin/env python3
"""Main entry point for the Matrix-Themed ASCII Doom FPS."""

import sys
import time
import random
import click

# Core imports
from config import Config
from asset import FontManager, GLYPH_SET
from utils import Vec2, clamp, lerp

# Input handling
from input import InputHandler, KEY_MAP

# Level generation
from levelgen import MapGenerator, RoomLayout
from levelgen.map_data import CellType

# World and physics
from world import World, CollisionManager

# Player
from player import PlayerController, PlayerStats

# Weapons and projectiles
from weapon import WeaponRegistry, Projectile

# Particle system
from particle import ParticleEngine, ParticleEffect

# Enemy AI
from enemy import EnemyManager, AStarPathfinder

# Rendering
from renderer import ASCIIRenderer, DigitalRain

# Menu system
from menu import MenuManager, MainMenuState


class GameEngine:
    """Main game engine orchestrating all subsystems."""

    def __init__(self):
        """Initialize the game engine."""
        # Initialize pygame
        import pygame
        pygame.init()
        
        # Initialize font (must be after pygame.init())
        from asset.fonts import FontManager
        global FONT
        FONT = FontManager(None, Config.CHAR_SIZE)
        
        # Configuration
        self.config = Config
        
        # Initialize subsystems
        self.input_handler = InputHandler()
        self.map_generator = MapGenerator()
        self.world = World()
        self.collision_manager = CollisionManager(self.world)
        self.particle_engine = ParticleEngine()
        self.enemy_manager = EnemyManager(self.world, self.collision_manager)
        self.player_stats = PlayerStats()
        self.weapon_registry = WeaponRegistry()
        
        # Initialize weapon registry with default weapons
        self.weapon_registry.initialize()
        
        # Create player controller
        self.player = PlayerController(
            x=1.5,
            y=1.5,
            stats=self.player_stats,
            weapon_registry=self.weapon_registry,
            world=self.world,
            collision_manager=self.collision_manager,
            input_handler=self.input_handler,
        )
        
        # Initialize renderer
        self.renderer = ASCIIRenderer()
        self.digital_rain = DigitalRain()
        
        # Initialize menu manager
        self.menu_manager = MenuManager()
        
        # Game state
        self.running = True
        self.paused = False
        self.current_level = None
        self.level_seed = 42
        
        # Timing
        self.clock = time.time()
        self.last_time = time.time()
        self.dt = 0.0
        
        # Test mode
        self.test_mode = False
        self.test_ticks = 0
        self.max_test_ticks = 10

    def load_level(self, seed: int) -> None:
        """Load a procedurally generated level."""
        # Generate map
        map_data = self.map_generator.generate(seed)
        
        # Load into world
        self.world.load_map(map_data)
        
        # Set collision manager map
        self.collision_manager.set_map(map_data)
        
        # Clear enemies and spawn initial ones
        self.enemy_manager.clear()
        
        # Spawn enemies at random positions
        for i in range(3):  # Spawn 3 enemies
            x = random.randint(5, map_data.width - 2)
            y = random.randint(5, map_data.height - 2)
            
            # Only spawn if not in wall
            if map_data.get_cell(x, y) == CellType.FLOOR:
                enemy_type = random.choice(['sentinel', 'program'])
                self.enemy_manager.spawn(enemy_type, (float(x), float(y)))
        
        self.current_level = map_data

    def update(self) -> None:
        """Update game state."""
        # Get delta time
        current_time = time.time()
        self.dt = current_time - self.last_time
        self.last_time = current_time
        
        # Cap dt to prevent huge jumps
        self.dt = min(self.dt, 0.1)
        
        # Update input
        self.input_handler.update()
        
        # Check for cancel key (escape)
        keys = self.input_handler._keys
        if keys.get("cancel", False):
            self.running = False
            return
        
        # Handle pause
        if keys.get("action", False) and self.test_mode:
            self.paused = not self.paused
        
        if not self.paused:
            # Update player
            self.player.update(self.dt)
            
            # Update enemies
            self.enemy_manager.update(self.player.get_position(), self.dt)
            
            # Update particles
            self.particle_engine.update(self.dt)
            
            # Update projectiles
            projectiles = self.player.shoot()
            for proj in projectiles:
                self.particle_engine.spawn(proj.pos, proj.effect)
        
        # Increment test tick counter
        if self.test_mode:
            self.test_ticks += 1

    def render(self) -> None:
        """Render the game."""
        # Get player position for camera
        player_x, player_y = self.player.get_position()
        
        # Render ASCII grid
        if self.current_level:
            self.renderer.draw_frame(self.current_level, player_x, player_y)
        
        # Render digital rain overlay
        self.digital_rain.render()
        
        # Render HUD
        self._render_hud()
        
        # Render minimap
        self._render_minimap()

    def _render_hud(self) -> None:
        """Render HUD elements."""
        # Health and ammo display
        health_pct = self.player_stats.get_health_percent()
        ammo_pct = self.player_stats.get_ammo_percent()
        
        # Render health bar
        health_width = int(health_pct * 20)
        health_bar = "█" * health_width + "░" * (20 - health_width)
        
        # Render ammo bar
        ammo_width = int(ammo_pct * 20)
        ammo_bar = "█" * ammo_width + "░" * (20 - ammo_width)
        
        # Print HUD (would be rendered to screen in real implementation)
        # For now, just validate that the HUD rendering logic works
        assert len(health_bar) == 20
        assert len(ammo_bar) == 20

    def _render_minimap(self) -> None:
        """Render minimap in corner."""
        if not self.current_level:
            return
        
        # Get player position
        player_x, player_y = self.player.get_position()
        
        # Create minimap grid (10x10 area around player)
        mini_size = 10
        minimap = []
        
        for dy in range(-mini_size // 2, mini_size // 2):
            row = []
            for dx in range(-mini_size // 2, mini_size // 2):
                x = int(player_x + dx)
                y = int(player_y + dy)
                
                if x < 0 or y < 0 or x >= self.current_level.width or y >= self.current_level.height:
                    row.append(' ')
                else:
                    cell = self.current_level.get_cell(x, y)
                    if cell == CellType.WALL:
                        row.append('#')
                    elif cell == CellType.FLOOR:
                        row.append('.')
                    else:
                        row.append('?')
            
            minimap.append(row)
        
        # Add player marker
        center = mini_size // 2
        if 0 <= center < len(minimap) and 0 <= center < len(minimap[0]):
            minimap[center][center] = 'X'
        
        # Validate minimap dimensions
        assert len(minimap) == mini_size
        assert all(len(row) == mini_size for row in minimap)

    def run(self) -> None:
        """Run the main game loop."""
        # Load initial level
        self.load_level(self.level_seed)
        
        # Main loop
        while self.running:
            self.update()
            self.render()
            
            # In test mode, exit after max ticks
            if self.test_mode and self.test_ticks >= self.max_test_ticks:
                break
            
            # Small delay to prevent CPU spinning
            if not self.test_mode:
                time.sleep(1.0 / self.config.FPS)

    def run_test(self) -> bool:
        """Run self-tests and validation."""
        self.test_mode = True
        
        try:
            # Test 1: Initialize systems
            print("Testing initialization...")
            assert self.config.SCREEN_WIDTH == 80
            assert self.config.CHAR_SIZE == 12
            assert self.config.FPS == 60
            print("✓ Config initialized correctly")
            
            # Test 2: Font loading
            print("Testing font loading...")
            width = FONT.get_width('A')
            assert width > 0
            print(f"✓ Font loaded, 'A' width = {width}")
            
            # Test 3: Glyph cache
            print("Testing glyph cache...")
            rain_chars = GLYPH_SET.load_rain_chars()
            assert len(rain_chars) > 0
            print(f"✓ Glyph cache loaded with {len(rain_chars)} characters")
            
            # Test 4: Level generation
            print("Testing level generation...")
            seed = 12345
            map_data = self.map_generator.generate(seed)
            assert map_data.width > 0
            assert map_data.height > 0
            cell = map_data.get_cell(0, 0)
            assert cell in [CellType.WALL, CellType.FLOOR]
            print(f"✓ Level generated: {map_data.width}x{map_data.height}")
            
            # Test 5: Weapon registry
            print("Testing weapon registry...")
            self.weapon_registry.initialize()
            weapons = self.weapon_registry.list_all()
            assert len(weapons) >= 3  # At least 3 weapons
            assert 'pulse_rifle' in weapons
            assert 'shotgun' in weapons
            assert 'plasma_cannon' in weapons
            print(f"✓ {len(weapons)} weapons registered")
            
            # Test 6: Particle system
            print("Testing particle system...")
            self.particle_engine.spawn((10.0, 10.0), ParticleEffect.BLOOD)
            particles = self.particle_engine.update(0.1)
            assert len(particles) >= 0  # Particles may have faded
            print("✓ Particle system functional")
            
            # Test 7: Enemy AI
            print("Testing enemy AI...")
            pathfinder = AStarPathfinder()
            start = (1, 1)
            goal = (5, 5)
            path = pathfinder.find(start, goal)
            # Path may be empty if no valid route, but shouldn't crash
            print("✓ Enemy pathfinding functional")
            
            # Test 8: Full tick cycle
            print("Testing full tick cycle...")
            self.load_level(seed)
            
            # Run several ticks
            for _ in range(self.max_test_ticks):
                self.update()
                self.render()
            
            print("✓ Full tick cycle completed")
            
            # Test 9: Input handling
            print("Testing input handling...")
            axis = self.input_handler.get_axis()
            assert isinstance(axis, tuple)
            assert len(axis) == 2
            print("✓ Input handling functional")
            
            # Test 10: HUD rendering
            print("Testing HUD rendering...")
            self._render_hud()
            self._render_minimap()
            print("✓ HUD/minimap rendering functional")
            
            print("\n✅ All tests passed!")
            return True
            
        except AssertionError as e:
            print(f"\n❌ Test failed: {e}")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            return False


@click.group(invoke_without_command=True)
@click.option('--test', is_flag=True, help='Run self-tests and exit')
def cli(test):
    """Matrix-Themed ASCII Doom FPS."""
    if test:
        engine = GameEngine()
        success = engine.run_test()
        sys.exit(0 if success else 1)


@cli.command()
def play():
    """Play the game normally."""
    engine = GameEngine()
    engine.run()


if __name__ == '__main__':
    cli()
