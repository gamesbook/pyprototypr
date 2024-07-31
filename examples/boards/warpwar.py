"""
A WarpWar map example for pyprototypr

The original map was created by Rick Smith and posted to https://groups.io/g/warpwar/
forum on 3 June 2024.

Code by: Derek Hohls
Created on: 30 July 2024
"""

from pyprototypr.draw import *

Create(filename="warpwar.pdf", margin=0.5, pagesize=A2)

# set map colors
map_fill = black
map_border = lightgrey
grid_line = "#AA9A38 "
system_label = "#1CAEE5"
warp_line = "#2ACD21"
# set star colors
small_red = "#FE1200"
big_orange = "#EC600C"
brown = "#6A4D05 "
# set nebula colors
cloud_edge = "#890B81"
cloud_lite = "#C23E83"
cloud_med = "#711F61"
cloud_dark = "#4D173E"

Rectangle(x=0.0, y=0.0, width=41, height=58.3, stroke=map_border, fill=map_fill)

# title line
txt = Common(y=57.5, font_size=21, align="left", stroke=white)
Text(common=txt, x=3,  text="2 Player Warp War Map:      Vedem Sector")
Text(common=txt, x=22, text="(c) 2024 by Richard W. Smith")

ww_grid = Hexagons(
    cols=20,
    rows=24,
    y=1.8,
    height=2.22,
    hex_offset="even",
    coord_position="t",
    coord_type_y="upper-multiple",
    coord_offset=-0.15,
    coord_font_size=12,
    coord_stroke=grid_line,
    coord_padding=0,
    coord_style="diagonal",
    fill=map_fill,
    stroke=grid_line,
)

print(f'{ww_grid}')

Save()
