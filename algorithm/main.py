from algorithm.app import AlgoApp
from algorithm.entities.assets.direction import Direction
from algorithm.entities.grid.obstacle import Obstacle

if __name__ == '__main__':
    # Fill in obstacle positions with respect to lower bottom left corner.
    # (x-coordinate, y-coordinate, Direction)
    obs = [
        Obstacle(155, 155, Direction.BOTTOM),
        Obstacle(55, 55, Direction.RIGHT),
        Obstacle(55, 155, Direction.LEFT),
        Obstacle(155, 55, Direction.TOP)
    ]

    app = AlgoApp(obs)
    app.execute()
