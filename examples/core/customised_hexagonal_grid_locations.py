"""
Show customised Hexagons grid locations for pyprototypr

Written by: Derek Hohls
Created on: 7 December 2024
"""

from pyprototypr import *

Create(
    filename="customised_hexagonal_grid_locations.pdf",
    paper=A8,
    margin=0.75,
    margin_right=0.2, margin_top=0.2,
    font_size=8,
    stroke_width=0.5
)

Footer(draw=False)

header = Common(x=0, y=6, font_size=8, align="left")
a_circle = Common(radius=0.2)

# ---- locastion -default coords
Blueprint(stroke_width=0.5)
Text(common=header, text="Locations: single")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
)
Locations(
    hexgrid,
    "0204, 0101",
    [circle(common=a_circle, label="{row}")]
)
PageBreak()

# ---- rectangular - flat
# Blueprint(stroke_width=0.5)
# Text(common=header, text="Locations: single;coord")
# hexgrid = Hexagons(
#     side=0.5,
#     x=0, y=0,
#     rows=6, cols=4,
#     coord_type_x="upper"
# )
# Location(
#     hexgrid,
#     "B2",
#     [circle(common=a_circle)]
# )
# PageBreak()

Save(
    output='png',
    dpi=300,
    directory="docs/images/custom/hexagonal_grid",
    names=[
        "hexgrid_location", "hexgrid_location_coord",
    ]
)
