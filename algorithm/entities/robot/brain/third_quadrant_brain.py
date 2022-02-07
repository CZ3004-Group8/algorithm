import math

from algorithm import settings
from algorithm.entities.commands.straight_command import StraightCommand
from algorithm.entities.commands.turn_command import TurnCommand
from algorithm.entities.robot.brain.quadrant_brain import QuadrantBrain


class ThirdQuadrantBrain(QuadrantBrain):
    def __init__(self, brain):
        super().__init__(brain)

    def south_image(self, curr_pos, target_pos, is_start):
        offset_pos = self.brain.wrt_bot(curr_pos, target_pos)

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
        step_1.apply_on_pos(curr_pos)

        realign_dist = -(settings.OBSTACLE_SAFETY_WIDTH + settings.ROBOT_TURN_RADIUS) - offset_pos.x
        step_2 = StraightCommand(realign_dist)
        self.commands.append(step_2)
        offset_pos.x = -(settings.OBSTACLE_SAFETY_WIDTH + settings.ROBOT_TURN_RADIUS)
        step_2.apply_on_pos(curr_pos)

        step_3 = TurnCommand(math.pi / 2, False)
        self.commands.append(step_3)
        offset_pos.x += settings.ROBOT_TURN_RADIUS
        offset_pos.y += settings.ROBOT_TURN_RADIUS
        step_3.apply_on_pos(curr_pos)

        step_4 = StraightCommand(-offset_pos.y)
        self.commands.append(step_4)
        offset_pos.y = 0
        step_4.apply_on_pos(curr_pos)

        step_5 = TurnCommand(-math.pi / 2, False)
        self.commands.append(step_5)
        offset_pos.x += settings.ROBOT_TURN_RADIUS
        offset_pos.y += settings.ROBOT_TURN_RADIUS
        step_5.apply_on_pos(curr_pos)

        realign_dist = -settings.ROBOT_TURN_RADIUS - offset_pos.x
        step_6 = StraightCommand(realign_dist)
        self.commands.append(step_6)
        offset_pos.x = -settings.ROBOT_TURN_RADIUS
        step_6.apply_on_pos(curr_pos)

        step_7 = TurnCommand(-math.pi / 2, False)
        self.commands.append(step_7)
        step_7.apply_on_pos(curr_pos)
        # END
        self.extend_then_clear_commands(self.brain.commands)

    def north_image(self, curr_pos, target_pos, is_start):
        pass

    def east_image(self, curr_pos, target_pos, is_start):
        # Get the offset
        offset_pos = self.brain.wrt_bot(curr_pos, target_pos)

        # If there is enough x-offset for the robot to do a forward turn to the left directly,
        # then we just travel backwards and leave enough y-offset for a forward turn to the left,
        # then travel straight to the obstacle.
        if offset_pos.x <= -settings.ROBOT_TURN_RADIUS:
            # Travel backwards and leave enough space for the turn.
            dist = offset_pos.y - settings.ROBOT_TURN_RADIUS
            self.commands.append(
                StraightCommand(dist).apply_on_pos(curr_pos)
            )
            offset_pos.y = settings.ROBOT_TURN_RADIUS

            # Do a forward turn to the left.
            self.commands.append(
                TurnCommand(math.pi / 2, False).apply_on_pos(curr_pos)
            )
            offset_pos.x += settings.ROBOT_TURN_RADIUS

            # Travel straight to the obstacle.
            self.commands.append(
                StraightCommand(-offset_pos.x).apply_on_pos(curr_pos)
            )

            # End
            self.extend_then_clear_commands(self.brain.commands)
            return
        else:
            # Travel backwards until y-offset is equal ROBOT_TURN_RADIUS
            dist = offset_pos.y + settings.ROBOT_TURN_RADIUS
            self.commands.append(
                StraightCommand(dist).apply_on_pos(curr_pos)
            )
            offset_pos.y = settings.ROBOT_TURN_RADIUS

            # Do a reverse turn to face west.
            self.commands.append(
                TurnCommand(math.pi / 2, True).apply_on_pos(curr_pos)
            )
            offset_pos.x -= settings.ROBOT_TURN_RADIUS
            offset_pos.y -= settings.ROBOT_TURN_RADIUS

            # Move until x-offset is 0.
            self.commands.append(
                StraightCommand(-offset_pos.x).apply_on_pos(curr_pos)
            )

            # End.
            self.extend_then_clear_commands(self.brain.commands)
            return

    def west_image(self, curr_pos, target_pos, is_start):
        pass
