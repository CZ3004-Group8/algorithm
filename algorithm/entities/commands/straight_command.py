from algorithm.entities.commands.command import Command


class StraightCommand(Command):
    def __init__(self, dist, time):
        super().__init__("straight", time)
        self.dist = dist

    def __str__(self):
        return f"StraightCommand(dist={self.dist})"

    __repr__ = __str__
