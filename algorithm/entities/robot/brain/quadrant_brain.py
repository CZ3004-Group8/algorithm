from abc import ABC, abstractmethod
from collections import deque

from algorithm.entities.grid.position import Position


class QuadrantBrain(ABC):
    def __init__(self, brain):
        self.brain = brain
        self.commands = []

    def extend_then_clear_commands(self, li: deque):
        li.extend(self.commands)
        self.commands.clear()

    @abstractmethod
    def plan(self, curr_pos: Position, target_pos: Position, is_start: bool):
        pass

    @abstractmethod
    def south_image(self, curr_pos, target_pos, is_start):
        pass

    @abstractmethod
    def north_image(self, curr_pos, target_pos, is_start):
        pass

    @abstractmethod
    def east_image(self, curr_pos, target_pos, is_start):
        pass

    @abstractmethod
    def west_image(self, curr_pos, target_pos, is_start):
        pass
