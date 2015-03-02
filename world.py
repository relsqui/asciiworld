#!/usr/bin/python

import curses, curses.panel, time

LOOP_TIME = .2

class Player(object):
    def __init__(self, y=None, x=None):
        if y is None:
            self.y = int(curses.LINES/2)
        if x is None:
            self.x = int(curses.COLS/2)
        self.window = curses.newwin(2, 2, self.y, self.x)
        self.window.addstr(0, 0, "O")
        self.window.addstr(1, 0, "|")
        self.panel = curses.panel.new_panel(self.window)

    def move(self, d_y, d_x):
        self.y = min(max(self.y + d_y, 0), curses.LINES-1)
        self.x = min(max(self.x + d_x, 0), curses.COLS-2)
        self.panel.move(self.y, self.x)

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    player = Player()
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

curses.wrapper(main)
