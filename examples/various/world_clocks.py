# -*- coding: utf-8 -*-
"""
Example code for pyprototypr

Written by: Derek Hohls
Created on: 20 August 2024
"""
from pyprototypr import *
from datetime import datetime, timedelta

Create(filename="world_clocks.pdf",
        pagesize=landscape(A5),
        margin_top=0.5,
        margin_left=0.15,
        margin_bottom=0.15,
        margin_right=0.5)

header = Common(x=0, y=9, font_size=14, align="left")

def the_clock(x=3, y=3.5, hours=12, minutes=0, day=True, label="PROTO", numbers=True):
    """Draw and label a clock shape for a specific time.
    """
    if day:
        face = white
    else:
        face = darkgrey
    # basic clock frame
    Circle(cx=x, cy=y, radius=2.5, fill=face, stroke_width=6,
           label_size=7, label_dy=1, label=label.upper())
    # minutes
    Circle(cx=x, cy=y, radius=2.3, radii=steps(0,360,6), stroke=face, fill=None,
           radii_length=0.15, radii_offset=2.2, radii_stroke_width=0.5)
    # hours
    Circle(cx=x, cy=y, radius=2.3, radii=steps(0,360,30), stroke=face, fill=None,
           radii_length=0.3, radii_offset=2.2, radii_stroke_width=1.5)
    # centre
    Circle(cx=x, cy=y, radius=.13, fill=black)
    # hour hand
    angle_hours = 3 - hours if hours <= 3 else 15 - hours
    delta = -1 * (60 - minutes) / 60 if hours <= 3 else minutes / 60.
    hr_angle = angle_hours * 30. -  delta * 30.
    Circle(cx=x, cy=y, radius=1.8, radii=[hr_angle], stroke=face, fill=None,
           radii_length=2, radii_offset=-.5,  radii_stroke_width=4)
    # minute hand
    angle_minutes = 15 - minutes if minutes <= 15 else 75 - minutes
    min_angle = angle_minutes * 6.
    Circle(cx=x, cy=y, radius=1.8, radii=[min_angle], stroke=face, fill=None,
           radii_length=2.3, radii_offset=-.5, radii_stroke_width=3)


def is_day(offset=0):
    """Define "daytime" according to AM/PM and actual hour."""
    current = datetime.now() + timedelta(hours=offset)
    if current.strftime('%p') == 'AM':
        day = True if current.hour > 6 else False
    else:
        day = True if current.hour < 6 else False
    return day


def main():
    # the_clock(hours=7, minutes=50, day=False)  # TEST
    now = datetime.now()
    the_clock(x=3, y=9, hours=now.hour - 1, minutes=now.minute, day=is_day(-1), label="London")
    the_clock(x=10, y=9, hours=now.hour, minutes=now.minute, day=is_day(0), label="Munich")
    the_clock(x=3, y=3.5, hours=now.hour - 6, minutes=now.minute, day=is_day(-6), label="New York")
    the_clock(x=10, y=3.5, hours=now.hour + 7, minutes=now.minute, day=is_day(7), label="Sydney")
    # Save(output='png', dpi=300)
    Save()


if __name__ == "__main__":
    main()
