"""
Show default shapes - and useful overrides - for pyprototypr

Written by: Derek Hohls
Created on: 20 March 2024
"""
from pyprototypr.draw import *

Create(filename='default_shapes.pdf',
       pagesize=A7,
       margin_top=0.25, margin_right=0.25)

header = Common(x=0, y=9, font_size=9, align="left")

AutoGrid(subdivisions=5, stroke_width=0.6)
Text(common=header, text="AutoGrid: 5 subdivisions")
PageBreak()

AutoGrid()
Text(common=header, text="Text")
Text(text='Hello World')
PageBreak()

AutoGrid()
Text(common=header, text="Line")
Line()
PageBreak()

AutoGrid()
Text(common=header, text="Circle")
Circle()
PageBreak()

AutoGrid()
Text(common=header, text="Rectangle")
Rectangle()
PageBreak()

AutoGrid()
Text(common=header, text="Octagon")
Octagon()
PageBreak()

AutoGrid()
Text(common=header, text="Hexagon")
Hexagon()
PageBreak()

AutoGrid()
Text(common=header, text="Hexagon: cx=1, cy=1")
Hexagon(cx=1, cy=1)
PageBreak()

AutoGrid()
Text(common=header, text="Rhombus")
Rhombus()
PageBreak()

AutoGrid()
Text(common=header, text="Star")
Star()
PageBreak()

AutoGrid()
Text(common=header, text="Ellipse")
Ellipse()
# Ellipse(xe=3, label="xe=3")
PageBreak()

AutoGrid()
Text(common=header, text="Polygon")
Polygon()
PageBreak()

AutoGrid()
Text(common=header, text="Arrow")
Arrow()
PageBreak()

AutoGrid()
Text(common=header, text="RightAngledTriangle")
RightAngledTriangle()
PageBreak()

# RightAngledTriangle(flip="up", hand="right", label="UR")
# RightAngledTriangle(flip="down", hand="right", label="DR")
# RightAngledTriangle(flip="up", hand="left", label="UL")
# RightAngledTriangle(flip="down", hand="left", label="DL")

AutoGrid()
Text(common=header, text="Compass")
Compass()
PageBreak()

# Compass(perimeter='hexagon')
# Compass(perimeter='octagon')
# Compass(perimeter='rectangle', height=2, width=3)

AutoGrid()
Text(common=header, text="Hexagons: rows=2, cols=2")
Hexagons(rows=2, cols=2)
PageBreak()

AutoGrid()
Text(common=header, text="Hexagon coord: position=middle; type=lower")
Hexagons(
    rows=2, cols=2,
    coord_position="m",
    coord_type_x="l",
)
PageBreak()

AutoGrid()
Text(common=header, text="Hexagons: caltrops and dots")
Hexagons(
    rows=2, cols=2,
    dot_size=0.04,
    caltrops="medium",
)
PageBreak()

# -- no defaults
# Arc()
# Polyline() # will get FEEDBACK

Save()
