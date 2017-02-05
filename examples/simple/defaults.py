"""
`defaults` example for pyprototypr

Written by: Derek Hohls
Created on: 29 February 2016
"""
from pyprototypr.draw import *

Create(filename='defaults.pdf', defaults='locals.json')

Polygon(x=4, y=26, radius=2, rotate=30, label="polygon6")
Polygon(x=9, y=26, radius=2, sides=8, rotate=22.5, label="polygon8")
Polygon(x=14, y=26, radius=2, sides=3, rotate=30, label="polygon3")
Rectangle(x=5, y=20, width=9, height=3, label="rectangle")
Hexagon(cx=9.5, cy=17, side=2, label="hexagon")
Star(x=10, y=12, vertices=5, radius=2, label="star")
Circle(cx=14, cy=7, radius=2.5, label="circle")
Ellipse(x=2, y=5, x1=9, y1=9, label="ellipse")
Rhombus(x=8.5, y=1, width=3, height=5, label="rhombus")
PageBreak()

Save()
