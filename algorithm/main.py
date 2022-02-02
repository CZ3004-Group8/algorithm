import math

from algorithm.app import AlgoApp
from algorithm.entities.grid.obstacle import Obstacle


if __name__ == '__main__':
    # Fill in obstacle positions with respect to lower bottom left corner.
    # (x-coordinate, y-coordinate, Direction)
    obs = [
        Obstacle(115, 45, math.pi),
        Obstacle(25, 95, -math.pi / 2),
        Obstacle(35, 175, -math.pi / 2),
        Obstacle(155, 165, math.pi),
        Obstacle(175, 85, math.pi),
    ]

    app = AlgoApp(obs)
    app.execute()
