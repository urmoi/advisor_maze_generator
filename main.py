import sys

from maze import Maze
from algorithm import Algorithm
from svg import SVG

# read the arguments from the command line
# main.py
#       -m --mode <mode>
#       -i --id <id>
#       -s --size <size>
#       -r --runs <runs|batchsize>
#       -a --algo <algorithms>
#       -v --verb <verbose>
#       -w --wrem <remove_walls>
#       -c --cont <contest_mode>
#       -g --grap <graphics>
# e.g. python main.py -m sim -s 16 16 -r 10 -a f -v 0 -w 15 -c yes -g yes

def main():

    mode: str = 'test'
    id_hash: str = ''
    size: tuple[int, int] = (-16, -16)
    runs: int = -10
    cutoff: int = 10
    algorithms: list[Algorithm] = [Algorithm.BFS]
    verbose: int = 0
    remove_walls: int = 15
    contest_mode: bool = False
    graphics: bool = True

    flag: str = ''

    for arg in sys.argv:
        if arg in ("-h", "--help"):
            error()

        if arg[0] == '-':
            if arg[1:2] == '-':
                flag = arg[2]
            else:
                flag = arg[1]
            if flag in ('m', 's', 'r', 'a', 'v', 'w', 'c', 'g', 'i'):
                continue
            else:
                error()

        if flag == 'm':
            mode = arg
            if mode in ('sim', 'bat', 'load', 'test'):
                continue
            else:
                error()
        if flag == 'i':
            id_hash = arg
        elif flag == 's':
            try:
                n = int(arg)
                if 8 > size[0] > 128:
                    error()
            except ValueError:
                error()

            if size[0] < 0:
                size = (n, n)
            else:
                size = (size[0], n)
        elif flag == 'r':
            try:
                n = int(arg)
                if n < 0:
                    error()
            except ValueError:
                error()
            
            if runs < 0:
                runs = n
            else:
                cutoff = n
        elif flag == 'a':
            for char in arg:
                if char == 'x':
                    algorithms = [alg for alg in Algorithm if alg != Algorithm._NONE]
                    break
                elif char == 'f':
                    algorithms.append(Algorithm.FloodFill)
                elif char == 'j':
                    algorithms.append(Algorithm.Dijkstra)
                elif char == 'a':
                    algorithms.append(Algorithm.AStar)
                elif char == 'b':
                    algorithms.append(Algorithm.BFS)
                elif char == 'd':
                    algorithms.append(Algorithm.DFS)
                else:
                    error()
        elif flag == 'v':
            try:
                verbose = int(arg)
                if verbose < 0 or verbose > 2:
                    error()
            except ValueError:
                error()
        elif flag == 'w':
            try:
                remove_walls = int(arg)
                if 0 > remove_walls > 50:
                    error()
            except ValueError:
                error()
        elif flag == 'c':
            if arg in ('yes', 'y', 'true', 't'):
                contest_mode = True
            elif arg in ('no', 'n', 'false', 'f'):
                contest_mode = False
            else:
                error()
        elif flag == 'g':
            if arg in ('yes', 'y', 'true', 't'):
                graphics = True
            elif arg in ('no', 'n', 'false', 'f'):
                graphics = False
            else:
                error()

    if size[0] < 0:
        size = (-1*size[0], -1*size[1])
    
    if runs < 0:
        runs = -1*runs

    if mode == 'sim':
        simulate(
            runs=runs,
            cutoff=cutoff,
            size=size,
            remove_walls=remove_walls,
            contest_mode=contest_mode,
            verbose=verbose,
            algorithms=algorithms,
            graphics=graphics
        )
    elif mode == 'bat':
        testbatch(
            batch_size=runs,
            size=size,
            remove_walls=remove_walls,
            contest_mode=contest_mode,
            verbose=verbose,
            algorithms=algorithms,
            graphics=graphics
        )
    elif mode == 'load':
        load(
            id_hash=id_hash,
            algorithms=algorithms,
            graphics=graphics
        )
    else:
        test(
            size=size,
            contest_mode=contest_mode,
            verbose=verbose,
            algorithms=algorithms,
            graphics=graphics
        )


def error():
    print()
    print(f"Usage: python main.py")
    print(f"         -h --help")
    print()
    print(f"         -m --mode  test                     >> default: test")
    print(f"                    sim   (simulation of multiple mazes)")
    print(f"                    bat   (batch of mazes from one maze)")
    print(f"                    load  (load maze from file with id)")
    print(f"         -i --id    #####")
    print(f"         -s --size  8-128 (8-128)            >> default: 16 16")
    print(f"         -r --runs  0-#   (0-# = cutoff)     >> default: 10")
    print(f"         -a --algo  x     (all)              >> default: b (BFS)")
    print(f"                    f     (FloodFill)")
    print(f"                    j     (Dijkstra)")
    print(f"                    a     (AStar)")
    print(f"                    b     (BFS)")
    print(f"                    d     (DFS)")
    print(f"         -v --verb  0     (none)             >> default: 0")
    print(f"                    1     (normal)")
    print(f"                    2     (steps)")
    print(f"         -w --wrem  0-50  (walls to remove)  >> default: 15")
    print(f"         -c --cont  y n                      >> default: n")
    print(f"         -g --grap  y n                      >> default: y")
    print()
    print("Example: python main.py -m sim -s 16 -r 10 5 -a fbd -v 0 -w 15")
    print()

    sys.exit(1)


def test(
    size: tuple[int, int] = (16, 16),
    contest_mode: bool = False,
    verbose: int = 0,
    algorithms: list[Algorithm] = [],
    graphics: bool = True
):

    maze: Maze = Maze(
        size=size,
        verbose=verbose,
        contest_mode=contest_mode
    )
    
    maze.make()

    maze.solve(
        algorithms=algorithms
    )

    maze.visualize(
        paths=True,
        visited=False,
        guide=False
    )
    
    maze.overview()

    maze.save()
    if graphics:
        SVG(maze, filename=f'maze', paths=False, overview=False)
        SVG(maze, filename=f'maze_build', paths=False, overview=False, helpers=True, changes=True)
        SVG(maze, filename=f'maze_solution', paths=True, overview=True)


def simulate(
    runs: int,
    cutoff: int=0,
    size: tuple[int, int]=(16, 16),
    remove_walls: int=15,
    contest_mode: bool=True,
    verbose: int=0,
    algorithms: list[Algorithm]=[],
    graphics: bool=True
):
    import time

    if not cutoff or cutoff > runs:
        cutoff = runs

    mazes: list[tuple[Maze, dict]] = []

    for i in range(runs):
        maze = Maze(
            size=size,
            verbose=verbose,
            remove_walls=remove_walls,
            contest_mode=contest_mode,
        )

        maze.make()

        maze.solve(algorithms=algorithms)

        maze.save()

        mazes.append((maze, maze.analyze(algorithm=algorithms[0])))

    # sort mazes by the algorithm's analysis path length
    mazes.sort(key=lambda m: m[1]['length'])

    print("\033c")
    
    __: str = ""
    __ += f"\n"
    __ += f"> Maze Simulation"
    __ += f" with {algorithms[0].name}"
    __ += f"\n\n"
    __ += f"  maze hash | Length | Turns | Branch\n"
    __ += f"  ----------|--------|-------|-------\n"
    for i, (maze, analysis) in enumerate(mazes):
        __ += f" {maze.hash:>10} |"
        __ += f" {analysis['length']:6} | {analysis['turns']:5} | {analysis['branches']:6}\n"
        if graphics:
            SVG(maze, filename=f'maze', paths=False, overview=False)
            SVG(maze, filename=f'maze_solution', paths=True, overview=True)
            if i+1 == cutoff:
                break
    print(__)


def testbatch(
    batch_size: int = 6,
    size: tuple[int, int] = (16, 16),
    remove_walls: int=15,
    contest_mode: bool = False,
    verbose: int = 0,
    algorithms: list[Algorithm] = [],
    graphics: bool = True
):
    from maker import MakerSteps

    maze: Maze = Maze(
        size=size,
        verbose=verbose,
        remove_walls=remove_walls,
        contest_mode=contest_mode)
    
    maze.make(steps=[
        MakerSteps.ZONES,
        MakerSteps.PATH
    ])
    
    maze.overview()

    maze.save()
    SVG(maze, filename=f'maze', paths=False, overview=False)

    maze_before = maze.copy().maze
    mazes: list[Maze] = []
    
    for i in range(batch_size):
        maze_copy = maze.copy()

        maze_copy.make(steps=[
            MakerSteps.MULTIPLE
        ])

        for y in range(len(maze.maze)):
            for x in range(len(maze.maze[y])):
                maze_copy.maze[y][x].walls = (maze_copy.maze[y][x].walls & 0x0F) | ((maze_before[y][x].walls & 0x0F) << 4)
        maze_before = maze_copy.copy().maze

        maze_copy.solve(algorithms=algorithms)

        mazes.append(maze_copy)

    for i, maze_ in enumerate(mazes):
        maze_.overview()

        maze_.save(filename=f'maze_{i+1:02d}')
        if graphics:
            SVG(maze_, filename=f'maze_{i+1:02d}', paths=False, overview=False)
            SVG(maze_, filename=f'maze_{i+1:02d}_build', paths=False, overview=False, helpers=True, changes=True)
            SVG(maze_, filename=f'maze_{i+1:02d}_solution', paths=True, overview=True)

def load(
    id_hash: str = '',
    algorithms: list[Algorithm] = [],
    graphics: bool = True
):
    if not id_hash:
        error()
    
    maze: Maze = Maze(size=(0, 0))
    maze.load(id_hash=id_hash)

    maze.solve(algorithms=algorithms)

    maze.visualize(paths=True, visited=False, guide=False)

    maze.overview()

    if graphics:
        SVG(maze, filename=f'__maze', paths=False, overview=False)
        SVG(maze, filename=f'__maze_build', paths=False, overview=False, helpers=True, changes=True)
        SVG(maze, filename=f'__maze_solution', paths=True, overview=True)

    
        

if __name__ == '__main__':
    main()


