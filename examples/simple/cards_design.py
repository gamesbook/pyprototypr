"""
`cards_design` example for pyprototypr

Written by: Derek Hohls
Created on: 19 February 2016
"""
from pyprototypr.draw import *

Create(filename='cards_design.pdf')

# design deck
Deck(cards=9, margin=0.85, margin_bottom=1.9,
     height=8.8, width=6.3, rounding=0.3, fill=ivory)

# simple shapes
l1 = line(x=0.8, x1=5.7, y=7.6, y1=8.9, stroke=gold, stroke_width=2)
r1 = rectangle(x=0.7, y=7.5, width=5, height=1.5, stroke_width=1, rounding=0.2)

# combined shapes
g1 = group(r1, l1)

# add shapes to cards
Card("1-3", r1, l1)
Card("4-6", r1)
Card("7-9", l1)
#Card("10-18", g1)

Save()
