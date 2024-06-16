import random
import time

from enum import Enum

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from maze import Maze

from cell import Cell, Zone
from algorithm import Algorithm
from direction import DIR, Dir

class MakerSteps(Enum):
    ZONES = 0
    PATH = 1
    MULTIPLE = 2
    FINAL = 3


class Maker:
    def __init__(self, maze: 'Maze') -> None:
        self.maze: 'Maze' = maze
        self.steps: dict[MakerSteps, bool] = {
            MakerSteps.ZONES: False,
            MakerSteps.PATH: False,
            MakerSteps.MULTIPLE: False,
            MakerSteps.FINAL: False
        }

    def __call__(self, steps: list[MakerSteps]=list(MakerSteps)) -> bool:
        if not self.maze:
            return False
        
        if not self.steps[MakerSteps.ZONES] and MakerSteps.ZONES in steps:
            self.steps[MakerSteps.ZONES] = self.make_zones()
        if not self.steps[MakerSteps.PATH] and MakerSteps.PATH in steps:
            self.steps[MakerSteps.PATH] = self.make_single_path()
        if not self.steps[MakerSteps.MULTIPLE] and self.steps[MakerSteps.PATH] and MakerSteps.MULTIPLE in steps:
            self.steps[MakerSteps.MULTIPLE] = self.make_multiple_paths()

        self.steps[MakerSteps.FINAL] = self.steps[MakerSteps.ZONES] and (self.steps[MakerSteps.PATH] or self.steps[MakerSteps.MULTIPLE])

        self.maze.hash = self.maze.__hash__()

        self.maze.visualize(step=True)

        return True
    
    def make_zones(self) -> bool:
        for pos in self.maze.start_zone:
            self.maze.cell(pos).zone = Zone.START
            if not pos in self.maze.start_path:
                self.maze.cell(pos).forbidden = True
        for pos in self.maze.end_zone:
            self.maze.cell(pos).zone = Zone.END
            if pos != self.maze.end_pos:
                self.maze.cell(pos).forbidden = True

        self.remove_zone_walls(self.maze.start_zone)
        self.insert_wall(self.maze.cell(self.maze.start_pos), DIR.DOWN)
        self.remove_zone_walls(self.maze.end_zone)

        for pos in self.maze.start_path:
            self.maze.cell(pos).forbidden = False

        return True
    
    def make_single_path(self) -> bool:
        self.recursive_backtrack(self.maze.cell(self.maze.start_pos))
        for row in self.maze.maze:
            for cell in row:
                cell._visited.clear()
                cell._paths.clear()
        return True
    
    def make_multiple_paths(self) -> bool:
        self.random_wall_remover()
        return True


    def recursive_backtrack(self, cell: Cell) -> None:
        cell.visited(Algorithm._NONE)
        self.maze.visualize(step=True)
        if cell.zone == Zone.END:
            return
        for neighbor, direction in cell.neighbors(self.maze.maze, all=True):
            if not neighbor.is_visited() and not neighbor.forbidden:
                if self.maze.contest_mode and neighbor.pos == self.maze.contest_end[0]:
                    if direction != self.maze.contest_end[1]:
                        continue
                self.remove_wall(cell, direction)
                self.recursive_backtrack(neighbor)

    def is_pole_empty(self, cell: Cell, direction: Dir) -> bool:
        directions: list[Dir] = [DIR.UP, DIR.RIGHT, DIR.DOWN, DIR.LEFT]
        dir_index: int = directions.index(direction)
        pos_index: int = dir_index
        walls: list[bool] = []
        for _ in range(3):
            cell = cell.neighbor(self.maze.maze, directions[pos_index], all=True)[0]
            pos_index: int = (pos_index + 1) % 4
            walls.append(bool(cell.walls & directions[pos_index].wall))
        return not any(walls)

    def random_wall_remover(self) -> None:
        walls_to_remove: int = self.maze.remove_walls
        while walls_to_remove > 0:
            y: int = random.randint(1, self.maze.height-2)
            x: int = random.randint(1, self.maze.width-2)
            cell: Cell = self.maze.cell((y, x))
            neighbor, direction = cell.neighbor(self.maze.maze, all=True)

            if not cell.zone == Zone.NONE or not neighbor.zone == Zone.NONE:
                continue
            if not cell.walls & direction.wall:
                continue
            if self.is_pole_empty(cell, direction) or self.is_pole_empty(neighbor, direction.opposite):
                continue
            
            self.remove_wall(cell, direction)
            walls_to_remove -= 1
            self.maze.visualize(step=True)

    def remove_zone_walls(self, zone: set) -> None:
        for pos in zone:
            cell: Cell = self.maze.cell(pos)
            for neighbor, direction in cell.neighbors(maze=self.maze.maze, all=True):
                if neighbor.pos in zone:
                    self.remove_wall(cell, direction)

    def remove_wall(self, cell: Cell, direction: Dir) -> None:
        cell.walls &= ~direction.wall
        neighbor: Cell = cell.neighbor(maze=self.maze.maze, direction=direction, all=True)[0]
        neighbor.walls &= ~direction.opposite.wall

    def insert_wall(self, cell: Cell, direction: Dir) -> None:
        cell.walls |= direction.wall
        neighbor: Cell = cell.neighbor(maze=self.maze.maze, direction=direction, all=True)[0]
        neighbor.walls |= direction.opposite.wall