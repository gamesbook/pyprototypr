"""
A chess board example, using a Rectangles grid approach, for pyprototypr

Written by: Derek Hohls
Created on: 3 August 2024
"""

from pyprototypr import *

Create(filename="chessboard_brown.pdf")

square_grid = Rectangles(
    rows=8,
    cols=8,
    width=2.25,
    height=2.25,
    stroke=saddlebrown,
    fill=saddlebrown,
    stroke_width=1,
    coord_type_x="lower",
    coord_padding=0,
)

Locations(
    square_grid,
    "a8,c8,e8,g8,b7,d7,f7,h7,"
    "a6,c6,e6,g6,b5,d5,f5,h5,"
    "a4,c4,e4,g4,b3,d3,f3,h3,"
    "a2,c2,e2,g2,b1,d1,f1,h1",
    [square(width=2.25, fill=tan, stroke=tan)],
)

Rectangle(
    x=-0.02, y=-0.02, height=18, width=18, stroke=saddlebrown, stroke_width=2, fill=None
)

# labels for board
grid_label = Common(font_size=18, align="left", stroke=saddlebrown)
Sequence(text(common=grid_label, x=0.75, y=-0.75), setting=('a', 'h'), gap_x=2.25)
Sequence(text(common=grid_label, x=-0.75, y=0.75), setting=(1, 8), gap_y=2.25)

Save()
