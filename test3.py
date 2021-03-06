#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8

import os
import curses


#===============================================================================
# implemented as a python class
#-------------------------------------------------------------------------------
class SplitScreen:

  max_row = 10
  screen = curses.initscr()
  activeBox = 0
  leftHighlightedCursor = 0
  rightHighlightedCursor = 0
  oldWidth = 0


#===============================================================================
# initializes the class
#-------------------------------------------------------------------------------
  def __init__(self):
    curses.noecho()
    curses.cbreak()
    curses.curs_set( 0 )                                                        #cursor visibility
    curses.start_color()
    SplitScreen.screen.keypad( 1 )
    curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(4,curses.COLOR_WHITE, curses.COLOR_BLUE)
    SplitScreen.highlightText = curses.color_pair( 3 )
    SplitScreen.highlightWindow = curses.color_pair( 1 )
    SplitScreen.coloredStatusbox = curses.color_pair( 4 )
    SplitScreen.normalText = curses.A_NORMAL
    SplitScreen.draw()
    SplitScreen.keyhandler()


#===============================================================================
# gets the geometry of the terminal window
#-------------------------------------------------------------------------------
  def getGeometry():
    y, x = os.popen('stty size', 'r').read().split()
    SplitScreen.rows = int(y)
    SplitScreen.cols = int(x)
    SplitScreen.middleCol = int(SplitScreen.cols/2)
    SplitScreen.middleRow = int(SplitScreen.rows/2)
    SplitScreen.statusRow = int(SplitScreen.rows-6)

#===============================================================================
# draws everything and recalculates the sizes on Terminal Window resize
#-------------------------------------------------------------------------------
  def draw():
      SplitScreen.getGeometry()
      SplitScreen.screen.clear()
      SplitScreen.screen.refresh()
      SplitScreen.screen.border( 0 )
      SplitScreen.screen.refresh()

      SplitScreen.leftBox = curses.newwin( SplitScreen.rows-6, SplitScreen.middleCol-1, 1, 1 )
      SplitScreen.rightBox = curses.newwin( SplitScreen.rows-6, SplitScreen.middleCol, 1, SplitScreen.middleCol )
      SplitScreen.statusBox = curses.newwin( 4, SplitScreen.cols-2, SplitScreen.statusRow+1, 1 )

      SplitScreen.leftBox.box()
      SplitScreen.rightBox.box()
      SplitScreen.statusBox.box()

      if SplitScreen.activeBox == 0:
        SplitScreen.leftBox.bkgd(SplitScreen.highlightWindow)
        SplitScreen.rightBox.bkgd(SplitScreen.normalText)
      if SplitScreen.activeBox == 1:
        SplitScreen.rightBox.bkgd(SplitScreen.highlightWindow)
        SplitScreen.leftBox.bkgd(SplitScreen.normalText)
        
      SplitScreen.populate(SplitScreen.leftBox, SplitScreen.leftHighlightedCursor)
      SplitScreen.leftBox.refresh()
      SplitScreen.populate(SplitScreen.rightBox, SplitScreen.rightHighlightedCursor)
      SplitScreen.rightBox.refresh()
        
      SplitScreen.statusBox.bkgd(SplitScreen.coloredStatusbox)
      SplitScreen.statusBox.addstr(1, 2, "Press [TAB] to switch the side", SplitScreen.coloredStatusbox)
      SplitScreen.statusBox.addstr(2, 2, "Press [ESC] to end", SplitScreen.coloredStatusbox)
      SplitScreen.statusBox.refresh()

#===============================================================================
# populates the left and the right box with random data
#-------------------------------------------------------------------------------
  def populate(box, selected):
    strings = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "l", "m", "n" ]
    i = 0
    for string in strings:
      if i == selected:
        box.addstr(i+1, 3, "line " + str(i) + ": "+string, SplitScreen.highlightText)
      else:
        box.addstr(i+1, 3, "line " + str(i) + ": "+string, SplitScreen.normalText)
      i = i + 1


#===============================================================================
# switches the active box (left = 0 / right = 1)
#-------------------------------------------------------------------------------
  def switchBox():
    SplitScreen.activeBox = (SplitScreen.activeBox+1)%2


#===============================================================================
# loop that handles the keys, TODO: should be implemented as listener instead of loop
#-------------------------------------------------------------------------------
  def keyhandler():
    x = SplitScreen.screen.getch()
    while x != 27:                                                              #end with the [ESC] key
        if x == curses.KEY_DOWN:
          if SplitScreen.activeBox == 0:
            SplitScreen.leftHighlightedCursor = SplitScreen.leftHighlightedCursor + 1
            SplitScreen.populate(SplitScreen.leftBox, SplitScreen.leftHighlightedCursor)
          if SplitScreen.activeBox == 1:
            SplitScreen.rightHighlightedCursor = SplitScreen.rightHighlightedCursor + 1


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

        SplitScreen.draw()
        x = SplitScreen.screen.getch()
      
      
    print("eXiting")  
    curses.endwin()
    exit(0)
      
      
      
      
# MAIN
# 
# ------------------------------------------------
def main():
  ss = SplitScreen()


if __name__ == "__main__": main()


