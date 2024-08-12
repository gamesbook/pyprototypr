"""
Standard playing cards script for pyprototypr

Written by: Derek Hohls
Created on: 12 August 2024

Notes:

symbols are from https://www.w3schools.com/charsets/ref_utf_symbols.asp
    ♠	2660	BLACK SPADE SUIT
    ♣	2663	BLACK CLUB SUIT
    ♥	2665	BLACK HEART SUIT
    ♦	2666	BLACK DIAMOND SUIT
"""
from pyprototypr.draw import *

# create deck
Create(filename='cards_standard.pdf')
Deck(cards=27,
     margin=0.85,
     margin_bottom=1.9,
     height=8.8,
     width=6.3,
     rounding=0.5,
     grid_marks=True)  #

# generate data for cards
combos = Matrix(
    labels=['SUIT', 'VALUE'],
    data=[
        ['\u2660', '\u2663', '\u2665', '\u2666'],  # spade, club, heart, diamond
        ['K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2', 'A'],
    ])
Data(matrix=combos, extra=2)  # (re)set no. of cards based on length

# card layout elements
value_base = text(x=1.0, y=8.4, font_size=40)
value_red = text(common=value_base, stroke=red, text=V('VALUE'))
value_black = text(common=value_base, stroke=black, text=V('VALUE'))

value_low = text(x=5.5, y=1.3, font_size=40, rotate=90)

marker_base = text(x=1.0, y=7.3, font_size=42, text=V('SUIT'))
marker_red = text(common=marker_base, stroke=red)
marker_black = text(common=marker_base, stroke=black)

# card setup
Card("1-26", value_black, marker_black)
Card("27-52", value_red, marker_red)
# royalty
# TODO
# jokers
Card("53",
     text(common=value_base, stroke=black, text='J'),
     text(common=value_low, stroke=black, text='J'),
     image("images/joker_black.png", x=1, y=3, width=5, height=5))
Card("54",
     text(common=value_base, stroke=red, text='J'),
     text(common=value_low, stroke=red, text='J'),
     image("images/joker_red.png", x=1, y=3, width=5, height=5))

Save()
