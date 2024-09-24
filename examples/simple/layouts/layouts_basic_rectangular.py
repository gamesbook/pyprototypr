# -*- coding: utf-8 -*-
"""
Virtual layout examples for pyprototypr

Written by: Derek Hohls
Created on: 19 May 2024
"""
from pyprototypr import *

Create(filename="layouts_basic_rectangular.pdf",
       paper=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2)

header = Common(x=0, y=6, font_size=6, align="left")
circles = Common(x=0, y=0, diameter=1.0, label="{count}/{col}-{row}", label_size=6)
a_circle = circle(common=circles)

# ---- regular

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NW->south")
rect = RectangularLayout(cols=3, rows=3, start="NW", direction="south")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NW->east")
rect = RectangularLayout(cols=3, rows=3, start="NW", direction="east")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NE->west")
rect = RectangularLayout(cols=3, rows=3, start="NE", direction="west")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NE->south")
rect = RectangularLayout(cols=3, rows=3, start="NE", direction="south")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: SE->north")
rect = RectangularLayout(cols=3, rows=3, start="SE", direction="north")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: SE->west")
rect = RectangularLayout(cols=3, rows=3, start="SE", direction="west")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: SW->north")
rect = RectangularLayout(cols=3, rows=3, start="SW", direction="north")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: SW->east")
rect = RectangularLayout(cols=3, rows=3, start="SW", direction="east")
Layout(rect, shapes=[a_circle,])
PageBreak()

# ---- snake

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NW->south: Snake")
rect = RectangularLayout(cols=3, rows=4, start="NW", direction="south", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NW->east: Snake")
rect = RectangularLayout(cols=3, rows=4, start="NW", direction="east", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NE->south: Snake")
rect = RectangularLayout(cols=3, rows=4, start="NE", direction="south", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NE->west: Snake")
rect = RectangularLayout(cols=3, rows=4, start="NE", direction="west", pattern="snake")
Layout(rect, shapes=[a_circle,])

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: SE->north: Snake")
rect = RectangularLayout(cols=3, rows=4, start="SE", direction="north", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: SE->west: Snake")
rect = RectangularLayout(cols=3, rows=4, start="SE", direction="west", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: SW->north: Snake")
rect = RectangularLayout(cols=3, rows=4, start="SW", direction="north", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: SW->east: Snake")
rect = RectangularLayout(cols=3, rows=4, start="SW", direction="east", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

# ---- outer

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NW->east: Outer")
rect = RectangularLayout(cols=3, rows=4, start="NW", direction="east", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NW->south: Outer")
rect = RectangularLayout(cols=3, rows=4, start="NW", direction="south", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NE->west: Outer")
rect = RectangularLayout(cols=3, rows=4, start="NE", direction="west", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NE->south: Outer")
rect = RectangularLayout(cols=3, rows=4, start="NE", direction="south", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: SE->north: Outer")
rect = RectangularLayout(cols=3, rows=4, start="SE", direction="north", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: SE->west: Outer")
rect = RectangularLayout(cols=3, rows=4, start="SE", direction="west", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: SW->east: Outer")
rect = RectangularLayout(cols=3, rows=4, start="SW", direction="east", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: SW->north: Outer")
rect = RectangularLayout(cols=3, rows=4, start="SW", direction="north", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

# ---- triangular spacing

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NW->south; triangular")
rect = RectangularLayout(cols=3, rows=3, side=1.0, start="NW", direction="south", row_even=-0.5)
Layout(rect, shapes=[a_circle,])
PageBreak()

Save()
