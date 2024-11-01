"""
Show customised Circles - and useful overides - for pyprototypr

Written by: Derek Hohls
Created on: 29 September 2024
"""

from pyprototypr import *

Create(filename="customised_circles.pdf",
       paper=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2,
       font_size=8)
Footer(draw=False)

txt = Common(x=0, y=6, font_size=8, align="left")

Text(common=txt, text="Circle START...")
PageBreak(footer=True)

# ---- circle hatch
Blueprint()
Text(common=txt, text="Circle: hatch")
Circle(cx=2, cy=5.2, radius=.7, hatch_stroke=red, hatch=4, label='4')  # all directions
Circle(cx=1, cy=3.7, radius=.7, hatch_stroke=red, hatch=5, hatch_directions='o', label='o')
Circle(cx=3, cy=3.7, radius=.7, hatch_stroke=red, hatch=5, hatch_directions='d', label='d')
Circle(cx=1, cy=2.2, radius=.7, hatch_stroke=red, hatch=5, hatch_directions='e', label='e')
Circle(cx=3, cy=2.2, radius=.7, hatch_stroke=red, hatch=5, hatch_directions='n', label='n')
Circle(cx=1, cy=0.7, radius=.7, hatch_stroke=red, hatch=5, hatch_directions='ne', label='ne')
Circle(cx=3, cy=0.7, radius=.7, hatch_stroke=red, hatch=7, hatch_directions='nw', label='nw')
PageBreak()

# ---- circle dot & cross
Blueprint()
Text(common=txt, text="Circle: Dots & Crosses")
Circle(cx=1, cy=1, radius=1, dot=0.1, dot_stroke=green)
Circle(cx=3, cy=1, radius=1, cross=0.25, cross_stroke=green, cross_stroke_width=1)
PageBreak()

# ---- circle radii
Blueprint()
Text(common=txt, text="Circle: radii (single & overlapped)")
Circle(x=0, y=0, radius=2,
       radii=[45,135,225,315],
       radii_stroke_width=1,
       radii_dotted=1,
       radii_offset=0.5,
       radii_length=1.25)
Circle(x=0, y=0, radius=2,
       fill=None,
       radii=[0,90,180,270],
       radii_stroke_width=3,
       radii_stroke=red)
Circle(cx=3, cy=5, radius=1,
       fill=green,
       stroke=orange,
       stroke_width=1,
       radii=[0,90,180,270,45,135,225,315],
       radii_stroke_width=8,
       radii_stroke=orange,
       radii_length=0.8)
PageBreak()

# ---- circle petals
Blueprint()
Text(common=txt, text="Circle: petals; triangle style")
Circle(cx=2, cy=1.5, radius=1,
        petals=11,
        petals_offset=0.25,
        petals_stroke_width=1,
        petals_dotted=1,
        petals_height=0.25,
        petals_fill=grey)
Circle(cx=2, cy=4.5, radius=1,
       stroke=None,
       fill=None,
       petals=8,
       petals_stroke_width=3,
       petals_height=0.25,
       petals_stroke=red,
       petals_fill=yellow)
PageBreak()

# ---- circle petals
Blueprint()
Text(common=txt, text="Circle: petals; curve style")
Circle(cx=2, cy=1.5, radius=1,
        petals=11,
        petals_style="curve",
        petals_offset=0.25,
        petals_stroke_width=1,
        petals_dotted=1,
        petals_height=0.5,
        petals_fill=grey)
Circle(cx=2, cy=4.5, radius=1,
       stroke=None,
       fill=None,
       petals=8,
       petals_style="c",
       petals_stroke_width=3,
       petals_height=0.5,
       petals_stroke=red,
       petals_fill=yellow)
PageBreak()

# ---- circle petals
Blueprint()
Text(common=txt, text="Circle: petals; petal style")
Circle(cx=2, cy=1.5, radius=1,
        petals=11,
        petals_style="petal",
        petals_offset=0.25,
        petals_stroke_width=1,
        petals_dotted=1,
        petals_height=0.25,
        petals_fill=grey)
Circle(cx=2, cy=4.5, radius=1,
       stroke=None,
       fill=None,
       petals=8,
       petals_style="p",
       petals_stroke_width=3,
       petals_height=0.25,
       petals_stroke=red,
       petals_fill=yellow)
PageBreak()

# ---- END
Text(common=txt, text="Rectangle END...")
PageBreak(footer=True)


Save(
     output='png',
     dpi=600,
     directory="docs/images/custom/circle",
     names=[
        None,
        "hatch", "dot_cross", "radii",
        "petals_triangle", "petals_curve", "petals_petal",
        None])
