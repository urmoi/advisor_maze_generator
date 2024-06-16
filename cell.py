import random

from enum import Enum
from algorithm import Algorithm
from direction import DIR, Dir

class Cell:
    def __init__(self, pos:tuple[int, int]):
        self.y: int = pos[0]
        self.x: int = pos[1]
        self.pos: tuple = pos
        self.walls: int = 0xFF
        self.zone: Zone = Zone.NONE
        self.forbidden: bool = False
        self._visited: set[Algorithm] = set()
        self._paths: set[Algorithm] = set()

    def path(self, algorithm:Algorithm):
        self._paths.add(algorithm)

    def visited(self, algorithm:Algorithm):
        self._visited.add(algorithm)

    def is_path(self, algorithm:Algorithm|None=None):
        if algorithm:
            return algorithm in self._paths
        return bool(self._paths)
    
    def is_visited(self, algorithm:Algorithm|None=None):
        if algorithm:
            return algorithm in self._visited
        return bool(self._visited)

    def neighbors(self, maze: list[list['Cell']], all: bool=False) -> list[tuple['Cell', Dir]]:
        neighbors: list[tuple[Cell, Dir]] = []
        for direction in [DIR.UP, DIR.RIGHT, DIR.DOWN, DIR.LEFT]:
            if not all and self.walls & direction.wall:
                continue
            (y, x) = (self.y + direction.y, self.x + direction.x)
            (height, width) = (len(maze), len(maze[0]))
            if 0 <= y < height and 0 <= x < width:
                neighbor: Cell = maze[y][x]
                if all or not neighbor.forbidden:
                    neighbors.append((neighbor, direction))
        random.shuffle(neighbors)
        return neighbors
    
    def neighbor(self, maze: list[list['Cell']], direction: Dir=DIR._EMPTY, all=False) -> tuple['Cell', Dir]:
        neighbors: list[tuple[Cell, Dir]] = self.neighbors(maze=maze, all=all)
        if not direction == DIR._EMPTY:
            y, x = (self.y + direction.y, self.x + direction.x)
            return (maze[y][x], direction)
        else:
            return neighbors[0]

    def __str__(self):
        return f"({self.y}, {self.x})"

    def __repr__(self):
        return f"Cell({self.y}, {self.x})"


class Zone(Enum):
    NONE = 0
    START = 1
    END = 2
