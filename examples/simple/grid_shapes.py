# -*- coding: utf-8 -*-
"""
Virtual grid examples for pyprototypr

Written by: Derek Hohls
Created on: 19 May 2024
"""
from pyprototypr.draw import *

Create(filename="grid_layout.pdf",
       pagesize=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2)
header = Common(x=0, y=6, font_size=6, align="left")
boxes = Common(x=0, y=0, height=1.0, label="N:{count}/{col}-{row}", label_size=6)


AutoGrid(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: BL/right")
small_box = square(common=boxes)
rg = RectangleGrid(cols=3, rows=3, start="BL", direction="right")
Layout(rg, shapes=[small_box,])
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: BR/up")
small_box = square(common=boxes)
rg = RectangleGrid(cols=3, rows=3, start="BR", direction="up")
Layout(rg, shapes=[small_box,])
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: TR/left")
small_box = square(common=boxes)
rg = RectangleGrid(cols=3, rows=3, start="TR", direction="left")
Layout(rg, shapes=[small_box,])
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: TL/down")
small_box = square(common=boxes)
rg = RectangleGrid(cols=3, rows=3, start="TL", direction="down")
Layout(rg, shapes=[small_box,])
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Layout: RectangleGrid: BL/right: Outer")
small_box = square(common=boxes)
rg = RectangleGrid(cols=3, rows=4, start="BL", direction="right", pattern="outer")
Layout(rg, shapes=[small_box,])
PageBreak()

Save()
