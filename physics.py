Y = 0
X = 1

def is_solid(char_no):
    if char_no == ord(" "):
        return False
    return True

class Physics(object):
    def __init__(self, obj, y, x):
        self.obj = obj
        self.position = [y, x]
        self.vector = [0, 0]
        self.above = self.obj.world.window.inch(self.position[Y]+2,
                                                self.position[X])

        # walking constants (absolute values).
        self.friction = 1
        self.max_walk = 5
        self.walk_accel = 2
        self.direction = 1

        # jumping constants (positive is down)
        self.gravity = 1
        self.max_fall = 3
        self.jump_accel = -2

    def walk(self, direction):
        self.direction = direction
        if self.walk_accel + (direction * self.vector[X]) <= self.max_walk:
            self.vector[X] += self.walk_accel * self.direction

    def jump(self):
        if not is_solid(self.above) or self.vector[Y] != 0:
            return
        self.vector[Y] += self.jump_accel

    def update_debug(self):
        pos_y, pos_x = self.position
        vec_y, vec_x = self.vector
        self.above = self.obj.world.window.inch(self.position[Y]+2,
                                                self.position[X])
        status = ("Position ({:2}, {:2}) / Vector ({:2}, {:2}) / Over ({})")
        status = status.format(pos_y, pos_x, vec_y, vec_x, self.above)
        self.obj.world.set_status(status)

    def tick(self):
        new_y = self.vector[Y]
        new_x = self.vector[X]

        if is_solid(self.above):
            if self.vector[X]:
                # if walking, apply friction
                new_x -= self.friction * self.direction
        else:
            # if jumping or falling, apply gravity
            new_y += self.gravity

        self.vector[Y] = min(new_y, self.max_fall)
        self.vector[X] = new_x

        # move to new position
        self.position[X] += self.vector[X]
        self.position[Y] += self.vector[Y]
        self.obj.panel.move(*self.position)

        self.update_debug()
