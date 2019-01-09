#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8

import os
import curses


class SplitScreen:

  max_row = 10
  screen = curses.initscr()
  activeBox = 1
  leftHighlightedCursor = 0
  rightHighlightedCursor = 0

  def __init__(self):
    SplitScreen.getGeometry()
    curses.noecho()
    curses.cbreak()
    curses.curs_set( 0 )                                                        #cursor visibility
    curses.start_color()
    SplitScreen.screen.keypad( 1 )
    curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_WHITE, curses.COLOR_RED)
    SplitScreen.highlightText = curses.color_pair( 3 )
    SplitScreen.highlightWindow = curses.color_pair( 1 )
    SplitScreen.normalText = curses.A_NORMAL
    SplitScreen.leftBox = curses.newwin( SplitScreen.max_row + 20, SplitScreen.middleCol-1, 1, 1 )
    SplitScreen.rightBox = curses.newwin( SplitScreen.max_row + 20, SplitScreen.middleCol, 1, SplitScreen.middleCol )
    SplitScreen.leftBox.box()
    SplitScreen.rightBox.box()
    SplitScreen.switchBox()
    SplitScreen.refresh()
    SplitScreen.keyhandler()


  def getGeometry():
    y, x = SplitScreen.screen.getmaxyx()
    SplitScreen.rows = int(y)
    SplitScreen.cols = int(x)
    SplitScreen.middleCol = int(SplitScreen.cols/2)
    

  def refresh():
    SplitScreen.getGeometry()
    SplitScreen.screen.border( 0 )
    SplitScreen.screen.refresh()
    SplitScreen.leftBox.border(0)
    SplitScreen.leftBox.refresh()
    SplitScreen.rightBox.border(0)
    SplitScreen.rightBox.refresh()
    resize = curses.is_term_resized(SplitScreen.rows, SplitScreen.cols)

    if resize is True:
      y, x = SplitScreen.screen.getmaxyx()
      SplitScreen.screen.clear()
      curses.resizeterm(y, x)
      SplitScreen.screen.refresh()

    SplitScreen.populate(SplitScreen.leftBox, 0)
    SplitScreen.populate(SplitScreen.rightBox, 0)

  def populate(box, selected):
    strings = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "l", "m", "n" ]
    i = 0
    for string in strings:
      if i == selected:
        box.addstr(i+1, 3, "line " + str(i) + ": "+string, SplitScreen.highlightText)
      else:
        box.addstr(i+1, 3, "line " + str(i) + ": "+string, SplitScreen.normalText)
      i = i + 1
    box.refresh()


  def switchBox():
    SplitScreen.activeBox = (SplitScreen.activeBox+1)%2
    if SplitScreen.activeBox == 0:
      SplitScreen.leftBox.bkgd(SplitScreen.highlightWindow)
      SplitScreen.rightBox.bkgd(SplitScreen.normalText)
      SplitScreen.populate(SplitScreen.leftBox, SplitScreen.leftHighlightedCursor)
      SplitScreen.leftBox.refresh()
      SplitScreen.rightBox.refresh()      

    if SplitScreen.activeBox == 1:
      SplitScreen.rightBox.bkgd(SplitScreen.highlightWindow)
      SplitScreen.leftBox.bkgd(SplitScreen.normalText)
      SplitScreen.populate(SplitScreen.rightBox, SplitScreen.rightHighlightedCursor)
      SplitScreen.rightBox.refresh()
      SplitScreen.leftBox.refresh()
      


  def keyhandler():
    x = SplitScreen.screen.getch()
    while x != 27:                                                              #end with the [ESC] key
        if x == curses.KEY_DOWN:
          if SplitScreen.activeBox == 0:
            SplitScreen.leftHighlightedCursor = SplitScreen.leftHighlightedCursor + 1
            SplitScreen.populate(SplitScreen.leftBox, SplitScreen.leftHighlightedCursor)
          if SplitScreen.activeBox == 1:
            SplitScreen.rightHighlightedCursor = SplitScreen.rightHighlightedCursor + 1
            SplitScreen.populate(SplitScreen.rightBox, SplitScreen.rightHighlightedCursor)

        if x == curses.KEY_UP:
          if SplitScreen.activeBox == 0:
            SplitScreen.leftHighlightedCursor = SplitScreen.leftHighlightedCursor - 1
            SplitScreen.populate(SplitScreen.leftBox, SplitScreen.leftHighlightedCursor)
          if SplitScreen.activeBox == 1:
            SplitScreen.rightHighlightedCursor = SplitScreen.rightHighlightedCursor - 1
            SplitScreen.populate(SplitScreen.rightBox, SplitScreen.rightHighlightedCursor)

        if x == curses.KEY_LEFT:
          pass
        if x == curses.KEY_RIGHT:
          pass
        if x == ord('\t'):
          SplitScreen.switchBox()

        SplitScreen.screen.refresh()
        #SplitScreen.leftBox.refresh()
        #SplitScreen.rightBox.refresh()
        x = SplitScreen.screen.getch()
      
      
    print("eXiting")  
    curses.endwin()
    exit(0)
      
      
      
      
# MAIN
# mostly for testing this module at the console
# ------------------------------------------------
def main():
  ss = SplitScreen()


if __name__ == "__main__": main()


