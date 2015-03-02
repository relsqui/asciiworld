import curses

class Player(object):
    def __init__(self, world, y=None, x=None):
        self.world = world
        if y is None:
            self.y = world.ground_level - 2
        if x is None:
            self.x = int(curses.COLS/2)
        self.window = curses.newwin(2, 2, self.y, self.x)
        self.window.addstr(0, 0, "p")
        self.window.addstr(1, 0, "|")
        self.facing = 1
        self.panel = curses.panel.new_panel(self.window)

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

    def move(self, d_y, d_x):
        if self.face(d_x/abs(d_x)):
            # if we changed direction, that takes up the move
            return
        self.y = min(max(self.y + d_y, 0), curses.LINES-1)
        self.x = min(max(self.x + d_x, 0), curses.COLS-2)
        self.panel.move(self.y, self.x)


