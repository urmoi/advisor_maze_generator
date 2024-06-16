from algorithm import Algorithm
from cell import Cell
from direction import DIR, Dir
from maze import Maze


def FloodFill(maze: Maze, cell: Cell) -> list[Cell]:
    resistance: list[list[int]] = [[-1 for _ in range(maze.width)] for _ in range(maze.height)]
    turns: list[list[int]] = [[-1 for _ in range(maze.width)] for _ in range(maze.height)]
    resistance[cell.y][cell.x] = 0
    turns[cell.y][cell.x] = 0
    queue: list[tuple[Cell, Dir]] = [(cell, DIR._EMPTY)]
    path: list[Cell] = []

    while queue:
        current, move_dir = queue.pop(0)
        current.visited(Algorithm.FloodFill)

        maze.visualize(step=True, algorithm=Algorithm.FloodFill)

        for neighbor, direction in current.neighbors(maze.maze):
            if resistance[neighbor.y][neighbor.x] == -1 and not neighbor.forbidden:
                resistance[neighbor.y][neighbor.x] = resistance[current.y][current.x] + 1
                if move_dir is DIR._EMPTY:
                    move_dir = direction
                turns[neighbor.y][neighbor.x] = turns[current.y][current.x] + (1 if direction != move_dir else 0)
                queue.append((neighbor, direction))

    current: Cell = maze.cell(maze.end_pos)
    while current.pos != maze.start_pos:
        path.append(current)
        current.path(Algorithm.FloodFill)

        neighbors: list[Cell] = [n for n, d in current.neighbors(maze.maze)]
        current = min(neighbors, key=lambda n: (turns[n.y][n.x], resistance[n.y][n.x]))
    path.append(current)
    current.path(Algorithm.FloodFill)

    path.reverse()
    return path