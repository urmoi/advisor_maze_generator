import os

from algorithm import Algorithm
from ascii import ASCII
from direction import DIR


class SVG:
    def __init__(self, maze, foldername: str, filename: str, to_pdf: bool=True, paths: bool=True, zones: bool=True, markers: bool=True, helpers: bool=False, changes: bool=False, overview: bool=True) -> None:
        self.paths: bool = paths
        self.zones: bool = zones
        self.markers: bool = markers
        self.helpers: bool = helpers
        self.changes: bool = changes
        self.overview: bool = overview

        file_name: str = f'{filename}_{maze.hash}'
        svg_name: str = f'{file_name}.svg'
        pdf_name: str = f'{file_name}.pdf'

        if not os.path.exists(foldername+'/svg/'):
            os.makedirs(foldername+'/svg/')

        try:
            with open(foldername+'/svg/'+svg_name, 'w') as f:
                f.write(self.svg(maze))
        except FileNotFoundError:
            return print(f"File {svg_name} can't be saved {foldername}/svg/.")
        
        if to_pdf:
            if not os.path.exists(foldername+'/pdf/'):
                os.makedirs(foldername+'/pdf/')
            try:
                from cairosvg import svg2pdf
                svg2pdf(url=foldername+'/svg/'+svg_name, write_to=foldername+'/pdf/'+pdf_name)
            except ImportError:
                return print("cairosvg is not installed. Please run 'pip install cairosvg' to install it.")
            except FileNotFoundError:
                return print(f"File {pdf_name} can't be saved to {foldername}/pdf/.")
    

    def svg(self, maze) -> str:
        factor: int = 2

        cell_size: int = 180
        frame_size: int = 100
        pole_size: int = 12*factor
        ball_radius: int = 40
        hole_radius: int = 3*factor
        border_size: int = 50
        line_width: int = 3
        zone_opacity: float = 0.25
        path_line_width: int = 20

        bg_color: str = "#FFFFFF"
        wall_color: str = "#000000"
        wall_out_color: str = "#CDCDCD"
        wall_in_color: str = "#FF0000"
        pole_color: str = "#000000"
        hole_color: str = pole_color
        start_color: str = "#0000FF"
        end_color: str = "#FF0000"
        helper_line_color: str = "#000000"
        helper_bg_color: str = "transparent"

        path_opacity: float = 0.75

        floodfill_color: str = "#FF0000"
        djikstra_color: str = "#00FF00"
        astar_color: str = "#0000FF"
        bfs_color: str = "#FF00FF"
        dfs_color: str = "#00FFFF"

        fonz_size: int = cell_size//3
        spacer_height: int = fonz_size if self.overview else 0
        text_height: int = fonz_size*15 if self.overview else 0

        def frame() -> str:
            return f'<rect x="0" y="0" width="{maze.width*cell_size+frame_size*2}" height="{maze.height*cell_size+frame_size*2}" fill="{bg_color}" />\n'

        def helpers() -> str:
            __: str = ""
            for iy in range(3):
                for ix in range(3):
                    y, x = frame_size-border_size+(iy*(4+2)*cell_size), frame_size-border_size+(ix*(4+2)*cell_size)
                    __ += f'<rect x="{x}" y="{y}" width="{4*cell_size+2*border_size}" height="{4*cell_size+2*border_size}" fill="none" stroke="{helper_line_color}" stroke-width="{line_width}" />\n'

            for i in range(4):
                counter_clockwize: bool = False
                translate: int = int(counter_clockwize)*(4+2)*cell_size
                __ += f'<rect transform="rotate({i*90}, {(maze.width*cell_size+frame_size*2)/2}, {(maze.height*cell_size+frame_size*2)/2})" x="{frame_size-border_size+translate}" y="{frame_size+border_size+(4*cell_size)}" width="{10*cell_size+2*border_size}" height="{2*cell_size-2*border_size}" fill="{helper_bg_color}" stroke="{helper_line_color}" stroke-width="{line_width}" />\n'
                __ += f'<rect transform="rotate({i*90}, {(maze.width*cell_size+frame_size*2)/2}, {(maze.height*cell_size+frame_size*2)/2})" x="{frame_size+border_size+(4*cell_size)+translate}" y="{frame_size-border_size}" width="{2*cell_size-2*border_size}" height="{4*cell_size+2*border_size}" fill="{helper_bg_color}" stroke="{helper_line_color}" stroke-width="{line_width}" />\n'
            return  __
        
        def walls() -> str:
            __: str = ""
            for ey, row in enumerate(maze.maze):
                for ex, cell in enumerate(row):
                    y, x = ey*cell_size+frame_size, ex*cell_size+frame_size
                    wall_as_lines: bool = True
                    if wall_as_lines:
                        __ += holes(x, y)
                        if cell.walls & DIR.UP.wall:
                            __ += pole(x, y, DIR.LEFT) + wall_line(x, y, DIR.UP) + pole(x+cell_size, y, DIR.RIGHT)
                        if cell.walls & DIR.RIGHT.wall:
                            __ += pole(x+cell_size, y, DIR.UP) + wall_line(x, y, DIR.RIGHT) + pole(x+cell_size, y+cell_size, DIR.DOWN)
                        if cell.walls & DIR.DOWN.wall:
                            __ += pole(x, y+cell_size, DIR.LEFT) + wall_line(x, y, DIR.DOWN) + pole(x+cell_size, y+cell_size, DIR.RIGHT)
                        if cell.walls & DIR.LEFT.wall:
                            __ += pole(x, y, DIR.UP) + wall_line(x, y, DIR.LEFT) + pole(x, y+cell_size, DIR.DOWN)
                    else:
                        if cell.walls & DIR.UP.wall:
                            __ += wall_rect(x, y, DIR.UP)
                        if cell.walls & DIR.RIGHT.wall:
                            __ += wall_rect(x, y, DIR.RIGHT)
                        if cell.walls & DIR.DOWN.wall:
                            __ += wall_rect(x, y, DIR.DOWN)
                        if cell.walls & DIR.LEFT.wall:
                            __ += wall_rect(x, y, DIR.LEFT)

                    if self.changes:
                        if cell.walls & 0xF0 != 0xF0:
                            # changes out
                            changes_mode: str = "out"
                            if cell.walls >> 4 & DIR.UP.wall and not cell.walls & DIR.UP.wall:
                                __ += wall_line(x, y, DIR.UP, changes=changes_mode)
                            if cell.walls >> 4 & DIR.RIGHT.wall and not cell.walls & DIR.RIGHT.wall:
                                __ += wall_line(x, y, DIR.RIGHT, changes=changes_mode)
                            if cell.walls >> 4 & DIR.DOWN.wall and not cell.walls & DIR.DOWN.wall:
                                __ += wall_line(x, y, DIR.DOWN, changes=changes_mode)
                            if cell.walls >> 4 & DIR.LEFT.wall and not cell.walls & DIR.LEFT.wall:
                                __ += wall_line(x, y, DIR.LEFT, changes=changes_mode)

                            # changes in
                            changes_mode: str = "in"

                            if not cell.walls >> 4 & DIR.UP.wall and cell.walls & DIR.UP.wall:
                                __ += pole(x, y, DIR.LEFT) + wall_line(x, y, DIR.UP, changes=changes_mode) + pole(x+cell_size, y, DIR.RIGHT)
                            if not cell.walls >> 4 & DIR.RIGHT.wall and cell.walls & DIR.RIGHT.wall:
                                __ += pole(x+cell_size, y, DIR.UP) + wall_line(x, y, DIR.RIGHT, changes=changes_mode) + pole(x+cell_size, y+cell_size, DIR.DOWN)
                            if not cell.walls >> 4 & DIR.DOWN.wall and cell.walls & DIR.DOWN.wall:
                                __ += pole(x, y+cell_size, DIR.LEFT) + wall_line(x, y, DIR.DOWN, changes=changes_mode) + pole(x+cell_size, y+cell_size, DIR.RIGHT)
                            if not cell.walls >> 4 & DIR.LEFT.wall and cell.walls & DIR.LEFT.wall:
                                __ += pole(x, y, DIR.UP) + wall_line(x, y, DIR.LEFT, changes=changes_mode) + pole(x, y+cell_size, DIR.DOWN)
            return __
        
        def holes(x: int, y: int) -> str:
            __: str = ""
            for iy in range(2):
                for ix in range(2):
                    __ += f'<circle cx="{x+(ix*cell_size)}" cy="{y+(iy*cell_size)}" r="{hole_radius}" fill="{hole_color}" />\n'
            return __

        def zones() -> str:
            __: str = ""
            for pos in maze.start_zone:
                x, y = frame_size+pos[1]*cell_size, frame_size+pos[0]*cell_size
                __ += f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{start_color}" fill-opacity="{zone_opacity}" />\n'
            for pos in maze.end_zone:
                y, x = frame_size+pos[0]*cell_size, frame_size+pos[1]*cell_size
                __ += f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{end_color}" fill-opacity="{zone_opacity}" />\n'
            return __
        
        def markers() -> str:
            __: str = ""
            sy, sx = frame_size+(maze.start_pos[0]+1)*cell_size/2, frame_size+(maze.start_pos[1]+1)*cell_size/2
            __ += f'<text x="{sx}" y="{sy}" font-size="{cell_size*0.67}" font-family="sans-serif" text-anchor="middle" alignment-baseline="central" fill="black" font-weight="bold">{ASCII.start.strip()}</text>\n'
            ey, ex = (maze.height*cell_size+frame_size*2)/2, (maze.width*cell_size+frame_size*2)/2
            __ += f'<text x="{ex}" y="{ey}" font-size="{cell_size*0.67}" font-family="sans-serif" text-anchor="middle" alignment-baseline="central" fill="black" font-weight="bold">{ASCII.end.strip()}</text>\n'
            return __
        
        def ball() -> str:
            color: str = "white"
            stroke: str = "black"
            stroke_width: int = line_width

            y, x = frame_size+maze.ball_marker[0]*cell_size, frame_size+maze.ball_marker[1]*cell_size
            return f'<circle cx="{x}" cy="{y}" r="{ball_radius}" fill="{color}" stroke="{stroke}" stroke-width="{stroke_width}" />\n'

        def pole(x, y, direction) -> str:
            __: str = ""
            x_pole, y_pole = x-pole_size/2, y-pole_size/2
            __ += f'<rect x="{x_pole}" y="{y_pole}" width="{pole_size}" height="{pole_size}" rx="{pole_size/4}" ry="{pole_size/4}" fill="{pole_color}" />\n'
            if direction == DIR.UP:
                x, y, width, height = x_pole, y, pole_size, pole_size/2
            elif direction == DIR.RIGHT:
                x, y, width, height = x_pole, y_pole, pole_size/2, pole_size
            elif direction == DIR.DOWN:
                x, y, width, height = x_pole, y_pole, pole_size, pole_size/2
            elif direction == DIR.LEFT:
                x, y, width, height = x, y_pole, pole_size/2, pole_size
            else:
                return ""
            __ += f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{pole_color}" />\n'
            return __
        
        def wall_rect(x, y, direction, changes=None) -> str:
            x, y = x-pole_size/2, y-pole_size/2
            wall_length: int = cell_size + pole_size
            wall_thickness: int = pole_size
            if direction == DIR.UP:
                x, y, h, w = x, y, wall_thickness, wall_length
            elif direction == DIR.RIGHT:
                x, y, h, w = x+cell_size, y, wall_length, wall_thickness
            elif direction == DIR.DOWN:
                x, y, h, w = x, y+cell_size, wall_thickness, wall_length
            elif direction == DIR.LEFT:
                x, y, h, w = x, y, wall_length, wall_thickness
            else:
                return ""
            color = wall_color if not changes else (wall_out_color if changes == "out" else wall_in_color)
            return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" />\n'
        
        def wall_line(x, y, direction, changes=None) -> str:
            x_pole, y_pole = x+pole_size/2, y+pole_size/2
            wall_length: int = cell_size
            if direction == DIR.UP:
                x1, y1, x2, y2 = x_pole, y, x_pole+wall_length, y
            elif direction == DIR.RIGHT:
                x1, y1, x2, y2 = x+cell_size, y_pole, x+cell_size, y_pole+wall_length
            elif direction == DIR.DOWN:
                x1, y1, x2, y2 = x_pole, y+cell_size, x_pole+wall_length, y+cell_size
            elif direction == DIR.LEFT:
                x1, y1, x2, y2 = x, y_pole, x, y_pole+wall_length
            else:
                return ""
            color = wall_color if not changes else (wall_out_color if changes == "out" else wall_in_color)
            return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{pole_size}" />\n'
        
        def paths() -> str:
            __: str = ""
            for algorithm in Algorithm:
                if algorithm == Algorithm._NONE:
                    continue
                color: str = ""
                offset: int = 0
                if algorithm is Algorithm.FloodFill:
                    color = floodfill_color
                    offset = -2
                elif algorithm is Algorithm.Dijkstra:
                    color = djikstra_color
                    offset = -1
                elif algorithm is Algorithm.AStar:
                    color = astar_color
                    offset = 0
                elif algorithm is Algorithm.BFS:
                    color = bfs_color
                    offset = 1
                elif algorithm is Algorithm.DFS:
                    color = dfs_color
                    offset = 2
                else:
                    continue
                path = maze.paths.get(algorithm)

                if not path:
                    continue

                __ += f'<path d=" '
                for i in range(len(path)):
                    cell = path[i]
                    x, y = frame_size+cell.pos[1]*cell_size+cell_size/2, frame_size+cell.pos[0]*cell_size+cell_size/2
                    if i == 0:
                        __ += f'M {x} {y+offset*(path_line_width*1.2)} '
                    elif i == len(path)-1:
                        before = path[i-1]
                        if cell.pos[0] == before.pos[0]:
                            y += offset*(path_line_width*1.2)
                        else:
                            x += offset*(path_line_width*1.2)
                        __ += f'L {x} {y} '
                    else:
                        __ += f'L {x+offset*(path_line_width*1.2)} {y+offset*(path_line_width*1.2)} '
                __ += f'" fill="none" stroke="{color}" stroke-width="{path_line_width}" stroke-opacity="{path_opacity}" stroke-linecap="round" stroke-linejoin="round" />\n'
            return __
        
        def overview() -> str:
            analysis_maze = maze.visualize.analysis_board()

            __: str = ""
            __ += f'<rect x="{frame_size}" y="{maze.height*cell_size+frame_size+fonz_size}" width="{maze.width*cell_size}" height="{text_height}" stroke="#676767" stroke-width="{path_line_width}" stroke-linejoin="round" fill="#DDDDDD" />\n'

            start_alg: int = 9

            for i, line in enumerate(analysis_maze.split('\n')):
                y = maze.height*cell_size+frame_size+fonz_size*(i+1)+spacer_height

                text_color = "#000000"
                if i == start_alg+0: text_color = floodfill_color
                if i == start_alg+1: text_color = djikstra_color
                if i == start_alg+2: text_color = astar_color
                if i == start_alg+3: text_color = bfs_color
                if i == start_alg+4: text_color = dfs_color

                __ += f'<text x="{frame_size+cell_size}" y="{y}" font-size="{fonz_size}" font-family="monospace" text-anchor="start" alignment-baseline="central" fill="{text_color}" font-weight="bold" xml:space="preserve">{line}</text>\n'
            return __

        __: str = f'<svg width="{maze.width*cell_size+frame_size*2}" height="{maze.height*cell_size+frame_size*2+spacer_height+text_height}" xmlns="http://www.w3.org/2000/svg">\n'

        __ += frame()
        __ += helpers() if self.helpers else ""
        __ += zones() if self.zones else ""
        __ += walls()
        __ += ball()
        __ += paths() if self.paths else ""
        __ += markers() if self.markers else ""
        __ += overview() if self.overview else ""
        
        __ += "</svg>"

        return __
    