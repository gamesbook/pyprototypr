"""
WIP tester for pyprototypr

Written by: Derek Hohls
Created on: 9 March 2024
"""
from pyprototypr.draw import *

Create(filename="wip.pdf",
        pagesize=A4,
        margin_top=0.5,
        margin_left=0.15,
        margin_bottom=0.15,
        margin_right=0.2)

header = Common(x=0, y=6, font_size=8, align="left")


# AutoGrid(stroke_width=0.5, subdivisions=10)
# Stadium(x=0, y=0, height=1, width=2, edges='t', fill=tan, label="t")
# Stadium(x=2, y=2, height=1, width=2, edges='b', fill=tan, label="b")
# Stadium(x=0, y=4, height=1, width=1, edges='r', fill=tan, label="r")
# Stadium(x=3, y=5, height=1, width=1, edges='l', fill=tan, label="l")
# PageBreak()

# Create(filename="wip.pdf",
#        pagesize=A6,
#        margin_top=0.5,
#        margin_right=0.15)
# DotGrid(stroke=darkgray, width=0.5, height=0.5, dot_point=1, offset_y=-0.25)

AutoGrid(stroke_width=0.75, subdivisions=10)

ww = 0.5 # 4.3  #
# Hexagon(x=1, y=1, height=2, stroke=red, dot_size=0.02, dot_color=red, fill=None)
Square(x=1, y=0.42, side=1.155, stroke=green, fill=None)  #, dot_size=0.01
#Arc(x=0.97, y=0.4, x1=2.17, y1=1.58, stroke_width=ww, angle=0, angle_width=120)
#Arc(x=1, y=0.42, x1=2.17, y1=1.58, stroke=pink, stroke_width=ww, angle=0, angle_width=120)
Line(x=1.96, y=1.67, x1=1.76, y1=1.35, stroke_width=ww)

Hexagon(
    x=1, y=1,
    height=2,
    stroke=blue, dot_size=0.01, dot_color=blue,
    fill=None,
    link_width=4.3,
    links="6 5 S, 6 1 S",
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
