import curses
import player

class World(object):
    def __init__(self, stdscr):
        self.window = stdscr
        self.ground_level = curses.LINES - 3
        self.window.addstr(self.ground_level, 0, "-" * curses.COLS)
        self.status_line = curses.newwin(2, curses.COLS-1,
                                         self.ground_level+1, 0)
        self.status_panel = curses.panel.new_panel(self.status_line)
        self.player = player.Player(self)

    def set_status(self, message):
        self.status_line.erase()
        self.status_line.addstr(0, 0, message)
        self.status_line.refresh()
