"""
"HexHex" game board, with dots, example for pyprototypr

Written by: Derek Hohls
Created on: 3 August 2024
Notes:
"""

from pyprototypr import *

Create(filename="hexhex_board_dots.pdf", margin=0.5, pagesize=A4)

# Game Board
Hexagons(
    sides=5,
    hex_layout="circle",
    stroke=white,
    fill=None,
    height=2.2,
    dot_size=0.06,
    dot_color=gray,
)

Save()
