import itertools
import math
from typing import List, Tuple


class Brain:
    def __init__(self, robot, grid):
        self.robot = robot
        self.grid = grid

        self.simple_hamiltonian = []
        self.compute_simple_hamiltonian_path()

    def compute_simple_hamiltonian_path(self):
        """
        Get the Hamiltonian Path to all points with the best possible effort.

        This is a simple calculation where we assume that we travel directly to the next obstacle.
        """
        # Generate all possible permutations for the image obstacles
        perms = list(itertools.permutations(self.grid.obstacles))

        # Get the path that has the least distance travelled.
        def calc_distance(path):
            # Create all target points, including the start.
            targets = [self.grid.get_start_box_rect().center]
            for obs in path:
                target, _ = obs.get_robot_target()
                targets.append(target.as_tuple())

            dist = 0
            for i in range(len(targets) - 1):
                dist += math.sqrt(((targets[i][0] - targets[i + 1][0]) ** 2) +
                                  ((targets[i][1] - targets[i + 1][1]) ** 2))
            return dist

        self.simple_hamiltonian = min(perms, key=calc_distance)
        print(f"Simple Hamiltonian Path: {self.simple_hamiltonian}")

    def tangent_points(self, c1x: float, c1y: float, c1r: float,
                       c2x: float, c2y: float, c2r: float) -> List[Tuple[float, float]]:
        c1c2 = math.hypot(c2x - c1x, c2y - c1y)
        t0 = math.atan2(c2y - c1y, c2x - c1x)
        ps: List[Tuple[float, float]] = []

        r1r2 = c1r + c2r
        if math.isclose(c1c2, r1r2):
            ps.append((c1x + c1r * math.cos(t0), c1y + c1r * math.sin(t0)))
        elif c1c2 > r1r2:
            t1 = math.acos(r1r2 / c1c2)
            ps.append((c1x + c1r * math.cos(t0 + t1), c1y + c1r * math.sin(t0 + t1)))
            ps.append((c1x + c1r * math.cos(t0 - t1), c1y + c1r * math.sin(t0 - t1)))

        r1r2 = c1r - c2r
        if math.isclose(c1c2, abs(r1r2)):
            if r1r2 > 0.0:
                t1 = 0.0
            else:
                t1 = math.pi
            ps.append((c1x + c1r * math.cos(t0 + t1), c1y + c1r * math.sin(t0 + t1)))
        elif c1c2 > abs(r1r2):
            if r1r2 > 0.0:
                t1 = math.acos(r1r2 / c1c2)
            else:
                t1 = math.pi - math.acos(-r1r2 / c1c2)
            ps.append((c1x + c1r * math.cos(t0 + t1), c1y + c1r * math.sin(t0 + t1)))
            ps.append((c1x + c1r * math.cos(t0 - t1), c1y + c1r * math.sin(t0 - t1)))

        return ps

    def plan_next_move(self):
        """
        Plan the next movements to get to the next target.
        """
        pass
