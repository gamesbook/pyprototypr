# -*- coding: utf-8 -*-
"""
Show default shapes - and useful overrides - for pyprototypr

Written by: Derek Hohls
Created on: 20 March 2024
"""

from pyprototypr import *

Create(filename="default_shapes.pdf",
       paper=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2)

header = Common(x=0, y=6, font_size=8, align="left")

Blueprint(stroke_width=0.5)
Text(common=header, text="Blueprint")
PageBreak()

Blueprint(subdivisions=5, stroke_width=0.8)
Text(common=header, text="Blueprint: subdivisions=5")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Text")
Text(text="Hello World")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Line")
Line()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rectangle")
Rectangle()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Circle")
Circle()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Circle: cx=1, cy=1")
Circle(cx=1, cy=1)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagon")
Hexagon()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagon: vertical")
Hexagon(orientation="pointy")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagon: cx=1, cy=1")
Hexagon(cx=1, cy=1)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rhombus")
Rhombus()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rhombus: cx=1, cy=1")
Rhombus(cx=1, cy=1)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Star")
Star()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Ellipse")
Ellipse()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Ellipse: cx=1, cy=1")
Ellipse(cx=1, cy=1)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Polygon")
Polygon()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Arrow")
Arrow()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="RightAngledTriangle")
RightAngledTriangle()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="EquilateralTriangle")
EquilateralTriangle()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Compass")
Compass()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: rows=2, cols=2")
Hexagons(rows=2, cols=2, margin_bottom=0, margin_left=0)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Grid")
Grid()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Arc")
Arc()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Bezier")
Bezier()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Polyline")
# Polyline() # will get FEEDBACK
Polyline(points=[(0, 0), (1, 1), (2, 0)])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Shape")
Shape(points="0,0 1,1 2,0")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Sector")
Sector()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Sequence")
Sequence(text())
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Square")
Square()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text='Stadium ("pill")')
Stadium()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="StarField")
Rectangle(x=0, y=0, fill=black)
StarField()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Dot")
Dot()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="DotGrid")
DotGrid()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Fill & Stroke")
Rectangle(fill=yellow, stroke=red, stroke_width=5)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Transparency")
Rectangle(x=0, y=0, height=2, width=2, fill=yellow, stroke=yellow)
Rectangle(x=1, y=1, height=2, width=2, fill=red, stroke=red, transparency=50)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Track: Rectangle: SW~clockwise")
Track()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Chord: 135 to 45 degrees")
Chord(shape=Circle(), angle=135, angle1=45)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Circle: radii [30,150]")
Circle(cx=1, cy=1, radii=[30,150])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text='RectangularLayout: "invisible"')
Layout(RectangularLayout())
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text='RectangularLayout: "debug"')
Layout(RectangularLayout(), debug='normal')
PageBreak()


Save(output='png', dpi=600)
