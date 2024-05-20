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
header = Common(x=0, y=6, font_size=8, align="left")

AutoGrid(stroke_width=0.5)
Text(common=header, text="layout: RectangleGrid")
small_box = square(x=0, y=0, height=1.0, label="z")
rg = RectangleGrid(rows=2, cols=2)
Layout(rg, shapes=[small_box,])
PageBreak()

Save()
