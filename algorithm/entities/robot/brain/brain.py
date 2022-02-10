import itertools
import math
from collections import deque
from typing import Tuple

from algorithm.entities.commands.scan_command import ScanCommand
from algorithm.entities.grid.obstacle import Obstacle
from algorithm.entities.robot.brain.hybrid_a_star import AStar


class Brain:
    def __init__(self, robot, grid):
        self.robot = robot
        self.grid = grid

        # Compute the simple Hamiltonian path for all obstacles
        self.simple_hamiltonian = tuple()

        # Create all the commands required to finish the course.
        self.commands = deque()

    def compute_simple_hamiltonian_path(self) -> Tuple[Obstacle]:
        """
        Get the Hamiltonian Path to all points with the best possible effort.
        This is a simple calculation where we assume that we travel directly to the next obstacle.
        """
        # Generate all possible permutations for the image obstacles
        perms = list(itertools.permutations(self.grid.obstacles))

        # Get the path that has the least distance travelled.
        def calc_distance(path):
            # Create all target points, including the start.
            targets = [self.robot.pos.xy_pygame()]
            for obstacle in path:
                targets.append(obstacle.pos.xy_pygame())

            dist = 0
            for i in range(len(targets) - 1):
                dist += math.sqrt(((targets[i][0] - targets[i + 1][0]) ** 2) +
                                  ((targets[i][1] - targets[i + 1][1]) ** 2))
            return dist

        simple = min(perms, key=calc_distance)
        print("Found a simple hamiltonian path:")
        for ob in simple:
            print(f"\t{ob}")
        return simple

    def plan_path(self):
        self.simple_hamiltonian = self.compute_simple_hamiltonian_path()

        curr = self.robot.pos.copy()  # We use a copy rather than get a reference.
        for obstacle in self.simple_hamiltonian:
            target = obstacle.get_robot_target_pos()
            print(f"Planning {curr} against {target}")
            res = AStar(self.grid, self, curr, target).start_astar()
            if res is None:
                print(f"No path found from {curr} to {obstacle}")
            else:
                curr = res
                self.commands.append(ScanCommand(2))
