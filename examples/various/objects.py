# -*- coding: utf-8 -*-
"""
Example code for pyprototypr

Written by: Derek Hohls
Created on: 19 August 2024
"""
from pyprototypr.draw import *

Create(filename="objects.pdf", margin=1, margin_top=0.25)

Text(common=header, text="Miscellaneous")

Text(common=header_font, x=6, y=23, text="Coin: circle with steps radii + an inner circle")
# circles 24 radii - i.e. one every 15 degrees
Circle(cx=3, cy=23, radius=2, fill=skyblue, stroke_width=2, radii=steps(0,360,15))
Circle(cx=3, cy=23, radius=1.5, fill=skyblue, label="5", font_size=48)

Text(align="left", x=9, y=20, wrap=True, width=10, height=4, font_size=16,
     text='<b>Warning Sign:</b> rounded rectangles plus a sequence of "E" chevrons')
Rectangle(x=1, y=17, width=7.5, height=3, rounded=0.5, stroke=black, fill=black)
Rectangle(x=1.1, y=17.1, width=7.3, height=2.8, rounded=0.5, stroke_width=2, stroke=yellow, fill=None)
Sequence(
    rectangle(x=1.5, y=17.1, width=1, height=2.8,
              chevron='E', chevron_height=1, stroke=yellow, fill=yellow),
    setting=(1, 3),
    gap_x=2,
)

Text(common=header_font, x=5, y=15, text="Leaded Window: rectangle w/hatches")
Rectangle(
    x=2, y=13.5,
    height=3, width=2,
    hatch=7, hatch_width=0.1, hatch_directions='d', hatch_stroke=black,
    stroke=saddlebrown, stroke_width=2, fill=lightcyan)

Text(common=header_font, x=5, y=11, text="Paned Window: rectangle w/hatch")
Rectangle(
    x=2, y=9.5,
    height=3, width=2,
    hatch=1, hatch_width=1, hatch_directions='o', hatch_stroke=sienna,
    stroke=sienna, stroke_width=3, fill=lightcyan)

Text(common=header_font, x=5, y=7, text="Start Player: circles + radii using steps())")
Octagon(x=1, y=6, height=3, width=3, fill=black)
Circle(x=1.25, y=6.25, fill=black, radius=1.25,
       radii=[0,45,90,135,180,225,270,315], radii_stroke=gold, radii_stroke_width=2)
Circle(x=2, y=7, stroke=black, fill=gold, radius=0.5, stroke_width=5)

pos = -0.5
Text(common=header_font, x=5, y=pos+3, text="Doorway: stadiums, dashline + radii")
Stadium(x=1, y=pos+1, height=3, width=3, fill=skyblue, stroke=darkgrey, stroke_width=8, edges="n")
Stadium(x=1.003, y=pos+1.003, height=3.003, width=3.003, fill=None, edges="n",
        stroke=fidred, stroke_width=5,
        dashes=[0.3, 0.05, 0.05, 0.0],)
Circle(cx=2.5, cy=pos+4, stroke=sienna, stroke_width=5, fill=skyblue, radius=1.3,
       radii=[30,90,150], radii_stroke=sienna, radii_stroke_width=3)
Circle(cx=2.5, cy=pos+4, stroke=sienna, stroke_width=5, fill=sienna, radius=0.3)
Rectangle(
    x=1.2, y=pos+0.9, height=3, width=2.6,
    stroke=sienna, stroke_width=5, fill=skyblue)
