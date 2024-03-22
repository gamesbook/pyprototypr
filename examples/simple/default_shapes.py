"""
Shows default shapes for pyprototypr

Written by: Derek Hohls
Created on: 20 March 2024
"""
from pyprototypr.draw import *

Create(filename='default_shapes.pdf',
       pagesize=A7,
       margin_top=0.25, margin_right=0.25)

AutoGrid()
Text(x=0, y=9, font_size=9, align="left", text="Line")
Line()
PageBreak()

AutoGrid()
Text(x=0, y=9, font_size=9, align="left", text="Circle")
Circle()
PageBreak()

AutoGrid()
Text(x=0, y=9, font_size=9, align="left", text="Rectangle")
Rectangle()
PageBreak()

AutoGrid()
Text(x=0, y=9, font_size=9, align="left", text="Octagon")
Octagon()
PageBreak()

AutoGrid()
Text(x=0, y=9, font_size=9, align="left", text="Hexagon")
Hexagon()
PageBreak()

AutoGrid()
Text(x=0, y=9, font_size=9, align="left", text="Hexagon: cx=1, cy=1")
Hexagon(cx=1, cy=1)
PageBreak()

AutoGrid()
Text(x=0, y=9, font_size=9, align="left", text="Rhombus")
Rhombus()
PageBreak()

AutoGrid()
Text(x=0, y=9, font_size=9, align="left", text="Star")
Star()
PageBreak()

AutoGrid()
Text(x=0, y=9, font_size=9, align="left", text="Ellipse")
Ellipse()
# Ellipse(xe=3, label="xe=3")
PageBreak()

AutoGrid()
Text(x=0, y=9, font_size=9, align="left", text="Polygon")
Polygon()
PageBreak()

AutoGrid()
Text(x=0, y=9, font_size=9, align="left", text="Arrow")
Arrow()
PageBreak()

AutoGrid()
Text(x=0, y=9, font_size=9, align="left", text="RightAngledTriangle")
RightAngledTriangle()
PageBreak()

# RightAngledTriangle(flip="up", hand="right", label="UR")
# RightAngledTriangle(flip="down", hand="right", label="DR")
# RightAngledTriangle(flip="up", hand="left", label="UL")
# RightAngledTriangle(flip="down", hand="left", label="DL")

AutoGrid()
Text(x=0, y=9, font_size=9, align="left", text="Compass")
Compass()
PageBreak()

# Compass(perimeter='hexagon')
# Compass(perimeter='octagon')
# Compass(perimeter='rectangle', height=2, width=3)

AutoGrid()
Text(x=0, y=9, font_size=9, align="left", text="Hexagons: rows=2, cols=2")
Hexagons(rows=2, cols=2)
PageBreak()

AutoGrid()
Text(x=0, y=9, font_size=9, align="left", text="Hexagon coord: position=middle; type=lower")
Hexagons(
    rows=2, cols=2,
    coord_position="m",
    coord_type_x="l",
)
PageBreak()

AutoGrid()
Text(x=0, y=9, font_size=9, align="left", text="Hexagons: caltrops and dots")
Hexagons(
    rows=2, cols=2,
    dot_size=0.04,
    caltrops="medium",
)
PageBreak()

# -- no display
# Text()
# Text(text='Text')

# -- no defaults
# Arc()
# Polyline() # will get FEEDBACK

Save()
