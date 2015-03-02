#!/usr/bin/python

import curses, curses.panel, time
import world

#LOOP_TIME = .1

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    game_world = world.World(stdscr)
    game_world.set_status("Welcome!")
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
        #time.sleep(LOOP_TIME)
        c = stdscr.getch()
        curses.flushinp()

curses.wrapper(main)
