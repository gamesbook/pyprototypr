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
Text(common=header, text="TriangularLayout: debug + no label")
tri = TriangularLayout()
Layout(tri, debug='n')
PageBreak()

# ---- default sizes - all facings

Blueprint(stroke_width=0.5)
Text(common=header, text="TriangularLayout: North/debug + no label")
tri = TriangularLayout(facing='north')
Layout(tri, debug='c', )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="TriangularLayout: East/debug + no label")
tri = TriangularLayout(facing='east')
Layout(tri, debug='c', )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="TriangularLayout: South/debug + no label")
tri = TriangularLayout(facing='south')
Layout(tri, debug='c', )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="TriangularLayout: West/debug + no label")
tri = TriangularLayout(facing='west')
Layout(tri, debug='c', )
PageBreak()

# ---- east facing; multirows

Blueprint(stroke_width=0.5)
Text(common=header, text="TriangularLayout: East/2 rows + debug")
tri = TriangularLayout(facing='east', x=4, y=3, side=.75, rows=2)
Layout(tri, debug='c', )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="TriangularLayout: East/4 rows + debug")
tri = TriangularLayout(facing='east', x=4, y=3, side=.75, rows=4)
Layout(tri, debug='c', )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="TriangularLayout: East/6 rows + debug")
tri = TriangularLayout(facing='east', x=4, y=3, side=.75, rows=6)
Layout(tri, debug='c', )
PageBreak()

# ---- north facing; multicols

Blueprint(stroke_width=0.5)
Text(common=header, text="TriangularLayout: North/2 cols + debug")
tri = TriangularLayout(facing='north', y=5, x=2, side=.66, cols=2)
Layout(tri, debug='c', )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="TriangularLayout: North/4 cols + debug")
tri = TriangularLayout(facing='north', y=5, x=2, side=.66, cols=4)
Layout(tri, debug='c', )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="TriangularLayout: North/6 cols + debug")
tri = TriangularLayout(facing='north', y=5, x=2, side=.66, cols=6)
Layout(tri, debug='c', )
PageBreak()

# ---- layout with shapes

circles = Common(x=0, y=0, diameter=1.0, label="{count}/{col}-{row}", label_size=6)
a_circle = circle(common=circles)

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Layout: Facing->east; 3 rows; side=dia")
tri = TriangularLayout(side=1.0, rows=3, x=3, y=3, facing="east")
Layout(tri, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Tri.Layout: Facing->south; 3 cols; side=dia")
tri = TriangularLayout(side=1.0, cols=3, x=2, y=2, facing="south")
Layout(tri, shapes=[a_circle,])
PageBreak()

#Save(directory="/tmp/dtest", output='png', names=[None]*10 + ['a','b','c'])
Save()
