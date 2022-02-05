import math

from algorithm import settings


class Command:
    def __init__(self, c, time):
        self.type = c  # Type of command.
        self.time = time  # Time in seconds in which this command is carried out.
        self.ticks = math.ceil(time * settings.FRAMES)  # Number of frame ticks that this command will take.

    def tick(self):
        self.ticks -= 1
