"""Procedural map generation with maze layouts."""

import random
from typing import List, Tuple

from config import Config
from utils import Vec2
from .map_data import MapData, RoomLayout, CellType


class MapGenerator:
    """Generates procedurally generated maps with maze-like layouts."""
    
    def __init__(self):
        """Initialize the map generator."""
        self.width = Config.SCREEN_WIDTH * 2  # Larger than screen for exploration
        self.height = Config.SCREEN_WIDTH * 2
        self.min_room_size = 5
        self.max_room_size = 15
        self.max_rooms = 10
    
    def generate(self, seed: int) -> MapData:
        """Generate a new map with the given seed."""
        random.seed(seed)
        
        # Initialize grid with walls
        cells = [[CellType.WALL for _ in range(self.width)] for _ in range(self.height)]
        rooms = []
        
        # Generate rooms
        for _ in range(self.max_rooms):
            room = self._create_random_room(cells, rooms)
            if room:
                rooms.append(room)
        
        # Connect rooms with corridors
        self._connect_rooms(cells, rooms)
        
        return MapData(
            width=self.width,
            height=self.height,
            cells=cells,
            rooms=rooms
        )
    
    def _create_random_room(self, cells: List[List[CellType]], existing_rooms: List[RoomLayout]) -> RoomLayout:
        """Create a random room that doesn't overlap with existing rooms."""
        width = random.randint(self.min_room_size, self.max_room_size)
        height = random.randint(self.min_room_size, self.max_room_size)
        x = random.randint(1, self.width - width - 1)
        y = random.randint(1, self.height - height - 1)
        
        # Check for overlap
        for room in existing_rooms:
            if (x < room.x + room.width + 1 and x + width + 1 > room.x and
                y < room.y + room.height + 1 and y + height + 1 > room.y):
                return None
        
        # Carve out the room
        for ry in range(y, y + height):
            for rx in range(x, x + width):
                if 0 < rx < self.width - 1 and 0 < ry < self.height - 1:
                    cells[ry][rx] = CellType.FLOOR
        
        return RoomLayout(x=x, y=y, width=width, height=height)
    
    def _connect_rooms(self, cells: List[List[CellType]], rooms: List[RoomLayout]) -> None:
        """Connect rooms with corridors using random walk."""
        for i in range(len(rooms) - 1):
            room1 = rooms[i]
            room2 = rooms[i + 1]
            
            # Get center points
            x1 = room1.x + room1.width // 2
            y1 = room1.y + room1.height // 2
            x2 = room2.x + room2.width // 2
            y2 = room2.y + room2.height // 2
            
            # Create L-shaped corridor
            # First horizontal, then vertical
            self._carve_corridor(cells, x1, y1, x2, y1)
            self._carve_corridor(cells, x2, y1, x2, y2)
    
    def _carve_corridor(self, cells: List[List[CellType]], x1: int, y1: int, x2: int, y2: int) -> None:
        """Carve a corridor from (x1, y1) to (x2, y2)."""
        # Horizontal corridor
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 < x < self.width - 1 and 0 < y1 < self.height - 1:
                cells[y1][x] = CellType.FLOOR
        
        # Vertical corridor
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 < x2 < self.width - 1 and 0 < y < self.height - 1:
                cells[y][x2] = CellType.FLOOR
