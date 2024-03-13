"""
"Orion Duel" game board example for pyprototypr

Written by: Derek Hohls
Created on:12 March 2024
Notes:
"""

from pyprototypr.draw import *

Create(filename="orion_game_board.pdf", margin=0.5, pagesize=A4)

# Background Areas
Circle(cx=10, cy=15, radius=10.3, fill="#ADCBF4", stroke=white)
Circle(cx=10, cy=15, radius=9.7, fill="#1344D5", stroke=black)
Circle(cx=10, cy=15, radius=9.1, fill="#091B70", stroke=black)
Circle(cx=10, cy=15, radius=8.5, fill=black)

# Game Board
Hexagons(
    sides=6,
    hex_layout="circle",
    fill=black,
    stroke=white,
    height=1.5,
    margin_bottom=6.5,
    margin_left=3.2,
)

Save()
