from maze import Maze
from cell import Cell
from algorithm import Algorithm

def DFS(maze: Maze, cell: Cell) -> list[Cell]:
    path: list[Cell] = []

    def recursive_DFS(cell: Cell) -> list[Cell]:
        cell.visited(Algorithm.DFS)
        
        maze.visualize(step=True, algorithm=Algorithm.DFS)

        if cell.pos == maze.end_pos:
            cell.path(Algorithm.DFS)
            return [cell]
        for neighbor, direction in cell.neighbors(maze.maze):
            if neighbor.is_visited(Algorithm.DFS) or neighbor.forbidden:
                continue
            path = recursive_DFS(neighbor)
            if path:
                path.append(cell)
                cell.path(Algorithm.DFS)
                return path
        return []
    
    path = recursive_DFS(cell)
    path.reverse()
    return path