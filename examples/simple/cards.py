"""
`cards` example for pyprototypr

Written by: Derek Hohls
Created on: 29 February 2016
"""
from pyprototypr.draw import *

Create(filename='cards.pdf')

# design deck
Deck()

# simple shapes
l1 = line(x=0.9, x1=5.7, y=7.1, y1=8.4, stroke=gold, stroke_width=2)
r1 = rectangle(x=0.8, y=7, width=5, height=1.5, stroke_width=1, rounding=0.2)

# add shapes to cards
Card("1-4", l1)
Card("5-9", r1)

Save()
