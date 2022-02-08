from algorithm.app import AlgoApp
from algorithm.entities.assets.direction import Direction
from algorithm.entities.grid.obstacle import Obstacle

if __name__ == '__main__':
    # Fill in obstacle positions with respect to lower bottom left corner.
    # (x-coordinate, y-coordinate, Direction)
    obs = [
        Obstacle(150, 150, Direction.RIGHT),
        Obstacle(0, 145, Direction.RIGHT),
        Obstacle(30, 20, Direction.RIGHT)
    ]

    app = AlgoApp(obs)
    app.execute()
