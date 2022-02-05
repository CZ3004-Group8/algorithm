import itertools
import math

from algorithm import settings
from algorithm.entities.commands.straight_command import StraightCommand
from algorithm.entities.commands.turn_command import TurnCommand
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
        is_start = True
        for obs in self.simple_hamiltonian:
            print("-" * 40)
            target_pos = obs.get_robot_target_pos()
            dest_pos = self.plan_curr_to_target(curr_pos, target_pos, is_start)
            is_start = False
            print("-" * 40)
            # Update the current pos and angle.
            curr_pos = dest_pos

    def plan_curr_to_target(self, curr_pos, target_pos, is_start):
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
            return self.plan_first_quadrant(curr_pos, target_pos, is_start)
        elif math.pi / 2 <= angle <= math.pi:
            print("Obstacle in robot's 2nd quadrant.")
            return self.plan_second_quadrant(curr_pos, target_pos, is_start)
        elif -math.pi <= angle < -math.pi / 2:
            print("Obstacle in robot's 3rd quadrant.")
            return self.plan_third_quadrant(curr_pos, target_pos, is_start)
        elif -math.pi / 2 <= angle < 0:
            print("Obstacle in robot's 4th quadrant.")
            return self.plan_fourth_quadrant(curr_pos, target_pos, is_start)

    def plan_first_quadrant(self, curr_pos, target_pos, is_start):
        return target_pos

    def first_quadrant_south_image(self, curr_pos, target_pos, is_start):
        # Get the offset.
        offset_pos = self.wrt_bot(curr_pos, target_pos)

        # If robot is moving from a starting point (no obstacle in front of the robot).
        if is_start:
            # STEPS:
            # 1. Go forward turning_radius distance.
            # 2. Do a reverse turn to face west.
            # 3. Reposition until enough x-offset to line up x-coordinate after a forward turn to the right.
            # 4. Do a forward turn to the right.
            # 5. Go straight until we reach the target.
            step_1 = StraightCommand(settings.ROBOT_TURN_RADIUS)
            self.commands.append(step_1)
            # Update offsets
            offset_pos.y -= settings.ROBOT_TURN_RADIUS
            curr_pos = step_1.apply_on_pos(curr_pos)

            step_2 = TurnCommand(math.pi / 2, True)
            self.commands.append(step_2)
            # Update offsets
            offset_pos.y += settings.ROBOT_TURN_RADIUS
            offset_pos.x -= settings.ROBOT_TURN_RADIUS
            curr_pos = step_2.apply_on_pos(curr_pos)

            # offset_x must be -turning_radius.
            realign_dist = -settings.ROBOT_TURN_RADIUS - offset_pos.x
            step_3 = StraightCommand(realign_dist)
            # Update offsets
            offset_pos.x = -settings.ROBOT_TURN_RADIUS
            curr_pos = step_3.apply_on_pos(curr_pos)

            step_4 = TurnCommand(-math.pi / 2, False)
            self.commands.append(step_4)
            # Update offsets
            offset_pos.x += settings.ROBOT_TURN_RADIUS
            offset_pos.y -= settings.ROBOT_TURN_RADIUS
            curr_pos = step_4.apply_on_pos(curr_pos)

            step_5 = StraightCommand(offset_pos.y)
            self.commands.append(step_5)
            # Only need to update curr_pos
            curr_pos = step_5.apply_on_pos(curr_pos)
            # END
            return curr_pos

        # There is an obstacle in front of the robot, so we need to move the robot away.
        # STEPS:
        # 1. Do a reverse turn to face to the west.
        # 2. Reverse another safety width distance.
        # 3. Do a forward turn to the right.
        # 4. Go forward another safety width distance.
        # 5. Recursively check for the path.
        step_1 = TurnCommand(math.pi / 2, True)
        self.commands.append(step_1)
        curr_pos = step_1.apply_on_pos(curr_pos)

        step_2 = StraightCommand(-settings.OBSTACLE_SAFETY_WIDTH)
        self.commands.append(step_2)
        curr_pos = step_2.apply_on_pos(curr_pos)

        step_3 = TurnCommand(-math.pi / 2, False)
        self.commands.append(step_3)
        curr_pos = step_3.apply_on_pos(curr_pos)

        step_4 = StraightCommand(settings.OBSTACLE_SAFETY_WIDTH)
        self.commands.append(step_4)
        curr_pos = step_4.apply_on_pos(curr_pos)

        # We set is_start to True, since we have moved away from the obstacle.
        return self.plan_curr_to_target(curr_pos, target_pos, True)

    def first_quadrant_east_image(self, curr_pos, target_pos, is_start):
        pass

    def plan_second_quadrant(self, curr_pos, target_pos, is_start):
        return target_pos

    def second_quadrant_south_image(self, curr_pos, target_pos, is_start):
        # Get the offset
        offset_pos = self.wrt_bot(curr_pos, target_pos)

        # If robot is moving from a starting point (no obstacle in front of the robot).
        if is_start:
            # STEPS:
            # 1. Go forward turning_radius distance.
            # 2. Do a reverse turn to face east.
            # 3. Reposition until enough x-offset to line up x-coordinate after a forward turn to the left.
            # 4. Do a forward turn to the left.
            # 5. Go straight until we reach the target.
            step_1 = StraightCommand(settings.ROBOT_TURN_RADIUS)
            self.commands.append(step_1)
            offset_pos.y -= settings.ROBOT_TURN_RADIUS
            curr_pos = step_1.apply_on_pos(curr_pos)

            step_2 = TurnCommand(-math.pi / 2, True)
            self.commands.append(step_2)
            offset_pos.x -= settings.ROBOT_TURN_RADIUS
            offset_pos.y += settings.ROBOT_TURN_RADIUS
            curr_pos = step_2.apply_on_pos(curr_pos)

            realign_dist = offset_pos.x - settings.ROBOT_TURN_RADIUS
            step_3 = StraightCommand(realign_dist)
            self.commands.append(step_3)
            offset_pos.x = settings.ROBOT_TURN_RADIUS
            curr_pos = step_3.apply_on_pos(curr_pos)

            step_4 = TurnCommand(math.pi / 2, False)
            self.commands.append(step_4)
            offset_pos.x += settings.ROBOT_TURN_RADIUS
            offset_pos.y -= settings.ROBOT_TURN_RADIUS
            curr_pos = step_3.apply_on_pos(curr_pos)

            step_5 = StraightCommand(offset_pos.y)
            self.commands.append(step_5)
            curr_pos = step_5.apply_on_pos(curr_pos)
            # END.
            return curr_pos

        # There is an obstacle in front of the robot, so we need to move the robot away.
        # STEPS:
        # 1. Do a reverse turn to face to the east.
        # 2. Reverse another safety width distance.
        # 3. Do a forward turn to the left.
        # 4. Go forward another safety width distance.
        # 5. Recursively check for the path.
        step_1 = TurnCommand(-math.pi / 2, True)
        self.commands.append(step_1)
        curr_pos = step_1.apply_on_pos(curr_pos)

        step_2 = StraightCommand(-settings.OBSTACLE_SAFETY_WIDTH)
        self.commands.append(step_2)
        curr_pos = step_2.apply_on_pos(curr_pos)

        step_3 = TurnCommand(math.pi / 2, False)
        self.commands.append(step_3)
        curr_pos = step_3.apply_on_pos(curr_pos)

        step_4 = StraightCommand(settings.OBSTACLE_SAFETY_WIDTH)
        self.commands.append(step_4)
        curr_pos = step_4.apply_on_pos(curr_pos)

        # We set is_start to True, since we have moved away from the obstacle.
        return self.plan_curr_to_target(curr_pos, target_pos, True)

    def second_quadrant_east_image(self, curr_pos, target_pos, is_start):
        pass

    def plan_third_quadrant(self, curr_pos, target_pos, is_start):
        return target_pos

    def third_quadrant_south_image(self, curr_pos, target_pos, is_start):
        offset_pos = self.wrt_bot(curr_pos, target_pos)

        # STEPS:
        # 1. Do a reverse turn to face west.
        # 2. Readjust to allow safety_width + turning_radius distance between target x-coordinate.
        # 3. Do a forward turn to the left.
        # 4. Go forward until lined up with target y-coordinate.
        # 5. Do a forward turn to the right.
        # 6. Realign to allow turning_radius distance between current and target x-coordinate.
        # 7. Do a forward turn to the right.
        step_1 = TurnCommand(math.pi / 2, True)
        self.commands.append(step_1)
        offset_pos.x -= settings.ROBOT_TURN_RADIUS
        offset_pos.y += settings.ROBOT_TURN_RADIUS
        curr_pos = step_1.apply_on_pos(curr_pos)

        realign_dist = -(settings.OBSTACLE_SAFETY_WIDTH + settings.ROBOT_TURN_RADIUS) - offset_pos.x
        step_2 = StraightCommand(realign_dist)
        self.commands.append(step_2)
        offset_pos.x = -(settings.OBSTACLE_SAFETY_WIDTH + settings.ROBOT_TURN_RADIUS)
        curr_pos = step_2.apply_on_pos(curr_pos)

        step_3 = TurnCommand(math.pi / 2, False)
        self.commands.append(step_3)
        offset_pos.x += settings.ROBOT_TURN_RADIUS
        offset_pos.y += settings.ROBOT_TURN_RADIUS
        curr_pos = step_3.apply_on_pos(curr_pos)

        step_4 = StraightCommand(-offset_pos.y)
        self.commands.append(step_4)
        offset_pos.y = 0
        curr_pos = step_4.apply_on_pos(curr_pos)

        step_5 = TurnCommand(-math.pi / 2, False)
        self.commands.append(step_5)
        offset_pos.x += settings.ROBOT_TURN_RADIUS
        offset_pos.y += settings.ROBOT_TURN_RADIUS
        curr_pos = step_5.apply_on_pos(curr_pos)

        realign_dist = -offset_pos.x - settings.ROBOT_TURN_RADIUS
        step_6 = StraightCommand(realign_dist)
        self.commands.append(step_6)
        offset_pos.x = -settings.ROBOT_TURN_RADIUS
        curr_pos = step_6.apply_on_pos(curr_pos)

        step_7 = TurnCommand(-math.pi / 2, False)
        self.commands.append(step_7)
        curr_pos = step_7.apply_on_pos(curr_pos)
        # END
        return curr_pos

    def third_quadrant_east_image(self, curr_pos, target_pos, is_start):
        pass

    def plan_fourth_quadrant(self, curr_pos, target_pos, is_start):
        return target_pos

    def fourth_quadrant_south_image(self, curr_pos, target_pos, is_start):
        offset_pos = self.wrt_bot(curr_pos, target_pos)

        # STEPS:
        # 1. Do a reverse turn to face east.
        # 2. Readjust to allow safety_width + turning_radius distance between target x-coordinate.
        # 3. Do a forward turn to the right.
        # 4. Go forward until lined up with target y-coordinate.
        # 5. Do a forward turn to the left.
        # 6. Realign to allow turning_radius distance between current and target x-coordinate.
        # 7. Do a forward turn to the left.
        step_1 = TurnCommand(-math.pi / 2, True)
        self.commands.append(step_1)
        offset_pos.x += settings.ROBOT_TURN_RADIUS
        offset_pos.y -= settings.ROBOT_TURN_RADIUS
        curr_pos = step_1.apply_on_pos(curr_pos)

        realign_dist = settings.OBSTACLE_SAFETY_WIDTH + settings.ROBOT_TURN_RADIUS - offset_pos.x
        step_2 = StraightCommand(realign_dist)
        self.commands.append(step_2)
        offset_pos.x = settings.OBSTACLE_SAFETY_WIDTH + settings.ROBOT_TURN_RADIUS
        curr_pos = step_2.apply_on_pos(curr_pos)

        step_3 = TurnCommand(-math.pi / 2, False)
        self.commands.append(step_3)
        offset_pos.x -= settings.ROBOT_TURN_RADIUS
        offset_pos.y -= settings.ROBOT_TURN_RADIUS
        curr_pos = step_3.apply_on_pos(curr_pos)

        step_4 = StraightCommand(-offset_pos.y)
        self.commands.append(step_4)
        offset_pos.y = 0
        curr_pos = step_4.apply_on_pos(curr_pos)

        step_5 = TurnCommand(math.pi / 2, False)
        self.commands.append(step_5)
        offset_pos.x -= settings.ROBOT_TURN_RADIUS
        offset_pos.y -= settings.ROBOT_TURN_RADIUS
        curr_pos = step_5.apply_on_pos(curr_pos)

        realign_dist = settings.ROBOT_TURN_RADIUS - offset_pos.x
        step_6 = StraightCommand(realign_dist)
        self.commands.append(step_6)
        offset_pos.x = settings.ROBOT_TURN_RADIUS
        curr_pos = step_6.apply_on_pos(curr_pos)

        step_7 = TurnCommand(math.pi / 2, False)
        self.commands.append(step_7)
        curr_pos = step_7.apply_on_pos(curr_pos)
        # END
        return curr_pos

    def fourth_quadrant_east_image(self, curr_pos, target_pos, is_start):
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
