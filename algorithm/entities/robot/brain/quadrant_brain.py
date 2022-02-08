from abc import ABC, abstractmethod
from collections import deque

from algorithm.entities.assets.direction import Direction
from algorithm.entities.grid.position import Position


class QuadrantBrain(ABC):
    def __init__(self, brain):
        self.brain = brain
        self.commands = []

    def extend_then_clear_commands(self, li: deque):
        """
        Append the generated commands from this quadrant brain into the main brain,
        and then clears all commands from this quadrant brain.
        """
        li.extend(self.commands)
        self.commands.clear()

    def plan(self, curr_pos: Position, target_pos: Position, is_start):
        """
        Make this quadrant brain plan the path for this iteration.
        """
        offset_pos = self.brain.wrt_bot(curr_pos, target_pos)
        if offset_pos.direction == Direction.BOTTOM:
            print("Planning for picture at south.")
            self.bottom_image(curr_pos, target_pos, is_start)
        elif offset_pos.direction == Direction.RIGHT:
            print("Planning for picture at east.")
            self.right_image(curr_pos, target_pos, is_start)
        elif offset_pos.direction == Direction.LEFT:
            print("Planning for picture at west.")
            self.left_image(curr_pos, target_pos, is_start)
        else:
            print("Planning for picture at north.")
            self.top_image(curr_pos, target_pos, is_start)

    @abstractmethod
    def bottom_image(self, curr_pos, target_pos, is_start):
        """
        Plan the path for when the obstacle image is facing top.
        """
        pass

    @abstractmethod
    def top_image(self, curr_pos, target_pos, is_start):
        """
        Plan the path for when the obstacle image is facing bottom.
        """
        pass

    @abstractmethod
    def right_image(self, curr_pos, target_pos, is_start):
        """
        Plan the path for when the obstacle image is facing right.
        """
        pass

    @abstractmethod
    def left_image(self, curr_pos, target_pos, is_start):
        """
        Plan the path for when the obstacle image is facing left.
        """
        pass
