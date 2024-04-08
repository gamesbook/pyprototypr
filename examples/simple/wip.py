"""
WIP tester for pyprototypr

Written by: Derek Hohls
Created on: 9 March 2024
"""
from pyprototypr.draw import *

Create(filename="wip.pdf",
       pagesize=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2)

header = Common(x=0, y=6, font_size=8, align="left")

AutoGrid(stroke_width=0.5)

Text(common=header, text="Hexagon: vertical")
Hexagon(hex_orientation="pointy", dot_size=0.1,)

Save()
