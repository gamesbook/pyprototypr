"""
Show customised shapes - and useful overides - for pyprototypr

Written by: Derek Hohls
Created on: 29 March 2024
"""

from pyprototypr import *

Create(filename="customised_shapes.pdf",
       pagesize=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2,
       font_size=8)
Footer(draw=False)

txt = Common(x=0, y=6, font_size=8, align="left")

Text(common=txt, text="START...")
PageBreak(footer=True)

# ---- blueprint custom
Blueprint(subdivisions=5, stroke_width=0.5, style='invert')
Text(common=txt, text="Blueprint: subdiv;invert;stroke")
PageBreak()

# ---- rectangle: notches
Blueprint()
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

# ---- circle hatch
Blueprint()
Text(common=txt, text="Circle: hatch")
Circle(cx=2, cy=5.2, radius=.7, hatch_stroke=red, hatch=4, label='4')  # all directions
Circle(cx=1, cy=3.7, radius=.7, hatch_stroke=red, hatch=5, hatch_directions='o', label='o')
Circle(cx=3, cy=3.7, radius=.7, hatch_stroke=red, hatch=5, hatch_directions='d', label='d')
Circle(cx=1, cy=2.2, radius=.7, hatch_stroke=red, hatch=5, hatch_directions='e', label='e')
Circle(cx=3, cy=2.2, radius=.7, hatch_stroke=red, hatch=5, hatch_directions='n', label='n')
Circle(cx=1, cy=0.7, radius=.7, hatch_stroke=red, hatch=5, hatch_directions='ne', label='ne')
Circle(cx=3, cy=0.7, radius=.7, hatch_stroke=red, hatch=7, hatch_directions='nw', label='nw')
PageBreak()

# ---- dot & cross
Blueprint()
Text(common=txt, text="Rectangle: dot & cross")
Rectangle(height=3, width=2, x=1, y=1, cross_size=0.75, dot_size=0.15)
PageBreak()

Blueprint()
Text(common=txt, text="Dots & Crosses")
Circle(cx=1, cy=1, radius=1, dot_size=0.1, dot_color=green)
Circle(cx=3, cy=1, radius=1, cross_size=0.25, cross_stroke=green)
Octagon(cx=1, cy=3, height=2, width=2, dot_size=0.1, dot_color=orange)
Octagon(cx=3, cy=3, height=2, width=2, cross_size=0.25, cross_stroke=orange)
Hexagon(x=0, y=4, height=2, dot_size=0.1, dot_color=red)
Hexagon(x=2, y=4, height=2, cross_size=0.25, cross_stroke=red, cross_stroke_width=1)
PageBreak()

# ---- centre placement
Blueprint()
Text(common=txt, text="Octagon: cx=2, cy=3")
Octagon(cx=2, cy=3)
PageBreak()

Blueprint()
Text(common=txt, text="Hexagon: cx=2, cy=3")
Hexagon(cx=2, cy=3)
PageBreak()

Blueprint()
Text(common=txt, text="Rhombus: cx=2, cy=3")
Rhombus(cx=2, cy=3)
PageBreak()

Blueprint()
Text(common=txt, text="Star")
Star()
PageBreak()

Blueprint()
Text(common=txt, text="Ellipse: xe=3, ye=2")
Ellipse(cx=2, cy=1, xe=4, ye=3)
PageBreak()

Blueprint()
Text(common=txt, text="Polygon: cx=2, cy=3, sides=10")
Polygon(cx=2, cy=3, sides=10)
PageBreak()

Blueprint()
Text(common=txt, text="Arrow")
Arrow()
PageBreak()

# ---- RA triangles
Blueprint()
Text(common=txt, text="Right Angled Triangle")
RightAngledTriangle(x=1, y=1, flip="up", hand="right", label="UR", fill="yellow")
RightAngledTriangle(x=2, y=2, flip="down", hand="right", label="DR", fill="green")
RightAngledTriangle(x=2, y=3, flip="up", hand="left", label="UL", fill="red")
RightAngledTriangle(x=3, y=4, flip="down", hand="left", label="DL", fill="blue")
PageBreak()

# ---- compass
Blueprint()
Text(common=txt, text="Compass")
Compass(cx=1, cy=1, perimeter='hexagon')
Compass(cx=2, cy=2, perimeter='octagon')
Compass(cx=3, cy=3, perimeter='rectangle', height=2, width=3)
PageBreak()

# ---- lines (multiple) labels
Blueprint()
Text(common=txt, text="Lines")
Lines(x=1, x1=4, y=1, y1=1, rows=2, height=1.0, label_size=8, label="rows; ht=1.0")
Lines(x=1, x1=1, y=3, y1=6, cols=2, width=1.5, label_size=8, label="col; wd=1.5")
PageBreak()

# ---- starfield
Blueprint()
Text(common=txt, text="StarField: Rectangle; multi-color")
Rectangle(x=0, y=0, height=3, width=3, fill=black)
StarField(
    density=20,
    enclosure=rectangle(x=0, y=0, height=3, width=3),
    colors=[white, white, white, red, green, blue],
    sizes=[0.2])
PageBreak()

Blueprint()
Text(common=txt, text="StarField: Circle; multi-size")
Circle(x=0, y=0, radius=1.5, fill=black)
StarField(
    density=20,
    enclosure=circle(x=0, y=0, radius=1.5),
    sizes=[0.15, 0.15, 0.15, 0.15, 0.3, 0.3, 0.45])
PageBreak()

Blueprint()
Text(common=txt, text="StarField: Poly. multi-color&size")
plys = Common(x=1.5, y=1.4, sides=10, radius=1.5)
Polygon(common=plys, fill=black)
StarField(
    density=50,
    enclosure=polygon(common=plys),
    colors=[white, white, white, red, green, blue],
    sizes=[0.15, 0.15, 0.15, 0.15, 0.3, 0.3, 0.45])
PageBreak()

# ---- rectangle hatch
Blueprint()
Text(common=txt, text="Rectangle: hatch + directions")
htch = Common(height=1.5, width=1, hatch=5, hatch_width=0.1, hatch_stroke=red)
Rectangle(common=htch, x=0, y=0,  hatch_directions='w', label="W")
Rectangle(common=htch, x=1.5, y=0, hatch_directions='e', label="E")
Rectangle(common=htch, x=3, y=0, hatch_directions='ne', label="NE\nSW")

Rectangle(common=htch, x=1.5, y=2, hatch_directions='n', label="N")
Rectangle(common=htch, x=0, y=2,  hatch_directions='s', label="S")
Rectangle(common=htch, x=3, y=2, hatch_directions='nw', label="NW\nSE")

Rectangle(common=htch, x=0, y=4, label="all")
Rectangle(common=htch, x=1.5, y=4, hatch_directions='o', label="O")
Rectangle(common=htch, x=3, y=4, hatch_directions='d', label="D")

PageBreak()

# ---- octagon hatch
Blueprint()
Text(common=txt, text="Octagon: hatch + directions")
octg = Common(height=1.5, width=1.5, hatch=4, hatch_stroke=red)
Octagon(common=octg, x=0, y=0, hatch_directions='e', label="e/w")
Octagon(common=octg, x=2, y=0, hatch_directions='n', label="n/s")
Octagon(common=octg, x=0, y=2, hatch_directions='ne', label="ne/se")
Octagon(common=octg, x=2, y=2, hatch_directions='nw', label="nw/ne")
Octagon(common=octg, x=1, y=4, label="all")
PageBreak()

# ---- hexagon hatch
Blueprint()
Text(common=txt, text="Hexagon: hatch + directions")
hxgn = Common(height=1.5, hatch=5, hatch_stroke=red)
Hexagon(common=hxgn, x=0, y=0, hex_top='flat', hatch_directions='e', label="e/w")
Hexagon(common=hxgn, x=2, y=0, hex_top='pointy', hatch_directions='n', label="n/s")
Hexagon(common=hxgn, x=0, y=2, hex_top='flat', hatch_directions='ne', label="ne/sw")
Hexagon(common=hxgn, x=2, y=2, hex_top='pointy', hatch_directions='ne', label="ne/sw")
Hexagon(common=hxgn, x=0, y=4, hex_top='flat', hatch_directions='nw', label="nw/se")
Hexagon(common=hxgn, x=2, y=4, hex_top='pointy', hatch_directions='nw', label="nw/se")
PageBreak()

# ---- hexagon hatch + text
Blueprint()
Text(common=txt, text="Hexagon: flat; text; hatch")
Hexagon(
    y=2,
    height=2,
    hatch=3,
    hatch_stroke=red,
    debug=True,
    title="Title",
    label="Label",
    heading="Heading")
PageBreak()

Blueprint()
Text(common=txt, text="Hexagon: pointy; text; hatch")
Hexagon(
    y=2,
    height=2,
    hatch=5,
    hatch_stroke=red,
    hex_top='pointy',
    title="Title",
    heading="Heading")
PageBreak()

# ---- equilateral triangle: hatch
Blueprint()
Text(common=txt, text="Equilateral Triangle; text; hatch")
EquilateralTriangle(x=0, y=1, side=4, hatch=5, hatch_stroke=red,
                    title='Title', heading='Heading', label='Label')
PageBreak()

# ---- RA Triangle
Blueprint()
Text(common=txt, text="Right Angled Triangle: flip/hand")
eqt = Common(x=2, y=2, side=2)
EquilateralTriangle(common=eqt, flip="up", hand="right", label="UR", fill="yellow")
EquilateralTriangle(common=eqt, flip="down", hand="right", label="DR", fill="green")
EquilateralTriangle(common=eqt, flip="up", hand="left", label="UL", fill="red")
EquilateralTriangle(common=eqt, flip="down", hand="left", label="DL", fill="blue")
PageBreak()

# ---- sector
Blueprint()
Text(common=txt, text="Sectors: 3 with same centre")
sctm = Common(cx=2, cy=3, radius=2, fill=black, angle_width=43,)
Sector(common=sctm, angle=40)
Sector(common=sctm, angle=160)
Sector(common=sctm, angle=280)
PageBreak()

# ---- grids (plain; dot)
Text(common=txt, text='Grid: gray; 1/3"; thick')
Grid(size=0.8, stroke=gray, stroke_width=0.5)
PageBreak()

Text(common=txt, text='DotGrid: "Moleskine" setting')
DotGrid(stroke=darkgray, width=0.5, height=0.5, dot_point=1, offset_y=-0.25)
PageBreak()

# ---- arc
Blueprint()
Text(common=txt, text="Arc; 'inside' rect")
Rectangle(x=1, y=1, height=1, width=2, dot_size=0.01,
          label_size=8, stroke=red, fill=None,
          label="Arc(x=1, y=1, x1=3, y1=2)")
Arc(x=1, y=1, x1=3, y1=2)
PageBreak()

# ---- stadium
Blueprint()
Text(common=txt, text="Stadium: edges")
Stadium(x=0, y=0, height=1, width=2, edges='n', fill=tan, label="north")
Stadium(x=2, y=2, height=1, width=2, edges='S', fill=tan, label="south")
Stadium(x=0, y=4, height=1, width=1, edges='e', fill=tan, label="east")
Stadium(x=3, y=5, height=1, width=1, edges='w', fill=tan, label="west")
PageBreak()

# ---- sequence
Blueprint()
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

Blueprint()
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

# ---- chord
Blueprint()
Text(common=txt, text="Chord: 135 to 45 degrees")
Chord(shape=Circle(cx=2, cy=2, radius=2, fill=None), angle=135, angle1=45, label="chord")
PageBreak()

# ---- circle radii
Blueprint()
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

# ---- rectangle chevron
Blueprint()
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

# ---- dates
Blueprint()
Text(common=txt, text="Dates: format and styles")
dtext = Common(x=0.5, align="left", font_size=8)
Text(common=dtext, y=5, text=Today())
Text(common=dtext, y=4, text=Today(details="date", style="usa"))
Text(common=dtext, y=3, text=Today(details="date", style="eur"))
Text(common=dtext, y=2, text=Today(details="datetime", style="usa"))
Text(common=dtext, y=1, text=Today(details="datetime", style="eur"))
PageBreak()

# ---- label offsets
Blueprint(stroke_width=0.5)
Text(common=txt, text="Shape label: default and offsets")
rct = Common(height=1.0, width=1.75, stroke_width=.5, label_size=7)
Rectangle(common=rct, x=0, y=0.0, label="offset -x, +y", label_dx=-0.2, label_dy=-0.2)
Rectangle(common=rct, x=0, y=1.5, label="offset -x", label_dx=-0.3)
Rectangle(common=rct, x=0, y=3.0, label="offset -x, +y", label_dx=-0.2, label_dy=0.2)
Rectangle(common=rct, x=2, y=0.0, label="offset -x, -y", label_dx=0.2, label_dy=-0.2)
Rectangle(common=rct, x=2, y=1.5, label="offset +x", label_dx=0.3)
Rectangle(common=rct, x=2, y=3.0, label="offset +x, +y", label_dx=0.2, label_dy=0.2)
Rectangle(common=rct, x=1, y=4.5, label="no offset")
PageBreak()

# ---- rotation: image
Rectangle(x=0, y=0, height=6, width=4, fill=khaki)
Text(common=txt, text="Images: normal & rotation")
Blueprint()
Image("sholes_typewriter.png", x=0, y=0, width=1.5, height=1.5, heading="PNG")
Image("sholes_typewriter.png", x=2, y=0, width=1.5, height=1.5, heading="60\u00B0", rotation=60)
Image("noun-typewriter-3933515.svg", x=0, y=4, width=1.5, height=1.6, scaling=0.15, title="SVG")
Image("noun-typewriter-3933515.svg", x=2, y=4, width=1.5, height=1.6, scaling=0.15, title="45\u00B0", rotation=45)
PageBreak()

# ---- rotation: rhombus
Blueprint()
Text(common=txt, text="Rhombus: red is rotation 60\u00B0")
Rhombus(cx=2, cy=3, width=1.5, height=2*equi(1.5), dot_size=0.06)
Rhombus(cx=2, cy=3, width=1.5, height=2*equi(1.5), fill=None,
        stroke=red, stroke_width=.3, rotation=60, dot_size=0.04)
PageBreak()

# ---- rotation: rect
Blueprint()
Text(common=txt, text="Rectangle: red rotation 45\u00B0")
Rectangle(cx=2, cy=3, width=1.5, height=3, dot_size=0.06)
Rectangle(cx=2, cy=3, width=1.5, height=3, fill=None,
          stroke=red, stroke_width=.3, rotation=45, dot_size=0.04)
PageBreak()

# ---- rotation: stadium
Blueprint()
Text(common=txt, text="Stadium: red rotation 30\u00B0")
Stadium(cx=2, cy=3, width=1.25, height=2, dot_size=0.06)
Stadium(cx=2, cy=3, width=1.25, height=2, fill=None,
        stroke=red, stroke_width=.3, rotation=30, dot_size=0.04)
PageBreak()

# ---- END
Text(common=txt, text="END...")
PageBreak(footer=True)

Save()
