import math

from algorithm import settings
from algorithm.entities.commands.straight_command import StraightCommand
from algorithm.entities.commands.turn_command import TurnCommand
from algorithm.entities.robot.brain.quadrant_brain import QuadrantBrain


class FirstQuadrantBrain(QuadrantBrain):
    def __init__(self, brain):
        super().__init__(brain)

    def south_image(self, curr_pos, target_pos, is_start):
        # Get the offset.
        offset_pos = self.brain.wrt_bot(curr_pos, target_pos)

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
            step_1.apply_on_pos(curr_pos)

            step_2 = TurnCommand(math.pi / 2, True)
            self.commands.append(step_2)
            # Update offsets
            offset_pos.y += settings.ROBOT_TURN_RADIUS
            offset_pos.x -= settings.ROBOT_TURN_RADIUS
            step_2.apply_on_pos(curr_pos)

            # offset_x must be -turning_radius.
            realign_dist = -settings.ROBOT_TURN_RADIUS - offset_pos.x
            step_3 = StraightCommand(realign_dist)
            self.commands.append(step_3)
            # Update offsets
            offset_pos.x = -settings.ROBOT_TURN_RADIUS
            step_3.apply_on_pos(curr_pos)

            step_4 = TurnCommand(-math.pi / 2, False)
            self.commands.append(step_4)
            # Update offsets
            offset_pos.x += settings.ROBOT_TURN_RADIUS
            offset_pos.y -= settings.ROBOT_TURN_RADIUS
            step_4.apply_on_pos(curr_pos)

            step_5 = StraightCommand(offset_pos.y)
            self.commands.append(step_5)
            step_5.apply_on_pos(curr_pos)
            # END
            self.extend_then_clear_commands(self.brain.commands)
            return

        # There is an obstacle in front of the robot, so we need to move the robot away.
        # STEPS:
        # 1. Do a reverse turn to face to the west.
        # 2. Reverse another safety width distance.
        # 3. Do a forward turn to the right.
        # 4. Go forward another safety width distance.
        # 5. Recursively check for the path.
        step_1 = TurnCommand(math.pi / 2, True)
        self.commands.append(step_1)
        step_1.apply_on_pos(curr_pos)

        step_2 = StraightCommand(-settings.OBSTACLE_SAFETY_WIDTH)
        self.commands.append(step_2)
        step_2.apply_on_pos(curr_pos)

        step_3 = TurnCommand(-math.pi / 2, False)
        self.commands.append(step_3)
        step_3.apply_on_pos(curr_pos)

        step_4 = StraightCommand(settings.OBSTACLE_SAFETY_WIDTH)
        self.commands.append(step_4)
        step_4.apply_on_pos(curr_pos)

        # We set is_start to True, since we have moved away from the obstacle.
        self.extend_then_clear_commands(self.brain.commands)
        self.brain.plan_curr_to_target(curr_pos, target_pos, True)

    def north_image(self, curr_pos, target_pos, is_start):
        pass

    def east_image(self, curr_pos, target_pos, is_start):
        pass

    def west_image(self, curr_pos, target_pos, is_start):
        pass
