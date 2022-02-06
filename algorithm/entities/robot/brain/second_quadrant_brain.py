import math

from algorithm import settings
from algorithm.entities.commands.straight_command import StraightCommand
from algorithm.entities.commands.turn_command import TurnCommand
from algorithm.entities.robot.brain.quadrant_brain import QuadrantBrain


class SecondQuadrantBrain(QuadrantBrain):
    def __init__(self, brain):
        super().__init__(brain)

    def south_image(self, curr_pos, target_pos, is_start):
        # Get the offset
        offset_pos = self.brain.wrt_bot(curr_pos, target_pos)
        if math.isclose(offset_pos.x, 0) and math.isclose(offset_pos.y, 0):
            return

        # If there is an obstacle currently in front of the robot.
        if not is_start:
            # Do a reverse turn to face west.
            self.commands.append(
                TurnCommand(math.pi / 2, True).apply_on_pos(curr_pos)
            )
            # Move forward OBSTACLE_SAFETY_WIDTH
            self.commands.append(
                StraightCommand(settings.OBSTACLE_SAFETY_WIDTH).apply_on_pos(curr_pos)
            )
            print(offset_pos.x)
            offset_pos.x = offset_pos.x - settings.ROBOT_TURN_RADIUS + settings.OBSTACLE_SAFETY_WIDTH
            offset_pos.y += settings.ROBOT_TURN_RADIUS
            print(offset_pos.x)

            # If the next obstacle is not on top of current obstacle
            if offset_pos.x <= -settings.OBSTACLE_SAFETY_WIDTH:
                # Move straight until there is ROBOT_TURN_RADIUS to turn forward left.
                dist = -settings.ROBOT_TURN_RADIUS - offset_pos.x
                self.commands.append(
                    StraightCommand(dist).apply_on_pos(curr_pos)
                )
                # Do a forward turn to the right
                self.commands.append(
                    TurnCommand(-math.pi / 2, False).apply_on_pos(curr_pos)
                )
                offset_pos.y -= settings.ROBOT_TURN_RADIUS

                # Move forward remaining y-offset.
                self.commands.append(
                    StraightCommand(offset_pos.y).apply_on_pos(curr_pos)
                )

                # End.
                self.extend_then_clear_commands(self.brain.commands)
                return
            # We need to navigate around the obstacle.
            # Do a forward turn to the right.
            self.commands.append(
                TurnCommand(-math.pi / 2, False).apply_on_pos(curr_pos)
            )
            # Move forward 2 * OBSTACLE_SAFETY_WIDTH to clear the current obstacle
            self.commands.append(
                StraightCommand(2 * settings.OBSTACLE_SAFETY_WIDTH).apply_on_pos(curr_pos)
            )

            # Recursively search for the path.
            self.extend_then_clear_commands(self.brain.commands)
            self.brain.plan_curr_to_target(curr_pos, target_pos, True)
            return
        # There is no obstacle in front of the robot.
        # Move forward until y-offset is 0
        self.commands.append(
            StraightCommand(offset_pos.y).apply_on_pos(curr_pos)
        )
        # Do a reverse turn to face east.
        self.commands.append(
            TurnCommand(-math.pi / 2, True).apply_on_pos(curr_pos)
        )
        offset_pos.x += settings.ROBOT_TURN_RADIUS
        offset_pos.y = settings.ROBOT_TURN_RADIUS

        # Move straight until we have ROBOT_TURN_RADIUS to do a forward turn to the left.
        dist = offset_pos.x - settings.ROBOT_TURN_RADIUS
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

    def north_image(self, curr_pos, target_pos, is_start):
        pass

    def east_image(self, curr_pos, target_pos, is_start):
        pass

    def west_image(self, curr_pos, target_pos, is_start):
        pass
