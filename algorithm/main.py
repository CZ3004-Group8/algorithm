from algorithm.app import AlgoApp
from algorithm.entities.assets.direction import Direction
from algorithm.entities.grid.obstacle import Obstacle

if __name__ == '__main__':
    # Fill in obstacle positions with respect to lower bottom left corner.
    # (x-coordinate, y-coordinate, Direction)
    obs = [
        Obstacle(115, 45, Direction.LEFT),
        Obstacle(25, 95, Direction.BOTTOM),
        Obstacle(35, 175, Direction.BOTTOM),
        Obstacle(155, 165, Direction.LEFT),
        Obstacle(175, 85, Direction.LEFT),
    ]

    app = AlgoApp(obs)
    app.execute()
