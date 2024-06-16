import random
import time

from algorithm import Algorithm
from analyzer import Analyzer
from ascii import ASCII
from cell import Cell
from direction import DIR, Dir
from files import Loader, Saver
from maker import Maker, MakerSteps
from solver import Solver
from visualizer import Visualizer


class Maze:
    def __init__(self, size: tuple[int, int], verbose: int=0, contest_mode:bool=False, remove_walls: int=15):
        self.height: int = size[0]
        self.width: int = size[1]

        self.hash: str = "########"

        self.remove_walls: int = remove_walls

        self.maze: list[list[Cell]] = [[Cell((y, x)) for x in range(self.width)] for y in range(self.height)]

        self.verbose: int = verbose

        self.make: Maker = Maker(maze=self)

        self.visualize: Visualizer = Visualizer(maze=self)

        self.solve: Solver = Solver(maze=self)

        self.analyze: Analyzer = Analyzer(maze=self)

        self.contest_mode: bool = contest_mode
        self.contest_end: tuple[tuple[int, int], Dir] = (
            (self.height//2, self.width//2),
            DIR.LEFT
        )

    # the start and end are defined
    # - start: zone top left 3x3 cells
        self.start_zone: set[tuple] = {
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2)}
        self.start_path: set[tuple] = {(0, 0), (0, 1), (0, 2)}
        self.start_pos: tuple = (0, 0)

    # - end: zone in the middle 2x2 cells
        self.end_zone: set = {
            (self.height//2-1, self.width//2-1), (self.height//2-1, self.width//2),
            (self.height//2, self.width//2-1), (self.height//2, self.width//2)
        }
        self.end_pos: tuple = random.choice(list(self.end_zone)) if not self.contest_mode else self.contest_end[0]
    # - markers for ascii
        self.ziel_marker: tuple = (self.height//2, self.width//2)
        self.ball_marker: tuple = (2, 2)

        self.paths: dict[Algorithm, list[Cell]] = {}
        self.visited: dict[Algorithm, list[Cell]] = {}

        self.solved: set[Algorithm] = set()

    def cell(self, pos: tuple) -> Cell:
        return self.maze[pos[0]][pos[1]]
    
    def save(self, foldername: str='mazes', filename: str='maze', fileext: str='') -> bool:
        filename = f'{filename}_{self.hash}'
        return Saver(maze=self, foldername=foldername, filename=filename, fileext=fileext)
    
    def load(self, foldername: str='mazes', filename: str='maze', fileext: str='', id_hash: str='') -> bool:
        return Loader(maze=self, foldername=foldername, filename=filename, fileext=fileext, id_hash=id_hash)

    def overview(self) -> None:
        print(self.visualize.analysis_board())

    def copy(self) -> 'Maze':
        from copy import deepcopy
        return deepcopy(self)
    
    def __hash__(self) -> str:
        import hashlib
        maze: str = self.__str__(algorithm=Algorithm._NONE, paths=False, visited=False, guide=False)
        hash_code: str = hashlib.sha1(maze.encode()).hexdigest()[:len(self.hash)]
        return hash_code
    
    def __str__(self, algorithm: Algorithm=Algorithm._NONE, paths: bool=False, visited: bool=False, guide: bool=False) -> str:
        
        elem: list = []
        if guide:
            elem.append(4*" ")
            for ex in range(self.width):
                    elem.append(f"{ex:2}")
                    if ex == self.width//2-1:
                        elem.append(" |")
                    else:
                        elem.append("  ")
            elem.append("\n")

        for ey in range(2*self.height+1):

            if guide:
                if ey % 2 != 0:
                    elem.append(f"{ey//2:2} ")
                elif ey == 2*self.height//2:
                    elem.append(3*"-")
                else:
                    elem.append(3*" ")
            
            for ex in range(2*self.width+1):

            # cell and pole positions
                cy, cx = (ey-1)//2, (ex-1)//2
                py, px = ey//2, ex//2

                cell = self.maze[cy][cx]
            # poles
                if ey % 2 == 0 and ex % 2 == 0:
                    if self.make.steps[MakerSteps.ZONES] and (py,px) == self.ball_marker:
                        elem.append(ASCII.ball)
                    elif self.make.steps[MakerSteps.ZONES] and py > 0 and px > 0 and (py,px) in self.start_zone-{(1,1)}:
                        elem.append(ASCII.pole_empty)
                    elif self.make.steps[MakerSteps.ZONES] and (py,px) == self.ziel_marker:
                        elem .append(ASCII.end)
                    else:
                        elem.append(ASCII.pole)
            # horizontal walls
                elif ey % 2 == 0:
                    if cell.walls & DIR.DOWN.wall:
                        elem.append(ASCII.wall_h)  
                    else:
                        elem.append(ASCII.wall_h_empty)
            # vertical walls
                elif ex % 2 == 0:
                    if cell.walls & DIR.RIGHT.wall:
                        elem.append(ASCII.wall_v)
                    else:
                        elem.append(ASCII.wall_v_empty)
            # cells
                else:
                    if self.make.steps[MakerSteps.ZONES] and cell.pos == self.start_pos:
                        elem.append(ASCII.start)
                    elif paths and (cell.is_path() and algorithm is Algorithm._NONE or cell.is_path(algorithm)):
                        if algorithm is Algorithm._NONE:
                            if len(cell._paths) > 1:
                                elem.append(ASCII.cell_path_general)
                            elif cell.is_path(Algorithm.FloodFill):
                                elem.append(ASCII.cell_path_floodfill)
                            elif cell.is_path(Algorithm.Dijkstra):
                                elem.append(ASCII.cell_path_dijkstra)
                            elif cell.is_path(Algorithm.AStar):
                                elem.append(ASCII.cell_path_astar)
                            elif cell.is_path(Algorithm.BFS):
                                elem.append(ASCII.cell_path_bfs)
                            elif cell.is_path(Algorithm.DFS):
                                elem.append(ASCII.cell_path_dfs)
                            else:
                                elem.append(ASCII.cell)
                        elif algorithm is Algorithm.FloodFill and cell.is_path(Algorithm.FloodFill):
                            elem.append(ASCII.cell_path_floodfill)
                        elif algorithm is Algorithm.Dijkstra and cell.is_path(Algorithm.Dijkstra):
                            elem.append(ASCII.cell_path_dijkstra)
                        elif algorithm is Algorithm.AStar and cell.is_path(Algorithm.AStar):
                            elem.append(ASCII.cell_path_astar)
                        elif algorithm is Algorithm.BFS and cell.is_path(Algorithm.BFS):
                            elem.append(ASCII.cell_path_bfs)
                        elif algorithm is Algorithm.DFS and cell.is_path(Algorithm.DFS):
                            elem.append(ASCII.cell_path_dfs)
                        else:
                            elem.append(ASCII.cell)
                    elif visited and self.make.steps[MakerSteps.FINAL] and (cell.is_visited() and algorithm is Algorithm._NONE or cell.is_visited(algorithm)):
                        if algorithm is Algorithm._NONE:
                            elem.append(ASCII.cell_visited)
                        elif algorithm is Algorithm.FloodFill and cell.is_visited(Algorithm.FloodFill):
                            elem.append(ASCII.cell_visited)
                        elif algorithm is Algorithm.Dijkstra and cell.is_visited(Algorithm.Dijkstra):
                            elem.append(ASCII.cell_visited)
                        elif algorithm is Algorithm.AStar and cell.is_visited(Algorithm.AStar):
                            elem.append(ASCII.cell_visited)
                        elif algorithm is Algorithm.BFS and cell.is_visited(Algorithm.BFS):
                            elem.append(ASCII.cell_visited)
                        elif algorithm is Algorithm.DFS and cell.is_visited(Algorithm.DFS):
                            elem.append(ASCII.cell_visited)
                        else:
                            elem.append(ASCII.cell)
                    else:
                        elem.append(ASCII.cell)

            elem.append("\n")
        __: str = "".join(elem)
        return __
    
    def __format__(self, format_spec: str='ascii') -> str:
        if format_spec == 'ascii':
            return self.__str__()
        elif format_spec == 'hex':
            __: str = ""
            for row in self.maze:
                for cell in row:
                    __ += f"{cell.walls:02X} "
                __ += "\n"
            return __
        elif format_spec == 'bin' or format_spec == 'bin8':
            __: str = ""
            for row in self.maze:
                for cell in row:
                    __ += f"{cell.walls:08b} "
                __ += "\n"
            return __
        elif format_spec == 'bin4':
            __: str = ""
            for row in self.maze:
                for cell in row:
                    __ += f"{cell.walls:08b} "[4:]
                __ += "\n"
            return __
        else:
            return ""