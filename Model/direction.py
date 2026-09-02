from enum import Enum

class Direction(Enum):
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
    UP = (-1, 0)

DIRECTIONS = (
    Direction.RIGHT,
    Direction.DOWN,
    Direction.LEFT,
    Direction.UP
)