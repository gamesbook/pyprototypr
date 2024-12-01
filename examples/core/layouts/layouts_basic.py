# -*- coding: utf-8 -*-
"""
Virtual layout examples for pyprototypr

Written by: Derek Hohls
Created on: 19 May 2024
"""
from pyprototypr import *

Create(filename="layouts_basic.pdf",
       paper=A8,
       margin=0.75,
       margin_right=0.2, margin_top=0.2,
       font_size=10,
       stroke_width=0.5)

header = Common(x=0, y=6, font_size=7, align="left")
circles = Common(x=0, y=0, diameter=1.0, label="{count}/{col}-{row}", label_size=6)
a_circle = circle(common=circles)

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: debug > no label")
rect = RectangularLocations(cols=3, rows=4)
Layout(rect, debug='none')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rec.Locations: debug > count")
rect = RectangularLocations(cols=3, rows=4)
Layout(rect, debug='count')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rec.Locations: debug > xy")
rect = RectangularLocations(cols=3, rows=4)
Layout(rect, debug='xy')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: default")
rect = RectangularLocations(cols=3, rows=4)
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->east")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW/east: even col shift")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east", col_even=0.5)
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW/east: odd row shift")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east", row_odd=-0.5)
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW/east: snake")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW/east: Outer")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW/east: Outer+Masked")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east", pattern="outer")
Layout(rect, shapes=[a_circle], masked=[2,7])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW/east: Outer+Visible")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east", pattern="outer")
Layout(rect, shapes=[a_circle], visible=[1,3,6,8])
PageBreak()

# Save()
Save(
     output='png',
     dpi=300,
     directory="docs/images/layouts",
     names=[
        "rect_basic_debug", "rect_basic_debug_count", "rect_basic_debug_xy",
        "rect_basic_default",
        "rect_basic_east", "rect_basic_east_even",  "rect_basic_east_odd",
        "rect_basic_snake",
        "rect_basic_outer", "rect_basic_outer_mask", "rect_basic_outer_visible",
     ]
)
