import math

import pygame

from algorithm import settings
from algorithm.entities.assets import colors
from algorithm.entities.assets.direction import Direction
from algorithm.entities.commands.command import Command
from algorithm.entities.commands.straight_command import StraightCommand
from algorithm.entities.commands.turn_command import TurnCommand
from algorithm.entities.grid.position import Position
from algorithm.entities.robot.brain.brain import Brain


class Robot:
    def __init__(self, x, y, direction: Direction, grid):
        """
        We take the robot as a point in the center.

        Note that the specified x, y coordinates are PyGame coordinates.
        """
        self.pos = Position(x, y, direction)
        self.brain = Brain(self, grid)

        self.image = pygame.transform.scale(pygame.image.load("entities/assets/left-arrow.png"),
                                            (settings.ROBOT_LENGTH / 2, settings.ROBOT_LENGTH / 2))
        self.rot_image = self.image  # Store rotated image

        self.path_hist = []  # Stores the history of the path taken by the robot.

        self.current_command = 0  # Index of the current command being executed.

    def get_current_pos(self):
        return self.pos

    def turn(self, d_angle, rev):
        """
        Turns the robot by the specified angle, and whether to do it in reverse or not.
        Take note that the angle is in radians.

        A negative angle will always cause the robot to be rotated in a clockwise manner, regardless
        of the value of rev.

        x_new = x + R(sin(∆θ + θ) − sin θ)
        y_new = y − R(cos(∆θ + θ) − cos θ)
        θ_new = θ + ∆θ
        R is the turning radius.

        Take note that:
            - +ve ∆θ -> rotate counter-clockwise
            - -ve ∆θ -> rotate clockwise

        Note that ∆θ is in radians.
        """
        TurnCommand(d_angle, rev).apply_on_pos(self.pos)

    def straight(self, dist):
        """
        Make a robot go straight.

        A negative number indicates that the robot will move in reverse, and vice versa.
        """
        StraightCommand(dist).apply_on_pos(self.pos)

    def draw_simple_hamiltonian_path(self, screen):
        prev = self.brain.grid.get_start_box_rect().center
        for obs in self.brain.simple_hamiltonian:
            target = obs.get_robot_target_pos()
            pygame.draw.line(screen, colors.DARK_GREEN,
                             prev, target.xy())
            prev = target.xy()

    def draw_self(self, screen):
        # The red background
        pygame.draw.circle(screen, colors.RED, self.pos.xy(), settings.ROBOT_LENGTH / 2)

        # The arrow to represent the direction of the robot.
        rot_image = pygame.transform.rotate(self.image,
                                            -math.degrees(math.pi / 2 - self.pos.angle))
        rect = rot_image.get_rect()
        rect.center = self.pos.xy()
        screen.blit(rot_image, rect)

    def draw_historic_path(self, screen):
        for dot in self.path_hist:
            pygame.draw.circle(screen, colors.BLACK, dot, 3)

    def draw(self, screen):
        # Draw the simple hamiltonian path found by the robot.
        self.draw_simple_hamiltonian_path(screen)

        # Draw the path sketched by the robot
        self.draw_historic_path(screen)
        if len(self.path_hist) == 0 or self.pos.xy() != self.path_hist[-1]:
            # Only add a new point history if there is none, and it is different from previous history.
            self.path_hist.append(self.pos.xy())

        # Draw the robot itself.
        self.draw_self(screen)

    def update(self):
        # If no more commands to execute, then return.
        if len(self.brain.commands) == 0:
            return

        # If not, the first command in the list is always the command to execute.
        command: Command = self.brain.commands[0]
        command.process_one_tick(self)
        # If there are no more ticks to do, then we can assume that we have
        # successfully completed this command, and so we can remove it.
        # The next time this method is run, then we will process the next command in the list.
        if command.ticks <= 0:
            print(f"Finished processing {command}, {self.pos}")
            self.brain.commands.popleft()
