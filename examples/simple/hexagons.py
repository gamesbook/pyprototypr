"""
Show customisation options for hexagons pyprototypr

Written by: Derek Hohls
Created on: 9 April 2024
"""

from pyprototypr.draw import *

Create(filename="customised_hexagons.pdf",
       pagesize=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2)

header = Common(x=0, y=6, font_size=8, align="left")

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagons: flat (F)")
Hexagons(
    height=1,
    x=0, y=0,
    rows=3, cols=3,
)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagons: pointy (P)")
Hexagons(
    height=1,
    x=0, y=0,
    rows=3, cols=3,
    hex_orientation='pointy',
)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagons: coordinates (F)")
Hexagons(
    height=1.1,
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

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagons: coordinates (P)")
Hexagons(
    height=1.1,
    x=0, y=0,
    rows=2, cols=2,
    hex_orientation='pointy',
    coord_position="middle", coord_prefix='z',
)
Hexagons(
    side=0.6,
    x=2, y=3,
    rows=2, cols=2,
    hex_orientation='pointy',
    fill=darkseagreen,
    hex_offset="odd",
    coord_position="top", coord_type_x="upper", coord_separator='::',
)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagons: caltrops&dots (F)")
Hexagons(
    height=1.5,
    rows=2,cols=2,
    x=0, y=0,
    dot_size=0.04,
    caltrops="medium",
)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagons: caltrops&dots (P)")
Hexagons(
    height=1.5,
    rows=2,cols=2,
    hex_orientation='pointy',
    x=0, y=0,
    dot_size=0.04,
    caltrops="medium",
)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagons: rows & cols // even")
Hexagons(
    height=0.7,
    x=0, y=0,
    rows=3, cols=3,
    coord_position="middle", coord_font_size=5,
    coord_separator=' r', coord_prefix='c',
)
Hexagons(
    height=0.7,
    x=1, y=3,
    rows=3, cols=3,
    hex_orientation='pointy',
    coord_position="middle", coord_font_size=5,
    coord_separator=' r', coord_prefix='c',
)
PageBreak()


AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagons: rows & cols // odd")
Hexagons(
    height=0.7,
    x=0, y=0,
    rows=3, cols=3,
    hex_offset="odd",
    coord_position="middle", coord_font_size=5,
    coord_separator=' r', coord_prefix='c',
)
Hexagons(
    height=0.7,
    x=1, y=3,
    rows=3, cols=3,
    hex_offset="odd",
    hex_orientation='pointy',
    coord_position="middle", coord_font_size=5,
    coord_separator=' r', coord_prefix='c',
)
PageBreak()

AutoGrid(stroke_width=0.5)
Text(common=header, text="Hexagons: masked")
Hexagons(
    height=0.7,
    x=1, y=3,
    rows=3, cols=3,
    hex_orientation='pointy',
    masked=[[1, 2,], [3, 3]]
)
Hexagons(
    height=0.7,
    x=0, y=0,
    rows=3, cols=3,
    masked=[[2, 1,], [2, 3]]
)
PageBreak()

Save()
