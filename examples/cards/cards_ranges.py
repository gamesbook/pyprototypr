"""
`cards_design` example for pyprototypr

Written by: Derek Hohls
Created on: 19 February 2016
"""
from pyprototypr import *

Create(filename='cards_ranges.pdf')

# design deck
Deck(
     cards=9,
     margin=0.85,
     margin_bottom=1.9,
     height=8.8,
     width=6.3,
     rounding=0.3,
     fill=ivory)

# basic shapes
l1 = line(x=0.8, x1=5.6, y=6.9, y1=8.2, stroke=gold, stroke_width=2)
r1 = rectangle(x=0.7, y=6.8, width=5, height=1.5, stroke_width=1, rounding=0.2)
low = group(r1, l1)

# add shapes to cards
Card(steps(1,9,2), r1)
Card(steps(2,9,2), l1)

Save()
