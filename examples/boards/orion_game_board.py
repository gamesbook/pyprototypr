"""
"Orion Duel" game board example for pyprototypr

Written by: Derek Hohls
Created on:12 March 2024
Notes:
"""
from pyprototypr.draw import *

Create(
    filename='orion_game_board.pdf',
    margin=0.5,
    pagesize=A4)

# Background Areas
Circle(cx=10, cy=15, radius=10, fill=steelblue, stroke=white)
Circle(cx=10, cy=15, radius=9, fill=black)

# Game Board
Hexagons(
    rows=11,
    hex_layout='circle',
    fill=black, stroke=white,
    height=1.5,
    margin_bottom=6.5, margin_left=3.0,
    )

Save()
