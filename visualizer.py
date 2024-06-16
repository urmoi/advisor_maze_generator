import time

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from maze import Maze

from algorithm import Algorithm
from maker import MakerSteps


class Visualizer:
    def __init__(self, maze: 'Maze'):
        self.maze: Maze = maze

    def __call__(self, paths: bool=True, visited: bool=False, guide: bool=False, step: bool=False, algorithm: Algorithm=Algorithm._NONE) -> None:
        if not self.maze: return

        if step:
            if self.maze.verbose == 2:
                print("\033c")
                if not self.maze.make.steps[MakerSteps.FINAL]:
                    print(self.maze.__str__(paths=False, visited=False, guide=guide))
                    print(self.maze_info(algorithm))
                elif algorithm is not Algorithm._NONE:
                    print(self.maze.__str__(algorithm=algorithm, paths=True, visited=True, guide=guide))
                    print(self.maze_info(algorithm))
                if algorithm in self.maze.solved:
                    time.sleep(1)
                else:
                    time.sleep(0.01)
                print("\033c")
            elif self.maze.verbose == 1:
                print("\033c")
                if self.maze.make.steps[MakerSteps.FINAL] and algorithm is Algorithm._NONE and not self.maze.solved:
                    print(self.maze.__str__(paths=False, visited=True, guide=guide))
                    print(self.maze_info(algorithm))
                    time.sleep(1)
                elif algorithm in self.maze.solved:
                    print(self.maze.__str__(algorithm=algorithm, paths=True, visited=True, guide=guide))
                    print(self.maze_info(algorithm))
                    time.sleep(1)
                print("\033c")

        else:
            print(self.maze.__str__(paths=paths, visited=visited, guide=guide))

    
    def maze_info(self, algorithm: Algorithm) -> str:
        if not self.maze: return ""
        
        ticks: int = 3
        tick: int = int(time.time()*2) % (ticks+1)

        visited: int = 0
        valid: int = 0

        for row in self.maze.maze:
            for cell in row:
                if cell.is_visited(algorithm):
                    visited += 1
                if not cell.forbidden:
                    valid += 1

        __: str = f"> "
        if not self.maze.make.steps[MakerSteps.FINAL]:
            __ += f"Making "
        elif self.maze.make.steps[MakerSteps.FINAL] and not self.maze.solved and algorithm == Algorithm._NONE:
            __ += f"Made   "
        elif algorithm not in self.maze.solved and algorithm != Algorithm._NONE:
            __ += f"Solving"
        elif algorithm in self.maze.solved and algorithm != Algorithm._NONE:
            __ += f"Solved!"
            tick = 3
        else:
            return ""
        __ += f" Maze{tick*'.'}{(ticks-tick)*' '}{visited:{ticks}} [{(visited/valid)*100:05.2f}%]"
        if self.maze.make.steps[MakerSteps.FINAL] and algorithm != Algorithm._NONE:
            __ += f" with {algorithm.name}"
        return __
        

    def analysis_board(self) -> str:
        if not self.maze: return ""
        
        analysis_maze: dict[str, int] = self.maze.analyze()

        __: str = f"> Maze Analysis"
        __ += f"{(44-len(self.maze.hash))*' '} hash {self.maze.hash}"
        __ += f"\n\n"
        __ += f"  > Maze Generator:  {self.maze.height}x{self.maze.width} || {self.maze.height*self.maze.width} [={analysis_maze['valid']:3}] cells | {self.maze.remove_walls:2} walls removed\n"
        __ += f"                     count || walls {analysis_maze['walls']:3} | poles {analysis_maze['poles']:3} | branches {analysis_maze['branches']:2}\n"
        __ += f"\n"

        __ += f"  > Path  Analysis:"
        if not self.maze.solved:
            __ += f"    not solved\n"
            return __
        algorithms = [algorithm for algorithm in Algorithm if algorithm in self.maze.solved]
        __ += f"\n\n"
        __ += f"  Algorithm | Length | Turns | Branch || Explored | Path% | Maze%\n"
        __ += f"  ----------|--------|-------|--------||----------|-------|------\n"
        for algorithm in algorithms:
            analysis = self.maze.analyze(algorithm)
            __ += f" {algorithm.name:>10} |"
            if analysis['length'] == 0:
                __ += f"     path not found      ||"
            else:
                __ += f" {analysis['length']:6} | {analysis['turns']:5} | {analysis['branches']:6} ||"
            __ += f" {analysis['visited']:8} | {analysis['length']/analysis['visited']*100:5.1f} | {analysis['visited']/analysis_maze['valid']*100:5.1f}\n"
        return __


    def path_cells(self, algorithms: list[Algorithm]=[], short: bool=False) -> None:
        if not self.maze: return
        
        if not algorithms:
            for algorithm in Algorithm:
                if algorithm == Algorithm._NONE:
                    continue
                algorithms.append(algorithm)
        
        __: str = f"> Path Cells\n\n"
                
        longest_path: int = max([len(path) for algorithm, path in self.maze.paths.items() if algorithm in algorithms])

        for algorithm in self.maze.paths:
            __ += f'  {algorithm.name:10}'
        __ += "\n"

        if short:
            for algorithm, path in self.maze.paths.items():
                __ += f'  {path[0].__str__():8}  '
            __ += "\n"
            for algorithm, path in self.maze.paths.items():
                __ += f'     |      '
            __ += "\n"
            for algorithm, path in self.maze.paths.items():
                __ += f'  {path[-1].__str__():8}  '
        else:
            for i in range(longest_path):
                for algorithm, path in self.maze.paths.items():
                    if i < len(path):
                        __ += f'  {path[i].__str__():8}  '
                    else:
                        __ += f'  {"":8}  '
                __ += "\n"
            __ += "\n"
        print(__)