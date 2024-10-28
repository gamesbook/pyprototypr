"""
"Underwater Cities" board example for pyprototypr

Written by: Derek Hohls
Created on: 27 October 2024
Notes:
    This is not a complete "copy" of the board; just to show how some aspects
    could be implemented
"""
from pyprototypr import *

Create(filename="underwater_cities.pdf", margin=0.0, paper=landscape(A2))

# Base Color - A2 page is 42cm x 59.4cm
deepsea = "#17366F"
Rectangle(x=0, y=0, width=59.4, height=42, fill=deepsea)

# World Map (#B6DCF4)
Image("images/world_map.png", x=7, y=6, width=52.4, height=32)

# Grid
Grid(x=0.25, y=0.4, side=1.25, stroke="#587CBC")

# Outline
drect = Common(fill=None, stroke=grey, dashed=[0,0.05,0.05], rounding=0.5, stroke_width=2)

# Action Cards Slots: Red
action_red = "#D4322D"
action_red_rect = rectangle(x=-0.5, y=4.5, width=6.5, height=5.5, fill_stroke=action_red, rounding=0.5)
Repeat(action_red_rect, rows=5, cols=1, offset=7, gap=1)

action_red_dark = "#9D2622"
red_dark = Rectangle(y=4.5, x=0, width=2.5, height=5.5, fill_stroke=action_red_dark)
Repeat(red_dark, rows=5, cols=1, offset=7, gap=1)

rrect = rectangle(common=drect, x=-0.5, y=4.25, height=6., width=6.75)
Repeat(rrect, rows=5, cols=1, offset=7, gap=1)

lock_red = image('images/padlock-open-red.png', x=1, y=7, width=1.5, height=1.5)
Repeat(lock_red, rows=5, cols=1, offset=7, gap=1)

# Action Cards Slots: Orange
action_ong = "#FFAD01"
action_ong_rect = rectangle(x=7, y=37, width=5.5, height=6.5, fill_stroke=action_ong, rounding=0.5)
Repeat(action_ong_rect, cols=5, rows=1, offset=7, gap=1)

action_ong_dark = "#FE9402"
ong_dark = Rectangle(y=40, x=7, width=5.5, height=2.5, fill_stroke=action_ong_dark)
Repeat(ong_dark, cols=5, rows=1, offset=7, gap=1)

orect = rectangle(common=drect, y=36.75, x=6.75, width=6., height=6.75)
Repeat(orect, cols=5, rows=1, offset=7, gap=1)

lock_grn = image('images/padlock-open-orange.png', x=7, y=36, width=1.5, height=1.5)
Repeat(lock_grn, rows=5, cols=1, offset=7, gap=1)

# Action Cards Slots: Green
action_grn = "#017A51"
action_grn_rect = rectangle(y=-0.5, x=7, width=5.5, height=6.5, fill_stroke=action_grn, rounding=0.5)
Repeat(action_grn_rect, cols=5, rows=1, offset=7, gap=1)

action_grn_dark = "#005D33"
grn_dark = Rectangle(y=0, x=7, width=5.5, height=2.5, fill_stroke=action_grn_dark)
Repeat(grn_dark, cols=5, rows=1, offset=7, gap=1)

grect = rectangle(common=drect, y=-0.5, x=6.75, width=6., height=6.75)
Repeat(grect, cols=5, rows=1, offset=7, gap=1)

lock_grn = image('images/padlock-open-green.png', x=7, y=1, width=1.5, height=1.5)
Repeat(lock_grn, rows=5, cols=1, offset=7, gap=1)

# Special Cards
special_grn = "#4A8D86"
special_grn_rect = rectangle(
    y=9.5, x=34.5, width=5.5, height=8.5, fill_stroke=special_grn, rounding=0.5,
    transparency=80, label="S", label_size=164, label_stroke="#69A8B9")
Repeat(special_grn_rect, cols=3, rows=2, offset_across=9.5, offset_down=7,)

# Government Cards
gov_blue = "#666D8A"
gov_blue_rect = rectangle(y=24, x=11, width=5.5, height=8.5, fill_stroke=gov_blue, rounding=0.5, transparency=90)
Repeat(gov_blue_rect, cols=3, rows=1, offset=7)

# Free Action Space
free_action_btm = "#3A495C"
free_action_top = "#517C8F"
Rectangle(x=19.5, y=9.5, width=5.5, height=2.5, fill_stroke=free_action_btm, rounding=0.5)
Rectangle(x=19.5, y=12, width=5.5, height=3.5, fill_stroke=free_action_top, rounding=0.5)
Rectangle(common=drect, x=19, y=9, height=7, width=6.5)

# Game Name
name_fill = "#4C588C"
name_stroke = "#788CCB"
name_rect = Common(fill=name_fill, stroke=name_stroke, stroke_width=2)
Rectangle(common=name_rect, x=45, y=1, width=10.5, height=4)
Rectangle(
    common=name_rect, x=45, y=3.75, width=10.5, height=1.25,
    label="PROJECT: UNDERWATER CITIES", label_size=18)

# Scoring Track


Save()
