from algorithm.entities.commands.command import Command


class StraightCommand(Command):
    def __init__(self, dist, time, rev):
        super().__init__("straight", time, rev)
        self.dist = dist

    def __str__(self):
        return f"StraightCommand(dist={self.dist}, rev={self.rev})"

    __repr__ = __str__
