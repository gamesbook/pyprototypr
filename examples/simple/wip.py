"""
WIP tester for pyprototypr

Written by: Derek Hohls
Created on: 9 March 2024
"""
from pyprototypr.draw import *

Create(filename="wip.pdf",
       pagesize=A8,
       margin_top=0.5,
       margin_left=0.15,
       margin_bottom=0.15,
       margin_right=0.2)

header = Common(x=0, y=6, font_size=8, align="left")
ww = 4.3  # 0.1 #
AutoGrid(stroke_width=0.5, subdivisions=10)
# Hexagon(x=1, y=1, height=2, stroke=red, dot_size=0.02, dot_color=red, fill=None)
Square(x=0.97, y=0.4, side=1.18, dot_size=0.01, stroke=red, fill=None)
Arc(x=0.97, y=0.4, x1=2.17, y1=1.58, stroke_width=ww, angle_width=120)
Line(x=1.96, y=1.67, x1=1.76, y1=1.35, stroke_width=ww)

Hexagon(
    x=1, y=1,
    height=2,
    stroke=blue, dot_size=0.01, dot_color=blue,
    fill=None,
    #link_width=4.3,
    links="6 5 S",
    # hex_top="pointy",
    debug=True)

PageBreak()

#AutoGrid(stroke_width=0.5)
#Text(common=header, text="Sector; same centre")
#Sector(cx=2, cy=3, radius=2, fill=red, angle=45, angle_width=30)
# Sector(cx=2, cy=3, radius=2, fill=black, angle=165, angle_width=30)
# Sector(cx=2, cy=3, radius=2, fill=black, angle=285, angle_width=30)
# PageBreak()

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
# PageBreak()

Save()
