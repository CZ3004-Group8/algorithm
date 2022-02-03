from algorithm.entities.commands.command import Command


class TurnCommand(Command):
    def __init__(self, angle, time, rev):
        super().__init__("turn", time)
        self.angle = angle
        self.rev = rev

    def __str__(self):
        return f"TurnCommand({self.angle:.2f}rad, {self.time:.2f}s)"

    __repr__ = __str__
