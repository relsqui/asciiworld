import curses

Y = 0
X = 1

TRAVERSIBLES = map(ord, " .:")

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
        self.obj = obj
        self.position = [y, x]
        self.vector = [0, 0]
        self.below = self.obj.world.window.inch(self.position[Y]+2,
                                                self.position[X])

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
            self.obj.world.set_status("Marking {}, {}".format(y, x))
            self.obj.world.window.addch(y, x, ".")
        except curses.error:
            self.obj.world.set_status("Can't mark {}, {} (out of bounds)".format(y, x))

    def sweep_collision(self):
        """
        Sweep the area that will be covered by the next tick's worth of
        movement along the object vector, check for colliding objects and
        update our position and vector either to the target position or
        reflecting what we bounced off of.

        In testing, don't actually change anything, just mark the places
        that were checked.
        """
        target_pos = list(self.position)
        target_pos[Y] += self.vector[Y]
        target_pos[X] += self.vector[X]
        if not self.vector[X]:
            x = self.position[X]
            for y in range(self.position[Y], target_pos[Y]):
                self.mark(y, x)
        elif not self.vector[Y]:
            y = self.position[Y]
            for x in range(self.position[X], target_pos[X]):
                self.mark(y, x)
        else:
            slope_unit = float(self.vector[X])/float(self.vector[Y])
            slope = slope_unit
            for x in range(self.position[X], target_pos[X]):
                y = int(self.position[Y] + slope)
                self.mark(y, x)
                slope += slope_unit
        self.mark(*target_pos)

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
        if self.below in TRAVERSIBLES or self.vector[Y] != 0:
            return
        self.vector[Y] += self.jump_accel

    def update_debug(self):
        """
        Put handy debugging information in the status bar.
        "Over" means "the number of the character the player is standing on."
        """
        pos_y, pos_x = self.position
        vec_y, vec_x = self.vector
        status = ("Position ({:2}, {:2}) / Vector ({:2}, {:2}) / Over ({})")
        status = status.format(pos_y, pos_x, vec_y, vec_x, self.below)
        self.obj.world.set_status(status)

    def tick(self):
        """
        Execute one cycle of updates: apply any relevant physical constants,
        update vector and position, and update the debugging output.
        This doesn't actually update the screen; the game loop handles that.
        """
        new_y_vec = self.vector[Y]
        new_x_vec = self.vector[X]

        if self.below not in TRAVERSIBLES:
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
        self.below = self.obj.world.window.inch(self.position[Y]+2,
                                                self.position[X])
        self.update_debug()
