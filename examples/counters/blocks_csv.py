"""
`blocks_csv` script for pyprototypr

Written by: Derek Hohls
Created on: 9 August 2024

Notes:

* Tile outline and dot colors:
    reds = "#790704"
    olives = "#937301"
    greens = "#57762C"
    blues = "#416E83"
"""
from pyprototypr.draw import *

# create counters
Create(filename='blocks_csv.pdf')
Deck(width=2.9, height=2.9, grid_marks=True)

# load data
Data(filename="blocks.csv")  # (re)set no. of cards based on chosen rows in file

# common colors
blue = "#005F9C"
red = "#A71C20"
lbrown = "#F1D7B5"

# basic elements
tile_red = rectangle(x=0.0, y=0.0, width=2.9, height=2.9, stroke=red, fill=red)
tile_blue = rectangle(x=0.0, y=0.0, width=2.9, height=2.9, stroke=blue, fill=blue)
base = rectangle(x=0.2, y=0.2, width=2.5, height=2.5, stroke=brown, fill=lbrown)

# per-tile values and elements
title = text(font_face="Times New Roman", font_size=8, x=1.4, y=2, align="centre", text=V('TITLE'))
move = text(font_face="Times New Roman", font_size=12, x=0.6, y=0.5, text=V('MOVE'))
strength = text(font_face="Times New Roman", font_size=12, x=2.1, y=0.5, text=V('STRENGTH'))
outline = rectangle(x=0.45, y=0.45, width=2.0, height=2.0, stroke_width=1, stroke=V('BORDER'), fill=None)
pic = image(V('IMAGE'), x=0.7, y=0.8, width=1.5, height=1.1)

# "dots" templates
top4 = sequence(
     square(x=0.9, y=2.35, side=0.25, stroke=lbrown, stroke_width=1, fill=V('BORDER')),
     setting=(1, 4),
     gap_x=0.29)
right3 = sequence(
     square(x=2.3, y=1.0, side=0.25, stroke=lbrown, stroke_width=1, fill=V('BORDER')),
     setting=(1, 3),
     gap_y=0.29)
low2 = sequence(
     square(x=1.2, y=0.35, side=0.25, stroke=lbrown, stroke_width=1, fill=V('BORDER')),
     setting=(1, 2),
     gap_x=0.29)
left1 = square(x=0.35, y=1.3, side=0.25, stroke=lbrown, stroke_width=1, fill=V('BORDER'))
dots4 = group(top4, right3, low2, left1)

top3 = sequence(
     square(x=1.05, y=2.35, side=0.25, stroke=lbrown, stroke_width=1, fill=V('BORDER')),
     setting=(1, 3),
     gap_x=0.29)
right2 = sequence(
     square(x=2.3, y=1.2, side=0.25, stroke=lbrown, stroke_width=1, fill=V('BORDER')),
     setting=(1, 2),
     gap_y=0.29)
low1 = square(x=1.3, y=0.35, side=0.25, stroke=lbrown, stroke_width=1, fill=V('BORDER'))
dots3 = group(top3, right2, low1)

# shields
shield = Common(x=1.1, y=.8, height=0.9, width=0.7, hatch=1, hatch_width=3)
shield_blue = rectangle(common=shield, fill=blue, hatch_stroke=white, hatch_directions='ne nw')
shield_red = rectangle(common=shield, fill=white, hatch_stroke=red, hatch_directions='n e')

# card construction
Card("all", Q("SIDE`=`English", tile_red))
Card("all", Q("SIDE`=`Scots", tile_blue))
Card("all", base, outline, move, title, strength, pic)
Card("all", Q("DOTS`=`4", dots4))
Card("all", Q("DOTS`=`3", dots3))
Card("all", Q("SHIELD`=`red", shield_red))
Card("all", Q("SHIELD`=`blue", shield_blue))

Save()
