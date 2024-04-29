"""
`cards_design` example for pyprototypr

Written by: Derek Hohls
Created on: 29 April 2024
"""
from pyprototypr.draw import *

Create(filename='cards_images.pdf')
# create the deck; use default sizes
# * deck card count will be based on number of images loaded below
Deck(grid_marks=True)
# load image data
Data(images="pictures", images_filter="*.png")
# add an image to each card
Card("*", image("*", x=1, y=2, width=3.5, height=3.5))
Save()
