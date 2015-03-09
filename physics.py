import curses

Y = 0
X = 1

TRAVERSIBLES = map(ord, " .:")
world = None # this will be initialized when Physics is instantiated

def is_solid(y, x):
    if world.window.inch(y, x) in TRAVERSIBLES:
        return False
    return True

class Physics(object):
    """
    Attributes and methods which are relevant to the physics of a game entity.
    In theory this is as separate from the rest of the qualities of that
    entity as possible. In practice, it's not yet. Still prototyping.
    """

    def __init__(self, obj, y, x):
        """
        Initialize physical constants etc.
        """
        global world

        self.obj = obj
        world = self.obj.world
        self.position = [y, x]
        self.vector = [0, 0]
        self.below = [self.position[Y]+2, self.position[X]]

        # walking constants (absolute values)
        self.friction = 1
        self.max_walk = 5
        self.walk_accel = 2
        self.direction = 1

        # jumping constants (positive is down)
        self.gravity = 1
        self.max_fall = 3
        self.jump_accel = -3

    def mark(self, y, x):
        """
        Put a traversible dot on the map at the specified point.
        (For debugging purposes.)
        """
        try:
            world.window.addch(y, x, ".")
        except curses.error:
            # out of bounds
            pass

    def sweep_collision(self):
        """
        Sweep the area that will be covered by the next tick's worth of
        movement along the object vector, check for colliding objects and
        update our position and vector either to the target position or
        reflecting what we bounced off of.

        In testing, don't actually change anything, just mark the places
        that were checked.
        """
        target_pos = [0, 0]
        step = [0, 0]
        for i in [Y, X]:
            target_pos[i] = self.position[i] + self.vector[i]
            step[i] = 1 if self.position[i] < target_pos[i] else -1
        if self.vector == [0, 0]:
            pass
        elif not self.vector[X]:
            x = self.position[X]
            for y in range(self.position[Y], target_pos[Y], step[Y]):
                self.mark(y, x)
                self.mark(y+1, x)
        elif not self.vector[Y]:
            y = self.position[Y]
            for x in range(self.position[X], target_pos[X], step[X]):
                self.mark(y, x)
                self.mark(y+1, x)
        else:
            y_inc = float(self.vector[Y])/abs(float(self.vector[X]))
            y_offset = y_inc
            for x in range(self.position[X], target_pos[X], step[X]):
                y = int(self.position[Y] + y_offset)
                self.mark(y, x)
                self.mark(y+1, x)
                y_offset += y_inc

    def walk(self, direction):
        """
        Increase horizontal velocity by the walk acceleration in the specified
        direction (-1 is left, 1 is right). Notably this does *not* check
        the facing direction; that's a sprite matter, and it's in the player
        object.
        """
        self.direction = direction
        if self.walk_accel + (direction * self.vector[X]) <= self.max_walk:
            self.vector[X] += self.walk_accel * self.direction

    def jump(self):
        """
        Increase vertical velocity by the jump acceleration. Unlike the above,
        this *does* check whether the surface the entity is on is jumpable
        (no double-jumping).
        """
        if self.vector[Y] != 0 or not is_solid(*self.below):
            return
        self.vector[Y] += self.jump_accel

    def update_debug(self):
        """
        Put handy debugging information in the status bar.
        "Over" means "the number of the character the player is standing on."
        """
        status = ("Position {} / Vector {} / Below {}")
        status = status.format(self.position, self.vector, self.below)
        world.set_status(status)

    def tick(self):
        """
        Execute one cycle of updates: apply any relevant physical constants,
        update vector and position, and update the debugging output.
        This doesn't actually update the screen; the game loop handles that.
        """
        new_y_vec = self.vector[Y]
        new_x_vec = self.vector[X]

        if is_solid(*self.below):
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

        self.sweep_collision()
        # move to new position and constrain to bounding box
        self.position[Y] += self.vector[Y]
        self.position[X] += self.vector[X]
        # this is a hack until we have proper collision detection
        self.position[Y] = max(min(self.position[Y], curses.LINES-5), 1)
        self.position[X] = max(min(self.position[X], curses.COLS-2), 1)
        self.obj.panel.move(*self.position)
        self.below = [self.position[Y]+2, self.position[X]]
        self.update_debug()
