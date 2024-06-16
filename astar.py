from maze import Maze
from cell import Cell
from algorithm import Algorithm

def AStar(maze: Maze, cell: Cell) -> list[Cell]:
    open_set: set = set([cell])
    closed_set: set = set()
    g_costs: dict = {cell: 0}
    parents: dict[Cell, Cell|None] = {cell: None}

    def heuristic(a: tuple, b: tuple) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def recursive_a_star(current: Cell) -> list[Cell]:
        current.visited(Algorithm.AStar)
        open_set.remove(current)
        closed_set.add(current)

        maze.visualize(step=True, algorithm=Algorithm.AStar)

        if current.pos == maze.end_pos:
            return reconstruct_path(current)

        for neighbor, direction in current.neighbors(maze.maze):
            if neighbor in closed_set or neighbor.forbidden:
                continue

            tentative_g_cost: int = g_costs[current] + 1

            if neighbor.pos not in g_costs or tentative_g_cost < g_costs[neighbor.pos]:
                g_costs[neighbor] = tentative_g_cost
                parents[neighbor] = current

                if not any(node.pos == neighbor.pos for node in open_set):
                    open_set.add(neighbor)

        if not open_set:
            return []

        open_list: list[Cell] = list(open_set)
        open_list.sort(key=lambda n: g_costs[n] + heuristic(n.pos, maze.end_pos))
        return recursive_a_star(open_list[0])
        
    
    def reconstruct_path(current: Cell|None) -> list[Cell]:
        if current is None:
            return []
        current.path(Algorithm.AStar)
        return reconstruct_path(parents.get(current)) + [current]

    return recursive_a_star(cell)