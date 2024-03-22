"""
A `wargame board` example for pyprototypr

Written by: Derek Hohls
Created on: 21 February 2024
Notes:
"""

from pyprototypr.draw import *

Create(filename="squadleader.pdf", margin=0.5, pagesize=landscape(A4))

Rectangle(x=-0.05, y=0.2, width=29, height=20, stroke=darkseagreen, fill=darkseagreen)

Hexagons(
    cols=16,
    rows=10,
    side=1.15,
    hex_offset="odd",
    margin_bottom=1.75,
    dot_size=0.04,
    dot_color=white,
    coord_position="t",
    coord_type_x="letter",
    coord_font_size=7,
    coord_padding=0,
    fill=darkseagreen,
    stroke=black,
)

Save()
