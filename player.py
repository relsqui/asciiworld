import curses
import physics

class Player(object):
    def __init__(self, world, y=None, x=None):
        self.world = world
        if y is None:
            y = world.ground_level - 2
        if x is None:
            x = int(curses.COLS/2)
        self.window = curses.newwin(2, 2, y, x)
        self.window.addstr(0, 0, "p")
        self.window.addstr(1, 0, "|")
        self.facing = 1
        self.panel = curses.panel.new_panel(self.window)
        self.physics = physics.Physics(self, y, x)

    def tick(self):
        self.physics.tick()

    def face(self, direction):
        """
        Turn the sprite to face left (-1) or right (1). Returns True if
        this changes the direction or False if it does not.
        """
        heads = ["", "p", "q"]
        if direction != self.facing:
            self.window.addstr(0, 0, heads[direction])
            self.facing = direction
            return True
        return False

    def walk(self, direction):
        if self.face(direction):
            # if we changed direction, that takes up the move
            return
        self.physics.walk(direction)
