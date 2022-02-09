import math
from queue import PriorityQueue

from algorithm.entities.grid.grid import Grid
from algorithm.entities.grid.node import Node
from algorithm.entities.grid.position import Position


class AStar:
    def __init__(self, grid, start: Position, end: Position):
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
            for nnode, npos in self.grid.get_neighbours(current_position):
                pass
