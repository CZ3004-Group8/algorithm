import math
import time

import pygame

from algorithm import settings
from algorithm.entities.commands.straight_command import StraightCommand
from algorithm.entities.commands.turn_command import TurnCommand
from algorithm.entities.robot.brain import Brain
from algorithm.entities.position import Position
from algorithm.entities.assets import colors


class Robot:
    S = settings.ROBOT_LENGTH / settings.ROBOT_TURN_RADIUS  # Used for calculating dt for angle change.

    def __init__(self, x, y, angle, grid):
        """
        We take the robot as a point in the center.
        """
        self.pos = Position(x, y, angle)
        self.brain = Brain(self, grid)

        self.image = pygame.transform.scale(pygame.image.load("entities/assets/left-arrow.png"),
                                            (settings.ROBOT_LENGTH / 2, settings.ROBOT_LENGTH / 2))
        self.rot_image = self.image  # Store rotated image

        self.path_hist = []

        self.current_command = 0  # Index of the current command being executed.
        self.command_started = time.time()  # Keep track of when last command was executed.

    def get_current_pos(self):
        return self.pos

    def turn(self, d_angle, rev):
        """
        x_new = x + R(sin(∆θ + θ) − sin θ)
        y_new = y − R(cos(∆θ + θ) − cos θ)
        θ_new = θ + ∆θ
        R is the turning radius.

        Take note that:
            - +ve ∆θ -> rotate counter-clockwise
            - -ve ∆θ -> rotate clockwise

        Note that ∆θ is in radians.
        """
        # Create a turn command.
        turn_command = TurnCommand(d_angle, rev)
        self.pos = turn_command.apply_on_pos(self.pos)

    def straight(self, dist):
        # Create the straight command
        straight_command = StraightCommand(dist)
        self.pos = straight_command.apply_on_pos(self.pos)

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
            self.path_hist.append(self.pos.xy())

        # Draw the robot itself.
        self.draw_self(screen)

    def update(self):
        # If no more commands to execute, then return.
        if self.current_command >= len(self.brain.commands):
            return

        command = self.brain.commands[self.current_command]
        # Check for elapsed time of this command.
        # If elapsed time is more than time needed for current command,
        # then we start executing the next command.
        if time.time() - self.command_started >= command.time:
            print(f"{command} finished.")
            print(self.pos)
            self.current_command += 1
            self.command_started = time.time()
            return

        # Check the command to execute.
        total_frames = settings.FRAMES * command.time
        if command.c == "turn":
            self.turn(command.angle / total_frames, command.rev)
        elif command.c == "straight":
            self.straight(command.dist / total_frames)
