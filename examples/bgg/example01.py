"""
Show how to retrieve game info from boardgamegeek.com, and display this
in cards via pyprototypr

Written by: Derek Hohls
Created on: 21 May 2016
Notes:
    uses `boardgamegeek` Python library 
"""
from pyprototypr.draw import *

num = 9
Create(filename="bgg_game_cards.pdf", offset=0.5)
Deck(cards=num, grid_marks=True, rounded=True)
# format of text
numbers = Common(font_face="Arial", font_size=20, stroke=black)
title = Common(font_face="Times New Roman", font_size=12, stroke=black)
body = Common(font_face="Times New Roman", font_size=10, stroke=black)
# source and location of images
time_img = image('time.png', x=0.2, y=6.8, width=1.8, height=1.8)
players_img = image('players.png', x=2.2, y=6.8, width=1.8, height=1.8)
age_img = image('age.png', x=4.2, y=6.8, width=1.8, height=1.8)
# number of games to retrieve
choice = range(1, num + 1)
# bgg game data -> progress is True so we can see rate of retrieval
games = BGG(ids=choice, progress=True)
# create a list of text elements for the cards
time = text(text=games.playingtime, common=numbers, x=1.1, y=6.9)
players = text(text=games.players, common=numbers, x=3.1, y=6.9)
minage = text(text=games.age, common=numbers, x=5.1, y=6.9)
name = text(text=games.name, common=title, x=3.15, y=6.4)
# special code to handle text boxes
for item in choice:
    desc = text(font_face="Times New Roman", font_size=11, stroke="#808080", 
                leading=11, x=0.075, y=1.0, width=6.125, height=4.8, 
                wrap=True, align="centre", text=games.description_short[item - 1])
    foot = text(font_face="Arial", font_size=8, stroke=black, leading=8,
                x=0.1, y=0.1, width=6.1, height=0.4, 
                wrap=True, align="centre", text=games.mechanics[item - 1])
    Card("%s" % item, desc)
    Card("%s" % item, foot)
# final layout
layout = group(time_img, age_img, players_img, time, players, minage, name)
Card("1-%s" % num, layout)
Save()

