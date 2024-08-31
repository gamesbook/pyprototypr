# -*- coding: utf-8 -*-
"""
Example code for pyprototypr

Written by: Derek Hohls
Created on: 20 August 2024

GMT Time :
    gmtime() =>
    time.struct_time(
        tm_year=2024, tm_mon=8, tm_mday=31, tm_hour=10, tm_min=52, tm_sec=46,
        tm_wday=5, tm_yday=244, tm_isdst=0)

"""
from pyprototypr import *
from datetime import datetime, timedelta
from time import gmtime, mktime
import argparse

Create(filename="world_clocks.pdf",
        pagesize=landscape(A5),
        margin_top=0.5,
        margin_left=0.15,
        margin_bottom=0.15,
        margin_right=0.5)

header = Common(x=0, y=9, font_size=14, align="left")

def the_clock(x=3, y=3.5, hours=12, minutes=0, gmt=0, label="PROTO", numbers=True):
    """Draw and label a clock shape for a specific time and time zone (GMT offset)
    """
    def hour_to_angle(hour):
        rot = (12 - hour) * 30 + 90
        if hour < 4:
             return abs(min(360 - rot, rot))
        return rot

    detail = is_day(gmt)
    if detail[0]:
        face = white
    else:
        face = darkgrey
    hand = red if detail[1] == 'AM' else black
    # adjust hours
    # breakpoint()
    # print(label, gmt, hours)
    hours = hours + gmt
    hours = hours if hours <= 12 else hours - 12
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
    Circle(cx=x, cy=y, radius=.13, fill=hand)
    # hour hand
    delta = minutes / 60. * 30.
    #delta = 0
    if hours == 12:
        hr_angle = hour_to_angle(hours) - delta
    elif hours < 2:
        hr_angle = hour_to_angle(hours) - delta
    else:
        hr_angle = hour_to_angle(hours) - delta
    #breakpoint()
    #print(label, f"{hours=} {minutes=}", hour_to_angle(hours), delta, hr_angle)
    Circle(cx=x, cy=y, radius=1.8, radii=[hr_angle], stroke=face, fill=None,
           radii_length=2, radii_offset=-.5, radii_stroke=hand, radii_stroke_width=4)
    # minute hand
    angle_minutes = 15 - minutes if minutes <= 15 else 75 - minutes
    min_angle = angle_minutes * 6.
    Circle(cx=x, cy=y, radius=1.8, radii=[min_angle], stroke=face, fill=None,
           radii_length=2.3, radii_offset=-.5, radii_stroke=hand, radii_stroke_width=3)


def is_day(offset=0):
    """Define "daytime" according to AM/PM and actual hour."""
    gmt_now = datetime.fromtimestamp(mktime(gmtime()))
    current = gmt_now + timedelta(hours=offset)
    # breakpoint()
    # print(offset, current.strftime('%p'), current.hour)
    if current.strftime('%p') == 'AM':
        day = True if current.hour > 6 else False
        period = 'AM'
    else:
        day = True if current.hour < 18 else False
        period = 'PM'
    return day, period


def main(offset=2):
    """offset is hours relative to GMT."""
    # the_clock(hours=7, minutes=50, gmt=0)  # TEST
    now = gmtime()
    Text(x=9, y=12.5, font_size=24, align="centre",
         text=f"everyone talk about... pop music! \n(GMT {now.tm_hour}:{now.tm_min:>02})")
    # the_clock(x=4, y=9, hours=now.tm_hour, minutes=now.tm_min, gmt=1, label="London")
    # the_clock(x=14, y=9, hours=now.tm_hour, minutes=now.tm_min, gmt=2, label="Munich")
    # the_clock(x=9, y=5.5, hours=now.tm_hour, minutes=now.tm_min, gmt=offset, label="Home")
    # the_clock(x=4, y=2, hours=now.tm_hour, minutes=now.tm_min, gmt=-4, label="New York")
    # the_clock(x=14, y=2, hours=now.tm_hour, minutes=now.tm_min, gmt=8, label="Hong Kong")
    # Save(output='png', dpi=300)

    the_clock(x=4, y=9, hours=now.tm_hour, minutes=now.tm_min, gmt=2, label="+2")
    the_clock(x=14, y=9, hours=now.tm_hour, minutes=now.tm_min, gmt=-1, label="-1")
    the_clock(x=9, y=5.5, hours=now.tm_hour, minutes=now.tm_min, gmt=0, label="0")
    the_clock(x=4, y=2, hours=now.tm_hour, minutes=now.tm_min, gmt=3, label="+3")
    the_clock(x=14, y=2, hours=now.tm_hour, minutes=now.tm_min, gmt=4, label="+4")

    Save()


if __name__ == "__main__":
    # breakpoint()
    # wcparser = argparse.ArgumentParser()
    # wcparser.add_argument(
    #     '-t', '--time', default=0,
    #     help="Offset of your home location from GMT")
    # wcargs = wcparser.parse_args()
    # main(offset=wcargs.time)
    main()
