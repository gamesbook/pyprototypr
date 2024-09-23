"""
`cards_design` example for pyprototypr

Written by: Derek Hohls
Created on: 19 February 2016
"""
from pyprototypr import *

Create(filename='cards_design.pdf')

# design deck
Deck(
     cards=9,
     margin=0.85,
     margin_bottom=1.9,
     height=8.8,
     width=6.3,
     rounding=0.3,
     fill=ivory)

# simple shapes
l1 = line(x=0.8, x1=5.7, y=7.6, y1=8.9, stroke=gold, stroke_width=2)
r1 = rectangle(x=0.7, y=7.5, width=5, height=1.5, stroke_width=1, rounding=0.2)
low = group(r1, l1)

# add shapes to cards
Card(steps(1,9,2), r1)
Card(steps(2,9,2), l1)

Save()
