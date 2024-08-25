"""
Matrix cards script, with "joker" cards, for pyprototypr

Written by: Derek Hohls
Created on: 12 August 2024
"""
from pyprototypr import *

# create deck
Create(filename='cards_matrix_two.pdf')
Deck(cards=27,
     margin=0.85,
     margin_bottom=1.9,
     height=8.8,
     width=6.3,
     rounding=0.5,
     grid_marks=True)

# generate data for cards
# Note: symbols are from https://www.w3schools.com/charsets/ref_utf_dingbats.asp
combos = Matrix(
    labels=['SUIT', 'VALUE', 'IMAGE'],
    data=[
        # red, green, skyblue, gold, hotpink
        ['#FF0000', '#9ACD32','#00BFFF', '#FFD700', '#FF69B4'],
        ['5', '3', '1'],
        # tapedrive, heart, snowflake
        ['\u2707', '\u2766', '\u2745']
    ])
Data(matrix=combos, extra=9)  # (re)set no. of cards based on length

# card layout elements
outline = rectangle(
    x=0.75, y=1.5,
    height=7.8, width=5.1,
    rounded=0.5,
    fill=V('SUIT'), stroke=V('SUIT'))
icon_top = hexagon(
    x=1.1, y=7.5,
    side=0.8,
    stroke=white)
value_top = text(
    x=1.9, y=7.8,
    font_size=28,
    text=V('VALUE'),
    align="centre",
    stroke=darkslategrey)
icon_btm = hexagon(
    x=3.9, y=1.8,
    side=0.8,
    stroke=white)
value_btm = text(
    x=4.7, y=2.8,
    font_size=28,
    align="centre",
    text=V('VALUE'),
    stroke=darkslategrey,
    rotation=180)
picture = text(
    x=3.15, y=4.4,
    stroke=white,
    font_size=76,
    text=V('IMAGE'))
deco_top = hexagon(
    x=1.2, y=7.6,
    side=0.7,
    fill=None,
    stroke=V('SUIT'))
deco_btm = hexagon(
    x=4, y=1.9,
    side=0.7,
    fill=None,
    stroke=V('SUIT'))

# card setup
Card("1-45",
     outline,
     picture,
     icon_top, icon_btm,
     deco_top, deco_btm,
     value_top, value_btm,
)

# custom cards
rectC = rectangle(
    y=1.5,
    height=7.8,
    width=1.02,
    rounded=1,
    stroke=white)
Card("46-48",
     rectangle(common=rectC, x=0.75, fill='#FF0000'),
     rectangle(common=rectC, x=1.77, fill='#FFD700'),
     rectangle(common=rectC, x=2.79, fill='#9ACD32'),
     rectangle(common=rectC, x=3.81, fill='#00BFFF'),
     rectangle(common=rectC, x=4.83, fill='#FF69B4')
)

hexN = Common(
    side=1.5,
    fill=None,
    font_size=28,
    stroke=black,
    stroke_width=2)
hexI = Common(
    side=1.3,
    fill=None,
    stroke=black,
    stroke_width=.5)
Card("49-51",
     hexagon(common=hexN, cx=2.0, cy=8.0, label="1"),
     hexagon(common=hexN, cx=3.3, cy=5.4, label="3"),
     hexagon(common=hexN, cx=4.6, cy=2.8, label="5"),
     hexagon(common=hexI, cx=2.0, cy=8.0),
     hexagon(common=hexI, cx=3.3, cy=5.4),
     hexagon(common=hexI, cx=4.6, cy=2.8),
)

Card("52-54",
     circle(fill=black, stroke=white, radius=1.25, cx=2, cy=8, font_size=48, label='\u2707'),
     circle(fill=black, stroke=white, radius=1.25, cx=3.3, cy=5.4, font_size=48, label='\u2766'),
     circle(fill=black, stroke=white, radius=1.25, cx=4.6, cy=2.8, font_size=48, label='\u2745'),
)

Save()
