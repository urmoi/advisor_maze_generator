from algorithm import Algorithm
from cell import Cell
from maze import Maze

def Djikstra(maze: Maze, cell: Cell) -> list[Cell]:
    distances: list[list[int]] = [[-1 for _ in range(maze.width)] for _ in range(maze.height)]
    distances[cell.y][cell.x] = 0
    parents: dict[Cell, Cell|None] = {cell: None}
    queue: list[Cell] = [cell]

    def recursive_djikstra() -> list[Cell]:        
        current = queue.pop(0)
        current.visited(Algorithm.Dijkstra)

        maze.visualize(step=True, algorithm=Algorithm.Dijkstra)

        if current.pos == maze.end_pos:
            return [current]

        for neighbor, direction in current.neighbors(maze.maze):
            if neighbor.is_visited(Algorithm.Dijkstra) or neighbor.forbidden:
                continue
            tentative_distance: int = distances[current.y][current.x] + 1
            if distances[neighbor.y][neighbor.x] == -1 or tentative_distance < distances[neighbor.y][neighbor.x]:
                distances[neighbor.y][neighbor.x] = tentative_distance
                parents[neighbor] = current
                queue.append(neighbor)

        if not queue:
            return []
        return recursive_djikstra()
    
    def reconstruct_path(current) -> list[Cell]:
        if current is None:
            return []
        current.path(Algorithm.Dijkstra)
        return reconstruct_path(parents.get(current)) + [current]
    
    current = recursive_djikstra()[0]

    return reconstruct_path(current)