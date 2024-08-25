"""
Standard playing cards script for pyprototypr

Written by: Derek Hohls
Created on: 12 August 2024

Notes:

Suit symbols are shown at: https://www.w3schools.com/charsets/ref_utf_symbols.asp
    ♠    2660    BLACK SPADE SUIT
    ♣    2663    BLACK CLUB SUIT
    ♥    2665    BLACK HEART SUIT
    ♦    2666    BLACK DIAMOND SUIT
"""
from pyprototypr import *

# create deck
Create(filename='cards_standard.pdf')
Deck(cards=27,
     margin=0.85,
     margin_bottom=1.9,
     height=8.8,
     width=6.3,
     rounding=0.5,
     grid_marks=True)

# generate data for cards
combos = Matrix(
    labels=['SUIT', 'VALUE'],
    data=[
        ['\u2660', '\u2663', '\u2665', '\u2666'],  # spade, club, heart, diamond
        ['K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2', 'A'],
    ])
Data(matrix=combos, extra=2)  # (re)set no. of cards based on length

# card layout elements
value_top = Common(x=1.0, y=8.4, font_size=40)
value_black = text(common=value_top, stroke=black, text=V('VALUE'))
value_red = text(common=value_top, stroke=red, text=V('VALUE'))

value_low = Common(x=5.5, y=2.4, font_size=40, rotation=180)
value_low_black = text(common=value_low, stroke=black, text=V('VALUE'))
value_low_red = text(common=value_low, stroke=red, text=V('VALUE'))

marker_base = Common(x=1.0, y=7.3, font_size=42)
marker_black = text(common=marker_base, stroke=black, text=V('SUIT'))
marker_red = text(common=marker_base, stroke=red, text=V('SUIT'))

marker_low = Common(x=5.5, y=3.6, font_size=42, rotation=180)
marker_low_black = text(common=marker_low, stroke=black, text=V('SUIT'))
marker_low_red = text(common=marker_low, stroke=red, text=V('SUIT'))

# cards setup
Card("1-26", value_black, value_low_black, marker_black, marker_low_black)
Card("27-52", value_red, value_low_red, marker_red, marker_low_red)

# royalty
royals = Common(x=1.5, y=3, width=3.5, height=5)
Card( "1", image("images/king_s.png", common=royals))
Card( "2", image("images/queen_s.png", common=royals))
Card( "3", image("images/jack_s.png", common=royals))
Card("29", image("images/jack_h.png", common=royals))
Card("14", image("images/king_c.png", common=royals))
Card("15", image("images/queen_c.png", common=royals))
Card("16", image("images/jack_c.png", common=royals))
Card("27", image("images/king_h.png", common=royals))
Card("28", image("images/queen_h.png", common=royals))
Card("29", image("images/jack_h.png", common=royals))
Card("40", image("images/king_d.png", common=royals))
Card("41", image("images/queen_d.png", common=royals))
Card("42", image("images/jack_d.png", common=royals))

# ace
Card("13",
     text(x=3.15, y=3.5, font_size=180, stroke=black, text='\u2660'),
     text(x=3.15, y=4.8, font_size=60, stroke=white, text='\u2660'))

# jokers (2 extra cards)
Card("53",
     text(common=value_top, stroke=black, text='J'),
     text(common=value_low, stroke=black, text='J'),
     image("images/joker_black.png", x=1, y=3, width=5, height=5))
Card("54",
     text(common=value_top, stroke=red, text='J'),
     text(common=value_low, stroke=red, text='J'),
     image("images/joker_red.png", x=1, y=3, width=5, height=5))

Save()
