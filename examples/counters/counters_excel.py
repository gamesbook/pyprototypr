"""
`counters_excel` script for pyprototypr

Written by: Derek Hohls
Created on: 29 February 2016
Updated on: 22 September 2024
"""
from pyprototypr import *

# create counters
Create(filename='tannenberg_excel.pdf')
Deck(width=2.6, height=2.6, fill=white)

# load data
Data(filename="counters.xls", headers=['NATION','TYPE','SIZE','VALUE','ID'])

# colors and text labels
grey = "#B8BAB1"
brown = "#B6A378"
value = text(font_face="Arial", font_size=18, x=1.3, y=0.5, text=T('{{VALUE}}'))
size = text(font_face="Arial", font_size=12, x=1.3, y=1.9, text=T('{{SIZE}}'))
ident = text(font_face="Arial", font_size=12, x=0.55, y=1.18, align='left', rotation=90,
             text=T('{{ID}}'))

# national colors
troop = Common(x=0, y=0, width=2.6, height=2.6, stroke_width=1)
german = rectangle(common=troop, fill=grey)
russian = rectangle(common=troop, fill=brown)

# unit symbol - basic elements
out = rectangle(x=0.8, y=1.2, width=1.0, height=0.6, stroke_width=0.5, fill=None)
lu = line(x=0.8, y=1.2, x1=1.8, y1=1.8, stroke=black, stroke_width=0.5)
ld = line(x=0.8, y=1.8, x1=1.8, y1=1.2, stroke=black, stroke_width=0.5)
rect1 = rectangle(x=0.8, y=1.2, width=1.0, height=0.3, stroke_width=0.5, fill=black)
circ1 = circle(cx=1.3, cy=1.5, radius=0.1, stroke_width=0.1, fill=black)

# unit symbols - types
inf = group(out, lu, ld)
cav = group(out, lu)
HQ = group(out, rect1)
art = group(out, circ1)

# markers
marker_german = group(
    german,
    image('ironcross_small.png', x=0.4, y=0.4, width=1.8, height=1.8))
marker_russian = group(
    russian,
    image('russianeagle_small.png', x=0.4, y=0.4, width=1.8, height=1.8))

# construct counters  ("small cards")
Card("all", S("{{ NATION == 'ger' }}", german))
Card("all", S("{{ NATION == 'rus' }}", russian))
Card("all",
     S("{{ TYPE == 'INF' }}", inf),
     S("{{ TYPE == 'CAV' }}", cav),
     S("{{ TYPE == 'ART' }}", art),
     S("{{ TYPE == 'HQ' }}", HQ))
Card("all", S("{{ TYPE == 'MARKER' and NATION == 'ger' }}", marker_german))
Card("all", S("{{ TYPE == 'MARKER' and NATION == 'rus' }}", marker_russian))
Card("all", value, size, ident)

Save()
