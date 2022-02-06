from algorithm import settings
from algorithm.entities.assets.direction import Direction
from algorithm.entities.commands.command import Command
from algorithm.entities.grid.position import Position


class StraightCommand(Command):
    COMMAND_TYPE = "straight"

    def __init__(self, dist):
        """
        Specified distance is scaled. Do not divide the provided distance by the scaling factor!
        """
        # Calculate the time needed to travel the required distance.
        time = abs(dist / settings.ROBOT_SPEED_PER_SECOND)
        super().__init__(self.COMMAND_TYPE, time)

        self.dist = dist

    def __str__(self):
        return f"StraightCommand(dist={self.dist / settings.SCALING_FACTOR}, {self.total_ticks} ticks)"

    __repr__ = __str__

    def process_one_tick(self, robot):
        if self.total_ticks == 0:
            return

        self.tick()
        distance = self.dist / self.total_ticks
        robot.straight(distance)

    def apply_on_pos(self, curr_pos: Position):
        """
        Apply this command onto a current Position object.
        """
        if curr_pos.direction == Direction.RIGHT:
            curr_pos.x += self.dist
        elif curr_pos.direction == Direction.TOP:
            curr_pos.y -= self.dist
        elif curr_pos.direction == Direction.BOTTOM:
            curr_pos.y += self.dist
        else:
            curr_pos.x -= self.dist
