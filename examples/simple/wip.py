"""
WIP tester for pyprototypr

Written by: Derek Hohls
Created on: 9 March 2024
"""
from pyprototypr.draw import *

Create(filename="wip.pdf",
       pagesize=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2)

header = Common(x=0, y=6, font_size=8, align="left")

# AutoGrid(stroke_width=0.5)
# Lines(x=1, x1=1, y=3, y1=6, cols=2, height=1.5, label_size=8, label="col; h=1.5")
# Lines(x=1, x1=4, y=1, y1=1, rows=2, height=1.0, label_size=8, label="rows; h=1.0")
# Text(common=header, text="Lines")
# PageBreak()

# AutoGrid(stroke_width=0.2, subdivisions=10)
# Text(common=header, text="Hexagon: pointy")
# Hexagon(hex_top="pointy", dot_size=0.1,)

# Hexagons(
#     side=0.6,
#     rows=3, cols=3,
#     y=0, x=0,
#     hex_top="pointy",
#     hex_offset="even",
#     dot_size=0.04,
# )

PageBreak()

Save()
