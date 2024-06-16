class Dir:
    def __init__(self, move: tuple[int, int], wall: int, name: str):
        self.name: str = name
        self.move: tuple[int, int] = move
        self.y: int = move[0]
        self.x: int = move[1]
        self.wall: int = wall
        self.opposite: Dir

    def set_opposite(self, opposite: 'Dir'):
        self.opposite = opposite

    def set_move_options(self, options: list['Dir']):
        self.move_options = options

    def __str__(self):
        return self.name


class DIR:
    UP: Dir = Dir(move=(-1, 0), wall=0x01, name="UP")
    RIGHT: Dir = Dir(move=(0, 1), wall=0x02, name="RIGHT")
    DOWN: Dir = Dir(move=(1, 0), wall=0x04, name="DOWN")
    LEFT: Dir = Dir(move=(0, -1), wall=0x08, name="LEFT")
    _EMPTY: Dir = Dir(move=(0, 0), wall=0x00, name="_EMPTY")

    # Setting opposites
    UP.set_opposite(DOWN)
    RIGHT.set_opposite(LEFT)
    DOWN.set_opposite(UP)
    LEFT.set_opposite(RIGHT)
    _EMPTY.set_opposite(_EMPTY)

    # Setting move options
    UP.set_move_options([UP, RIGHT, LEFT])
    RIGHT.set_move_options([UP, RIGHT, DOWN])
    DOWN.set_move_options([RIGHT, DOWN, LEFT])
    LEFT.set_move_options([UP, DOWN, LEFT])
    _EMPTY.set_move_options([UP, RIGHT, DOWN, LEFT])

    ALL: list[Dir] = [UP, RIGHT, DOWN, LEFT]