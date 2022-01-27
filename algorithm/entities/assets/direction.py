from enum import Enum

import math


class Direction(Enum):
    """
    Possible directions for an Obstacle. This is an enumeration.
    """
    NORTH = math.pi / 2
    SOUTH = -math.pi / 2
    EAST = 0
    WEST = math.pi