# -*- coding: utf-8 -*-
"""
Virtual layout examples for pyprototypr

Written by: Derek Hohls
Created on: 19 May 2024
"""
from pyprototypr import *

Create(filename="layouts_basic_rectangular.pdf",
       paper=A8,
       margin=0.75,
       margin_right=0.2, margin_top=0.2,
       font_size=8,
       stroke_width=0.5)

header = Common(x=0, y=6, font_size=6, align="left")
circles = Common(x=0, y=0, diameter=1.0, label="{count}/{col}-{row}", label_size=6)
a_circle = circle(common=circles)

# ---- regular

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->south")
rect = RectangularLocations(cols=3, rows=3, start="NW", direction="south")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->east")
rect = RectangularLocations(cols=3, rows=3, start="NW", direction="east")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NE->west")
rect = RectangularLocations(cols=3, rows=3, start="NE", direction="west")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NE->south")
rect = RectangularLocations(cols=3, rows=3, start="NE", direction="south")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SE->north")
rect = RectangularLocations(cols=3, rows=3, start="SE", direction="north")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SE->west")
rect = RectangularLocations(cols=3, rows=3, start="SE", direction="west")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SW->north")
rect = RectangularLocations(cols=3, rows=3, start="SW", direction="north")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SW->east")
rect = RectangularLocations(cols=3, rows=3, start="SW", direction="east")
Layout(rect, shapes=[a_circle,])
PageBreak()

# ---- snake

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->south: Snake")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="south", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->east: Snake")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NE->south: Snake")
rect = RectangularLocations(cols=3, rows=4, start="NE", direction="south", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NE->west: Snake")
rect = RectangularLocations(cols=3, rows=4, start="NE", direction="west", pattern="snake")
Layout(rect, shapes=[a_circle,])

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SE->north: Snake")
rect = RectangularLocations(cols=3, rows=4, start="SE", direction="north", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SE->west: Snake")
rect = RectangularLocations(cols=3, rows=4, start="SE", direction="west", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SW->north: Snake")
rect = RectangularLocations(cols=3, rows=4, start="SW", direction="north", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SW->east: Snake")
rect = RectangularLocations(cols=3, rows=4, start="SW", direction="east", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

# ---- outer

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->east: Outer")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->south: Outer")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="south", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NE->west: Outer")
rect = RectangularLocations(cols=3, rows=4, start="NE", direction="west", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NE->south: Outer")
rect = RectangularLocations(cols=3, rows=4, start="NE", direction="south", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SE->north: Outer")
rect = RectangularLocations(cols=3, rows=4, start="SE", direction="north", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SE->west: Outer")
rect = RectangularLocations(cols=3, rows=4, start="SE", direction="west", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SW->east: Outer")
rect = RectangularLocations(cols=3, rows=4, start="SW", direction="east", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SW->north: Outer")
rect = RectangularLocations(cols=3, rows=4, start="SW", direction="north", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

# ---- triangular spacing

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->south; triangular")
rect = RectangularLocations(cols=3, rows=3, side=1.0, start="NW", direction="south", row_even=-0.5)
Layout(rect, shapes=[a_circle,])
PageBreak()

Save()
