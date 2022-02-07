from algorithm.app import AlgoApp
from algorithm.entities.assets.direction import Direction
from algorithm.entities.grid.obstacle import Obstacle

if __name__ == '__main__':
    # Fill in obstacle positions with respect to lower bottom left corner.
    # (x-coordinate, y-coordinate, Direction)
    obs = [
        Obstacle(30, 70, Direction.BOTTOM),
        Obstacle(30, 170, Direction.BOTTOM),
        Obstacle(100, 150, Direction.BOTTOM),
        Obstacle(150, 60, Direction.BOTTOM)
    ]

    app = AlgoApp(obs)
    app.execute()
