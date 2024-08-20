"""
Matrix cards script for pyprototypr

Written by: Derek Hohls
Created on: 12 August 2024
"""
from pyprototypr.draw import *

# create deck
Create(filename='cards_matrix_one.pdf')
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
Data(matrix=combos)  # (re)set no. of cards based on length

# card layout elements
outline = rectangle(
    x=0.75, y=1.5,
    height=7.8, width=5.1,
    rounded=0.5,
    fill=V('SUIT'), stroke=V('SUIT'))
value_top = hexagon(
    x=1.1, y=7.5,
    side=0.8,
    fill=white, stroke=white,
    font_size=28,
    label=V('VALUE'), label_stroke=black)
value_btm = hexagon(
    x=1.1, y=1.5,
    side=0.8,
    fill=white, stroke=white,
    font_size=28,
    label=V('VALUE'), label_stroke=black, label_rotate=180)
picture = text(
    x=3.15, y=4.4,
    stroke=white,
    font_size=76,
    text=V('IMAGE'))
deco = hexagon(
    x=1.2, y=7.6,
    side=0.7,
    fill=None,
    stroke=V('SUIT'))

# card setup
Card("*", outline, value_top, value_btm, picture, deco)

Save()
