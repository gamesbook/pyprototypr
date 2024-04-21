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

Text(common=header, text="START...")
PageBreak(footer=True)

AutoGrid(subdivisions=5, stroke_width=0.8)
Rectangle(height=2, width=1, x=0, y=0, label="x:0 y:0")
Text(common=header, text="AutoGrid: subdivisions=5")
Footer()
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
Text(common=header, text="Rectangle & Notches")
Rectangle(height=2, width=1, x=0, y=0, label="x:0 y:0", label_size=5)
Rectangle(
    x=2, y=1,
    height=2, width=1,
    notch=0.25,
    label="notch:0.5",
    label_size=5,
    )
Rectangle(
    x=1, y=4,
    height=1, width=2,
    notch_y=0.25,
    notch_x=0.5,
    notch_corners="NW SE",
    label="notch:.25/.5 loc: NW, SE",
    label_size=5,
    )
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Circle: cx=2, cy=3")
Circle(cx=2, cy=3)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Circle: hatch")
Circle(cx=2, cy=5, radius=.7, hatch=1, label='1')
Circle(cx=2, cy=3.5, radius=.7, hatch=4, label='4', rotate=60)
Circle(cx=2, cy=2, radius=.7, hatch=5, label='5')
Circle(cx=1, cy=1, radius=.7, hatch=5, hatch_directions='e', label='e')
Circle(cx=3, cy=1, radius=.7, hatch=5, hatch_directions='n', label='n')
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Rectangle: dot & cross")
Rectangle(height=3, width=2, x=1, y=1, cross_size=0.75, dot_size=0.15)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Dots & Crosses")
Circle(cx=1, cy=1, radius=1, dot_size=0.1, dot_color=green)
Circle(cx=3, cy=1, radius=1, cross_size=0.25, cross_stroke=green)
Octagon(cx=1, cy=3, height=2, width=2, dot_size=0.1, dot_color=orange)
Octagon(cx=3, cy=3, height=2, width=2, cross_size=0.25, cross_stroke=orange)
Hexagon(x=0, y=4, height=2, dot_size=0.1, dot_color=red)
Hexagon(x=2, y=4, height=2, cross_size=0.25, cross_stroke=red, cross_stroke_width=1)
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
Text(common=header, text="Lines")
Lines(x=1, x1=4, y=1, y1=1, rows=2, height=1.0, label_size=8, label="rows; ht=1.0")
Lines(x=1, x1=1, y=3, y1=6, cols=2, width=1.5, label_size=8, label="col; wd=1.5")
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="StarField: Rectangle; multicolor")
Rectangle(x=0, y=0, height=3, width=3, fill=black)
StarField(
    density=20,
    enclosure=rectangle(x=0, y=0, height=3, width=3),
    colors=[white, white, white, red, green, blue],
    sizes=[0.2])
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="StarField: Circle; multisize")
Circle(x=0, y=0, radius=1.5, fill=black)
StarField(
    density=20,
    enclosure=circle(x=0, y=0, radius=1.5),
    sizes=[0.15, 0.15, 0.15, 0.15, 0.3, 0.3, 0.45])
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Rectangle: hatch")
Rectangle(
    height=2, width=2,
    hatch=15, hatch_width=0.1, hatch_stroke=black,
    stroke=saddlebrown, stroke_width=0.2, fill=lightcyan)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Octagon: hatch")
Octagon(x=0, y=0, height=1.5, width=1.5, hatch=4, hatch_directions='e', label="e")
Octagon(x=2, y=0, height=1.5, width=1.5, hatch=4, hatch_directions='n', label="n")
Octagon(x=0, y=2, height=1.5, width=1.5, hatch=4, hatch_directions='ne', label="ne")
Octagon(x=2, y=2, height=1.5, width=1.5, hatch=4, hatch_directions='nw', label="nw")
Octagon(x=1, y=4, height=1.5, width=1.5, hatch=4)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagon: hatch")
Hexagon(x=0, y=0, height=1.5, hex_top='flat', hatch=5, hatch_directions='e', label="e")
Hexagon(x=2, y=0, height=1.5, hex_top='pointy', hatch=5, hatch_directions='n', label="n")
Hexagon(x=0, y=2, height=1.5, hex_top='flat', hatch=5, hatch_directions='ne', label="ne")
Hexagon(x=2, y=2, height=1.5, hex_top='pointy', hatch=5, hatch_directions='ne', label="ne")
Hexagon(x=0, y=4, height=1.5, hex_top='flat', hatch=5, hatch_directions='nw', label="nw")
Hexagon(x=2, y=4, height=1.5, hex_top='pointy', hatch=5, hatch_directions='nw', label="nw")
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagon: flat; text; hatch")
Hexagon(
    height=2,
    hatch=3,
    debug=True,
    title="Title",
    label="Label",
    heading="Heading")
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagon: pointy; text; hatch")
Hexagon(
    height=2,
    hatch=3,
    hex_top='pointy',
    title="Title",
    label="Label",
    heading="Heading")
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Right Angled Triangle")
EquilateralTriangle(x=1, y=3, side=2, hatch=3, title='Title', heading='Heading')
EquilateralTriangle(x=1, y=1, flip="up", hand="right", label="UR", fill="yellow")
EquilateralTriangle(x=1, y=1, flip="down", hand="right", label="DR", fill="green")
EquilateralTriangle(x=1, y=1, flip="up", hand="left", label="UL", fill="red")
EquilateralTriangle(x=1, y=1, flip="down", hand="left", label="DL", fill="blue")
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Sector; same centre")
Sector(cx=2, cy=3, radius=2, fill=black, angle=45, angle_width=30)
Sector(cx=2, cy=3, radius=2, fill=black, angle=165, angle_width=30)
Sector(cx=2, cy=3, radius=2, fill=black, angle=285, angle_width=30)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Arc; 'inside' rect")
Rectangle(x=1, y=1, height=1, width=2, dot_size=0.01, stroke=red, fill=None,
          label="Arc(x=1, y=1, x1=3, y1=2)")
Arc(x=1, y=1, x1=3, y1=2)
PageBreak()

Text(common=header, text="END...")
PageBreak(footer=True)

Save()
