"""Map data structures for level generation."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class CellType(Enum):
    """Types of cells in the map."""
    EMPTY = 0
    WALL = 1
    FLOOR = 2
    DOOR = 3


@dataclass
class RoomLayout:
    """Represents a room in the map."""
    x: int
    y: int
    width: int
    height: int
    room_type: str = "standard"


@dataclass
class MapData:
    """Complete map data structure."""
    width: int
    height: int
    cells: List[List[CellType]]
    rooms: List[RoomLayout]
    
    def get_cell(self, x: int, y: int) -> CellType:
        """Get the cell type at the given coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return CellType.EMPTY
    
    def set_cell(self, x: int, y: int, cell_type: CellType) -> None:
        """Set the cell type at the given coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x] = cell_type
