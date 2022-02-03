import itertools
import math

from algorithm.entities.position import Position


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

    def plan_curr_to_target(self, curr_pos, target_pos):
        """
        Plan a path for the robot to travel from the current position to the target position.
        """
        # Get the current offset of the obstacle from the robot's perspective.
        offset_pos = self.wrt_bot(curr_pos, target_pos)

    @classmethod
    def wrt_bot(cls, bot_pos, target_pos) -> Position:
        """
        Return a new Position object that has the bot always facing north and at the origin, and having the target
        offset from the robot.
        """
        # Get the x, y difference between the current and target
        x_diff, y_diff = target_pos.x - bot_pos.x, bot_pos.y - target_pos.y

        # Figure out which quadrant the next target is
        # WITH RESPECT TO the current location and orientation.
        # Note that we use 0-indexing.
        quad = 3
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
        if bot_pos.angle == 0:
            print("Robot currently facing east.")
            quad += 1
        elif bot_pos.angle == -math.pi / 2:
            print("Robot currently facing south.")
            quad += 2
        elif bot_pos.angle == math.pi:
            print("Robot currently facing west.")
            quad += 3
        else:
            print("Robot currently facing north.")
        # Modulo and make it 1-indexed.
        quad = (quad % 4) + 1
        print(f"With respect to current position and orientation, obstacle is at quadrant {quad}")

        # TODO: Junyan, do it here.
        return None
