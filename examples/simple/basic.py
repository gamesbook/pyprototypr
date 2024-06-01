"""Purpose: Show various `basic` examples for pyprototypr

Written by: Derek Hohls
Created on: 29 February 2016

Source:
    * pattern from http://elemisfreebies.com/11/07/20-abstract-patterns/
    * SVG from
"""

from pyprototypr.draw import *

Create(filename="basic.pdf", margin=1, margin_top=0.25)
Footer()

# one BIG hex
Hexagon(
    x=2, y=8,
    side=8,
    label="WELCOME!\nto the basic pyprototypr demo...",
    label_size=16)
PageBreak()

# test default labels and autogrid
AutoGrid()
Polygon(x=4, y=25, radius=2, rotate=30, label="polygon6")
Polygon(x=10, y=25, radius=2, sides=8, rotate=22.5, label="polygon8")
Polygon(x=16, y=24.5, radius=2.5, sides=2.5, rotate=30, label="polygon3")
Rectangle(x=2, y=18.5, width=6, height=3, label="rectangle")
Stadium(x=12.5, y=18.5, width=4, height=3, label="stadium")
Hexagon(x=2, y=13, side=2, label="hexagon")
Hexagon(x=8, y=13, side=2, hex_top="pointy", label="hexagon")
Star(x=11, y=9, vertices=5, radius=2, label="star")
Octagon(cx=16, cy=15, width=3.5, height=3.5, label="octagon")
Circle(cx=16, cy=9, radius=2, label="circle")
Ellipse(x=1, y=7, xe=8, ye=11, label="ellipse")
Rhombus(x=8.5, y=1, width=3, height=5, label="rhombus")
Compass(cx=4, cy=3, radius=2, title="compass")
Square(x=14, y=1, side=4, label="square")
PageBreak()

# centre shapes and autogrid
AutoGrid()
dot = Common(dot_size=0.1, dot_color=yellow)
# Polygon(cx=4, cy=25, radius=2, rotate=30, label="polygon6")
# Polygon(cx=10, cy=25, radius=2, sides=8, rotate=22.5, label="polygon8")
# Polygon(cx=16, cy=24.5, radius=2.5, sides=2.5, rotate=30, label="polygon3")
Rectangle(cx=5, cy=21, width=5, height=4, label="rectangle:5-21", common=dot)
Stadium(cx=13, cy=21, width=4, height=3, label="stadium:13-21", common=dot)
Hexagon(cx=3, cy=15, side=2, label="hexagon:3-15", hex_top="flat", common=dot)
Compass(cx=9, cy=8, radius=2, title="compass:9-8", common=dot)
Hexagon(cx=3, cy=8, side=2, label="hexagon:3-8", hex_top="pointy", common=dot)
Octagon(cx=16, cy=15, width=3.5, height=3.5, label="octagon:16-15", common=dot)
Circle(cx=16, cy=8, radius=2, label="circle:16-8", common=dot)
Ellipse(cx=9, cy=15, xe=4, ye=6, label="ellipse:9-15", common=dot)
Star(cx=3, cy=3, vertices=5, radius=2, label="star:3-2", common=dot)
Rhombus(cx=16, cy=3, width=3, height=5, label="rhombus:16-3", common=dot)
Square(cx=9, cy=3, side=3, label="square:9-3", common=dot)
PageBreak()

# simple shapes
Line(x=11, y=17, x1=11, y1=20, stroke=yellow, stroke_width=2)
Line(x=11, y=17, x1=15, y1=17, stroke=red, stroke_width=2)
Line(x=11, y=20, length=5, angle=-36.86, stroke=blue, stroke_width=2, dot_size=0.1, dot_color=blue)

Rectangle(x=6, y=8, width=5, height=3, stroke_width=2, dot_size=0.1)
Rhombus(x=1, y=7, width=3, height=5, stroke_width=1, ill=lightyellow, dot_size=0.1)
Circle(cx=15.5, cy=10, radius=2.5, fill=green, stroke=red, stroke_width=1, dot_size=0.1)
Ellipse(x=3, y=16, x1=9, y1=20, fill=tan, stroke=green, dot_size=0.1)
# different-sided polygons
Polygon(x=3, y=25, radius=2, fill=gold, dot_size=0.1, rotate=30)  # sides=6
Polygon(sides=8, x=8, y=25, radius=2, fill=saddlebrown, dot_size=0.1, rotate=22.5)
Polygon(sides=3, x=13, y=25, radius=2, fill=olive, dot_size=0.1, rotate=30)
Rectangle(x=16, y=24, width=3, height=3, pattern="13.png", dot_size=0.1)
# house
points = [
    (7, 2),
    (7, 5),
    (10, 6),
    (13, 5),
    (13, 2),
    (11, 2),
    (11, 3.5),
    (9, 3.5),
    (9, 2),
    (7, 2),
]
Shape(points=points, stroke=indianred, fill=red)
pointstr = "0,0 0,1 2,0 2,1 0,0"
Shape(x=9, y=4, points=pointstr, stroke=blue)
PageBreak()

# pentangle star
Star(
    x=9.5,
    y=13.8,
    vertices=5,
    radius=3,
    fill=gold,
    stroke=red,
    label="Radius:5",
    label_stroke=red,
    heading="Star!",
    title="Fig 1: Five-pointed star",
)
PageBreak()

# set of stickers
Rectangles(
    rows=13,
    cols=6,
    width=3,
    height=2,
    rounding=0.4,
    margin=1,
    fill=lightyellow,
    stroke=green,
)
PageBreak()

# ~2cm hex grid - numbered "wargame" style
Hexagons(
    rows=11,
    cols=9,
    side=1.69,
    margin_left=-1.69,
    margin_bottom=-2.529,
    dot_size=0.04,
    dot_color=black,
    coord_position="top",
    coord_font_size=9,
    coord_stroke=darkslategrey,
    fill=white,
    stroke=darkslategrey,
    caltrops="medium",
)
PageBreak()

# lines
Polyline(
    points=[(0, 13), (2, 15), (4, 13), (6, 15), (8, 13), (10, 15), (12, 13)],
    stroke=grey,
)
Polyline(points="0,11 2,13 4,11 6,13 8,11 10,13 12,11", stroke=grey)
Line(x=0, y=0, length=33, angle=55.3, stroke=red, stroke_width=3)  # thick diagonal
Line(x=0, y=3, x1=19, y1=3, stroke=black, stroke_width=2)
Line(
    x=0,
    y=9,
    x1=19,
    y1=9,
    dashes=[0.2, 0.2, 0.2, 0.2, 1.0, 0.0],
    stroke=green,
    stroke_width=2,
    label="dashes=[0.2, 0.2, 0.2, 0.2, 1, 0]",
)
Line(x=0, y=5, x1=19, y1=5, line_dots=True, stroke=blue, stroke_width=2, label="dots")
PageBreak()

# bezier / arc
AutoGrid()
Bezier(x=2, y=7, x1=12, y1=9, x2=12, y2=16, x3=17, y3=20, stroke=blue, stroke_width=2)
Arc(x=1, y=7, x1=4, y1=4, stroke=red, stroke_width=2)
PageBreak()

# common
AutoGrid()
cmm = Common(x=0, y=0, length=19, dots=True, stroke=darkmagenta, stroke_width=2)
Line(common=cmm)
Line(common=cmm, angle=15)
Line(common=cmm, angle=30)
Line(common=cmm, angle=45)
Line(common=cmm, angle=60)
Line(common=cmm, angle=75)
Line(common=cmm, angle=90)
PageBreak()

# common, with a loop
AutoGrid()
for angle in range(0, 100, 10):
    Line(common=cmm, angle=angle, stroke=darkmagenta)
PageBreak()

# school book page with margin
Lines(x=0, x1=19, y=0, y1=0, rows=28, height=1.0, stroke=lightsteelblue)
Line(x=2, x1=2, y=0, y1=28, stroke=orangered)
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

# PNG image and various text positions
Rectangle(x=5.9, y=10.9, width=7.2, height=6.2, stroke=silver)
Image(
    "sholes_typewriter.png",
    x=6,
    y=11,
    width=7,
    height=6,
    label="sholes typewriter",
    label_stroke=red,
    heading="Sholes Typewriter",
    heading_stroke=blue,
    title="Fig 2. Sholes typewriter",
    title_stroke=green,
)
PageBreak()

# SVG image
# Typewriter by ZakaUddin from
# <a href="https://thenounproject.com/browse/icons/term/typewriter/" target="_blank" title="Typewriter Icons">Noun Project</a> (CC BY 3.0)
Rectangle(x=6, y=11, width=7, height=6.25, stroke=silver)
Image(
    # "Typewriter_Vector.svg",
    "noun-typewriter-3933515.svg",
    x=6,
    y=11,
    width=7,
    height=6,
    label="noun typewriter",
    label_stroke=red,
    heading="Noun Typewriter",
    heading_stroke=blue,
    title="Fig 3. nounproject.com typewriter (AlekZakaUddin, CC BY 3.0)",
    title_stroke=green,
    scaling=0.6,
)
PageBreak()


# text wrapping & justification
LATIN = """At cum perfecto praesent, ne causae voluptua reprimique usu,
his id odio tamquam <strike>senserit</strike>.<br/>
<br/>
Eu facete audire assentor usu. Legendos reformidans et vel. Ignota <u>seprehendunt</u>
nam an, vix ad veri maiorum vivendo. Per at ullum iracundia intellegam, alii
nonumy deterruisset ne sed, cum cu quet reque <b>signiferumque</b>.<br/>
<br/>
<font face="times" color="red">Qui at primis regione consetetur. </font>
Id vis viris antiopam gloriatur, muscipit ex has, an ius mazim <i>similique</i>.
"""
Rectangle(x=4.5, y=0, width=10, height=5, stroke_width=1, stroke=grey)
Text(
    x=4.5, y=0.25, width=10, height=5, wrap=True, align="left", text=LATIN, stroke=blue
)
Rectangle(x=4.5, y=6, width=10, height=5, stroke_width=1, stroke=grey)
Text(x=4.5, y=6.25, width=10, height=5, wrap=True, align="right", text=LATIN)
Rectangle(x=4.5, y=12, width=10, height=5, stroke_width=1, stroke=grey)
Text(x=4.5, y=12.25, width=10, height=5, wrap=True, align="centre", text=LATIN)
Rectangle(x=4.5, y=18, width=10, height=5, stroke_width=1, stroke=grey)
Text(x=4.5, y=18.25, width=10, height=5, wrap=True, align="justify", text=LATIN)

# text alignment (default is centre);
Text(text="sholes\ntypewriter!", x=4.5, y=26)  #  add line break via \n
Text(text="sholes typewriter!", x=4.5, y=25, align="centre")
Text(text="sholes typewriter!>", x=4.5, y=24.5, align="right")
Text(text="<sholes typewriter!", x=4.5, y=24, align="left")
PageBreak()

Save()
