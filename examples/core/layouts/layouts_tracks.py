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
shp = circle(cx=1, cy=1, radius=0.5, fill=None)
Track(rectangle(), shapes=[shp]*4)
PageBreak()

# ---- default track + cirlce
Blueprint()
Text(common=txt, text="Track: default + count")
shp = circle(cx=1, cy=1, radius=0.5, label='{count}')
Track(rectangle(), shapes=[shp]*4)
PageBreak()

# ---- square track + star
Blueprint()
Text(common=txt, text="Track: square: star")
shp = star(cx=1, cy=1, vertices=5, radius=0.5, label='{count}')
Track(square(side=1.5), shapes=[shp]*4)
PageBreak()

# ---- polygon track + hex
Blueprint()
Text(common=txt, text="Track: polygon: 8-sides")
shp = hexagon(cx=1, cy=1, height=0.5, label='{count}')
Track(polygon(cx=2, cy=3, radius=1.5, sides=8), shapes=[shp]*8)
PageBreak()

# ---- polygon track + hex
Blueprint()
Text(common=txt, text="Track: polygon with stop")
shp = hexagon(cx=1, cy=1, height=0.5, label='{count}')
Track(polygon(cx=2, cy=3, radius=1.5, sides=8), shapes=[shp]*8, stop=7)
PageBreak()

# ---- polyline track + shape
Blueprint()
Text(common=txt, text="Track: polyline")
shp = hexagon(cx=1, cy=1, height=0.5, label='{count}')
Track(Polyline(points=[(0, 0), (1, 2), (2, 1), (3, 3), (1, 5)]), shapes=[shp]*8)
PageBreak()

# # ---- circle track + shape
Blueprint()
Text(common=txt, text="Track: circle displayed")
#shp = rhombus(cx=1, cy=1, width=0.25, height=0.5, label='{count}')
shp = hexagon(cx=1, cy=1, height=0.5, label='{count}')
Track(Circle(cx=2, cy=3, radius=1.5), angles=[30,120,210,300], shapes=[shp]*8)
PageBreak()

# ---- polygon track
Blueprint()
Text(common=txt, text="Track: polygon: 6-sides")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{count}', peaks=[("n", 0.25)])
Track(
    polygon(cx=2, cy=3, sides=6, radius=1.5),
    shapes=[shp]*6,
)
PageBreak()

# ---- polygon track + anticlockwise
Blueprint()
Text(common=txt, text="Track: polygon: anticlockwise")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{count}', peaks=[("n", 0.25)])
Track(
    polygon(cx=2, cy=3, sides=6, radius=1.5),
    shapes=[shp]*6,
    anticlockwise='t',
)
PageBreak()

# ---- polygon track + rotation shape
Blueprint()
Text(common=txt, text="Track: polygon: rotate 'i'")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{count}', peaks=[("n", 0.25)])
Track(
    polygon(cx=2, cy=3, sides=6, radius=1.5),
    shapes=[shp]*6,
    rotation_style='i',
)
PageBreak()

# ---- polygon track + rotation shape
Blueprint()
Text(common=txt, text="Track: polygon/shape rotate 'o'")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{count}', peaks=[("n", 0.25)])
Track(
    polygon(cx=2, cy=3, sides=6, radius=1.5),
    shapes=[shp]*6,
    rotation_style='o',
)
PageBreak()

# ---- circle track + rotation shape
Blueprint()
Text(common=txt, text="Track: Circle: rotate 'o'")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{count}', peaks=[("n", 0.25)])
Track(
    Circle(cx=2, cy=3, radius=1.5),
    angles=[30,120,210,300],
    shapes=[shp]*4,
    rotation_style='o',
)
PageBreak()

# ---- square track + rotation shape
Blueprint()
Text(common=txt, text="Track: square: rotate 'i'")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{count}', peaks=[("n", 0.25)])
Track(
    Square(cx=2, cy=3, side=2),
    shapes=[shp]*4,
    rotation_style='i',
)
PageBreak()

# ---- square track + rotation shape
Blueprint()
Text(common=txt, text="Track: square: rotate 'o'")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{count}', peaks=[("n", 0.25)])
Track(
    Square(cx=2, cy=3, side=2),
    shapes=[shp]*4,
    rotation_style='o',
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
        None,
     ]
)
