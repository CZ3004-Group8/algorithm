class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_tuple(self):
        return self.x, self.y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    __repr__ = __str__
