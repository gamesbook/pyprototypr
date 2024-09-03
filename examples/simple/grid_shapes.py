# -*- coding: utf-8 -*-
"""
Virtual grid examples for pyprototypr

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
boxes = Common(x=0, y=0, height=1.0, label="{count}/{col}-{row}", label_size=6)
small_box = square(common=boxes)

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: SW/east")
rg = RectangleGrid(cols=3, rows=3, start="SW", direction="east")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: NW/south")
rg = RectangleGrid(cols=3, rows=3, start="NW", direction="south")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: NE/west")
rg = RectangleGrid(cols=3, rows=3, start="NE", direction="west")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: SE/north")
rg = RectangleGrid(cols=3, rows=3, start="SE", direction="north")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: SW/north: Snake")
rg = RectangleGrid(cols=3, rows=4, start="SW", direction="north", pattern="snake")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: NW/south: Snake")
rg = RectangleGrid(cols=3, rows=4, start="NW", direction="south", pattern="snake")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: SW/east: Snake")
rg = RectangleGrid(cols=3, rows=4, start="SW", direction="east", pattern="snake")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: SE/west: Snake")
rg = RectangleGrid(cols=3, rows=4, start="SE", direction="west", pattern="snake")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: SW/east: Outer")
rg = RectangleGrid(cols=3, rows=4, start="SW", direction="east", pattern="outer")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: SW/north: Outer")
rg = RectangleGrid(cols=3, rows=4, start="SW", direction="north", pattern="outer")
Layout(rg, shapes=[small_box,])
PageBreak()

Save()
