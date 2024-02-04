#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Shows pre-defined colors for pyprototypr
Written by: Derek Hohls
Created on: 29 February 2016
"""
# lib
# local
from pyprototypr.draw import Create, Text, Save, Rectangle, black, red
from pyprototypr.utils.tools import color_to_hex
from pyprototypr.base import COLORS


Create(filename='colorset.pdf')

row, col = 0, 0
for a_color in sorted(COLORS.keys()):
    label_color = black
    if a_color in [
            'midnightblue', 'navy', 'darkblue', 'mediumblue', 'black',
            'darkslategray', 'darkslategrey', 'indigo', 'teal', 'blue',
            'darkgreen', 'seagreen', 'maroon', 'purple', 'darkslateblue']:
        label_color = 'white'
    Rectangle(
        row=row, col=col, width=2.7, height=1.25, fill=COLORS[a_color])
    Text(
        x=col * 2.7 + 1.35, y=row * 1.25 + 0.75,
        text="%s\n%s" % (a_color, color_to_hex(COLORS[a_color])),
        font_size=8, stroke=label_color)
    col += 1
    if col > 6:
        col = 0
        row += 1

Text(x=13.5, y=27, text='Report Lab: Named Color Set', stroke=red)
Save()
