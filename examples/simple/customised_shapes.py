"""
Show customised shapes - and useful overides - for pyprototypr

Written by: Derek Hohls
Created on: 29 March 2024
"""

from pyprototypr.draw import *

Create(filename="customised_shapes.pdf",
       pagesize=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2)

txt = Common(x=0, y=6, font_size=8, align="left")

Text(common=txt, text="START...")
PageBreak(footer=True)

Blueprint(subdivisions=5, stroke_width=0.8)
Text(common=txt, text="Blueprint: subdivisions=5")
Footer()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Text")
Text(text="Hello World")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Line")
Line()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Rectangle & Notches")
Rectangle(height=2, width=1, x=0, y=0, label="x:0 y:0", label_size=5)
Rectangle(
    x=2, y=1,
    height=2, width=1,
    notch=0.25,
    label="notch:0.5",
    label_size=5,
    )
Rectangle(
    x=1, y=4,
    height=1, width=2,
    notch_y=0.25,
    notch_x=0.5,
    notch_corners="NW SE",
    label="notch:.25/.5 loc: NW, SE",
    label_size=5,
    )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Circle: cx=2, cy=3")
Circle(cx=2, cy=3)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Circle: hatch")
Circle(cx=2, cy=5, radius=.7, hatch=1, label='1')
Circle(cx=2, cy=3.5, radius=.7, hatch=4, label='4', rotate=60)
Circle(cx=2, cy=2, radius=.7, hatch=5, label='5')
Circle(cx=1, cy=1, radius=.7, hatch=5, hatch_directions='e', label='e')
Circle(cx=3, cy=1, radius=.7, hatch=5, hatch_directions='n', label='n')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Rectangle: dot & cross")
Rectangle(height=3, width=2, x=1, y=1, cross_size=0.75, dot_size=0.15)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Dots & Crosses")
Circle(cx=1, cy=1, radius=1, dot_size=0.1, dot_color=green)
Circle(cx=3, cy=1, radius=1, cross_size=0.25, cross_stroke=green)
Octagon(cx=1, cy=3, height=2, width=2, dot_size=0.1, dot_color=orange)
Octagon(cx=3, cy=3, height=2, width=2, cross_size=0.25, cross_stroke=orange)
Hexagon(x=0, y=4, height=2, dot_size=0.1, dot_color=red)
Hexagon(x=2, y=4, height=2, cross_size=0.25, cross_stroke=red, cross_stroke_width=1)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Octagon: cx=2, cy=3")
Octagon(cx=2, cy=3)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Hexagon: cx=2, cy=3")
Hexagon(cx=2, cy=3)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Rhombus: cx=2, cy=3")
Rhombus(cx=2, cy=3)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Star")
Star()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Ellipse: xe=3,ye=2")
Ellipse(cx=2, cy=1, xe=4, ye=3)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Polygon")
Polygon()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Arrow")
Arrow()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Right Angled Triangle")
RightAngledTriangle(x=1, y=1, flip="up", hand="right", label="UR", fill="yellow")
RightAngledTriangle(x=2, y=2, flip="down", hand="right", label="DR", fill="green")
RightAngledTriangle(x=2, y=3, flip="up", hand="left", label="UL", fill="red")
RightAngledTriangle(x=3, y=4, flip="down", hand="left", label="DL", fill="blue")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Compass")
Compass(cx=1, cy=1, perimeter='hexagon')
Compass(cx=2, cy=2, perimeter='octagon')
Compass(cx=3, cy=3, perimeter='rectangle', height=2, width=3)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Lines")
Lines(x=1, x1=4, y=1, y1=1, rows=2, height=1.0, label_size=8, label="rows; ht=1.0")
Lines(x=1, x1=1, y=3, y1=6, cols=2, width=1.5, label_size=8, label="col; wd=1.5")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="StarField: Rectangle; multi-color")
Rectangle(x=0, y=0, height=3, width=3, fill=black)
StarField(
    density=20,
    enclosure=rectangle(x=0, y=0, height=3, width=3),
    colors=[white, white, white, red, green, blue],
    sizes=[0.2])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="StarField: Circle; multi-size")
Circle(x=0, y=0, radius=1.5, fill=black)
StarField(
    density=20,
    enclosure=circle(x=0, y=0, radius=1.5),
    sizes=[0.15, 0.15, 0.15, 0.15, 0.3, 0.3, 0.45])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="StarField: Poly. multi-color&size")
Polygon(x=2, y=2, radius=1.5, sides=10, fill=black)
StarField(
    density=50,
    enclosure=polygon(x=2, y=2, sides=10, radius=1.5),
    colors=[white, white, white, red, green, blue],
    sizes=[0.15, 0.15, 0.15, 0.15, 0.3, 0.3, 0.45])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Rectangle: hatch")
Rectangle(
    height=2, width=2,
    hatch=15, hatch_width=0.1, hatch_stroke=black,
    stroke=saddlebrown, stroke_width=0.2, fill=lightcyan)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Octagon: hatch")
Octagon(x=0, y=0, height=1.5, width=1.5, hatch=4, hatch_directions='e', label="e")
Octagon(x=2, y=0, height=1.5, width=1.5, hatch=4, hatch_directions='n', label="n")
Octagon(x=0, y=2, height=1.5, width=1.5, hatch=4, hatch_directions='ne', label="ne")
Octagon(x=2, y=2, height=1.5, width=1.5, hatch=4, hatch_directions='nw', label="nw")
Octagon(x=1, y=4, height=1.5, width=1.5, hatch=4)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Hexagon: hatch")
Hexagon(x=0, y=0, height=1.5, hex_top='flat', hatch=5, hatch_directions='e', label="e")
Hexagon(x=2, y=0, height=1.5, hex_top='pointy', hatch=5, hatch_directions='n', label="n")
Hexagon(x=0, y=2, height=1.5, hex_top='flat', hatch=5, hatch_directions='ne', label="ne")
Hexagon(x=2, y=2, height=1.5, hex_top='pointy', hatch=5, hatch_directions='ne', label="ne")
Hexagon(x=0, y=4, height=1.5, hex_top='flat', hatch=5, hatch_directions='nw', label="nw")
Hexagon(x=2, y=4, height=1.5, hex_top='pointy', hatch=5, hatch_directions='nw', label="nw")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Hexagon: flat; text; hatch")
Hexagon(
    y=2,
    height=2,
    hatch=3,
    debug=True,
    title="Title",
    label="Label",
    heading="Heading")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Hexagon: pointy; text; hatch")
Hexagon(
    y=2,
    height=2,
    hatch=5,
    hex_top='pointy',
    title="Title",
    heading="Heading")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Equilateral Triangle; text; hatch")
EquilateralTriangle(x=1, y=3, side=2, hatch=3, title='Title', heading='Heading')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Right Angled Triangle")
EquilateralTriangle(x=1, y=1, flip="up", hand="right", label="UR", fill="yellow")
EquilateralTriangle(x=1, y=1, flip="down", hand="right", label="DR", fill="green")
EquilateralTriangle(x=1, y=1, flip="up", hand="left", label="UL", fill="red")
EquilateralTriangle(x=1, y=1, flip="down", hand="left", label="DL", fill="blue")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Sector; same centre")
Sector(cx=2, cy=3, radius=2, fill=black, angle=45, angle_width=30)
Sector(cx=2, cy=3, radius=2, fill=black, angle=165, angle_width=30)
Sector(cx=2, cy=3, radius=2, fill=black, angle=285, angle_width=30)
PageBreak()

Text(common=txt, text='1/3" Gray Grid')
Grid(size=0.85, stroke=gray)
PageBreak()

Text(common=txt, text="Moleskine Dot Grid")
DotGrid(stroke=darkgray, width=0.5, height=0.5, dot_point=1, offset_y=-0.25)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Arc; 'inside' rect")
Rectangle(x=1, y=1, height=1, width=2, dot_size=0.01,
          label_size=8, stroke=red, fill=None,
          label="Arc(x=1, y=1, x1=3, y1=2)")
Arc(x=1, y=1, x1=3, y1=2)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Stadium: edges")
Stadium(x=0, y=0, height=1, width=2, edges='top', fill=tan, label="top")
Stadium(x=2, y=2, height=1, width=2, edges='bottom', fill=tan, label="bottom")
Stadium(x=0, y=4, height=1, width=1, edges='right', fill=tan, label="right")
Stadium(x=3, y=5, height=1, width=1, edges='left', fill=tan, label="left")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Sequence: direction and value")
Sequence(
    text(x=1, y=4),
    setting=('h','b',-2,'letter'),
    gap_y=0.5,
    gap_x=0.5,
    )
Sequence(
    text(x=1, y=3.5),
    setting=('B','H',2,'letter'),
    gap_y=-0.5,
    gap_x=0.5,
    )
Sequence(
    text(x=1, y=1.5),
    setting=(10,2,-2,'number'),
    gap_x=0.5,
    )
Sequence(
    text(x=1, y=.85),
    setting=(10,14,1,'number'),
    gap_x=0.66,
    )
Sequence(
    text(x=1, y=0.25, text="${SEQUENCE}"),
    setting=(1,5,1,'number'),
    gap_x=0.66,
    )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Sequence: shapes, label, title")
Sequence(
    rectangle(x=0.25, y=0.25, height=0.75, width=1, label_size=8, label="${SEQUENCE}"),
    setting=(1, 3, 1, 'number'),
    gap_x=1.2,
    )
Sequence(
    circle(x=0.25, y=1.5, radius=0.5, title_size=8, title="Fig. {SEQUENCE}"),
    setting=('C', 'A', -1),
    gap_y=1.5,
    )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Chord: 135 to 45 degrees")
Chord(shape=Circle(cx=2, cy=2, radius=2, fill=None), angle=135, angle1=45, label="chord")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Circle: radii (single & overlapped)")
Circle(x=0, y=0,
       radius=2,
       radii=[45,135,225,315],
       radii_stroke_width=1,
       radii_length=1.5)
Circle(x=0, y=0,
       radius=2,
       fill=None,
       radii=[0,90,180,270],
       radii_stroke_width=3,
       radii_stroke=red)
Circle(cx=3, cy=5,
       radius=1,
       fill=green,
       stroke=orange,
       stroke_width=1,
       radii=[0,90,180,270,45,135,225,315],
       radii_stroke_width=8,
       radii_stroke=orange,
       radii_length=0.8)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Rectangle: chevron")
Rectangle(
    x=3, y=2,
    height=2, width=1,
    font_size=4,
    chevron='N',
    chevron_height=0.5,
    label="chevron:N:0.5",
    title="title-N",
    heading="head-N",
    )
Rectangle(
    x=0, y=2,
    height=2, width=1,
    font_size=4,
    chevron='S',
    chevron_height=0.5,
    label="chevron:S:0.5",
    title="title-S",
    heading="head-S",
    )
Rectangle(
    x=1, y=4.5,
    height=1, width=2,
    font_size=4,
    chevron='W',
    chevron_height=0.5,
    label="chevron:W:0.5",
    title="title-W",
    heading="head-W",
    )
Rectangle(
    x=1, y=0.5,
    height=1, width=2,
    font_size=4,
    chevron='E',
    chevron_height=0.5,
    label="chevron:E:0.5",
    title="title-E",
    heading="head-E",
    )
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=txt, text="Dates: format and styles")
dtext = Common(x=0.5, align="left", font_size=8)
Text(common=dtext, y=5, text=Today())
Text(common=dtext, y=4, text=Today(details="date", style="usa"))
Text(common=dtext, y=3, text=Today(details="date", style="eur"))
Text(common=dtext, y=2, text=Today(details="datetime", style="usa"))
Text(common=dtext, y=1, text=Today(details="datetime", style="eur"))
PageBreak()

Text(common=txt, text="END...")
PageBreak(footer=True)

Save()
