#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Shows pre-defined colors for pyprototypr
Written by: Derek Hohls
Created on: 29 February 2016
"""
# lib
import sys
sys.path.insert(0, '..')
# local
from draw import Create, Text, Save, Rectangle, black, white, red
from utils.tools import color_to_hex
from base import COLORS


Create(filename='colorset.pdf')

row, col = 0, 0
for a_color in sorted(COLORS.keys()):
    label_color = black
    if a_color in ['midnightblue', 'navy', 'darkblue', 'mediumblue', 'black',
                   'darkslategray', 'darkslategrey', 'indigo', 'teal', 'blue',
                   'darkgreen', 'seagreen', 'maroon']:
        label_color = white
    Rectangle(
        row=row, col=col, width=2.7, height=1.25, fill=COLORS[a_color],
        label="%s\n%s" % (a_color, color_to_hex(COLORS[a_color])),
        stroke_label=label_color, font_size=9, line_width=0.1)
    col += 1
    if col > 6:
        col = 0
        row += 1

Text(x=13.5, y=27, text='Report Lab: Named Color Set', stroke=red)
Save()
