"""World module for physics, collision detection, and entity management."""

from typing import List, Tuple

from config import Config
from utils import Vec2
from levelgen import MapData, CellType


class World:
    """Manages the game world, entities, and map data."""
    
    def __init__(self):
        """Initialize the world."""
        self.map_data: MapData = None
        self.entities: List[object] = []
    
    def load_map(self, map_data: MapData) -> None:
        """Load a map into the world."""
        self.map_data = map_data
    
    def update_entity_pos(self, entity: object, dx: float, dy: float) -> bool:
        """Update entity position with collision detection."""
        if self.map_data is None:
            return False
        
        # Get current position
        x, y = entity.x, entity.y
        
        # Calculate new position
        new_x = x + dx
        new_y = y + dy
        
        # Check for collisions with walls
        if self._is_wall(new_x, new_y):
            return False
        
        # Update position
        entity.x = new_x
        entity.y = new_y
        return True
    
    def _is_wall(self, x: float, y: float) -> bool:
        """Check if a position is a wall."""
        if self.map_data is None:
            return True
        
        # Convert to grid coordinates
        grid_x = int(x)
        grid_y = int(y)
        
        # Check bounds
        if grid_x < 0 or grid_y < 0 or grid_x >= self.map_data.width or grid_y >= self.map_data.height:
            return True
        
        # Check cell type
        cell = self.map_data.get_cell(grid_x, grid_y)
        return cell == CellType.WALL
    
    def get_entities_in_area(self, center_x: float, center_y: float, radius: float) -> List[object]:
        """Get entities within a radius of the given position."""
        nearby = []
        for entity in self.entities:
            ex, ey = entity.x, entity.y
            dist = ((ex - center_x) ** 2 + (ey - center_y) ** 2) ** 0.5
            if dist <= radius:
                nearby.append(entity)
        return nearby


class CollisionManager:
    """Manages collision detection in the world."""
    
    def __init__(self, world: World):
        """Initialize collision manager."""
        self.world = world
    
    def set_map(self, map_data: MapData) -> None:
        """Set the map for collision detection."""
        self.world.map_data = map_data
    
    def raycast(self, start: Tuple[float, float], direction: Tuple[float, float]) -> Tuple[bool, float]:
        """
        Perform raycast for collision detection.
        
        Args:
            start: Starting position (x, y)
            direction: Direction vector (dx, dy)
        
        Returns:
            Tuple of (blocked, distance)
        """
        if self.world.map_data is None:
            return (True, 0.0)
        
        x, y = start
        dx, dy = direction
        
        # Normalize direction
        length = (dx ** 2 + dy ** 2) ** 0.5
        if length > 0:
            dx, dy = dx / length, dy / length
        
        # Raycast step size
        step = 0.1
        max_distance = 10.0  # Max raycast distance
        
        distance = 0.0
        while distance < max_distance:
            # Calculate position
            check_x = x + dx * distance
            check_y = y + dy * distance
            
            # Check if wall
            if self.world._is_wall(check_x, check_y):
                return (True, distance)
            
            distance += step
        
        return (False, max_distance)
    
    def check_aabb(self, x: float, y: float, width: float, height: float) -> bool:
        """Check if an AABB collides with walls."""
        # Check corners
        corners = [
            (x, y),
            (x + width, y),
            (x, y + height),
            (x + width, y + height),
        ]
        
        for cx, cy in corners:
            if self.world._is_wall(cx, cy):
                return True
        
        return False
