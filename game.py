#!/usr/bin/python

import curses, curses.panel, time

LOOP_TIME = .1

class World(object):
    def __init__(self, stdscr):
        self.window = stdscr
        self.ground_level = curses.LINES - 3
        self.window.addstr(self.ground_level, 0, "-" * curses.COLS)
        self.status_line = curses.newwin(2, curses.COLS-1,
                                         self.ground_level+1, 0)
        self.status_panel = curses.panel.new_panel(self.status_line)

    def set_status(self, message):
        self.status_line.erase()
        self.status_line.addstr(0, 0, message)
        self.status_line.refresh()


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

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    world = World(stdscr)
    world.set_status("Welcome!")
    player = Player(world)
    c = None
    while True:
        # do things
        if c == ord('q'):
            break
        elif c == ord('h'):
            player.move(0, -1)
        elif c == ord('l'):
            player.move(0, 1)
        curses.panel.update_panels()
        stdscr.refresh()
        c = stdscr.getch()
        curses.flushinp()
        time.sleep(LOOP_TIME)

curses.wrapper(main)
