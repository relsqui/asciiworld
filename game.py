#!/usr/bin/python

import curses, curses.panel
import world

TICK_TIME = 100

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.clear()
    game_world = world.World()
    c = None
    while True:
        # do things
        if c == ord('q'):
            break
        elif c == ord('h'):
            game_world.player.walk(-1)
        elif c == ord('l'):
            game_world.player.walk(1)
        game_world.tick()
        curses.panel.update_panels()
        stdscr.refresh()
        curses.napms(TICK_TIME)
        c = stdscr.getch()
        curses.flushinp()

curses.wrapper(main)
