import math
import pygame

from algorithm.entities.robot.brain import Brain
from algorithm.entities.position import Position
from algorithm.entities.assets import colors
from algorithm.settings import SCALING_FACTOR


class Robot:
    ROBOT_LENGTH = 21 * SCALING_FACTOR  # Front to back
    ROBOT_WIDTH = 20 * SCALING_FACTOR  # Left to right
    TURNING_RADIUS = 25 * SCALING_FACTOR  # Turning radius of the robot in centimeters. Theoretical value is 25.

    SPEED_PER_SECOND = 20 * SCALING_FACTOR  # Speed of the robot
    S = ROBOT_LENGTH / TURNING_RADIUS  # Used for calculating dt for angle change.

    def __init__(self, x, y, angle, grid):
        """
        We take the robot as a point in the center.
        """
        self.pos = Position(x, y, angle)
        self.brain = Brain(self, grid)

        self.image = pygame.transform.scale(pygame.image.load("entities/assets/left-arrow.png"),
                                            (self.ROBOT_LENGTH / 2, self.ROBOT_LENGTH / 2))
        self.rot_image = self.image  # Store rotated image

        self.path_hist = []

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
        # Get change in (x, y) coordinate.
        x_change = self.TURNING_RADIUS * (math.sin(self.pos.angle + d_angle) - math.sin(self.pos.angle))
        y_change = self.TURNING_RADIUS * (math.cos(self.pos.angle + d_angle) - math.cos(self.pos.angle))

        if d_angle < 0 and not rev:  # Wheels to right moving forward.
            self.pos.x -= x_change
            self.pos.y -= y_change
        elif (d_angle < 0 and rev) or \
                (d_angle >= 0 and not rev):  # (Wheels to left moving backwards) or (Wheels to left moving forwards).
            self.pos.x += x_change
            self.pos.y += y_change
        else:  # Wheels to right moving backwards.
            self.pos.x -= x_change
            self.pos.y -= y_change
        self.pos.angle += d_angle

        if self.pos.angle <= -math.pi:
            self.pos.angle += 2 * math.pi
        elif self.pos.angle >= math.pi:
            self.pos.angle -= 2 * math.pi

    def turn_left(self, rev):
        self.turn(-math.pi / 2, rev)

    def turn_right(self, rev):
        self.turn(math.pi / 2, rev)

    def straight(self, dt, rev):
        # Get straight distance travelled within this time.
        distance = dt * self.SPEED_PER_SECOND
        
        if self.pos.angle == 0:
            self.pos.x += distance if not rev else -distance
        elif self.pos.angle == math.pi / 2:
            self.pos.y -= distance if not rev else -distance
        elif self.pos.angle == -math.pi / 2:
            self.pos.y += distance if not rev else -distance
        else:
            self.pos.x -= distance if not rev else -distance

    def draw_simple_hamiltonian_path(self, screen):
        prev = self.brain.grid.get_start_box_rect().center
        for obs in self.brain.simple_hamiltonian:
            target = obs.get_robot_target_pos()
            pygame.draw.line(screen, colors.DARK_GREEN,
                             prev, target.xy())
            prev = target.xy()

    def draw_self(self, screen):
        # The red background
        pygame.draw.circle(screen, colors.RED, self.pos.xy(), self.ROBOT_WIDTH / 2)

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
        self.path_hist.append(self.pos.xy())

        # Draw the robot itself.
        self.draw_self(screen)
