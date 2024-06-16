from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from maze import Maze

from algorithm import Algorithm
from cell import Cell


class Solver:
    def __init__(self, maze: 'Maze'):
        self.maze: Maze = maze

    def __call__(self, algorithms: list[Algorithm]=[]) -> bool:
        if not algorithms:
            for algorithm in Algorithm:
                if algorithm == Algorithm._NONE:
                    continue
                algorithms.append(algorithm)
        
        start_cell: Cell = self.maze.cell(self.maze.start_pos)
        solutions = set()
        for algorithm in algorithms:
            path: list[Cell] = []
            if algorithm == Algorithm.FloodFill:
                from floodfill import FloodFill
                path = FloodFill(self.maze, start_cell)
            elif algorithm == Algorithm.Dijkstra:
                from dijkstra import Djikstra
                path = Djikstra(self.maze, start_cell)
            elif algorithm == Algorithm.AStar:
                from astar import AStar
                path = AStar(self.maze, start_cell)
            elif algorithm == Algorithm.BFS:
                from bfs import BFS
                path = BFS(self.maze, start_cell)
            elif algorithm == Algorithm.DFS:
                from dfs import DFS
                path = DFS(self.maze, start_cell)

            if path:
                solutions.add(algorithm)
                self.maze.paths[algorithm] = path
                self.maze.solved.add(algorithm)
                self.maze.visualize(step=True, algorithm=algorithm)

        return bool(solutions)