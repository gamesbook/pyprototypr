"""
Show a `game board` example for pyprototypr

Written by: Derek Hohls
Created on: 29 February 2016
Notes:
    Chess font from: http://www.enpassant.dk/chess/fontimg/alpha.htm
"""
from pyprototypr.draw import *

Create(filename='chessboard.pdf', margin=1.25)

# chess
rect = rectangle(x=0, y=4, width=2.25, height=2.25, stroke_width=2,
                 stroke=black, transparent=True)
rect_fill = rectangle(x=0, y=4, width=2.25, height=2.25, stroke_width=1, fill=grey)
Repeat(rect_fill, cols=8, rows=8, across=(1,3,5,7), down=(1,3,5,7), offset=2.25)
Repeat(rect_fill, cols=8, rows=8, across=(2,4,6,8), down=(2,4,6,8), offset=2.25)
Repeat(rect, cols=8, rows=8, offset=2.25)

# common not working ...?
#common = Common(cols=8, rows=8, offset=2.25)
#Repeat(rect_fill, across=(1, 3, 5, 7), down=(1, 3, 5, 7), common=common)
#Repeat(rect_fill, across=(2, 4, 6, 8), down=(2, 4, 6, 8), common=common)
#Repeat(rect, common=common)

PageBreak()
Save()
