"""
`cards7` example for pyprototypr

Written by: Derek Hohls
Created on: 29 February 2016
"""
from pyprototypr.draw import *

Create(filename="example7.pdf", offset=0.5)

# deck design - a "template" that all cards will use
Deck(cards=9,
     fill=darkgreen,
     side=3,
     grid_marks=True,
     shape='hexagon')

times = Common(font_face="Times New Roman", font_size=48, stroke=white, x=3, y=2)

# create a list of text elements for the cards, containing single letters
mytext1 = text(text=split("N S ! A G O H E X"), common=times)

# specify a range of cards to contain these letters
Card("1-9", mytext1)

# create the output card file, using the card 'deck'
Save()
