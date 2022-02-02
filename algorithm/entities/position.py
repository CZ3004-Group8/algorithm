class Position:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def xy(self):
        return self.x, self.y

    def __str__(self):
        return f"Point({self.x}, {self.y}, angle={self.angle:.2f})"

    __repr__ = __str__
