import sys

from maze import Maze
from algorithm import Algorithm
from svg import SVG

# read the arguments from the command line
# main.py
#       -m --mode <mode>
#       -i --id <id>
#       -u --upwa <updatewalls>
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
    algorithms: list[Algorithm] = []
    verbose: int = 0
    remove_walls: int = 15
    contest_mode: bool = False
    graphics: bool = True
    modifications: list[str] = []

    flag: str = ''

    for arg in sys.argv:
        if arg in ("-h", "--help"):
            error()

        if arg[0] == '-':
            if arg[1:2] == '-':
                flag = arg[2]
            else:
                flag = arg[1]
            if flag in ('m', 'u', 's', 'r', 'a', 'v', 'w', 'c', 'g', 'i'):
                continue
            else:
                error()

        if flag == 'm':
            mode = arg
            if mode in ('sim', 'bat', 'load', 'test'):
                continue
            else:
                error()
        elif flag == 'i':
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
        elif flag == 'u':
            modifications.append(arg)
            

    if size[0] < 0:
        size = (-1*size[0], -1*size[1])
    
    if runs < 0:
        runs = -1*runs

    if algorithms == []:
        algorithms = [Algorithm.BFS]

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
            modifications=modifications,
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
    print(f"         -i --id    ####  (when loading or modifying a maze)")
    print(f"         -u --upwa  y.x.[u(p)|r(ight)|d(own)|l(eft)].[r(emove)|i(nsert)]")
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
    size: tuple[int, int],
    contest_mode: bool,
    verbose: int,
    algorithms: list[Algorithm],
    graphics: bool
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
        SVG(maze, foldername=f'graphics', filename=f'maze', paths=False, overview=False)
        SVG(maze, foldername=f'graphics', filename=f'maze_build', paths=False, overview=False, helpers=True, changes=True)
        SVG(maze, foldername=f'graphics', filename=f'maze_solution', paths=True, overview=True)


def simulate(
    runs: int,
    cutoff: int,
    size: tuple[int, int],
    remove_walls: int,
    contest_mode: bool,
    verbose: int,
    algorithms: list[Algorithm],
    graphics: bool
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

        mazes.append((maze, maze.analyze(algorithm=algorithms[0])))

    # sort mazes by the algorithm's analysis path length
    mazes.sort(key=lambda m: m[1]['length'])

    foldername: str = f'simulation_{time.strftime("%Y%m%d-%H%M%S")}'
    
    __: str = ""
    __ += f"\n"
    __ += f"> Maze Simulation with {algorithms[0].name}\n"
    __ += f"            [{remove_walls} random walls removed]"
    __ += f"\n\n"
    __ += f"  maze hash | Length | Turns | Branch\n"
    __ += f"  ----------|--------|-------|-------\n"
    for i, (maze, analysis) in enumerate(mazes):
        __ += f" {maze.hash:>10} |"
        __ += f" {analysis['length']:6} | {analysis['turns']:5} | {analysis['branches']:6}\n"
        maze.save(foldername=foldername+'/mazes')
        if graphics:
            SVG(maze, foldername=foldername+'/mazes', filename=f'maze', paths=False, overview=False)
            SVG(maze, foldername=foldername+'/solutions', filename=f'maze', paths=True, overview=True)
        if i+1 == cutoff:
            break
    print(__)

    with open(f'{foldername}/simulation_summary.txt', 'w') as file:
        file.write(__)


def testbatch(
    batch_size: int,
    size: tuple[int, int],
    remove_walls: int,
    contest_mode: bool,
    verbose: int,
    algorithms: list[Algorithm],
    graphics: bool
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

    foldername: str = f'batch_{maze.hash}'
    maze.save(foldername=foldername)
    SVG(maze, foldername=foldername, filename=f'maze', paths=False, overview=False)

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
            SVG(maze_, foldername=foldername, filename=f'maze_{i+1:02d}', paths=False, overview=False)
            SVG(maze_, foldername=foldername, filename=f'maze_{i+1:02d}_build', paths=False, overview=False, helpers=True, changes=True)
            SVG(maze_, foldername=foldername, filename=f'maze_{i+1:02d}_solution', paths=True, overview=True)

def load(
    id_hash: str,
    algorithms: list[Algorithm],
    modifications: list[str],
    graphics: bool
):
    if not id_hash:
        error()
    
    maze: Maze = Maze(size=(0, 0))

    if not maze.load(id_hash=id_hash):
        sys.exit(1)
    
    if modifications:
        from direction import DIR, Dir

        for modification in modifications:
            y_, x_, d_, c = modification.split('.')
            try:
                y = int(y_)
                x = int(x_)
            except ValueError:
                error()
            if y < 0 or y >= maze.height or x < 0 or x >= maze.width:
                error()
            d: Dir = DIR._EMPTY
            if d_ == 'u':
                d = DIR.UP
            elif d_ == 'r':
                d = DIR.RIGHT
            elif d_ == 'd':
                d = DIR.DOWN
            elif d_ == 'l':
                d = DIR.LEFT
            else:
                error()
            if c == 'i':
                maze.make.insert_wall(maze.cell((y, x)), d)
            elif c == 'r':
                maze.make.remove_wall(maze.cell((y, x)), d)
            else:
                error()

        maze.hash = maze.__hash__()
        maze.save(foldername=f'mazes_{maze.hash}')

    maze.solve(algorithms=algorithms)

    maze.visualize(paths=True, visited=False, guide=False)

    maze.overview()

    if graphics:
        foldername: str = f'graphics_{maze.hash}'
        SVG(maze, foldername=foldername, filename=f'__maze', paths=False, overview=False)
        SVG(maze, foldername=foldername, filename=f'__maze_build', paths=False, overview=False, helpers=True, changes=True)
        SVG(maze, foldername=foldername, filename=f'__maze_solution', paths=True, overview=True)

if __name__ == '__main__':
    main()


