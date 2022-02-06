from algorithm import settings
from algorithm.entities.assets.direction import Direction


class Position:
    def __init__(self, x, y, direction: Direction, angle=None):
        """
        Take note that x and y are both PyGame coordinates, and not coordinates
        in terms of the arena grid.
        """
        self.x = x
        self.y = y

        self.direction = direction
        self.angle = angle
        if angle is None:
            self.angle = self.direction.get_angle()

    def __str__(self):
        return f"Position({(self.x / settings.SCALING_FACTOR):.2f}, " \
               f"{(self.y / settings.SCALING_FACTOR):.2f}, " \
               f"direction={self.direction}, " \
               f"angle={self.angle:.2f})"

    __repr__ = __str__

    def xy(self):
        return self.x, self.y

    def angle(self):
        return self.angle

    def copy(self):
        return Position(self.x, self.y, self.direction, self.angle)
