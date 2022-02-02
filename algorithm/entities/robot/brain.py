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

    def plan_path(self):
        """
        Plan the next movements to get to the next target.
        """

        # Plan the path.
        curr_pos, curr_angle = self.robot.get_current_pos()
        for obs in self.simple_hamiltonian:
            print("-" * 40)
            target_pos, target_angle = obs.get_robot_target()
            self.plan_curr_to_target(curr_pos, curr_angle, target_pos, target_angle)
            print("-" * 40)
            # Update the current pos and angle
            curr_pos, curr_angle = target_pos, target_angle

    @classmethod
    def plan_curr_to_target(cls, curr_center, curr_angle, target_center, target_angle):
        # Get the x, y difference between the current and target
        x_diff, y_diff = target_center.x - curr_center.x, curr_center.y - target_center.y

        if x_diff >= 0 and y_diff >= 0:
            quad = 1
            print("Next point in 1st quadrant.")
        elif x_diff >= 0 and y_diff < 0:
            quad = 4
            print("Next point in 4th quadrant.")
        elif x_diff < 0 and y_diff >= 0:
            quad = 2
            print("Next point in 2nd quadrant.")
        else:
            quad = 3
            print("Next point in 3rd quadrant.")

        # Check if the x_diff is within the limits.
        # If not, we have to move the robot.
        angle_diff = target_angle - curr_angle
        if angle_diff == 0:
            print("Target orientation same.")
        elif angle_diff == math.pi:
            print("Target orientation is opposite.")
        elif angle_diff == math.pi / 2:
            print("Target orientation is left of current.")
        else:
            print("Target orientation is right of current.")
