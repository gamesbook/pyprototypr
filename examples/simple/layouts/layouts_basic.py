# -*- coding: utf-8 -*-
"""
Virtual layout examples for pyprototypr

Written by: Derek Hohls
Created on: 19 May 2024
"""
from pyprototypr import *

Create(filename="layouts_basic.pdf",
       pagesize=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2)

header = Common(x=0, y=6, font_size=6, align="left")
circles = Common(x=0, y=0, diameter=1.0, label="{count}/{col}-{row}", label_size=6)
a_circle = circle(common=circles)

Blueprint(stroke_width=0.5)
Text(common=header, text="RectangularLayout: debug + no label")
rect = RectangularLayout(cols=3, rows=4)
Layout(rect, debug='n')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="RectangularLayout: debug + count")
rect = RectangularLayout(cols=3, rows=4)
Layout(rect, debug='c')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="RectangularLayout: NW->east")
rect = RectangularLayout(cols=3, rows=4, start="NW", direction="east")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NW->east: even col shift")
rect = RectangularLayout(cols=3, rows=4, start="NW", direction="east", col_even=0.5)
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NW->east: odd row shift")
rect = RectangularLayout(cols=3, rows=4, start="NW", direction="east", row_odd=-0.5)
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NW->east: snake")
rect = RectangularLayout(cols=3, rows=4, start="NW", direction="east", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NW->east: Outer")
rect = RectangularLayout(cols=3, rows=4, start="NW", direction="east", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NW->east: Outer+Hidden")
rect = RectangularLayout(cols=3, rows=4, start="NW", direction="east", pattern="outer")
Layout(rect, shapes=[a_circle], hidden=[2,7])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: NW->east: Outer+Shown")
rect = RectangularLayout(cols=3, rows=4, start="NW", direction="east", pattern="outer")
Layout(rect, shapes=[a_circle], shown=[1,3,6,8])
PageBreak()

Save()
