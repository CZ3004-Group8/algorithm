import math
from queue import PriorityQueue
from typing import List, Tuple

from algorithm import settings
from algorithm.entities.commands.straight_command import StraightCommand
from algorithm.entities.commands.turn_command import TurnCommand
from algorithm.entities.grid.grid import Grid
from algorithm.entities.grid.node import Node
from algorithm.entities.grid.position import Position, RobotPosition


class AStar:
    def __init__(self, grid, start: RobotPosition, end: RobotPosition):
        # We use a copy of the grid rather than use a reference
        # to the exact grid.
        self.grid: Grid = grid.copy()

        self.start = start
        self.end = end

    @classmethod
    def change_of_basis(cls, p1: Position, p2: Position):
        """
        Change the offset of p2 from p1 to be in terms of p1 as the origin
        and x-axis with angle p1.angle.
        """
        theta1 = math.radians(p1.direction.value)
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        new_x = dx * math.cos(theta1) + dy * math.sin(theta1)
        new_y = -dx * math.sin(theta1) + dy * math.cos(theta1)
        return new_x, new_y

    def get_neighbours(self, pos: RobotPosition) -> List[Tuple[Node, RobotPosition, int]]:
        """
        Get movement neighbours from this position.

        Note that all values in the Position object (x, y, direction) are all with respect to the grid!

        We also expect the return Positions to be with respect to the grid.
        """
        # We assume the robot will always make a full 90-degree turn to the next neighbour, and that it will travel
        # a fix distance of 10 when travelling straight.
        neighbours = []

        # Check travel straights.
        straight_dist = 10 * settings.SCALING_FACTOR
        straight_commands = [
            StraightCommand(straight_dist),
            StraightCommand(-straight_dist)
        ]
        for c in straight_commands:
            p = pos.copy()
            c.apply_on_pos(p)
            if self.grid.check_valid_position(p) and (after := self.grid.get_coordinate_node(*p.xy())):
                neighbours.append((after, p, straight_dist))

        # Check turns
        turn_penalty = 2 * settings.ROBOT_TURN_RADIUS
        turn_commands = [
            TurnCommand(90, False),  # Forward right turn
            TurnCommand(-90, False),  # Forward left turn
            TurnCommand(90, True),  # Reverse with wheels to right.
            TurnCommand(-90, False),  # Reverse with wheels to left.
        ]
        for c in turn_commands:
            p = pos.copy()
            c.apply_on_pos(p)
            after = self.grid.get_coordinate_node(*p.xy())
            if self.grid.check_valid_position(p) and (after := self.grid.get_coordinate_node(*p.xy())):
                neighbours.append((after, p, turn_penalty))
        return neighbours

    def start_astar(self):
        frontier = PriorityQueue()  # Store frontier nodes to travel to.
        backtrack = dict()  # Store the sequence of nodes being travelled.

        # We can check what the goal node is
        goal_node = self.grid.get_coordinate_node(*self.end.xy())

        # Add starting node set into the frontier.
        start_node: Node = self.grid.get_coordinate_node(*self.start.xy())
        start_node.direction = self.start.direction  # Make the node know which direction the robot is facing.

        start_pair = (start_node, self.start)
        frontier.put((0, start_pair))
        backtrack[start_pair] = None  # Having None as the value means this key is the starting node.

        while not frontier.empty():  # While there are still nodes to process.
            # Get the highest priority node.
            current_node, current_position = frontier.get()

            # If the current node is our goal.
            if current_node == goal_node:
                break

            # Otherwise, we check through all possible locations that we can
            # travel to from this node.
            for n_node, n_pos, weight in self.get_neighbours(current_position):
                print(n_node, n_pos, weight)
