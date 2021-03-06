import curses
import physics

class Player(object):
    def __init__(self, world, y=None, x=None):
        """
        Initialize position, sprite, and physics.
        This hardcodes some stuff that won't be later, just for prototyping.
        """
        self.world = world
        if y is None:
            y = int(curses.LINES/2)
        if x is None:
            x = int(curses.COLS/2)
        self.window = curses.newwin(2, 1, y, x)
        self.window.addch(0, 0, ord("p"))
        self.window.insch(1, 0, ord("|"))
        self.facing = 1
        self.panel = curses.panel.new_panel(self.window)
        self.physics = physics.Physics(self, y, x)
        self.above = None

    def tick(self):
        """
        Execute an update cycle. Currently just passes through to physics,
        but could also be used for walk animations and so forth.
        """
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
        """
        Execute a walk command from the (human) player.
        """
        if self.face(direction):
            # if we changed direction, that takes up the move
            return
        self.physics.walk(direction)

    def jump(self):
        """
        Execute a walk command from the (human) player.
        """
        self.physics.jump()
