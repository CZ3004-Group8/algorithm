import itertools

from algorithm.entities.point import Point
from algorithm.entities import colors
from algorithm.settings import SCALING_FACTOR

import math
import pygame


class Robot:
    ROBOT_LENGTH = 21 * SCALING_FACTOR  # Front to back
    ROBOT_WIDTH = 20 * SCALING_FACTOR  # Left to right
    TURNING_RADIUS = 25 * SCALING_FACTOR  # Turning radius of the robot in centimeters. Theoretical value is 25.

    SPEED_PER_SECOND = 5 * SCALING_FACTOR  # Speed of the robot

    def __init__(self, x, y, angle, grid):
        """
        We take the robot as a point in the center.
        """
        self.center = Point(x, y)
        self.angle = angle

        self.grid = grid

        self.color = colors.RED
        self.image = pygame.transform.scale(pygame.image.load("entities/assets/left-arrow.png"),
                                            (self.ROBOT_LENGTH / 2, self.ROBOT_LENGTH / 2))
        self.rot_image = self.image  # Store rotated image

        # Used for storing the pre-calculated simple hamiltonian path between targets.
        self.simple_hamiltonian_path = []

        # Stores the specific movements that the robot will make
        self.movements = []

    def compute_simple_hamiltonian_path(self):
        """
        Get the Hamiltonian Path to all points with the best possible effort.

        This is a simple calculation where we assume that we travel directly to the next obstacle.
        """
        # Generate all possible permutations for the image obstacles
        perms = list(itertools.permutations(self.grid.obstacles))

        # Get the path that has the least distance travelled.
        def calc_distance(path):
            # Create all target points, including the start.
            targets = [self.grid.get_start_box_rect().center]
            for obs in path:
                target, _ = obs.get_robot_target()
                targets.append(target.as_tuple())

            dist = 0
            for i in range(len(targets) - 1):
                dist += math.sqrt(((targets[i][0] - targets[i + 1][0]) ** 2) +
                                  ((targets[i][1] - targets[i + 1][1]) ** 2))
            return dist

        self.simple_hamiltonian_path = min(perms, key=calc_distance)
        print(f"Simple Hamiltonian Path: {self.simple_hamiltonian_path}")

    def plan_movement(self):
        """
        Plan how to move to next destination based on current location.
        """
        # Create a new Robot to plan the route.
        # We use this robot to track the movement of the robot for any step we take.
        sim = Robot(self.center.x, self.center.y, math.pi / 2, self.grid)

        # We try to visit all points.
        self.movements = []
        index = 0
        while index < len(self.simple_hamiltonian_path):
            # Obstacle
            obstacle = self.simple_hamiltonian_path[index]
            # Current target
            target, orient = obstacle.get_robot_target()

            # Calculate the difference in the points
            x_diff, y_diff = target.x - sim.center.x, sim.center.y - target.y
            print(x_diff, y_diff)
            if x_diff >= 0 and y_diff >= 0:
                print("Next point in 1st quadrant.")
            elif x_diff >= 0 and y_diff < 0:
                print("Next point in 4th quadrant.")
            elif x_diff < 0 and y_diff >= 0:
                print("Next point in 2nd quadrant.")
            else:
                print("Next point in 3rd quadrant.")

            # Find the difference in angle required.
            angle_diff = math.degrees(math.atan2(y_diff, x_diff))
            print(f"Angle from x-axis: {angle_diff}")
            print("-" * 10)
            sim.center = Point(target.x, target.y)
            index += 1

    def turn(self, d_angle, to_left):
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
        x_change = self.TURNING_RADIUS * (math.sin(self.angle + d_angle) - math.sin(self.angle))
        y_change = self.TURNING_RADIUS * (math.cos(self.angle + d_angle) - math.cos(self.angle))

        if to_left:  # Robot wants to turn left.
            self.center.x += x_change
            self.center.y += y_change
        else:  # Robot wants to turn right.
            self.center.x -= x_change
            self.center.y += y_change
        self.angle += d_angle

        self.rot_image = pygame.transform.rotate(self.image,
                                                 math.degrees(-self.angle + math.pi / 2) * (-1 if to_left else 1))

    def draw_shortest_path(self, screen):
        prev = self.grid.get_start_box_rect().center
        for obs in self.simple_hamiltonian_path:
            target, _ = obs.get_robot_target()
            pygame.draw.line(screen, colors.DARK_GREEN,
                             prev, target.as_tuple())
            prev = target.as_tuple()

    def draw_self(self, screen):
        # The red background
        pygame.draw.circle(screen, colors.RED, self.center.as_tuple(), self.ROBOT_WIDTH / 2)

        # The arrow to represent the direction of the robot.
        rect = self.rot_image.get_rect()
        rect.center = self.center.as_tuple()
        screen.blit(self.rot_image, rect)

    def draw(self, screen):
        # Draw the simple hamiltonian path found by the robot.
        self.draw_shortest_path(screen)

        # Draw the robot itself.
        self.draw_self(screen)
