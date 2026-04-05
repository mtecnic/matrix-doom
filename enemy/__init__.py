"""Enemy AI and pathfinding module."""

from dataclasses import dataclass
from typing import List, Tuple
import heapq

from config import Config
from utils import Vec2
from world import World, CollisionManager
from levelgen import MapData, CellType


@dataclass
class EnemyEntity:
    """Represents an enemy in the game."""
    x: float
    y: float
    health: int = 100
    max_health: int = 100
    damage: int = 20
    speed: float = 2.0
    enemy_type: str = "sentinel"
    alive: bool = True
    
    def take_damage(self, amount: int) -> None:
        """Take damage and check if dead."""
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False
    
    def get_position(self) -> Tuple[float, float]:
        """Get current position."""
        return (self.x, self.y)


class AStarPathfinder:
    """A* pathfinding for enemy movement."""
    
    def __init__(self):
        """Initialize pathfinder."""
        self.world: World = None
    
    def set_world(self, world: World) -> None:
        """Set the world for pathfinding."""
        self.world = world
    
    def find(self, start: Tuple[float, float], goal: Tuple[float, float]) -> List[Tuple[float, float]]:
        """
        Find path from start to goal using A*.
        
        Args:
            start: Starting position (x, y)
            goal: Goal position (x, y)
        
        Returns:
            List of positions representing the path
        """
        if self.world is None or self.world.map_data is None:
            return []
        
        start_grid = (int(start[0]), int(start[1]))
        goal_grid = (int(goal[0]), int(goal[1]))
        
        # Check if start or goal is in a wall
        if self._is_wall(start_grid[0], start_grid[1]):
            return []
        if self._is_wall(goal_grid[0], goal_grid[1]):
            return []
        
        # A* algorithm
        open_set = [(0, start_grid)]
        came_from = {}
        g_score = {start_grid: 0}
        f_score = {start_grid: self._heuristic(start_grid, goal_grid)}
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current == goal_grid:
                # Reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path
            
            for neighbor in self._get_neighbors(current):
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._heuristic(neighbor, goal_grid)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return []  # No path found
    
    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Calculate heuristic (Manhattan distance)."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def _get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring cells."""
        neighbors = []
        x, y = pos
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.world.map_data.width and 
                0 <= ny < self.world.map_data.height and
                not self._is_wall(nx, ny)):
                neighbors.append((nx, ny))
        
        return neighbors
    
    def _is_wall(self, x: int, y: int) -> bool:
        """Check if a cell is a wall."""
        cell = self.world.map_data.get_cell(x, y)
        return cell == CellType.WALL


class EnemyManager:
    """Manages all enemies in the game."""
    
    def __init__(self, world: World, collision_manager: CollisionManager):
        """Initialize enemy manager."""
        self.world = world
        self.collision_manager = collision_manager
        self.enemies: List[EnemyEntity] = []
        self.pathfinder = AStarPathfinder()
        self.pathfinder.set_world(world)
    
    def spawn(self, type: str, pos: Tuple[float, float]) -> EnemyEntity:
        """Spawn a new enemy."""
        enemy = EnemyEntity(
            x=pos[0],
            y=pos[1],
            enemy_type=type,
            health=100 if type == "sentinel" else 50,
            damage=20 if type == "sentinel" else 15,
            speed=2.0 if type == "sentinel" else 2.5
        )
        self.enemies.append(enemy)
        self.world.entities.append(enemy)
        return enemy
    
    def update(self, player_pos: Tuple[float, float], dt: float) -> None:
        """Update all enemies."""
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            
            # Calculate distance to player
            ex, ey = enemy.x, enemy.y
            px, py = player_pos
            dist = ((px - ex) ** 2 + (py - ey) ** 2) ** 0.5
            
            # Move towards player if within aggro range
            if dist < 8.0:  # Aggro range
                # Find path to player
                path = self.pathfinder.find((enemy.x, enemy.y), player_pos)
                
                if path and len(path) > 1:
                    # Move towards next path point
                    next_pos = path[1]
                    dx = next_pos[0] - enemy.x
                    dy = next_pos[1] - enemy.y
                    
                    # Normalize and apply speed
                    length = (dx ** 2 + dy ** 2) ** 0.5
                    if length > 0:
                        dx, dy = dx / length, dy / length
                        speed = enemy.speed * dt
                        
                        # Try to move
                        old_x, old_y = enemy.x, enemy.y
                        success = self.world.update_entity_pos(enemy, dx * speed, dy * speed)
                        
                        # If couldn't move, try alternate direction
                        if not success:
                            # Try perpendicular directions
                            for alt_dx, alt_dy in [(dy, -dx), (-dy, dx)]:
                                if self.world.update_entity_pos(enemy, alt_dx * speed, alt_dy * speed):
                                    break
    
    def clear(self) -> None:
        """Clear all enemies."""
        self.enemies.clear()
        self.world.entities = [e for e in self.world.entities if not isinstance(e, EnemyEntity)]
