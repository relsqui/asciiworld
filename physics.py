import curses

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
        self.below = self.obj.world.window.inch(self.position[Y]+2,
                                                self.position[X])

        # walking constants (absolute values).
        self.friction = 1
        self.max_walk = 5
        self.walk_accel = 2
        self.direction = 1

        # jumping constants (positive is down)
        self.gravity = 1
        self.max_fall = 3
        self.jump_accel = -3

    def walk(self, direction):
        self.direction = direction
        if self.walk_accel + (direction * self.vector[X]) <= self.max_walk:
            self.vector[X] += self.walk_accel * self.direction

    def jump(self):
        if not is_solid(self.below) or self.vector[Y] != 0:
            return
        self.vector[Y] += self.jump_accel

    def update_debug(self):
        pos_y, pos_x = self.position
        vec_y, vec_x = self.vector
        self.below = self.obj.world.window.inch(self.position[Y]+2,
                                                self.position[X])
        status = ("Position ({:2}, {:2}) / Vector ({:2}, {:2}) / Over ({})")
        status = status.format(pos_y, pos_x, vec_y, vec_x, self.below)
        self.obj.world.set_status(status)

    def tick(self):
        new_y_vec = self.vector[Y]
        new_x_vec = self.vector[X]

        if is_solid(self.below):
            if self.vector[X]:
                # if walking, apply friction
                new_x_vec -= self.friction * self.direction
            if self.vector[Y] > 0:
                # we were falling but we hit something
                new_y_vec = 0
        else:
            # if jumping or falling, apply gravity
            new_y_vec += self.gravity

        self.vector[Y] = min(new_y_vec, self.max_fall)
        self.vector[X] = new_x_vec

        # move to new position and constrain to bounding box
        self.position[Y] += self.vector[Y]
        self.position[X] += self.vector[X]
        # we don't need to check the high (bottom) bound for Y, because
        # we already did when we were choosing whether to apply gravity
        self.position[Y] = max(self.position[Y], 1)
        self.position[X] = max(min(self.position[X], curses.COLS-2), 1)
        self.obj.panel.move(*self.position)

        self.update_debug()
