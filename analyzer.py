from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from maze import Maze

from cell import Cell
from algorithm import Algorithm
from ascii import ASCII

class Analyzer:
    def __init__(self, maze: 'Maze'):
        self.maze: 'Maze' = maze

    def __call__(self, algorithm: Algorithm=Algorithm._NONE) -> dict[str, int]:
        if algorithm is Algorithm._NONE:
            return self.analyze_maze()
        else:
            return self.analyze_path(algorithm)


    def analyze_path(self, algorithm: Algorithm) -> dict[str, int]:
        path: list[Cell] = self.maze.paths[algorithm]

        length: int = len(path)

        turns: int = 0
    
        for i in range(len(path)-2):
            if not (path[i].y == path[i+2].y or path[i].x == path[i+2].x):
                turns += 1
        
        branches: int = 0
        for i in range(len(path)):
            cell: Cell = path[i]
            if len(cell.neighbors(self.maze.maze)) > 2:
                branches += 1

        visited: int = sum([1 for row in self.maze.maze for cell in row if cell.is_visited(algorithm)])

        return {
            'length': length,
            'turns': turns,
            'branches': branches,
            'visited': visited
        }

    def analyze_maze(self) -> dict[str, int]:
        valid = sum([1 for row in self.maze.maze for cell in row if not cell.forbidden])

        branches = sum([1 for row in self.maze.maze for cell in row if len(cell.neighbors(self.maze.maze)) > 2])

        walls_count: int = str(self.maze).count(ASCII.wall_v) + str(self.maze).count(ASCII.wall_h)

        poles_count: int = str(self.maze).count(ASCII.pole)

        return {
            'valid': valid,
            'branches': branches,
            'walls': walls_count,
            'poles': poles_count
        }