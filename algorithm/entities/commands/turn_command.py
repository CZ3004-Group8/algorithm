import math

from algorithm import settings
from algorithm.entities.commands.command import Command
from algorithm.entities.position import Position


class TurnCommand(Command):
    def __init__(self, angle, rev):
        time = abs((angle * settings.ROBOT_LENGTH) / (settings.ROBOT_SPEED_PER_SECOND * settings.ROBOT_S_FACTOR))
        super().__init__("turn", time)
        self.angle = angle
        self.rev = rev

    def __str__(self):
        return f"TurnCommand({self.angle:.2f}rad, {self.time:.2f}s, rev={self.rev})"

    __repr__ = __str__

    def apply_on_pos(self, curr_pos: Position) -> Position:
        """
        x_new = x + R(sin(∆θ + θ) − sin θ)
        y_new = y − R(cos(∆θ + θ) − cos θ)
        θ_new = θ + ∆θ
        R is the turning radius.

        Take note that:
            - +ve ∆θ -> rotate counter-clockwise
            - -ve ∆θ -> rotate clockwise

        Note that ∆θ is in radians.
        """
        # Get change in (x, y) coordinate.
        x_change = settings.ROBOT_TURN_RADIUS * (math.sin(curr_pos.angle + self.angle) - math.sin(curr_pos.angle))
        y_change = settings.ROBOT_TURN_RADIUS * (math.cos(curr_pos.angle + self.angle) - math.cos(curr_pos.angle))

        if self.angle < 0 and not self.rev:  # Wheels to right moving forward.
            curr_pos.x -= x_change
            curr_pos.y -= y_change
        elif (self.angle < 0 and self.rev) or \
                (self.angle >= 0 and not self.rev):  # (Wheels to left moving backwards) or (Wheels to left moving forwards).
            curr_pos.x += x_change
            curr_pos.y += y_change
        else:  # Wheels to right moving backwards.
            curr_pos.x -= x_change
            curr_pos.y -= y_change
        curr_pos.angle += self.angle

        if curr_pos.angle <= -math.pi:
            curr_pos.angle += 2 * math.pi
        elif curr_pos.angle >= math.pi:
            curr_pos.angle -= 2 * math.pi

        return curr_pos
