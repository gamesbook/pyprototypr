"""
Show a `game board` example for pyprototypr

Written by: Derek Hohls
Created on: 1 February 2024
Notes:
"""
from pyprototypr.draw import *

Create(
    filename='squadleader.pdf',
    margin=1.25,
    pagesize=landscape(A4))
Hexagons(
    rows=10, cols=16,
    side=1.15,
    margin_left=-1.15, margin_bottom=-1.15,
    dot_size=0.04, dot_color=white,
    coord_type_x="letter", coord_type_y="number",
    coord_position="t", coord_offset=0,
    coord_font_size=7, coord_stroke=black,
    coord_padding=0,
    fill=darkseagreen, stroke=black)
Save()
