"""
A chess board example for pyprototypr

Written by: Derek Hohls
Created on: 29 February 2016
Notes:
    Chess font from: http://www.enpassant.dk/chess/fontimg/alpha.htm
"""

from pyprototypr import *

Create(filename="chessboard.pdf", margin=1.25)

rect = rectangle(x=0, y=4, width=2.25, height=2.25, stroke_width=2, fill=None)
rect_fill = rectangle(x=0, y=4, width=2.25, height=2.25, stroke_width=1, fill=grey)

Repeat(rect_fill, cols=8, rows=8, across=(1, 3, 5, 7), down=(1, 3, 5, 7), offset=2.25)
Repeat(rect_fill, cols=8, rows=8, across=(2, 4, 6, 8), down=(2, 4, 6, 8), offset=2.25)
Repeat(rect, cols=8, rows=8, offset=2.25)

PageBreak()
Save()
