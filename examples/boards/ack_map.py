"""
"Adventurer Conqueror King System" map example for pyprototypr

Written by: Derek Hohls
Created on: 3 March 2024
Notes:
"""
from pyprototypr.draw import *

Create(
    filename='ack_map.pdf',
    margin=0.5,
    pagesize=landscape(A3))

deepgrey = "#666666"

# Header Section
Text(
    x=1.5, y=28, width=15, height=1, align="left",
    font_face="Times New Roman", font_size=23,
    text="ADVENTURER CONQUEROR KING")
Rectangle(x=15, y=27.5, width=22.5, height=1.5, stroke=darkgrey, stroke_width=1.5)

# Base Map (small numbered hexes)
Hexagons(
    rows=16, cols=25,
    height=1.66,  # ~two-thirds of an inch
    margin_bottom=0.25, margin_left=2.0,
    coord_position="top", coord_offset=-0.1,
    coord_font_size=8, coord_stroke=deepgrey,
    coord_padding=2,
    fill=white, stroke=deepgrey, stroke_width=1.2)

# Overlay (large hexes)
Hexagons(
    rows=4, cols=6,
    height=6.64,  # 4 small hexes high
    margin_bottom=4.4, margin_left=2.0,
    hex_offset="odd",
    fill=None, stroke=darkgrey, stroke_width=3)

# Tidy bottom edge
Rectangle(x=-0.2, y=-1.05, width=38.5, height=1.55, stroke=white, fill=white)

Save()
