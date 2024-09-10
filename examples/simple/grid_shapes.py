# -*- coding: utf-8 -*-
"""
Virtual layout examples for pyprototypr

Written by: Derek Hohls
Created on: 19 May 2024
"""
from pyprototypr import *

Create(filename="grid_layout.pdf",
       pagesize=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2)

header = Common(x=0, y=6, font_size=6, align="left")
circles = Common(x=0, y=0, diameter=1.0, label="{count}/{col}-{row}", label_size=6)
a_circle = circle(common=circles)

Blueprint(stroke_width=0.5)
Text(common=header, text="RectangularLayout: SW->east")
rect = RectangularLayout(cols=3, rows=3, start="SW", direction="east")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="RectangularLayout: NW->south")
rect = RectangularLayout(cols=3, rows=3, start="NW", direction="south")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="RectangularLayout: NE->west")
rect = RectangularLayout(cols=3, rows=3, start="NE", direction="west")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="RectangularLayout: SE->north")
rect = RectangularLayout(cols=3, rows=3, start="SE", direction="north")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="RectangularLayout: SW->north: Snake")
rect = RectangularLayout(cols=3, rows=4, start="SW", direction="north", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="RectangularLayout: NW->south: Snake")
rect = RectangularLayout(cols=3, rows=4, start="NW", direction="south", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="RectangularLayout: SW->east: Snake")
rect = RectangularLayout(cols=3, rows=4, start="SW", direction="east", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="RectangularLayout: SE->west: Snake")
rect = RectangularLayout(cols=3, rows=4, start="SE", direction="west", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="RectangularLayout: SW->east: Outer")
rect = RectangularLayout(cols=3, rows=4, start="SW", direction="east", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="RectangularLayout: SW->north: Outer")
rect = RectangularLayout(cols=3, rows=4, start="SW", direction="north", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="RectangularLayout: debug + no label")
rect = RectangularLayout(cols=3, rows=3)
Layout(rect, debug='n')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="RectangularLayout: debug: snake")
rect = RectangularLayout(cols=3, rows=3, start="NW", direction="south", pattern="snake")
Layout(rect, debug='s')
PageBreak()

Save()
