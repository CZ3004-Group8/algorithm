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
            # If the next obstacle is almost directly on top of current obstacle.
            if offset_pos.x > -settings.OBSTACLE_SAFETY_WIDTH:
                # Do a reverse turn to face west.
                self.commands.append(
                    TurnCommand(math.pi / 2, True).apply_on_pos(curr_pos)
                )
                # Move forward OBSTACLE_SAFETY_WIDTH
                self.commands.append(
                    StraightCommand(settings.OBSTACLE_SAFETY_WIDTH).apply_on_pos(curr_pos)
                )

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
            else:
                # We move backwards ROBOT_TURN_RADIUS.
                self.commands.append(
                    StraightCommand(-settings.ROBOT_TURN_RADIUS).apply_on_pos(curr_pos)
                )
                offset_pos.y += settings.ROBOT_TURN_RADIUS
        elif offset_pos.y < settings.ROBOT_TURN_RADIUS:
            # There is no obstacle in front of the robot, and current y-offset is not enough for
            # ROBOT_TURN_RADIUS.
            # We move back just enough to allow ROBOT_TURN_RADIUS.
            dist = offset_pos.y - settings.ROBOT_TURN_RADIUS
            self.commands.append(
                StraightCommand(dist).apply_on_pos(curr_pos)
            )
            offset_pos.y = settings.ROBOT_TURN_RADIUS

        # We do a forward turn to the left.
        self.commands.append(
            TurnCommand(math.pi / 2, False).apply_on_pos(curr_pos)
        )
        offset_pos.x += settings.ROBOT_TURN_RADIUS
        offset_pos.y -= settings.ROBOT_TURN_RADIUS

        # If there is enough y-offset such that we can do a direct forward turn to the right,
        # we do so. However, we only do this if the x-offset is enough to not have to travel
        # backwards.
        if offset_pos.y >= settings.ROBOT_TURN_RADIUS and offset_pos.x <= -settings.ROBOT_TURN_RADIUS:
            # We travel until we have ROBOT_TURN_RADIUS left.
            dist = -settings.ROBOT_TURN_RADIUS - offset_pos.x
            self.commands.append(
                StraightCommand(dist).apply_on_pos(curr_pos)
            )
            offset_pos.x = -settings.ROBOT_TURN_RADIUS

            # Do a forward turn to the right.
            self.commands.append(
                TurnCommand(-math.pi / 2, False).apply_on_pos(curr_pos)
            )
            offset_pos.y -= settings.ROBOT_TURN_RADIUS
        else:
            # We travel straight until we overshoot ROBOT_TURN_RADIUS
            dist = settings.ROBOT_TURN_RADIUS - offset_pos.x
            self.commands.append(
                StraightCommand(dist).apply_on_pos(curr_pos)
            )

            # We do a reverse turn to face north.
            self.commands.append(
                TurnCommand(-math.pi / 2, True).apply_on_pos(curr_pos)
            )
            offset_pos.y += settings.ROBOT_TURN_RADIUS
        # We travel remaining distance to target.
        self.commands.append(
            StraightCommand(offset_pos.y).apply_on_pos(curr_pos)
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
