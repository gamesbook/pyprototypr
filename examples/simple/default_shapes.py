# -*- coding: utf-8 -*-
"""
Show default shapes - and useful overrides - for pyprototypr

Written by: Derek Hohls
Created on: 20 March 2024
"""

from pyprototypr.draw import *

Create(filename="default_shapes.pdf",
       pagesize=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2)

header = Common(x=0, y=6, font_size=8, align="left")

AutoGrid(stroke_width=0.5)
Text(common=header, text="AutoGrid")
PageBreak()

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
Text(common=header, text="Circle")
Circle()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Circle: cx=1, cy=1")
Circle(cx=1, cy=1)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Octagon")
Octagon()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Octagon: cx=1, cy=1")
Octagon(cx=1, cy=1)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagon")
Hexagon()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagon: vertical")
Hexagon(hex_top="pointy")
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagon: cx=1, cy=1")
Hexagon(cx=1, cy=1)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Rhombus")
Rhombus()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Rhombus: cx=1, cy=1")
Rhombus(cx=1, cy=1)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Star")
Star()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Ellipse")
Ellipse()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Ellipse: cx=1, cy=1")
Ellipse(cx=1, cy=1)
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
Text(common=header, text="RightAngledTriangle")
RightAngledTriangle()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="EquilateralTriangle")
EquilateralTriangle()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Compass")
Compass()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagons: rows=2, cols=2")
Hexagons(rows=2, cols=2)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Grid")
Grid()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Arc")
Arc()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Bezier")
Bezier()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Polyline")
# Polyline() # will get FEEDBACK
Polyline(points=[(0, 0), (1, 1), (2, 0)])
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Shape")
Shape(points="0,0 1,1 2,0")
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="StarField")
Rectangle(x=0, y=0, fill=black)
StarField()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Square")
Square()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Sector")
Sector()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Dot")
Dot()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Lozenge")
Lozenge()
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Fill & Stroke")
Rectangle(fill=yellow, stroke=red, stroke_width=5)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Transparency")
Rectangle(height=2, width=2, fill=yellow, stroke=yellow)
Rectangle(x=2, y=2, height=2, width=2, fill=red, stroke=red, transparency=50)
PageBreak()

Save()
