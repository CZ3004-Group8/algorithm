import itertools
import math
from collections import deque
from typing import Tuple

from algorithm import settings
from algorithm.entities.assets.direction import Direction
from algorithm.entities.grid.obstacle import Obstacle
from algorithm.entities.grid.position import Position
from algorithm.entities.robot.brain.first_quadrant_brain import FirstQuadrantBrain
from algorithm.entities.robot.brain.fourth_quadrant_brain import FourthQuadrantBrain
from algorithm.entities.robot.brain.second_quadrant_brain import SecondQuadrantBrain
from algorithm.entities.robot.brain.third_quadrant_brain import ThirdQuadrantBrain


class Brain:
    def __init__(self, robot, grid):
        self.robot = robot
        self.grid = grid

        self.first = FirstQuadrantBrain(self)
        self.second = SecondQuadrantBrain(self)
        self.third = ThirdQuadrantBrain(self)
        self.fourth = FourthQuadrantBrain(self)

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
            targets = [self.grid.get_start_box_rect().center]
            for ob in path:
                targets.append(ob.get_robot_target_pos().xy())

            dist = 0
            for i in range(len(targets) - 1):
                dist += math.sqrt(((targets[i][0] - targets[i + 1][0]) ** 2) +
                                  ((targets[i][1] - targets[i + 1][1]) ** 2))
            return dist
        return min(perms, key=calc_distance)

    def plan_path(self):
        """
        Plan the next movements to get to the next target.
        """
        # Calculate simple hamiltonian path.
        self.simple_hamiltonian = self.compute_simple_hamiltonian_path()

        curr_pos = self.robot.get_current_pos().copy()
        is_start = True  # At starting position, the robot has no obstacle in front of it.
        for obs in self.simple_hamiltonian:
            print("-" * 40)
            target_pos = obs.get_robot_target_pos()
            self.plan_curr_to_target(curr_pos, target_pos, is_start)
            is_start = False
            print("-" * 40)
            curr_pos = target_pos
            break

        for c in self.commands:
            print(c)

    def plan_curr_to_target(self, curr_pos: Position, target_pos: Position, is_start: bool):
        """
        Plan a path for the robot to travel from the current position to the target position.
        """
        # Get the current offset of the obstacle from the robot's perspective.
        # Take note that the offset is in pygame coordinates (which is scaled)
        offset_pos = self.wrt_bot(curr_pos, target_pos)
        print(f"Target's new coordinate wrt to robot's POV is {offset_pos.x / settings.SCALING_FACTOR}, "
              f"{offset_pos.y / settings.SCALING_FACTOR}")
        # Find which quadrant the obstacle is wrt to the robot.
        angle = math.atan2(offset_pos.y, offset_pos.x)

        if 0 <= angle < math.pi / 2:
            print("Obstacle in robot's 1st quadrant.")
            self.first.plan(curr_pos, target_pos, is_start)
        elif math.pi / 2 <= angle <= math.pi:
            print("Obstacle in robot's 2nd quadrant.")
            self.second.plan(curr_pos, target_pos, is_start)
        elif -math.pi < angle < -math.pi / 2:
            print("Obstacle in robot's 3rd quadrant.")
            self.third.plan(curr_pos, target_pos, is_start)
        else:
            print("Obstacle in robot's 4th quadrant.")
            self.fourth.plan(curr_pos, target_pos, is_start)

    @staticmethod
    def wrt_bot(bot_pos: Position, target_pos: Position) -> Position:
        """
        Return a new Position object that has the bot always facing north and at the origin, and having the target
        offset from the robot.
        """
        # Get the x, y difference between the current and target
        x_diff, y_diff = target_pos.x - bot_pos.x, bot_pos.y - target_pos.y

        facing = 0
        # We change it to depend on the current orientation.
        if bot_pos.direction == Direction.RIGHT:
            facing = 3
        elif bot_pos.direction == Direction.BOTTOM:
            facing = 2
        elif bot_pos.direction == Direction.LEFT:
            facing = 1

        # check target's next coordinates with respect to robot's pov
        offset_x = bot_pos.x + (math.cos(facing * 0.5) * x_diff) - (math.sin(facing * 0.5) * y_diff) - bot_pos.x
        offset_y = bot_pos.y + (math.sin(facing * 0.5) * x_diff) + (math.cos(facing * 0.5) * y_diff) - bot_pos.y

        # TODO: Logic to get correct direction.
        return Position(offset_x, offset_y, Direction.BOTTOM)
