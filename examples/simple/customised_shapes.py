"""
Show customised shapes - and useful overides - for pyprototypr

Written by: Derek Hohls
Created on: 29 March 2024
"""

from pyprototypr.draw import *

Create(filename="customised_shapes.pdf",
       pagesize=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2)

header = Common(x=0, y=6, font_size=8, align="left")

AutoGrid(subdivisions=5, stroke_width=0.8)
Text(common=header, text="AutoGrid: subdivisions=5")
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Text")
Text(text="Hello World")
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Line")
Line()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Rectangle")
Rectangle()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Circle: cx=2, cy=3")
Circle(cx=2, cy=3)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Octagon: cx=2, cy=3")
Octagon(cx=2, cy=3)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagon: cx=2, cy=3")
Hexagon(cx=2, cy=3)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Rhombus: cx=2, cy=3")
Rhombus(cx=2, cy=3)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Star")
Star()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Ellipse: xe=3,ye=2")
Ellipse(cx=2, cy=1, xe=4, ye=3)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Polygon")
Polygon()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Arrow")
Arrow()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Right Angled Triangle")
RightAngledTriangle(x=1, y=1, flip="up", hand="right", label="UR", fill="yellow")
RightAngledTriangle(x=2, y=2, flip="down", hand="right", label="DR", fill="green")
RightAngledTriangle(x=2, y=3, flip="up", hand="left", label="UL", fill="red")
RightAngledTriangle(x=3, y=4, flip="down", hand="left", label="DL", fill="blue")
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Compass")
Compass(cx=1, cy=1, perimeter='hexagon')
Compass(cx=2, cy=2, perimeter='octagon')
Compass(cx=3, cy=3, perimeter='rectangle', height=2, width=3)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagons: coordinates")
Hexagons(
    height=1.1,
    rows=2,
    cols=2,
    coord_position="middle",
)
Hexagons(
    side=0.6,
    margin_left=3,
    margin_bottom=4.5,
    rows=2,
    cols=2,
    fill=darkseagreen,
    hex_offset="odd",
    coord_position="top",
    coord_type_x="upper",
    coord_separator=':',
)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagons: caltrops and dots")
Hexagons(
    height=1.5,
    rows=2,
    cols=2,
    dot_size=0.04,
    #caltrops="medium",
)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Lines")
Lines(x=0, x1=6, y=0, y1=0, rows=7, height=1.0)
PageBreak()
# -- no defaults
# Arc()
# Polyline() # will get FEEDBACK

AutoGrid(stroke_width=0.5)
Text(common=header, text="StarField")
Rectangle(x=0, y=0, height=3, width=3, fill=black)
StarField(
    density=20,
    enclosure=rectangle(x=0, y=0, height=3, width=3),
    colors=[white, white, white, red, blue],
    sizes=[0.15, 0.15, 0.15, 0.15, 0.3, 0.3, 0.45])
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="StarField")
Circle(x=0, y=0, radius=1.5, fill=black)
StarField(
    density=20,
    enclosure=circle(x=0, y=0, radius=1.5),
    colors=[white, white, white, green, blue],
    sizes=[0.15, 0.15, 0.15, 0.3, 0.3, 0.45])
PageBreak()

Save()
