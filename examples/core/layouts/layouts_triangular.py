# -*- coding: utf-8 -*-
"""
Virtual layout examples for protograf

Written by: Derek Hohls
Created on: 14 September 2024
"""
from protograf import *

Create(filename="layouts_basic_triangular.pdf",
       paper=A8,
       margin=0.75,
       margin_right=0.2, margin_top=0.2,
       font_size=8,
       stroke_width=0.5)

header = Common(x=0, y=6, font_size=6, align="left")
d_circle = circle(x=0, y=0, radius=0.33)
a_circle = circle(
    x=0, y=0, diameter=1.0, label="{{sequence}}//{{col}}-{{row}}", label_size=6)

# ---- all defaults

Blueprint(stroke_width=0.5)
Text(common=header, text="TriangularLocations: default/debug")
tri = TriangularLocations()
Layout(tri, shapes=[d_circle,], debug='cr')
PageBreak()

# ---- east facing; multirows

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: East/2 rows + debug")
tri = TriangularLocations(facing='east', x=4, y=3, side=.66, rows=2)
Layout(tri, shapes=[d_circle,], debug='cr')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: East/6 rows + debug")
tri = TriangularLocations(facing='east', x=4, y=3, side=.66, rows=6)
Layout(tri, shapes=[d_circle,], debug='cr')
PageBreak()

# ---- north facing; multicols

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: North/2 cols + debug")
tri = TriangularLocations(facing='north', y=5, x=2, side=.66, cols=2)
Layout(tri, shapes=[d_circle,], debug='cr')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: North/6 cols + debug")
tri = TriangularLocations(facing='north', y=5, x=2, side=.66, cols=6)
Layout(tri, shapes=[d_circle,], debug='cr')
PageBreak()

# ---- layout with labelled shape

circles = Common(x=0, y=0, diameter=1.0, label="{{sequence}}//{{col}}-{{row}}", label_size=6)
a_circle = circle(common=circles)

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: West; 3 rows; side=dia")
tri = TriangularLocations(side=1.0, rows=3, x=1, y=3, facing="west")
Layout(tri, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: South; 3 cols; side=dia")
tri = TriangularLocations(side=1.0, cols=3, x=2, y=2, facing="south")
Layout(tri, shapes=[a_circle,])
PageBreak()

# Save()
Save(
     output='png',
     dpi=300,
     directory="docs/images/layouts",
     names=[
        "layout_tri_default",
        "layout_tri_east_row2", "layout_tri_east_row6",
        "layout_tri_east_col2", "layout_tri_east_col6",
        "layout_tri_west_row3", "layout_tri_south_col3",
     ]
)
