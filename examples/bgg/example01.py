"""
Retrieve game info from boardgamegeek.com, and display this in cards via pyprototypr

Written by: Derek Hohls
Created on: 21 May 2016

Notes:
    BGG() uses the `bgg-api` Python library (https://github.com/SukiCZ/boardgamegeek)
"""
from pyprototypr import *

num = 9  # number of cards to be used
Create(filename="cards_bgg.pdf", offset=0.5)

# number of games to retrieve
choice = range(1, num + 1)

# BGG game data -> progress is True so we can see the rate of retrieval
games = BGG(ids=choice, progress=True, short=610)  # short: number of characters

Deck(cards=num, grid_marks=True, rounded=True)

# format of text
numbers = Common(font_face="Arial", font_size=18, stroke=black)
title = Common(font_face="Times New Roman", font_size=12, stroke=black)
body = Common(font_face="Times New Roman", font_size=9, stroke=black)

# source and location of images
time_img = image('time.png', x=0.2, y=6.8, width=1.8, height=1.8)
players_img = image('players.png', x=2.2, y=6.8, width=1.8, height=1.8)
age_img = image('age.png', x=4.2, y=6.8, width=1.8, height=1.8)

# create a list of text elements for the cards
time = text(common=numbers, x=1.1, y=6.9, text=games.playingtime)
players = text(common=numbers, x=3.1, y=6.9, text=games.players)
minage = text(common=numbers, x=5.1, y=6.9, text=games.age)
name = text(common=title, x=3.15, y=6.4, text=games.name)

# special code to handle text boxes
for item in choice:
    desc = text(
        font_face="Times New Roman", font_size=9, stroke="#808080",
        leading=11, x=0.075, y=6.35, width=6.125, height=4.8,
        wrap=True, align="centre", text=games.description_short[item - 1])
    foot = text(
        font_face="Arial", font_size=7, stroke=black, leading=8,
        x=0.1, y=0.85, width=6.1, height=0.4,
        wrap=True, align="centre", text=games.mechanics[item - 1])
    Card(f"{item}", desc)
    Card(f"{item}", foot)

# final layout for non-textbox items
layout = group(time_img, age_img, players_img, time, players, minage, name)
Card(f"1-{num}", layout)

Save()
