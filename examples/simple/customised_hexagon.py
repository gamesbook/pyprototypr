"""
Show customised Hexagon for pyprototypr

Written by: Derek Hohls
Created on: 19 September 2024
"""

from pyprototypr import *

Create(filename="customised_hexagon.pdf",
       pagesize=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2,
       font_size=8)
Footer(draw=False)

txt = Common(x=0, y=6, font_size=8, align="left")

Text(common=txt, text="Hexagon START...")
PageBreak(footer=True)

# ---- centre placement
Blueprint()
Text(common=txt, text="Hexagon: cx=2, cy=3")
Hexagon(cx=2, cy=3)
PageBreak()

# ---- dot & cross
Blueprint()
Text(common=txt, text="Dots & Crosses")
Hexagon(x=-0.25, y=4, height=2, dot_size=0.1, dot_stroke=red)
Hexagon(x=1.75, y=3.5, height=2, cross_size=0.25, cross_stroke=red, cross_stroke_width=1)
Hexagon(x=0, y=1, height=2, dot_size=0.1, dot_stroke=red,
        orientation='pointy')
Hexagon(x=2, y=1, height=2, cross_size=0.25, cross_stroke=red, cross_stroke_width=1,
        orientation='pointy')
PageBreak()

# ---- hatch
Blueprint()
Text(common=txt, text="Hexagon: hatch + directions")
hxgn = Common(height=1.5, hatch=5, hatch_stroke=red)
Hexagon(common=hxgn, x=0, y=0, orientation='flat', hatch_directions='e', label="e/w")
Hexagon(common=hxgn, x=2, y=0, orientation='pointy', hatch_directions='n', label="n/s")
Hexagon(common=hxgn, x=0, y=2, orientation='flat', hatch_directions='ne', label="ne/sw")
Hexagon(common=hxgn, x=2, y=2, orientation='pointy', hatch_directions='ne', label="ne/sw")
Hexagon(common=hxgn, x=0, y=4, orientation='flat', hatch_directions='nw', label="nw/se")
Hexagon(common=hxgn, x=2, y=4, orientation='pointy', hatch_directions='nw', label="nw/se")
PageBreak()

# ---- hatch + text
Blueprint()
Text(common=txt, text="Hexagon: flat; text; hatch")
Hexagon(
    y=2,
    height=2,
    hatch=3,
    hatch_stroke=red,
    debug=True,
    title="Title",
    label="Label",
    heading="Heading")
PageBreak()

Blueprint()
Text(common=txt, text="Hexagon: pointy; text; hatch")
Hexagon(
    y=2,
    height=2,
    hatch=5,
    hatch_stroke=red,
    orientation='pointy',
    title="Title",
    heading="Heading")
PageBreak()

# ---- radii - pointy
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hex Pointy: radii")
hxg = Common(height=1.5, dot_size=0.05, dot_stroke=red, orientation="pointy", font_size=8)
Hexagon(common=hxg, x=0.25, y=0.25, radii='sw', label="SW")
Hexagon(common=hxg, x=0.25, y=2.15, radii='nw', label="NW")
Hexagon(common=hxg, x=0.25, y=4, radii='n', label="N")
Hexagon(common=hxg, x=2.25, y=4, radii='ne', label="NE")
Hexagon(common=hxg, x=2.25, y=0.25, radii='s', label="S")
Hexagon(common=hxg, x=2.25, y=2.15, radii='se', label="SE")
PageBreak()

# ---- radii - flat
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hex Flat: radii")
hxg = Common(height=1.5, dot_size=0.05, dot_stroke=red, orientation="flat", font_size=8)
Hexagon(common=hxg, x=0.25, y=0.25, radii='sw', label="SW")
Hexagon(common=hxg, x=0.25, y=2.15, radii='w', label="W")
Hexagon(common=hxg, x=0.25, y=4, radii='nw', label="NW")
Hexagon(common=hxg, x=2.25, y=4, radii='ne', label="NE")
Hexagon(common=hxg, x=2.25, y=2.15, radii='e', label="E")
Hexagon(common=hxg, x=2.25, y=0.25, radii='se', label="SE")
PageBreak()

# ---- END
Text(common=txt, text="Hexagon END...")
PageBreak(footer=True)

Save()
# Save(output='png', dpi=600)
