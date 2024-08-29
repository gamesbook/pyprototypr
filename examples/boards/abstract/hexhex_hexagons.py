"""
"HexHex" game board, with inset hexagons, example for pyprototypr

Written by: Derek Hohls
Created on: 31 August 2024
Notes:
"""

from pyprototypr import *

Create(filename="hexhex_board_hexagons.pdf", margin=0.5, pagesize=A4)

# Game Board
Hexagons(
    sides=5,
    hex_layout="circle",
    stroke=white,
    fill=None,
    height=2.2,
    centre_shape=hexagon(stroke=black, fill=white, height=2, stroke_width=2),
    margin_bottom=4,
    masked=[[5, 5]],
)

Save(output='png')
