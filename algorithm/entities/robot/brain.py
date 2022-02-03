import itertools
import math
from algorithm import settings

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
                targets.append(ob.get_robot_target_pos().xy())

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
        curr_pos = self.robot.get_current_pos()
        for obs in self.simple_hamiltonian:
            print("-" * 40)
            target_pos = obs.get_robot_target_pos()
            self.plan_curr_to_target(curr_pos, target_pos)
            print("-" * 40)
            # Update the current pos and angle
            curr_pos = target_pos

    @classmethod
    def plan_curr_to_target(cls, curr_pos, target_pos):
        # Get the x, y difference between the current and target
        x_diff, y_diff = target_pos.x - curr_pos.x, curr_pos.y - target_pos.y

        # Figure out which quadrant the next target is
        # WITH RESPECT TO the current location and orientation.
        # Note that we use 0-indexing.
        quad = 3
        facing = 0
        if x_diff >= 0 and y_diff >= 0:
            quad = 0
            print("Next point in 1st quadrant.")
        elif x_diff < 0 and y_diff >= 0:
            quad = 1
            print("Next point in 2nd quadrant.")
        elif x_diff < 0 and y_diff < 0:
            quad = 2
            print("Next point in 3rd quadrant.")
        else:
            print("Next point in 4th quadrant.")

        # We change it to depend on the current orientation.
        if curr_pos.angle == 0:
            print("Robot currently facing east.")
            quad += 1
            facing = 3
        elif curr_pos.angle == -math.pi / 2:
            print("Robot currently facing south.")
            quad += 2
            facing = 2
        elif curr_pos.angle == math.pi:
            print("Robot currently facing west.")
            quad += 3
            facing = 1
        else:
            print("Robot currently facing north.")
        # Modulo and make it 1-indexed.
        quad = (quad % 4) + 1
        print(f"With respect to current position and orientation, obstacle is at quadrant {quad}")

        # check target's next coordinates with respect to robot's pov
        newcoord_x = curr_pos.x + (math.cos(facing*0.5) * (x_diff)) - (math.sin(facing*0.5) * (y_diff)) - curr_pos.x
        newcoord_y = curr_pos.y + (math.sin(facing*0.5) * (x_diff)) + (math.cos(facing*0.5) * (y_diff)) - curr_pos.y
        print(f"Target's new coordinate wrt to robot's POV is {newcoord_x/settings.SCALING_FACTOR}, {newcoord_y/settings.SCALING_FACTOR}")

        # Check if the x_diff is within the limits.
        # If not, we have to move the robot.
        angle_diff = target_pos.angle - curr_pos.angle
        if angle_diff == 0:
            print("Target orientation same.")
        elif angle_diff == math.pi:
            print("Target orientation is opposite.")
        elif angle_diff == math.pi / 2:
            print("Target orientation is left of current.")
        else:
            print("Target orientation is right of current.")

