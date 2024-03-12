"""
"Hex" game board example for pyprototypr

Written by: Derek Hohls
Created on: 8 March 2024
Notes:
"""
from pyprototypr.draw import *

Create(
    filename='hex_game_board.pdf',
    margin=0.5,
    pagesize=landscape(A4))

# Background Player Areas
RightAngledTriangle(
    x=-1.0, y=10.0, height=9, width=15.35, fill=black, flip='up', hand='left')
RightAngledTriangle(
    x=-1.0, y=10.0, height=9, width=15.35, fill=white, flip='down', hand='left')
RightAngledTriangle(
    x=29.7, y=10.0, height=9, width=15.35, fill=white, flip='up', hand='right')
RightAngledTriangle(
    x=29.7, y=10.0, height=9, width=15.35, fill=black, flip='down', hand='right')

# Hex Game Board
Hexagons(
    rows=11, cols=21,
    hex_layout='diamond',
    height=1.5,
    margin_bottom=2.25, margin_left=1.0,
    )

Save()
