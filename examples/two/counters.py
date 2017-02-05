"""
`counters` script for pyprototypr

Written by: Derek Hohls
Created on: 29 February 2016
"""
from pyprototypr.draw import *

# create counters
Create(filename='tannenberg.pdf')  #,
Deck(cards=18, width=2.6, height=2.6, fill=yellow)

# basic values
german_marker = 'ironcross_small.png'  # http://cliparts.co/clipart/3214807
russian_marker = 'russianeagle_small.png'  # http://www.free-vectors.com/vector-russian-eagle/
grey = "#B8BAB1"
brown = "#B6A378"

# simple shapes
german = rectangle(x=0, y=0, width=2.6, height=2.6, stroke_width=1, fill=grey)
russian = rectangle(x=0, y=0, width=2.6, height=2.6, stroke_width=1, fill=brown)
out = rectangle(x=0.8, y=1.2, width=1.0, height=0.6, stroke_width=0.5, transparent=1)
lu = line(x=0.8, y=1.2, x1=1.8, y1=1.8, stroke=black, stroke_width=0.5)
ld = line(x=0.8, y=1.8, x1=1.8, y1=1.2, stroke=black, stroke_width=0.5)
rect1 = rectangle(x=0.8, y=1.2, width=1.0, height=0.3, stroke_width=0.5, fill=black)
circ1 = circle(x=1.3, y=1.5, radius=0.1, stroke_width=0.1, fill=black)

# unit types
inf = group(out, lu, ld)
cav = group(out, lu)
HQ = group(out, rect1)
art = group(out, circ1)

# markers
marker_german = group(german,
                      image(german_marker, x=0.4, y=0.4, width=1.8, height=1.8))
marker_russian = group(russian,
                       image(russian_marker, x=0.4, y=0.4, width=1.8, height=1.8))

# text
inf_A = text(font_face="Arial", font_size=18, x=1.3, y=0.5, text="2-3-4")
division = text(font_face="Arial", font_size=12, x=1.3, y=1.9, text="XX")
battalion = text(font_face="Arial", font_size=12, x=1.3, y=1.9, text="X")

# create final counters
inf_german = group(german, inf)
cav_german = group(german, cav)
inf_russian = group(russian, inf)
inf_russian_A = group(inf_russian, inf_A, division)
HQ_russian = group(russian, HQ)
art_russian = group(russian, art, battalion)

# generate counter images
Card("1-3", inf_german)
Card("4-6", cav_german)
Card("7-9", HQ_russian)
Card("10-12", inf_russian_A)
Card("13-14", art_russian)
Card("15-16", marker_german)
Card("17-18", marker_russian)

Save()
