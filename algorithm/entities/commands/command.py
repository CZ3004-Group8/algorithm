import math
from abc import ABC, abstractmethod

from algorithm import settings


class Command(ABC):
    def __init__(self, c, time):
        self.type = c  # Type of command.
        self.time = time  # Time in seconds in which this command is carried out.
        self.ticks = math.ceil(time * settings.FRAMES)  # Number of frame ticks that this command will take.
        self.total_ticks = self.ticks  # Keep track of original total ticks.

    def tick(self):
        self.ticks -= 1

    @abstractmethod
    def process_one_tick(self, robot):
        """
        Overriding method must call tick().
        """
        pass

    @abstractmethod
    def apply_on_pos(self, curr_pos):
        """
        Apply this command to a Position, such that its attributes will reflect the correct values
        after the command is done.
        """
        pass
