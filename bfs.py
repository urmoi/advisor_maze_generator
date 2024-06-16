from maze import Maze
from cell import Cell
from algorithm import Algorithm

def BFS(maze: Maze, cell: Cell) -> list[Cell]:
    queue: list[Cell] = [cell]
    parents: dict[Cell, Cell|None] = {cell: None}
    
    while queue:
        current: Cell|None = queue.pop(0)
        current.visited(Algorithm.BFS)
        
        maze.visualize(step=True, algorithm=Algorithm.BFS)
        
        if current.pos == maze.end_pos:
            path: list[Cell] = []
            while current is not None:
                path.append(current)
                current.path(Algorithm.BFS)
                current = parents.get(current)
            path.reverse()
            return path

        for neighbor, direction in current.neighbors(maze.maze):
            if neighbor.is_visited(Algorithm.BFS) or neighbor.forbidden:
                continue
            if neighbor not in parents:
                parents[neighbor] = current
                queue.append(neighbor)
    return []