#!/usr/bin/python

import curses, curses.panel
import world

TICK_TIME = 100

def main(stdscr):
    curses.curs_set(0) # don't show the cursor
    stdscr.nodelay(True) # don't wait for enter before reading keys
    stdscr.clear() # empty the screen
    game_world = world.World()
    keys = set()
    while True:
        # do things
        if ord("q") in keys:
            break
        if ord("c") in keys:
            game_world.create_map()
        if ord("h") in keys:
            game_world.player.walk(-1)
        if ord("l") in keys:
            game_world.player.walk(1)
        if ord(" ") in keys:
            game_world.player.jump()
        game_world.tick()
        curses.panel.update_panels()
        stdscr.refresh()
        keys = set()
        curses.napms(TICK_TIME)
        while -1 not in keys:
            # collect all the keypresses which occurred during the tick delay
            keys.add(stdscr.getch())

curses.wrapper(main)
