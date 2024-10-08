"""
Show customised shapes - and useful overides - for pyprototypr

Written by: Derek Hohls
Created on: 29 March 2024
"""

from pyprototypr import *

Create(filename="customised_shapes.pdf",
       paper=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2,
       font_size=8)
Footer(draw=False)

txt = Common(x=0, y=6, font_size=8, align="left")

Text(common=txt, text="Shapes START...")
PageBreak(footer=True)

# ---- blueprint custom
Blueprint(subdivisions=5, stroke_width=0.5, style='invert')
Text(common=txt, text="Blueprint: subdiv;invert;stroke")
PageBreak()

# ---- dot & cross
Blueprint()
Text(common=txt, text="Dots & Crosses")
Rhombus(cx=1, cy=5, side=2, dot=0.1, dot_stroke=red)
Rhombus(cx=3, cy=5, side=2, cross=0.25, cross_stroke=red, cross_stroke_width=1)
Polygon(cx=1, cy=3, sides=8, radius=1, dot=0.1, dot_stroke=orange)
Polygon(cx=3, cy=3, sides=8, diameter=2, cross=0.25, cross_stroke=orange, cross_stroke_width=1)
Stadium(cx=1, cy=1, side=1, dot=0.1, dot_stroke=blue)
Stadium(cx=3, cy=1, side=1, cross=0.25, cross_stroke=blue, cross_stroke_width=1)
PageBreak()

# ---- centre placement
# Blueprint()
# Text(common=txt, text="Trapezoid: cx=2, cy=3")
# Trapezoid(cx=2, cy=3)
# PageBreak()

Blueprint()
Text(common=txt, text="Rhombus: cx=2, cy=3")
Rhombus(cx=2, cy=3)
PageBreak()

Blueprint()
Text(common=txt, text="Star")
Star()
PageBreak()

Blueprint()
Text(common=txt, text="Ellipse: centre; width=3, height=2")
Ellipse(cx=2, cy=1, width=3, height=2)
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
RightAngledTriangle(x=1, y=1, flip="north", hand="east", label="NE", fill="yellow")
RightAngledTriangle(x=2, y=2, flip="south", hand="east", label="SE", fill="green")
RightAngledTriangle(x=2, y=3, flip="north", hand="west", label="NW", fill="red")
RightAngledTriangle(x=3, y=4, flip="south", hand="west", label="SW", fill="blue")
PageBreak()

# ---- compass
Blueprint()
Text(common=txt, text="Compass")
Compass(cx=1, cy=1, perimeter='hexagon')
Compass(cx=2, cy=2, perimeter='circle')
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
Text(common=txt, text="StarField: Poly; multi-color&size")
plys = Common(x=1.5, y=1.4, sides=10, radius=1.5)
Polygon(common=plys, fill=black)
StarField(
    density=50,
    enclosure=polygon(common=plys),
    colors=[white, white, white, red, green, blue],
    sizes=[0.15, 0.15, 0.15, 0.15, 0.3, 0.3, 0.45])
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
EquilateralTriangle(common=eqt, flip="north", hand="east", label="UR", fill="yellow")
EquilateralTriangle(common=eqt, flip="south", hand="east", label="DR", fill="green")
EquilateralTriangle(common=eqt, flip="north", hand="west", label="UL", fill="red")
EquilateralTriangle(common=eqt, flip="south", hand="west", label="DL", fill="blue")
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
Grid(side=0.85, stroke=gray, stroke_width=0.5)
PageBreak()

Text(common=txt, text='DotGrid: "Moleskine" setting')
DotGrid(stroke=darkgray, width=0.5, height=0.5, dot_point=1, offset_y=-0.25)
PageBreak()

# ---- arc
Blueprint()
Text(common=txt, text="Arc; 'inside' rect")
Rectangle(x=1, y=1, height=1, width=2, dot=0.01,
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

# ---- trapezoid
Blueprint()
Text(common=txt, text="Trapezoid: flip")
eqt = Common(x=2, y=2, side=2)
Trapezoid(
    x=2, y=2,
    width=3, width2=2,
    flip="south",
    label="flip",
    hand="east", fill="yellow")
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

# ---- polygon radii
Blueprint()
Text(common=txt, text="Polygon: radii (default & custom)")
Polygon(cx=2, cy=4, sides=8, radius=1, radii=1)
Polygon(
    cx=2, cy=1, sides=10, radius=1, radii=1,
    radii_offset=0.5, radii_length=0.25, radii_stroke_width=1,
    dot=0.1, dot_stroke=red)
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
Text(common=txt, text="Rhombus: red => rotation 60\u00B0")
Rhombus(cx=2, cy=3, width=1.5, height=2*equi(1.5), dot=0.06)
Rhombus(cx=2, cy=3, width=1.5, height=2*equi(1.5), fill=None,
        stroke=red, stroke_width=.3, rotation=60, dot=0.04)
PageBreak()

# ---- rotation: stadium
Blueprint()
Text(common=txt, text="Stadium: red => rotation 60\u00B0")
Stadium(cx=2, cy=3, width=1.25, height=2, dot=0.06)
Stadium(cx=2, cy=3, width=1.25, height=2, fill=None,
        stroke=red, stroke_width=.3, rotation=60, dot=0.04)
PageBreak()

# ---- rotation: polygon
Blueprint()
Text(common=txt, text="Polygon: rotation (flat)")
poly6 = Common(fill=None, sides=6, diameter=1, stroke_width=1, orientation='flat')
Polygon(common=poly6, y=1, x=1.0, label="0")
Polygon(common=poly6, y=2, x=1.5, rotation=15, label="15")
Polygon(common=poly6, y=3, x=2.0, rotation=30, label="30")
Polygon(common=poly6, y=4, x=2.5, rotation=45, label="45")
Polygon(common=poly6, y=5, x=3.0, rotation=60, label="60")
PageBreak()

Blueprint()
Text(common=txt, text="Polygon: rotation (pointy)")
poly6 = Common(fill=None, sides=6, diameter=1, stroke_width=1, orientation='pointy')
Polygon(common=poly6, y=1, x=1.0, label="0")
Polygon(common=poly6, y=2, x=1.5, rotation=15, label="15")
Polygon(common=poly6, y=3, x=2.0, rotation=30, label="30")
Polygon(common=poly6, y=4, x=2.5, rotation=45, label="45")
Polygon(common=poly6, y=5, x=3.0, rotation=60, label="60")
PageBreak()

# ---- END
Text(common=txt, text="Shapes END...")
PageBreak(footer=True)

Save()
# Save(output='png', dpi=600)
