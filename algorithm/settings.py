# PyGame settings
SCALING_FACTOR = 4
FRAMES = 60
WINDOW_SIZE = 800, 800

# Connection to RPi
HOST: str = "192.168.8.8"
PORT: int = 0
MUST_CONNECT = False

# Robot Attributes
ROBOT_LENGTH = 20 * SCALING_FACTOR
ROBOT_TURN_RADIUS = 30 * SCALING_FACTOR
ROBOT_SPEED_PER_SECOND = 100 * SCALING_FACTOR
ROBOT_S_FACTOR = ROBOT_LENGTH / ROBOT_TURN_RADIUS  # Please read briefing notes from Imperial
ROBOT_SAFETY_DISTANCE = 15 * SCALING_FACTOR

# Grid Attributes
GRID_LENGTH = 200 * SCALING_FACTOR
GRID_CELL_LENGTH = 10 * SCALING_FACTOR
GRID_START_BOX_LENGTH = 30 * SCALING_FACTOR
GRID_NUM_GRIDS = GRID_LENGTH // GRID_CELL_LENGTH

# Obstacle Attributes
OBSTACLE_LENGTH = 10 * SCALING_FACTOR
OBSTACLE_SAFETY_WIDTH = ROBOT_SAFETY_DISTANCE // 3 * 4  # With respect to the center of the obstacle

# Path Finding Attributes
PATH_TURN_COST = 10 * ROBOT_TURN_RADIUS
# NOTE: Higher number == Lower Granularity == Faster Checking.
# Must be an integer more than 0! Number higher than 3 not recommended.
PATH_TURN_CHECK_GRANULARITY = 3
