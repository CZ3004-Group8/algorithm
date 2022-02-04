import itertools
import math

from algorithm import settings
from algorithm.entities.position import Position


class Brain:
    OFFSET_THRESHOLD: int = 0

    def __init__(self, robot, grid):
        self.robot = robot
        self.OFFSET_THRESHOLD = self.robot.TURNING_RADIUS

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
        # Take note that the offset is in pygame coordinates (which is scaled)
        offset_pos = self.wrt_bot(curr_pos, target_pos)
        # Find which quadrant the obstacle is wrt to the robot.
        angle = math.atan2(offset_pos.y, offset_pos.x)
        if 0 <= angle < math.pi / 2:
            print("Obstacle in robot's 1st quadrant.")
            self.plan_first_quadrant(curr_pos, target_pos)
        elif math.pi / 2 <= angle <= math.pi:
            print("Obstacle in robot's 2nd quadrant.")
            self.plan_second_quadrant(curr_pos, target_pos)
        elif -math.pi <= angle < -math.pi / 2:
            print("Obstacle in robot's 3rd quadrant.")
            self.plan_third_quadrant(curr_pos, target_pos)
        elif -math.pi / 2 <= angle < 0:
            print("Obstacle in robot's 4th quadrant.")
            self.plan_fourth_quadrant(curr_pos, target_pos)

    def plan_first_quadrant(self, offset_pos):
        pass

    def first_quadrant_facing_south(self, offset_pos):
        pass

    def plan_second_quadrant(self, curr_pos, target_pos):
        pass

    def plan_third_quadrant(self, curr_pos, target_pos):
        pass

    def plan_fourth_quadrant(self, curr_pos, target_pos):
        pass

    def fourth_quadrant_facing_south(self, curr_pos, target_pos):
        pass

    @classmethod
    def wrt_bot(cls, bot_pos, target_pos) -> Position:
        """
        Return a new Position object that has the bot always facing north and at the origin, and having the target
        offset from the robot.
        """
        # Get the x, y difference between the current and target
        x_diff, y_diff = target_pos.x - bot_pos.x, bot_pos.y - target_pos.y

        facing = 0
        # We change it to depend on the current orientation.
        if bot_pos.angle == 0:
            print("Robot currently facing east.")
            facing = 3
        elif bot_pos.angle == -math.pi / 2:
            print("Robot currently facing south.")
            facing = 2
        elif bot_pos.angle == math.pi:
            print("Robot currently facing west.")
            facing = 1
        else:
            print("Robot currently facing north.")

        # check target's next coordinates with respect to robot's pov
        offset_x = bot_pos.x + (math.cos(facing * 0.5) * x_diff) - (math.sin(facing * 0.5) * y_diff) - bot_pos.x
        offset_y = bot_pos.y + (math.sin(facing * 0.5) * x_diff) + (math.cos(facing * 0.5) * y_diff) - bot_pos.y
        print(f"Target's new coordinate wrt to robot's POV is {offset_x / settings.SCALING_FACTOR}, "
              f"{offset_y / settings.SCALING_FACTOR}")

        return Position(offset_x, offset_y, 0)
