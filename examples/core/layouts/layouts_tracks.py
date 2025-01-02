"""
Show customised Tracks - and useful overides - for pyprototypr

Written by: Derek Hohls
Created on: 24 September 2024
"""
from pyprototypr import *

Create(filename="customised_tracks.pdf",
       paper=A8,
       margin=0.75,
       margin_right=0.2, margin_top=0.2,
       font_size=8,
       stroke_width=0.5)

Footer(draw=False)

txt = Common(x=0, y=6, font_size=8, align="left")

Text(common=txt, text="Tracks START...")
PageBreak(footer=True)

# ---- default track
Blueprint()
Text(common=txt, text="Track: default")
Track()
PageBreak()

# ---- default track + shape
Blueprint()
Text(common=txt, text="Track: default + shape")
shp = circle(cx=1, cy=1, radius=0.25, fill=None)
Track(rectangle(), shapes=[shp])
PageBreak()

# ---- default track + circle
Blueprint()
Text(common=txt, text="Track: default + sequence")
shp = circle(cx=1, cy=1, radius=0.25, label='{{sequence}}')
Track(rectangle(), shapes=[shp])
PageBreak()

# ---- square track + star
Blueprint()
Text(common=txt, text="Track: square; star")
shp = star(cx=1, cy=1, vertices=5, radius=0.5, label='{{sequence}}')
Track(square(side=1.5), shapes=[shp])
PageBreak()

# ---- polygon track + hex
Blueprint()
Text(common=txt, text="Track: polygon; 8-sided")
shp = hexagon(cx=1, cy=1, height=0.5, label='{{sequence}}')
Track(polygon(cx=2, cy=3, radius=1.5, sides=8), shapes=[shp])
PageBreak()

# ---- polygon track + hex
Blueprint()
Text(common=txt, text="Track: polygon with start/stop")
shp = hexagon(cx=1, cy=1, height=0.5, label='{{sequence}}')
Track(polygon(cx=2, cy=3, radius=1.5, sides=8), shapes=[shp], start=3, stop=6)
PageBreak()

# ---- polyline track + shape
Blueprint()
Text(common=txt, text="Track: polyline")
shp = circle(cx=1, cy=1, radius=0.25, label='{{sequence}}')
Track(Polyline(points=[(0, 0), (1, 2), (2, 1), (3, 3), (1, 5)]), shapes=[shp])
PageBreak()

# # ---- circle track + shape
Blueprint()
Text(common=txt, text="Track: circle; clockwise")
#shp = rhombus(cx=1, cy=1, width=0.25, height=0.5, label='{{sequence}}')
shp = hexagon(cx=1, cy=1, height=0.5, label='{{sequence}}')
Track(
     Circle(cx=2, cy=3, radius=1.5),
     angles=[30,120,210,300],
     shapes=[shp],
     clockwise=True
)
PageBreak()

# ---- polygon track
Blueprint()
Text(common=txt, text="Track: polygon; 6-sided")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{{sequence}}', peaks=[("n", 0.25)])
Track(
    polygon(cx=2, cy=3, sides=6, radius=1.5),
    shapes=[shp],
)
PageBreak()

# ---- polygon track + clockwise
Blueprint()
Text(common=txt, text="Track: polygon; clockwise")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{{sequence}}', peaks=[("n", 0.25)])
Track(
    polygon(cx=2, cy=3, sides=6, radius=1.5),
    shapes=[shp],
    clockwise=True,
)
PageBreak()

# ---- polygon track + rotation shape
Blueprint()
Text(common=txt, text="Track: polygon; rotate 'i'")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{{sequence}}', peaks=[("n", 0.25)])
Track(
    polygon(cx=2, cy=3, sides=6, radius=1.5),
    shapes=[shp],
    rotation_style='i',
)
PageBreak()

# ---- polygon track + rotation shape
Blueprint()
Text(common=txt, text="Track: polygon; rotate 'o'")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{{sequence}}', peaks=[("n", 0.25)])
Track(
    polygon(cx=2, cy=3, sides=6, radius=1.5),
    shapes=[shp],
    rotation_style='o',
)
PageBreak()

# ---- circle track + rotation shape
Blueprint()
Text(common=txt, text="Track: circle; rotate 'o'")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{{sequence}}', peaks=[("n", 0.25)])
Track(
    Circle(cx=2, cy=3, radius=1.5),
    angles=[30,120,210,300],
    shapes=[shp],
    rotation_style='o',
)
PageBreak()

# ---- rectangle track + rotation shape
Blueprint()
Text(common=txt, text="Track: rectangle; rotate 'i'")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{{sequence}}', peaks=[("n", 0.25)])
Track(
    Rectangle(cx=2, cy=3, height=2, width=2),
    shapes=[shp],
    rotation_style='i',
)
PageBreak()

# ---- rectangle track + rotation shape
Blueprint()
Text(common=txt, text="Track: rectangle; rotate 'o'")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{{sequence}}', peaks=[("n", 0.25)])
Track(
    Rectangle(cx=2, cy=3, height=2, width=2),
    shapes=[shp],
    rotation_style='o',
)
PageBreak()

# ---- polygon track + sequences
Blueprint()
Text(common=txt, text="Track: polygon; sequences")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{{sequence}}', peaks=[("n", 0.25)])
Track(
    polygon(cx=2, cy=3, sides=12, radius=1.5),
    shapes=[shp],
    rotation_style='o',
    sequences=[1,3,5,7,9,11]
)
PageBreak()

# ---- clock shape
Blueprint()
Text(common=txt, text="Track: circles; 'clock'")
Circle(cx=2, cy=3, radius=1.8, stroke_width=2, dot=0.1)
shp = circle(cx=1, cy=1, radius=0.25, stroke=white,
             label='{{sequence}}', label_stroke=black)
Track(
    circle(cx=2, cy=3, radius=1.5),
    angles=[60,90,120,150,180,210,240,270,300,330,0,30],
    shapes=[shp],
    rotation_style='o',
    clockwise=True,
)
PageBreak()

# ---- scoring track
Blueprint()
Text(common=txt, text="Track: polygon; 'scoring'")
trk = polygon(cx=2, cy=3, sides=30, radius=1.75)
shp = circle(cx=1, cy=1, radius=0.18, stroke=navy,
             label='{{sequence}}', label_size=6)
Track(
    trk,
    shapes=[shp],
    rotation_style='o',
    clockwise=True,
    start=24
)
shp5 = circle(cx=1, cy=1, radius=0.18, stroke=navy, fill=aqua,
             label='{{sequence}}', label_size=6)
Track(
    trk,
    shapes=[shp5],
    rotation_style='o',
    clockwise=True,
    start=24,
    sequences=[5,10,15,20,25,30,35]
)
PageBreak()

# ---- END
Text(common=txt, text="Tracks END...")
PageBreak(footer=True)

# Save()
Save(
     output='png',
     dpi=300,
     directory="docs/images/tracks",
     names=[
        None,
        "track_default", "track_default_circle", "track_default_count",
        "track_square_star",
        "track_polygon_hex",  "track_polygon_hex_stop",
        "track_polyline",
        "track_circle",
        "track_polygon_six",  "track_polygon_anti",
        "track_polygon_rotate_i", "track_polygon_rotate_o",
        "track_circle_rotate_o",
        "track_square_rotate_i", "track_square_rotate_o",
        "track_sequences",
        "track_clock", "track_score",
        None,
     ]
)
