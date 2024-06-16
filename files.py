import os
import pickle

from maker import Maker
from visualizer import Visualizer
from solver import Solver
from analyzer import Analyzer

from direction import DIR
from ascii import ASCII


def Saver(maze, foldername: str, filename: str, fileext: str="") -> bool:
    def _save_txt() -> bool:
        if not os.path.exists(foldername+'/txt/'):
            os.makedirs(foldername+'/txt/')
        try:
            with open(foldername+'/txt/'+filename+'.txt', "w") as file:
                file.write(maze.__format__('ascii'))
            return True
        except FileNotFoundError:
            print(f"File {filename}.txt can't be saved to {foldername}/txt/.")
            return False

    def _save_pickle() -> bool:
        if not os.path.exists(foldername+'/pkl/'):
            os.makedirs(foldername+'/pkl/')
        try:
            with open(foldername+'/pkl/'+filename+'.pkl', "wb") as file:
                pickle.dump(maze, file)
            return True
        except FileNotFoundError:
            print(f"File {filename}.pkl can't be saved to {foldername}/pkl/.")
            return False
    
    if fileext == 'txt':
        return _save_txt()
    elif fileext == 'pkl':
        return _save_pickle()
    else:
        return _save_txt() and _save_pickle()

def Loader(maze, foldername: str, filename: str, fileext: str="", id_hash: str="") -> bool:
    def _load_from_hash() -> bool:
        import os
        try:
            files = os.listdir(foldername+'/pkl/')
            for file in files:
                if id_hash in file:
                    nonlocal filename
                    filename = file.split('.')[0]
                    return _load_pickle()
            raise FileNotFoundError
        except FileNotFoundError:
            print(f"File with id {id_hash} not found in {foldername}/pkl/.")
            return False
                

    def _load_txt() -> bool:
        try:
            with open(foldername+'/txt/'+filename+'.txt', "r") as file:
                read: list = file.readlines()
                maze.height = len(read) // 2
                maze.width = len(read[0]) // 4
                maze.maze = [[maze.cell((y, x)) for x in range(maze.width)] for y in range(maze.height)]
                for y in range(1, len(read), 2):
                    for x in range(2, len(read[y]), 4):
                        y_pos: int = y//2
                        x_pos: int = x//4
                        cell = maze.cell((y_pos, x_pos))

                        if read[y-1][x-1:x+2] != ASCII.wall_h:
                            cell.walls &= ~DIR.UP.wall
                        if read[y][x+2] != ASCII.wall_v:
                            cell.walls &= ~DIR.RIGHT.wall
                        if read[y+1][x-1:x+2] != ASCII.wall_h:
                            cell.walls &= ~DIR.DOWN.wall
                        if read[y][x-2] != ASCII.wall_v:
                            cell.walls &= ~DIR.LEFT.wall
                        
                        maze.maze[y_pos][x_pos] = cell
                
                maze.hash = maze.__hash__()
                maze.make = Maker(maze=maze)
                maze.visualize = Visualizer(maze=maze)
                maze.solve = Solver(maze=maze)
                maze.analyze = Analyzer(maze=maze)
            return True
        except FileNotFoundError:
            print(f"File {filename}.txt not found in {foldername}/pkl/.")
            return False

    def _load_pickle() -> bool:
        try:
            with open(foldername+'/pkl/'+filename+'.pkl', "rb") as file:
                loaded_maze = pickle.load(file)

                maze.height = loaded_maze.height
                maze.width = loaded_maze.width
                maze.hash = loaded_maze.hash
                maze.maze = loaded_maze.maze
                maze.verbose = loaded_maze.verbose
                maze.remove_walls = loaded_maze.remove_walls
                maze.make = Maker(maze=maze)
                maze.make.steps = loaded_maze.make.steps
                maze.visualize = Visualizer(maze=maze)
                maze.solve = Solver(maze=maze)
                maze.analyze = Analyzer(maze=maze)
                maze.contest_mode = loaded_maze.contest_mode
                maze.contest_end = loaded_maze.contest_end
                maze.start_zone = loaded_maze.start_zone
                maze.start_path = loaded_maze.start_path
                maze.start_pos = loaded_maze.start_pos
                maze.end_zone = loaded_maze.end_zone
                maze.end_pos = loaded_maze.end_pos
                maze.ziel_marker = loaded_maze.ziel_marker
                maze.ball_marker = loaded_maze.ball_marker
                maze.paths = loaded_maze.paths
                maze.visited = loaded_maze.visited
                maze.solved = loaded_maze.solved
            return True
        except FileNotFoundError:
            print(f"File {filename}.pkl not found in {foldername}/pkl/.")
            return False
    
    if id_hash:
        return _load_from_hash()

    if fileext == 'txt':
        return _load_txt()
    elif fileext == 'pkl':
        return _load_pickle()
    else:
        return _load_txt() or _load_pickle()