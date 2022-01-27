import itertools
import math


class Brain:
    def __init__(self, robot, grid):
        self.robot = robot
        self.grid = grid

        # Compute the simple Hamiltonian path for all obstacles
        self.simple_hamiltonian = tuple()
        self.compute_simple_hamiltonian_path()

        # Create all the commands required to finish the course.
        self.commands = []
        self.plan_path()

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
            for ob in path:
                target, _ = ob.get_robot_target()
                targets.append(target.as_tuple())

            dist = 0
            for i in range(len(targets) - 1):
                dist += math.sqrt(((targets[i][0] - targets[i + 1][0]) ** 2) +
                                  ((targets[i][1] - targets[i + 1][1]) ** 2))
            return dist

        self.simple_hamiltonian = min(perms, key=calc_distance)
        print(f"Simple Hamiltonian Path:")
        for obs in self.simple_hamiltonian:
            print(f"\t{obs}")

    def plan_start(self):
        print("Planning from starting point to next obstacle.")

        # Get the starting turning circle from the grid.
        grid_start = self.grid.start_turning_circle
        # Get the next image obstacle to travel to.
        next_obs_circles = self.simple_hamiltonian[0].turning_circles
        print(f"Planning from {grid_start} to either of {next_obs_circles}")
        self.commands.extend(grid_start.find_tangents(next_obs_circles[0]))
        self.commands.extend(next_obs_circles[0].find_tangents(grid_start))

    def plan_path(self):
        """
        Plan the next movements to get to the next target.
        """
        # Plan from start to next obstacle.
        self.plan_start()
