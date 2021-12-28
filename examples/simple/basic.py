# show various `basic` examples for pyprototypr
# Written by: Derek Hohls
# Created on: 29 February 2016
# pattern from http://elemisfreebies.com/11/07/20-abstract-patterns/
from pyprototypr.draw import *

Create(filename='basic.pdf', margin=1)
Footer()

# one big hex
Hexagon(cx=9.5, cy=13.8, side=8, label="WELCOME!\nto the basic demo...",
        label_size=16)
PageBreak()

# test default labels and autogrid
AutoGrid()
Polygon(x=4, y=25, radius=2, rotate=30, label="polygon6")
Polygon(x=9, y=25, radius=2, sides=8, rotate=22.5, label="polygon8")
Polygon(x=14, y=25, radius=2, sides=3, rotate=30, label="polygon3")
Rectangle(x=5, y=19, width=9, height=3, label="rectangle")
Hexagon(cx=9.5, cy=16, side=2, label="hexagon")
Star(x=10, y=12, vertices=5, radius=2, label="star")
Circle(cx=14, cy=7, radius=2, label="circle")
Ellipse(x=2, y=5, x1=9, y1=9, label="ellipse")
Rhombus(x=8.5, y=0, width=3, height=5, label="rhombus")
PageBreak()

# simple shapes
Line(x=11, y=17, x1=11, y1=20, stroke=yellow, stroke_width=2)
Line(x=11, y=17, x1=15, y1=17, stroke=red, stroke_width=2)
Line(x=11, y=20, length=5, angle=-36.86, stroke=blue, stroke_width=2)

Rectangle(x=6, y=8, width=5, height=3, stroke_width=2)
Rhombus(x=1, y=7, width=3, height=5, stroke_width=1, fill=lightyellow)
Circle(cx=15.5, cy=10, radius=2.5, fill=green, stroke=red, stroke_width=1)
Ellipse(x=3, y=16, x1=9, y1=20, fill=tan, stroke=green)
# different-sided polygons
Polygon(x=3, y=25, radius=2, fill=gold, dot_size=0.1, rotate=30)  # sides=6
Polygon(sides=8, x=8, y=25, radius=2, fill=saddlebrown, dot_size=0.1, rotate=22.5)
Polygon(sides=3, x=13, y=25, radius=2, fill=olive, dot_size=0.1, rotate=30)
Rectangle(x=16, y=24, width=3, height=3, pattern='13.png')
# house
points = [(7, 2), (7, 5), (10, 6), (13, 5), (13, 2), (11, 2), (11, 3.5),
          (9, 3.5), (9, 2), (7, 2)]
Shape(points=points, stroke=indianred, fill=red)
pointstr = "0,0 0,1 2,0 2,1 0,0"
Shape(x=9, y=4, points=pointstr, stroke=blue, transparent=True)
PageBreak()

# pentangle star
Star(x=9.5, y=13.8, vertices=5, radius=2, fill=gold, stroke=red,
     label="10", stroke_label=red, heading='Star!',
     title='Fig 1.0: Five-pointed star')
PageBreak()

# set of stickers
Rectangles(rows=13, cols=6, width=3, height=2, rounding=0.4, margin=1,
           fill=lightyellow, stroke=green)
PageBreak()

# ~2cm hex grid - tactical "wargame" style
Hexagons(rows=11, cols=9, side=1.686, margin_left=-1.686, margin_bottom=-1.686,
         dot_size=0.04, dot_color=black,
         fill="#C9EC9A", stroke=darkslategrey)
PageBreak()

# lines
Polyline(points=[(0,13), (2,15), (4,13), (6,15), (8,13), (10,15), (12,13)], stroke=grey)
Polyline(points="0,11 2,13 4,11 6,13 8,11 10,13 12,11", stroke=grey)
Line(x=0, y=0, length=33, angle=55.3, stroke=red, stroke_width=3)  # thick diagonal
Line(x=0, y=3, x1=19, y1=3, stroke=black, stroke_width=2)
Line(x=0, y=9, x1=19, y1=9, line_dotdash=[2, 2, 2, 2, 10], stroke=green, stroke_width=2)
Line(x=0, y=7, x1=19, y1=7, dashes=True, stroke=blue, stroke_width=2)
Line(x=0, y=5, x1=19, y1=5, line_dots=True, stroke=blue, stroke_width=2)
PageBreak()

# bezier / arc
AutoGrid()
Bezier(x=2, y=7, x1=12, y1=9, x2=12, y2=16, x3=17, y3=20, stroke=blue, stroke_width=2)
Arc(x=1, y=7, x1=4, y1=4, stroke=red, stroke_width=2)
PageBreak()

# common
cmm = Common(x=0, y=0, length=19, dashes=True, stroke=blue, stroke_width=2)
Line(common=cmm)
Line(common=cmm, angle=15)
Line(common=cmm, angle=30)
Line(common=cmm, angle=45)
Line(common=cmm, angle=60)
Line(common=cmm, angle=75)
Line(common=cmm, angle=90)
PageBreak()

# common, with a loop
for angle in range(0, 100, 10):
    Line(common=cmm, angle=angle)
PageBreak()

# school book page
Lines(x=0, x1=20, y=0, y1=0, rows=28, height=1.0, stroke=lightsteelblue)
PageBreak()

# school book page - landscape
Lines(x=0, x1=0, y=0, y1=28.5, cols=20, width=1.0, stroke=lightsteelblue)
PageBreak()

# business cards
Grid(rows=3, cols=4, width=4.5, height=8.5, stroke=grey)
PageBreak()

# graph paper
Grid(rows=135, cols=95, size=0.2, stroke=mediumseagreen, stroke_width=0.9)
Grid(rows=27, cols=19, size=1.0, stroke=mediumseagreen, stroke_width=1.5)
PageBreak()

# image
Image("sholes_typewriter.png", x=6, y=11, width=7, height=6,
      label="sholes typewriter", stroke_label=red,
      heading="Sholes Typewriter", stroke_heading=blue,
      title="Fig 1. Sholes typewriter", stroke_title=green)
Rectangle(x=6, y=11, width=7, height=6, transparent=True, stroke=silver)
PageBreak()

# text wrapping & justification
LATIN = """At cum perfecto
praesent, ne causae voluptua reprimique usu, his id odio tamquam
<strike>senserit</strike>.<br/>
<br/>
Eu facete audire assentor usu. Legendos reformidans et vel. Ignota reprehendunt
nam an, vix ad veri maiorum vivendo. Per at ullum iracundia intellegam, alii
nonumy deterruisset ne sed, cum cu stet reque <b>signiferumque</b>.<br/>
<br/>
Qui at primis regione consetetur. Id vis viris antiopam gloriatur, suscipit
ex has, an ius mazim <i>similique</i>.
"""
Rectangle(x=4.5, y=0, width=10, height=5, stroke_width=1, stroke=grey)
Text(x=4.5, y=0.25, width=10, height=5, wrap=True, align="left", text=LATIN, stroke=blue)
Rectangle(x=4.5, y=6, width=10, height=5, stroke_width=1, stroke=grey)
Text(x=4.5, y=6.25, width=10, height=5, wrap=True, align="right", text=LATIN)
Rectangle(x=4.5, y=12, width=10, height=5, stroke_width=1, stroke=grey)
Text(x=4.5, y=12.25, width=10, height=5, wrap=True, align="centre", text=LATIN)
Rectangle(x=4.5, y=18, width=10, height=5, stroke_width=1, stroke=grey)
Text(x=4.5, y=18.25, width=10, height=5, wrap=True, align="justify", text=LATIN)

# text alignment (default is centre); add line break via \n
Text(text="<sholes typewriter!", x=4.5, y=24, align="left")
Text(text="sholes typewriter!>", x=4.5, y=24.5, align="right")
Text(text="sholes typewriter!", x=4.5, y=25, align="centre")
Text(text="sholes\ntypewriter!", x=4.5, y=26)
PageBreak()

Save()
