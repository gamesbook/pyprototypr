# -*- coding: utf-8 -*-
"""
Layout examples of multiple shapes on outer edge of Rectangle for pyprototypr

Written by: Derek Hohls
Created on: 15 September 2024
"""
from pyprototypr import *

Create(filename="layouts_shapes_outer.pdf",
       pagesize=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2)

header = Common(x=0, y=6, font_size=6, align="left")
sqr_common = Common(label="{count_zero}")
sqr = square(common=sqr_common, side=0.9, label_size=6)
sqr5 = square(common=sqr_common, side=1.0, label_size=8, fill=yellow)
rct_common = Common(label="{count}", label_size=5, rounding=0.05, )

# ---- multi-shapes

# Blueprint(stroke_width=0.5)
# Text(common=header, text="Rect.Layout: SW->north/Outer")
# rect = RectangularLayout(
#     x=0.5, y=0.5, cols=4, rows=5, start="SW", direction="north", pattern="outer")
# Layout(rect, shapes=[sqr5] + [sqr]*4)
# PageBreak()

# ---- single shape + stop

# rct1 = rectangle(common=rct_common, height=0.48, width=0.48, fill=lightgreen)
# Blueprint(stroke_width=0.5)
# Text(common=header, text="Rect.Layout: NW->east + stop")
# rect = RectangularLayout(
#     x=0.25, y=-0.75, cols=8, rows=12, interval=0.5, stop=17,
#     start="NW", direction="east", pattern="outer")
# Layout(rect, shapes=[rct1])
# PageBreak()

# ---- rotation + corners

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Layout: SW->north/Outer + rotate")
rct2 = rectangle(common=rct_common, height=0.64, width=0.48, fill=tan)
rct3 = rectangle(common=rct_common, height=0.64, width=0.48, fill=maroon, stroke=white)
rrect = RectangularLayout(
    x=0.5, y=0.5, cols=4, rows=5,  interval=0.5,
    start="SW", direction="north", pattern="outer")
Layout(rrect, shapes=[rct3] + [rct2]*4, rotations=[("1-5", 45)])
PageBreak()

Save()
