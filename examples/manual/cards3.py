"""
`cards3` example for pyprototypr

Written by: Derek Hohls
Created on: 29 February 2016
"""
from pyprototypr import *

Create(filename="example3.pdf", offset=0.5)

# deck design - a "template" that all cards will use
Deck(cards=50,
     fill="#702EB0",
     height=5,
     width=3.8)

# create the output card file, using the card 'deck'
Save()
