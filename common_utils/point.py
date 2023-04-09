class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if other.x == self.x and other.y == self.y:
            return True
        return False

    def __str__(self):
        return "x=" + str(self.x) + ",y=" + str(self.y)

    def __hash__(self):
        return hash(str(self))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def norm(self):
        return abs(self.x) + abs(self.y)

    def dist_to(self, point2):
        dx = abs(self.x - point2.x)
        dy = abs(self.y - point2.y)
        return dx + dy


