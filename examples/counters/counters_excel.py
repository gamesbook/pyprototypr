"""
`counters_excel` script for pyprototypr

Written by: Derek Hohls
Created on: 29 February 2016
"""
from pyprototypr.draw import *

# create counters
Create(filename='tannenberg_excel.pdf')
Deck(width=2.6, height=2.6, fill=yellow)

# load data
Data(filename="counters.xls", headers=['NATION','TYPE','SIZE','VALUE','ID'])

# basic values
grey = "#B8BAB1"
brown = "#B6A378"
value = text(font_face="Arial", font_size=18, x=1.3, y=0.5, text=V('VALUE'))
size = text(font_face="Arial", font_size=12, x=1.3, y=1.9, text=V('SIZE'))
german = rectangle(x=0, y=0, width=2.6, height=2.6, stroke_width=1, fill=grey)
russian = rectangle(x=0, y=0, width=2.6, height=2.6, stroke_width=1, fill=brown)

# unit - basic elements
out = rectangle(x=0.8, y=1.2, width=1.0, height=0.6, stroke_width=0.5, fill=None)
lu = line(x=0.8, y=1.2, x1=1.8, y1=1.8, stroke=black, stroke_width=0.5)
ld = line(x=0.8, y=1.8, x1=1.8, y1=1.2, stroke=black, stroke_width=0.5)
rect1 = rectangle(x=0.8, y=1.2, width=1.0, height=0.3, stroke_width=0.5, fill=black)
circ1 = circle(x=1.3, y=1.5, radius=0.1, stroke_width=0.1, fill=black)
# unit - types
inf = group(out, lu, ld)
cav = group(out, lu)
HQ = group(out, rect1)
art = group(out, circ1)

# markers
marker_german = group(german,
                      image('ironcross_small.png',
                            x=0.4, y=0.4, width=1.8, height=1.8))
marker_russian = group(russian,
                       image('russianeagle_small.png',
                             x=0.4, y=0.4, width=1.8, height=1.8))

# construct cards
Card("all", Q("NATION`=`ger", german))
Card("all", Q("NATION`=`rus", russian))
Card("all", Q("TYPE`=`INF", inf), Q("TYPE`=`CAV", cav),
            Q("TYPE`=`ART", art), Q("TYPE`=`HQ", HQ))
Card("all", Q("TYPE`=`MARKER`&`NATION`=`ger", marker_german))
Card("all", Q("TYPE`=`MARKER`&`NATION`=`rus", marker_russian))
Card("all", value, size)

Save()
