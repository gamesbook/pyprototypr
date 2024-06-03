# -*- coding: utf-8 -*-
"""
Virtual track examples for pyprototypr

Written by: Derek Hohls
Created on: 26 May 2024
"""
from pyprototypr.draw import *

Create(filename="track_layout.pdf",
       pagesize=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2)

header = Common(x=0, y=6, font_size=6, align="left")
Text(common=header, text="Track: Rectangle: BL~clockwise")
AutoGrid(stroke_width=0.5)

boxes = Common(x=0, y=0, height=0.5, width=0.5, fill=None, label="{count}", label_size=6)
small_box = square(common=boxes)
rg = RectangleTrack(height=1, width=1, start="BL", direction="clockwise")
Track(rg, shapes=[small_box,], spaces=8)
#Track()


PageBreak()
Save()
