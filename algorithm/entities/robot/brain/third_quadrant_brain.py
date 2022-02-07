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

        # If the target is not below current position, then we can just reverse.
        if offset_pos.x <= -settings.OBSTACLE_SAFETY_WIDTH:
            # Reverse until y-offset is ROBOT_TURN_RADIUS
            dist = -settings.ROBOT_TURN_RADIUS + offset_pos.y
            self.commands.append(
                StraightCommand(dist).apply_on_pos(curr_pos)
            )
            offset_pos.y = settings.ROBOT_TURN_RADIUS

            # Do a forward turn to the left
            self.commands.append(
                TurnCommand(math.pi / 2, False).apply_on_pos(curr_pos)
            )
            offset_pos.x += settings.ROBOT_TURN_RADIUS
            offset_pos.y -= settings.ROBOT_TURN_RADIUS

            # Make the x-offset +ROBOT_TURN_RADIUS
            dist = -offset_pos.x + settings.ROBOT_TURN_RADIUS
            self.commands.append(
                StraightCommand(dist).apply_on_pos(curr_pos)
            )

            # Do a reverse turn to face north.
            self.commands.append(
                TurnCommand(-math.pi / 2, True).apply_on_pos(curr_pos)
            )
            offset_pos.y += settings.ROBOT_TURN_RADIUS

            # Go forward.
            self.commands.append(
                StraightCommand(offset_pos.y).apply_on_pos(curr_pos)
            )

            # End.
            self.extend_then_clear_commands(self.brain.commands)
            return
        else:
            # Do a reverse turn to face east.
            self.commands.append(
                TurnCommand(-math.pi / 2, True).apply_on_pos(curr_pos)
            )
            offset_pos.x += settings.ROBOT_TURN_RADIUS
            offset_pos.y += settings.ROBOT_TURN_RADIUS

            # Move until ROBOT_TURN_RADIUS + OBSTACLE_SAFETY_RADIUS
            dist = offset_pos.x - (settings.ROBOT_TURN_RADIUS + settings.OBSTACLE_SAFETY_WIDTH)
            self.commands.append(
                StraightCommand(dist).apply_on_pos(curr_pos)
            )
            offset_pos.x = settings.ROBOT_TURN_RADIUS + settings.OBSTACLE_SAFETY_WIDTH

            # Do a forward turn to the right.
            self.commands.append(
                TurnCommand(-math.pi / 2, False).apply_on_pos(curr_pos)
            )
            offset_pos.x -= settings.ROBOT_TURN_RADIUS
            offset_pos.y += settings.ROBOT_TURN_RADIUS

            # Align y-offsets.
            self.commands.append(
                StraightCommand(-offset_pos.y).apply_on_pos(curr_pos)
            )
            offset_pos.y = 0

            # Do a forward turn to the left.
            self.commands.append(
                TurnCommand(math.pi / 2, False).apply_on_pos(curr_pos)
            )
            offset_pos.x -= settings.ROBOT_TURN_RADIUS
            offset_pos.y += settings.ROBOT_TURN_RADIUS

            # Realign so we can do a forward left turn to the target.
            dist = -(settings.ROBOT_TURN_RADIUS - offset_pos.x)
            self.commands.append(
                StraightCommand(dist).apply_on_pos(curr_pos)
            )

            # Do a forward left turn to target.
            self.commands.append(
                TurnCommand(math.pi / 2, False).apply_on_pos(curr_pos)
            )

            # End.
            self.extend_then_clear_commands(self.brain.commands)
            return

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
