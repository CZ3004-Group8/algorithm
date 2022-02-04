from algorithm.entities.commands.command import Command


class TurnCommand(Command):
    def __init__(self, angle, time, rev):
        super().__init__("turn", time)
        self.angle = angle
        self.rev = rev

    def __str__(self):
        return f"TurnCommand({self.angle:.2f}rad, {self.time:.2f}s, rev={self.rev})"

    __repr__ = __str__

    @classmethod
    def apply_on_pos(cls, pos):
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
        x_change = self.TURNING_RADIUS * (math.sin(self.pos.angle + d_angle) - math.sin(self.pos.angle))
        y_change = self.TURNING_RADIUS * (math.cos(self.pos.angle + d_angle) - math.cos(self.pos.angle))

        if d_angle < 0 and not rev:  # Wheels to right moving forward.
            self.pos.x -= x_change
            self.pos.y -= y_change
        elif (d_angle < 0 and rev) or \
                (d_angle >= 0 and not rev):  # (Wheels to left moving backwards) or (Wheels to left moving forwards).
            self.pos.x += x_change
            self.pos.y += y_change
        else:  # Wheels to right moving backwards.
            self.pos.x -= x_change
            self.pos.y -= y_change
        self.pos.angle += d_angle

        if self.pos.angle <= -math.pi:
            self.pos.angle += 2 * math.pi
        elif self.pos.angle >= math.pi:
            self.pos.angle -= 2 * math.pi