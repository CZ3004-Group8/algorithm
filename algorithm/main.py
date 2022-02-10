from algorithm.app import AlgoSimulator
from algorithm.entities.assets.direction import Direction
from algorithm.entities.grid.obstacle import Obstacle

if __name__ == '__main__':
    # Fill in obstacle positions with respect to lower bottom left corner.
    # (x-coordinate, y-coordinate, Direction)
    obs = [
        Obstacle(55, 85, Direction.RIGHT),
        Obstacle(105, 35, Direction.TOP),
        Obstacle(135, 105, Direction.RIGHT),
        Obstacle(185, 185, Direction.LEFT),
        Obstacle(65, 175, Direction.LEFT),
    ]

    app = AlgoSimulator(obs)
    app.execute()
