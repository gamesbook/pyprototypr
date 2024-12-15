"""
`cards_images` example for pyprototypr

Written by: Derek Hohls
Created on: 29 April 2024
"""
from pyprototypr import *

Create(filename='cards_images.pdf')

# create the deck with default size cards
# * card count will be based on number of images loaded via Data()
Deck(grid_marks=True)

# load image data
Data(images="pictures", images_filter=".png,.jpg")

# add an image to each card
Card("*", image("*", x=0, y=0, width=6.3, height=8.8))

Save()
