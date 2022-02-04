import math

from algorithm.entities.commands.command import Command
from algorithm.entities.position import Position


class StraightCommand(Command):
    def __init__(self, dist, time):
        super().__init__("straight", time)
        self.dist = dist

    def __str__(self):
        return f"StraightCommand(dist={self.dist})"

    __repr__ = __str__

    def apply_on_pos(self, curr_pos: Position) -> Position:
        # Get straight distance travelled within this time.
        if curr_pos.angle == 0:
            curr_pos.x += self.dist
        elif curr_pos.angle == math.pi / 2:
            curr_pos.y += self.dist
        elif curr_pos.angle == -math.pi / 2:
            curr_pos.y -= self.dist
        else:
            curr_pos.x -= self.dist

        return curr_pos
