"""
Show customised Hexagons grid locations and linklines for pyprototypr

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
a_circle = Common(radius=0.4)


# ---- location - single shape
Blueprint(stroke_width=0.5)
Text(common=header, text="Location: single shape")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
)
Location(
    hexgrid,
    "0101",
    [circle(common=a_circle)]
)
PageBreak()

# ---- location - multiple shapes
Blueprint(stroke_width=0.5)
Text(common=header, text="Location: multiple shapes")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
)
Location(
    hexgrid,
    "0101",
    [circle(common=a_circle), dot()]
)
PageBreak()

# ---- locations - multiple shapes
Blueprint(stroke_width=0.5)
Text(common=header, text="Locations: multiple shapes")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
)
Locations(
    hexgrid,
    "0204, 0101",
    [circle(common=a_circle), dot()]
)
PageBreak()

# ---- locations - sequence numbers
Blueprint(stroke_width=0.5)
Text(common=header, text="Locations: sequence numbers")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
)
Locations(
    hexgrid,
    "all",
    [circle(common=a_circle, label="s{{sequence}}")]
)
PageBreak()

# ---- locations - col & row numbers
Blueprint(stroke_width=0.5)
Text(common=header, text="Locations: col&row")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
)
Locations(
    hexgrid,
    "all",
    [circle(common=a_circle, label="c{{col}}r{{row}}")]
)
PageBreak()

# ---- locations - labels
Blueprint(stroke_width=0.5)
Text(common=header, text="Locations: labels")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
)
Locations(
    hexgrid,
    "all",
    [circle(common=a_circle, label="l{{label}}")]
)
PageBreak()


Save(
    output='png',
    dpi=300,
    directory="docs/images/custom/hexagonal_grid",
    names=[
        "hexgrid_location_single", "hexgrid_location_multiple",
        "hexgrid_locations_multi",
        "hexgrid_locations_seq", "hexgrid_locations_colrow", "hexgrid_locations_labels",
    ]
)
