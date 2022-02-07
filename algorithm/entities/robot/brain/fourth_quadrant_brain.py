import math

from algorithm import settings
from algorithm.entities.commands.straight_command import StraightCommand
from algorithm.entities.commands.turn_command import TurnCommand
from algorithm.entities.robot.brain.quadrant_brain import QuadrantBrain


class FourthQuadrantBrain(QuadrantBrain):
    def __init__(self, brain):
        super().__init__(brain)

    def south_image(self, curr_pos, target_pos, is_start):
        offset_pos = self.brain.wrt_bot(curr_pos, target_pos)

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
        offset_pos.y += settings.ROBOT_TURN_RADIUS
        step_1.apply_on_pos(curr_pos)

        realign_dist = offset_pos.x - (settings.OBSTACLE_SAFETY_WIDTH + settings.ROBOT_TURN_RADIUS)
        step_2 = StraightCommand(realign_dist)
        self.commands.append(step_2)
        offset_pos.x = settings.OBSTACLE_SAFETY_WIDTH + settings.ROBOT_TURN_RADIUS
        step_2.apply_on_pos(curr_pos)

        step_3 = TurnCommand(-math.pi / 2, False)
        self.commands.append(step_3)
        offset_pos.x -= settings.ROBOT_TURN_RADIUS
        offset_pos.y += settings.ROBOT_TURN_RADIUS
        step_3.apply_on_pos(curr_pos)

        step_4 = StraightCommand(-offset_pos.y)
        self.commands.append(step_4)
        offset_pos.y = 0
        step_4.apply_on_pos(curr_pos)

        step_5 = TurnCommand(math.pi / 2, False)
        self.commands.append(step_5)
        offset_pos.x -= settings.ROBOT_TURN_RADIUS
        offset_pos.y += settings.ROBOT_TURN_RADIUS
        step_5.apply_on_pos(curr_pos)

        realign_dist = offset_pos.x - settings.ROBOT_TURN_RADIUS
        step_6 = StraightCommand(realign_dist)
        self.commands.append(step_6)
        offset_pos.x = settings.ROBOT_TURN_RADIUS
        step_6.apply_on_pos(curr_pos)

        step_7 = TurnCommand(math.pi / 2, False)
        self.commands.append(step_7)
        step_7.apply_on_pos(curr_pos)
        # END
        self.extend_then_clear_commands(self.brain.commands)

    def north_image(self, curr_pos, target_pos, is_start):
        pass

    def east_image(self, curr_pos, target_pos, is_start):
        # Get the offset
        offset_pos = self.brain.wrt_bot(curr_pos, target_pos)

        # If the current x-offset is less than 2 * OBSTACLE_SAFETY_WIDTH,
        # that means we cannot just reverse, as we may collide. Instead, we need
        # to sidestep the obstacle.
        if offset_pos.x < 2 * settings.OBSTACLE_SAFETY_WIDTH:
            # Do a reverse turn to face east.
            self.commands.append(
                TurnCommand(-math.pi / 2, True).apply_on_pos(curr_pos)
            )
            offset_pos.x += settings.ROBOT_TURN_RADIUS
            offset_pos.y += settings.ROBOT_TURN_RADIUS

            # Move straight until we line up the x-offsets.
            self.commands.append(
                StraightCommand(offset_pos.x).apply_on_pos(curr_pos)
            )
            offset_pos.x = 0

            # Do a forward turn to the right.
            self.commands.append(
                TurnCommand(-math.pi / 2, False).apply_on_pos(curr_pos)
            )
            offset_pos.x -= settings.ROBOT_TURN_RADIUS
            offset_pos.y += settings.ROBOT_TURN_RADIUS

            # Move until we have enough y-offset to make a forward turn to the right.
            dist = -offset_pos.y - settings.ROBOT_TURN_RADIUS
            self.commands.append(
                StraightCommand(dist).apply_on_pos(curr_pos)
            )

            # Do a forward turn to the right.
            self.commands.append(
                TurnCommand(-math.pi / 2, False).apply_on_pos(curr_pos)
            )

            # End.
            self.extend_then_clear_commands(self.brain.commands)
            return
        else:
            # We reverse until we have enough y-offset to do a forward turn to the right,
            # leaving OBSTACLE_SAFETY_WIDTH.
            dist = offset_pos.y - settings.OBSTACLE_SAFETY_WIDTH - settings.ROBOT_TURN_RADIUS
            self.commands.append(
                StraightCommand(dist).apply_on_pos(curr_pos)
            )
            offset_pos.y = settings.OBSTACLE_SAFETY_WIDTH + settings.ROBOT_TURN_RADIUS

            # Do a forward turn to the right
            self.commands.append(
                TurnCommand(-math.pi / 2, False).apply_on_pos(curr_pos)
            )
            offset_pos.x -= settings.ROBOT_TURN_RADIUS
            offset_pos.y -= settings.ROBOT_TURN_RADIUS

            # Move straight to align x-offset
            self.commands.append(
                StraightCommand(offset_pos.x).apply_on_pos(curr_pos)
            )
            offset_pos.x = 0

            # Do a forward turn to the left
            self.commands.append(
                TurnCommand(math.pi / 2, False).apply_on_pos(curr_pos)
            )
            offset_pos.x -= settings.ROBOT_TURN_RADIUS
            offset_pos.y -= settings.ROBOT_TURN_RADIUS

            # Move straight until we have enough distance to make a forward turn to left.
            dist = -settings.ROBOT_TURN_RADIUS + offset_pos.y
            self.commands.append(
                StraightCommand(dist).apply_on_pos(curr_pos)
            )

            # Do a forward turn to the left.
            self.commands.append(
                TurnCommand(math.pi / 2, False).apply_on_pos(curr_pos)
            )

            # End.
            self.extend_then_clear_commands(self.brain.commands)
            return

    def west_image(self, curr_pos, target_pos, is_start):
        pass
