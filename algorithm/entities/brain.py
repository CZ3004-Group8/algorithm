import itertools
import math


class Brain:
    def __init__(self, robot, grid):
        self.robot = robot
        self.grid = grid

        self.simple_hamiltonian = []

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

        self.simple_hamiltonian = min(perms, key=calc_distance)
        print(f"Simple Hamiltonian Path: {self.simple_hamiltonian}")

    def plan_next_move(self):
        """
        Plan the next movements to get to the next target.
        """

    def plan_movement(self):
        """
        Plan how to move to next destination based on current location.
        """
        # Create a new Robot to plan the route.
        # We use this robot to track the movement of the robot for any step we take.
        sim = Robot(self.center.x, self.center.y, math.pi / 2, self.grid)

        # We try to visit all points.
        self.commands = []
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
            final_angle = math.atan2(y_diff, x_diff)
            print(f"Angle from x-axis: {math.degrees(final_angle)}")
            to_turn = final_angle - sim.angle
            print(f"Angle to turn: {math.degrees(to_turn)}")

            # Get the time required for turning
            # ∆θ = (v∆tsins)/L
            # ∆t = ∆θL/vsins
            dt = abs((to_turn * self.ROBOT_LENGTH) / (self.SPEED_PER_SECOND * self.S))
            print(f"Time for change: {dt}s")
            self.commands.append(TurnCommand(to_turn, dt, False))

            print("-" * 10)
            sim.center = Point(target.x, target.y)
            sim.angle = final_angle
            index += 1