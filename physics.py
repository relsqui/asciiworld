Y = 0
X = 1

class Physics(object):
    def __init__(self, obj, y, x):
        self.obj = obj
        self.friction = 1
        self.speed = 2
        self.direction = 1
        self.position = [y, x]
        self.vector = [0, 0]

    def walk(self, direction):
        self.direction = direction
        if not self.vector[X]:
            self.vector[X] = self.speed * self.direction

    def tick(self):
        if self.vector[X]:
            self.vector[X] -= self.friction * self.direction
        self.position[X] += self.vector[X]
        self.obj.panel.move(*self.position)
