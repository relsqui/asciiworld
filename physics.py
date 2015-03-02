Y = 0
X = 1

class Physics(object):
    def __init__(self, obj, y, x):
        self.obj = obj
        self.friction = 1
        self.max_walk = 5
        self.walk_accel = 2
        self.direction = 1
        self.position = [y, x]
        self.vector = [0, 0]

    def walk(self, direction):
        self.direction = direction
        if self.walk_accel + (direction * self.vector[X]) <= self.max_walk:
            self.vector[X] += self.walk_accel * self.direction

    def tick(self):
        if self.vector[X]:
            self.vector[X] -= self.friction * self.direction
        self.position[X] += self.vector[X]
        self.obj.panel.move(*self.position)
        pos_y, pos_x = self.position
        vec_y, vec_x = self.vector
        ovr = chr(self.obj.world.window.inch(self.position[Y]+1, self.position[X]))
        self.obj.world.set_status("Position ({:2}, {:2}) / Vector ({:2}, {:2}) / Over ({})".format(pos_y, pos_x, vec_y, vec_x, ovr))
