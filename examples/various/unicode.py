# -*- coding: utf-8 -*-
"""
Example Unicode symbols for pyprototypr

Written by: Derek Hohls
Created on: 19 September 2024
"""
from pyprototypr import *

Create(filename="unicode.pdf", margin=1, margin_top=0.25)

header = Common(x=0, y=27, font_size=24, align="left")
header_font = Common(font_size=18, align="left")

Text(common=header, text="Unicode Text: Prefix number with \ u")

Text(common=header_font, x=2, y=25,
     text="\u2248 ...  2248 ... approximately")
Text(common=header_font, x=2, y=24,
     text="\u2022 ...  2022 ... bullet")
Text(common=header_font, x=2, y=2,
     text="\u0000 ...  0000 ... .")
Save()
