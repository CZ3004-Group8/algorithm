import math

from algorithm import settings
from algorithm.entities.commands.straight_command import StraightCommand
from algorithm.entities.commands.turn_command import TurnCommand
from algorithm.entities.robot.brain.quadrant_brain import QuadrantBrain


class FourthQuadrantBrain(QuadrantBrain):
    def __init__(self, brain):
        super().__init__(brain)

    def bottom_image(self, curr_pos, target_pos, is_start):
        offset_pos = self.brain.wrt_bot(curr_pos, target_pos)

        # If the target is not below current position, then we can just reverse.
        if offset_pos.x >= settings.OBSTACLE_SAFETY_WIDTH:
            # Reverse until y-offset is ROBOT_TURN_RADIUS
            dist = -settings.ROBOT_TURN_RADIUS + offset_pos.y
            self.commands.append(
                StraightCommand(dist).apply_on_pos(curr_pos)
            )
            offset_pos.y = settings.ROBOT_TURN_RADIUS

            # Do forward turn to the right.
            self.commands.append(
                TurnCommand(-math.pi / 2, False).apply_on_pos(curr_pos)
            )
            offset_pos.x -= settings.ROBOT_TURN_RADIUS
            offset_pos.y -= settings.ROBOT_TURN_RADIUS

            # Make the x-offset +ROBOT_TURN_RADIUS
            dist = offset_pos.x + settings.ROBOT_TURN_RADIUS
            self.commands.append(
                StraightCommand(dist).apply_on_pos(curr_pos)
            )

            # Do a reverse turn to face north.
            self.commands.append(
                TurnCommand(math.pi / 2, True).apply_on_pos(curr_pos)
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
            # Do a reverse turn to face west.
            self.commands.append(
                TurnCommand(math.pi / 2, True).apply_on_pos(curr_pos)
            )
            offset_pos.x -= settings.ROBOT_TURN_RADIUS
            offset_pos.y += settings.ROBOT_TURN_RADIUS

            # Move until ROBOT_TURN_RADIUS + OBSTACLE_SAFETY_WIDTH
            dist = -(settings.ROBOT_TURN_RADIUS + settings.OBSTACLE_SAFETY_WIDTH) - offset_pos.x
            self.commands.append(
                StraightCommand(dist).apply_on_pos(curr_pos)
            )
            offset_pos.x = -(settings.ROBOT_TURN_RADIUS + settings.OBSTACLE_SAFETY_WIDTH)

            # Do a forward turn to the left.
            self.commands.append(
                TurnCommand(math.pi / 2, False).apply_on_pos(curr_pos)
            )
            offset_pos.x += settings.ROBOT_TURN_RADIUS
            offset_pos.y += settings.ROBOT_TURN_RADIUS

            # Align y-offsets.
            self.commands.append(
                StraightCommand(-offset_pos.y).apply_on_pos(curr_pos)
            )
            offset_pos.y = 0

            # Do a forward turn to the right.
            self.commands.append(
                TurnCommand(-math.pi / 2, False).apply_on_pos(curr_pos)
            )
            offset_pos.x += settings.ROBOT_TURN_RADIUS
            offset_pos.y += settings.ROBOT_TURN_RADIUS

            # Realign so we can do a forward right turn to the target.
            dist = -(settings.ROBOT_TURN_RADIUS + offset_pos.x)
            self.commands.append(
                StraightCommand(dist).apply_on_pos(curr_pos)
            )

            # Do a forward right turn to the target.
            self.commands.append(
                TurnCommand(-math.pi / 2, False).apply_on_pos(curr_pos)
            )

            # End.
            self.extend_then_clear_commands(self.brain.commands)
            return

    def top_image(self, curr_pos, target_pos, is_start):
        pass

    def right_image(self, curr_pos, target_pos, is_start):
        # Get the offset
        offset_pos = self.brain.wrt_bot(curr_pos, target_pos)

        # If the current y-offset is enough for us to path from the top,
        # then we do so.
        if offset_pos.y <= -settings.ROBOT_TURN_RADIUS - settings.OBSTACLE_SAFETY_WIDTH:
            # Do a reverse turn to face west.
            self.commands.append(
                TurnCommand(math.pi / 2, True).apply_on_pos(curr_pos)
            )
            offset_pos.x -= settings.ROBOT_TURN_RADIUS
            offset_pos.y += settings.ROBOT_TURN_RADIUS

            # Move straight until we line up the x-offsets.
            self.commands.append(
                StraightCommand(-offset_pos.x).apply_on_pos(curr_pos)
            )
            offset_pos.x = 0

            # Do a reverse turn to face south.
            self.commands.append(
                TurnCommand(math.pi / 2, True).apply_on_pos(curr_pos)
            )
            offset_pos.x -= settings.ROBOT_TURN_RADIUS
            offset_pos.y -= settings.ROBOT_TURN_RADIUS

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
            # The target is too high, so we need to go from the bottom.
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

    def left_image(self, curr_pos, target_pos, is_start):
        pass
