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
Text(common=header, text="Layout: RectangleGrid: BL/right")
rg = RectangleGrid(cols=3, rows=3, start="BL", direction="right")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: TL/down")
rg = RectangleGrid(cols=3, rows=3, start="TL", direction="down")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: TR/left")
rg = RectangleGrid(cols=3, rows=3, start="TR", direction="left")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: BR/up")
rg = RectangleGrid(cols=3, rows=3, start="BR", direction="up")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: BL/up: Snake")
rg = RectangleGrid(cols=3, rows=4, start="BL", direction="up", pattern="snake")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: TL/down: Snake")
rg = RectangleGrid(cols=3, rows=4, start="TL", direction="down", pattern="snake")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: BL/right: Snake")
rg = RectangleGrid(cols=3, rows=4, start="BL", direction="right", pattern="snake")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: BR/left: Snake")
rg = RectangleGrid(cols=3, rows=4, start="BR", direction="left", pattern="snake")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: BL/right: Outer")
rg = RectangleGrid(cols=3, rows=4, start="BL", direction="right", pattern="outer")
Layout(rg, shapes=[small_box,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: BL/up: Outer")
rg = RectangleGrid(cols=3, rows=4, start="BL", direction="up", pattern="outer")
Layout(rg, shapes=[small_box,])
PageBreak()

Save()
