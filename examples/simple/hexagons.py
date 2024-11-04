"""
Show customisation options for hexagons pyprototypr

Written by: Derek Hohls
Created on: 9 April 2024
"""

from pyprototypr import *

Create(filename="customised_hexagons.pdf",
       paper=A8,
       margin=0.75,
       margin_right=0.2, margin_top=0.2,
       font_size=8,
       stroke_width=0.5)

header = Common(x=0, y=6, font_size=8, align="left")

Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: flat (F)")
Hexagons(
    side=0.5,
    x=0, y=0,
    rows=3, cols=3,
)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: pointy (P)")
Hexagons(
    side=0.5,
    x=0, y=0,
    rows=3, cols=3,
    orientation='pointy',
)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: coordinates (flat)")
Hexagons(
    side=0.6,
    x=0, y=0,
    rows=2, cols=2,
    coord_position="middle", coord_prefix='z',
)
Hexagons(
    side=0.6,
    x=2, y=3,
    rows=2, cols=2,
    fill=darkseagreen,
    hex_offset="odd",
    coord_position="top", coord_type_x="upper", coord_separator='::',
)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: coordinates (pointy)")
Hexagons(
    side=0.6,
    x=0, y=0,
    rows=2, cols=2,
    orientation='pointy',
    coord_position="middle", coord_prefix='z',
)
Hexagons(
    side=0.6,
    x=1, y=3,
    rows=2, cols=2,
    orientation='pointy',
    fill=darkseagreen,
    hex_offset="odd",
    coord_position="top", coord_type_x="upper", coord_separator='::',
)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: caltrops&dots (flat)")
Hexagons(
    side=0.6,
    rows=3, cols=3,
    x=0, y=0,
    dot_size=0.04,
    caltrops="medium",
)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: caltrops&dots (pointy)")
Hexagons(
    side=0.6,
    rows=3,cols=3,
    orientation='pointy',
    x=0, y=0,
    dot_size=0.04,
    caltrops="large",
)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: rows & cols // even")
Hexagons(
    side=0.5,
    x=0, y=0,
    rows=3, cols=3,
    coord_position="middle", coord_font_size=5,
    coord_separator=' r', coord_prefix='c',
)
Hexagons(
    side=0.5,
    x=1, y=3,
    rows=3, cols=3,
    orientation='pointy',
    coord_position="middle", coord_font_size=5,
    coord_separator=' r', coord_prefix='c',
)
PageBreak()


Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: rows & cols // odd")
Hexagons(
    side=0.5,
    x=0, y=0,
    rows=3, cols=3,
    hex_offset="odd",
    coord_position="middle", coord_font_size=5,
    coord_separator=' r', coord_prefix='c',
)
Hexagons(
    side=0.5,
    x=1, y=3,
    rows=3, cols=3,
    hex_offset="odd",
    orientation='pointy',
    coord_position="middle", coord_font_size=5,
    coord_separator=' r', coord_prefix='c',
)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: hidden")
Hexagons(
    side=0.5,
    x=1, y=3,
    rows=3, cols=3,
    orientation='pointy',
    hidden=[[1, 2,], [3, 3]]
)
Hexagons(
    side=0.5,
    x=0, y=0,
    rows=3, cols=3,
    hidden=[[2, 1,], [2, 3]]
)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: radii")
Hexagons(
    side=0.5,
    x=0.5, y=0,
    rows=3, cols=3,
    hex_offset="odd",
    radii="w ne se",
)
Hexagons(
    side=0.5,
    x=1.25, y=3,
    rows=3, cols=3,
    stroke=red,
    radii_stroke=red,
    hex_offset="even",
    radii="e nw sw",
)
PageBreak()


Save()
