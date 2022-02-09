import math
import time
from queue import PriorityQueue
from typing import List, Tuple

from algorithm import settings
from algorithm.entities.commands.command import Command
from algorithm.entities.commands.straight_command import StraightCommand
from algorithm.entities.commands.turn_command import TurnCommand
from algorithm.entities.grid.grid import Grid
from algorithm.entities.grid.node import Node
from algorithm.entities.grid.position import RobotPosition


class AStar:
    def __init__(self, grid, brain, start: RobotPosition, end: RobotPosition):
        # We use a copy of the grid rather than use a reference
        # to the exact grid.
        self.grid: Grid = grid.copy()
        self.brain = brain

        self.start = start
        self.end = end

    def get_neighbours(self, pos: RobotPosition) -> List[Tuple[Node, RobotPosition, int, Command]]:
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
                after.pos.direction = p.direction
                neighbours.append((after.copy(), p, straight_dist, c))

        # Check turns
        turn_penalty = 2 * settings.ROBOT_TURN_RADIUS
        turn_commands = [
            TurnCommand(90, False),  # Forward right turn
            TurnCommand(-90, False),  # Forward left turn
            TurnCommand(90, True),  # Reverse with wheels to right.
            TurnCommand(-90, True),  # Reverse with wheels to left.
        ]
        for c in turn_commands:
            p = pos.copy()
            c.apply_on_pos(p)
            # TODO: Check that turning does not cause position to go into invalid positions.
            if self.grid.check_valid_position(p) and (after := self.grid.get_coordinate_node(*p.xy())):
                after.pos.direction = p.direction
                neighbours.append((after.copy(), p, turn_penalty, c))
        return neighbours

    def heuristic(self, curr_pos: RobotPosition):
        """
        Measure the difference in distance between the provided position and the
        end position.
        """
        dx = abs(curr_pos.x - self.end.x)
        dy = abs(curr_pos.y - self.end.y)
        return math.sqrt(dx ** 2 + dy ** 2)

    def start_astar(self):
        frontier = PriorityQueue()  # Store frontier nodes to travel to.
        backtrack = dict()  # Store the sequence of nodes being travelled.
        cost = dict()  # Store the cost to travel from start to a node.

        # We can check what the goal node is
        goal_node = self.grid.get_coordinate_node(*self.end.xy()).copy()  # Take note of copy!
        goal_node.pos.direction = self.end.direction  # Set the required direction at this node.

        # Add starting node set into the frontier.
        start_node: Node = self.grid.get_coordinate_node(*self.start.xy()).copy()  # Take note of copy!
        start_node.direction = self.start.direction  # Make the node know which direction the robot is facing.

        frontier.put((0, time.time(), (start_node, self.start)))  # Extra time parameter to tie-break same priority.
        cost[start_node] = 0
        # Having None as the parent means this key is the starting node.
        backtrack[start_node] = (None, None)  # Parent, Command

        while not frontier.empty():  # While there are still nodes to process.
            # Get the highest priority node.
            priority, _, (current_node, current_position) = frontier.get()
            # If the current node is our goal.
            if current_node == goal_node:
                print(f"Found path to {self.end}!")
                break

            # Otherwise, we check through all possible locations that we can
            # travel to from this node.
            for new_node, new_pos, weight, c in self.get_neighbours(current_position):
                new_cost = cost.get(current_node) + weight

                if new_node not in backtrack or new_cost < cost[new_node]:
                    priority = new_cost + self.heuristic(new_pos)

                    frontier.put((priority, time.time(), (new_node, new_pos)))
                    backtrack[new_node] = (current_node, c)
                    cost[new_node] = new_cost

        # Get the commands needed to get to destination.
        self.extract_commands(backtrack, goal_node)

    def extract_commands(self, backtrack, goal_node):
        """
        Extract required commands to get to destination.
        """
        commands = []
        curr = goal_node
        while curr:
            curr, c = backtrack.get(curr, (None, None))
            if c:
                commands.append(c)
        commands.reverse()
        self.brain.commands.extend(commands)
