# -*- coding: utf-8 -*-
"""
Example code for pyprototypr

Written by: Derek Hohls
Created on: 19 August 2024
"""
from pyprototypr.draw import *

Create(filename="clock.pdf",
        pagesize=A7,
        margin_top=0.5,
        margin_left=0.15,
        margin_bottom=0.15,
        margin_right=0.5)

header = Common(x=0, y=9, font_size=14, align="left")

Blueprint(stroke_width=0.5)
Text(common=header, text="Basic Clock")

def the_clock(hours=12, minutes=0):
    # basic clock frame
    Circle(cx=3, cy=4.5, radius=2.5, fill=white, stroke_width=6,
           label_size=6, label_dy=1, label="PROTO")
    # minutes
    Circle(cx=3, cy=4.5, radius=2.3, radii=steps(0,360,6), stroke=white, fill=None,
           radii_length=0.15, radii_offset=2.2, radii_stroke_width=0.5)
    # hours
    Circle(cx=3, cy=4.5, radius=2.3, radii=steps(0,360,30), stroke=white, fill=None,
           radii_length=0.3, radii_offset=2.2, radii_stroke_width=1.5)
    # centre
    Circle(cx=3, cy=4.5, radius=.13, fill=black)
    # hour hand
    hr_angle = 360. * hours/12 + 90.
    Circle(cx=3, cy=4.5, radius=1.8, radii=[hr_angle], stroke=white, fill=None,
           radii_length=2, radii_offset=-.5,  radii_stroke_width=4)
    # minute hand
    min_angle = 360. * minutes/60 + 90.
    Circle(cx=3, cy=4.5, radius=1.8, radii=[min_angle], stroke=white, fill=None,
           radii_length=2.3, radii_offset=-.5, radii_stroke_width=3)

the_clock(hours=2, minutes=50)
# TODO print relative clocks for : london newyork paris munich

# Save(output='png', dpi=300)
Save()
