from abc import ABC, abstractmethod
from collections import deque

from algorithm.entities.assets.direction import Direction
from algorithm.entities.grid.position import Position


class QuadrantBrain(ABC):
    def __init__(self, brain):
        self.brain = brain
        self.commands = []

    def extend_then_clear_commands(self, li: deque):
        li.extend(self.commands)
        self.commands.clear()

    def plan(self, curr_pos: Position, target_pos: Position, is_start):
        offset_pos = self.brain.wrt_bot(curr_pos, target_pos)
        if offset_pos.direction == Direction.BOTTOM:
            print("Planning for picture at south.")
            self.south_image(curr_pos, target_pos, is_start)
        elif offset_pos.direction == Direction.RIGHT:
            print("Planning for picture at east.")
            self.east_image(curr_pos, target_pos, is_start)
        elif offset_pos.direction == Direction.LEFT:
            print("Planning for picture at west.")
            self.west_image(curr_pos, target_pos, is_start)
        else:
            print("Planning for picture at north.")
            self.north_image(curr_pos, target_pos, is_start)

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
