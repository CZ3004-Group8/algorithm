class Command:
    def __init__(self, c):
        self.c = c


class TurnCommand(Command):
    def __init__(self, angle, time):
        super().__init__("turn")
        self.angle = angle
        self.time = time
