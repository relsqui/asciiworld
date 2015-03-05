import curses
import player

class World(object):
    """
    Singleton for holding map state, entities, and other universals.
    """
    tick_count = 0

    def __init__(self):
        """
        Initialize windows and make a player.
        """
        self.window = curses.newwin(curses.LINES-2, curses.COLS, 0, 0)
        self.window.box()
        self.window.addch(curses.LINES-4, 10, "*")
        self.panel = curses.panel.new_panel(self.window)
        self.status_line = curses.newwin(2, curses.COLS-1, curses.LINES-2, 0)
        self.status_panel = curses.panel.new_panel(self.status_line)
        self.player = player.Player(self, 40, 1)

    def set_status(self, message):
        """
        Update the information in the status bar.
        """
        self.status_line.erase()
        self.status_line.addstr(0, 0, message)

    def tick(self):
        """
        Execute one cycle of the game loop.
        """
        self.player.tick()
        self.tick_count += 1
