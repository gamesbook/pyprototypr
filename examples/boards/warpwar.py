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
warp = "#2ACD21"
# set star colors
m_red = "#FE1200"
k_orange = "#EC600C"
d_brown = "#6A4D05 "
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

# numbered map grid
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
    stroke_width=2,
)

# star properties
dstar = Common(fill=d_brown, stroke=d_brown, radius=0.2)
kstar = Common(fill=k_orange, stroke=k_orange, radius=0.2)
mstar = Common(fill=m_red, stroke=m_red, radius=0.1)
sname = Common(font_size=12, align="centre", stroke=system_label)
mask = rectangle(height=0.5, width=1.2, fill=map_fill, stroke=map_fill, dx=-0.6, dy=0.55)
dwarf_outer = circle(fill=d_brown, stroke=d_brown, radius=0.2),
dwarf_inner = rectangle(height=0.1, width=0.1, fill=map_fill, stroke=map_fill),

# system details at map locations
Location(
    ww_grid,
    "2B",
    [
     mask,
     circle(common=mstar, dx=-0.1, dy=0.8),
     circle(common=mstar, dx=-0.6, dy=-0.5),
     text(common=sname, dx=-0.3, dy=-0.1, text="Redstar\n    3"),
    ])

Location(
    ww_grid,
    "4B",
    [
     circle(common=mstar, dx=-0.6, dy=-0.7),
     text(common=sname, dx=-0.4, dy=-0.1, text="Lattur\n     2"),
    ])

Location(
    ww_grid,
    "4E",
    [
     mask,
     circle(common=mstar, dx=0.2, dy=0.8),
     text(common=sname, dx=0.0, dy=-0.1, text="Rebb\n1"),
    ])

Location(
    ww_grid,
    "1C",
    [
     circle(common=kstar, dx=0.5, dy=0.0),
     text(common=sname, dx=-0.4, dy=-0.1, text="Bezsin\n      4"),
    ])

Location(
    ww_grid,
    "8L",
    [
     hexagon(fill=cloud_dark, stroke=cloud_dark, height=2.15, dx=0, dy=0),
     circle(common=kstar, dx=-0.5, dy=-0.6),
     text(common=sname, dx=0.4, dy=0.1, text="Highlakes\n    3"),
    ])

Location(
    ww_grid,
    "7F",
    [
     mask,
     text(common=sname, dx=-0.4, dy=0.4, text="  BD7F\nREE+4\n  2"),
     #group(dwarf_outer, dwarf_inner, dx=0.1, dy=-0.8),
    ])

# warp lines
warp_line = Common(stroke=warp, stroke_width=3)

Linker(ww_grid, [("2B", -0.5, -0.7), ("4E", 0.05, 0.9)], common=warp_line)
Linker(ww_grid, [("2B", 0.15, 0.85), ("4B", -0.75, -0.8)], common=warp_line)
Linker(ww_grid, [("4E", 0.25, 1.05), ("4B", -0.6, -0.9)], common=warp_line)
Linker(ww_grid, [("1C", 0.75, -0.2), ("8L", -0.6, 0.3)], common=warp_line)

Save()
