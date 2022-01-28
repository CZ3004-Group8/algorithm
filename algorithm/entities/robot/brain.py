import itertools
import math

from algorithm.entities.assets.direction import Direction


class Brain:
    def __init__(self, robot, grid):
        self.robot = robot
        self.grid = grid

        # Compute the simple Hamiltonian path for all obstacles
        self.simple_hamiltonian = tuple()
        self.compute_simple_hamiltonian_path()

        # Create all the commands required to finish the course.
        self.commands = []
        self.plan_path()

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
            for ob in path:
                target, _ = ob.get_robot_target()
                targets.append(target.as_tuple())

            dist = 0
            for i in range(len(targets) - 1):
                dist += math.sqrt(((targets[i][0] - targets[i + 1][0]) ** 2) +
                                  ((targets[i][1] - targets[i + 1][1]) ** 2))
            return dist

        self.simple_hamiltonian = min(perms, key=calc_distance)
        print(f"Simple Hamiltonian Path:")
        for obs in self.simple_hamiltonian:
            print(f"\t{obs}")

    def calculate_angle_difference(self, center1, center2):
        """
        Calculate the angle of center2 from center1
        """
        x_diff, y_diff = center2.x - center1.x, center1.y - center2.y
        quad = None
        if x_diff >= 0 and y_diff >= 0:
            quad = 1
            print("Next point in 1st quadrant.")
        elif x_diff >= 0 and y_diff < 0:
            quad = 2
            print("Next point in 4th quadrant.")
        elif x_diff < 0 and y_diff >= 0:
            quad = 3
            print("Next point in 2nd quadrant.")
        else:
            quad = 4
            print("Next point in 3rd quadrant.")

        # Angle difference
        angle_diff = math.atan2(y_diff, x_diff)
        print(f"Angle of next point wrt current point: {math.degrees(angle_diff)}")
        print(f"Robot needs to turn: {math.degrees(angle_diff - self.robot.angle)}")
        return angle_diff, quad

    def plan_start(self):
        print("Planning from starting point to next obstacle.")
        # Get the starting turning circle from the grid.
        start_circle = self.grid.start_turning_circle
        # Get the next image obstacle to travel to.
        next_obs = self.simple_hamiltonian[0]

        # Find the angle between current location and next obstacle.
        # Find the robot target for the obstacle
        target, orient = next_obs.get_robot_target()
        angle, quadrant = self.calculate_angle_difference(self.robot.center, target)
        assert quadrant != 3  # The obstacle can never be located in the third quadrant from the start position.

        # Depending on the angle, and orientation, we decide which turning circle to travel to.
        target_circle = None
        if quadrant == 1:
            # Note that orient is the angle that the ROBOT needs to target, and NOT the orientation of
            # the obstacle.
            if orient == Direction.NORTH:
                print("Robot targeting NORTH")
                target_circle = next_obs.turning_circles[0]
            elif orient == Direction.SOUTH:
                print("Robot targeting SOUTH")
                target_circle = next_obs.turning_circles[0]
            elif orient == Direction.EAST:
                print("Robot targeting EAST")
                target_circle = next_obs.turning_circles[1]
            else:
                print("Robot targeting WEST")
                target_circle = next_obs.turning_circles[1]

        # Calculate all tangents from source and then from target
        source_points = start_circle.find_tangents(target_circle)
        target_points = target_circle.find_tangents(start_circle)

        # TODO: How to find corresponding tangent?
        for source_point in source_points:
            for target_point in target_points:
                print(f"Checking {source_point} with {target_point}")
                if start_circle.check_corresponding_tangent(source_point, target_circle, target_point):
                    self.commands.append((source_point, target_point))

    def plan_rest(self):
        pass

    def plan_path(self):
        """
        Plan the next movements to get to the next target.
        """
        # Plan from start to next obstacle.
        self.plan_start()

        self.plan_rest()
