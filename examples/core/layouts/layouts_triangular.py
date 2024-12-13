# -*- coding: utf-8 -*-
"""
Virtual layout examples for pyprototypr

Written by: Derek Hohls
Created on: 14 September 2024
"""
from pyprototypr import *

Create(filename="layouts_basic_triangular.pdf",
       paper=A8,
       margin=0.75,
       margin_right=0.2, margin_top=0.2,
       font_size=8,
       stroke_width=0.5)

header = Common(x=0, y=6, font_size=6, align="left")

# ---- all defaults

Blueprint(stroke_width=0.5)
Text(common=header, text="TriangularLocations: debug + no label")
tri = TriangularLocations()
Locations(tri, [], [], debug='n')
PageBreak()

# ---- default sizes - all facings

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: North/debug + no label")
tri = TriangularLocations(facing='north')
Locations(tri, debug='c', )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: East/debug + no label")
tri = TriangularLocations(facing='east')
Locations(tri, debug='c', )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: South/debug + no label")
tri = TriangularLocations(facing='south')
Locations(tri, debug='c', )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: West/debug + no label")
tri = TriangularLocations(facing='west')
Locations(tri, debug='c', )
PageBreak()

# ---- east facing; multirows

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: East/2 rows + debug")
tri = TriangularLocations(facing='east', x=4, y=3, side=.75, rows=2)
Locations(tri, debug='c', )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: East/4 rows + debug")
tri = TriangularLocations(facing='east', x=4, y=3, side=.75, rows=4)
Locations(tri, debug='c', )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: East/6 rows + debug")
tri = TriangularLocations(facing='east', x=4, y=3, side=.75, rows=6)
Locations(tri, debug='c', )
PageBreak()

# ---- north facing; multicols

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: North/2 cols + debug")
tri = TriangularLocations(facing='north', y=5, x=2, side=.66, cols=2)
Locations(tri, debug='c', )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: North/4 cols + debug")
tri = TriangularLocations(facing='north', y=5, x=2, side=.66, cols=4)
Locations(tri, debug='c', )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: North/6 cols + debug")
tri = TriangularLocations(facing='north', y=5, x=2, side=.66, cols=6)
Locations(tri, debug='c', )
PageBreak()

# ---- layout with shapes

circles = Common(x=0, y=0, diameter=1.0, label="{{sequence}}//{{col}}-{{row}}", label_size=6)
a_circle = circle(common=circles)

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: Facing->east; 3 rows; side=dia")
tri = TriangularLocations(side=1.0, rows=3, x=3, y=3, facing="east")
Locations(tri, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Locations: Facing->south; 3 cols; side=dia")
tri = TriangularLocations(side=1.0, cols=3, x=2, y=2, facing="south")
Locations(tri, shapes=[a_circle,])
PageBreak()

Save()
# Save(
#      output='png',
#      dpi=300,
#      directory="docs/images/layouts",
#      names=[
#         "layout_tri_..",
#      ]
# )
