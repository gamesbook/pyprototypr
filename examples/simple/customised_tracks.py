"""
Show customised Tracks - and useful overides - for pyprototypr

Written by: Derek Hohls
Created on: 24 September 2024
"""
from pyprototypr import *

Create(filename="customised_tracks.pdf",
       paper=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2,
       font_size=8)
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
shp = circle(cx=1, cy=1, radius=0.5, label='X-{count}', fill=None)
Track(rectangle(), shapes=[shp]*4)
PageBreak()

# ---- default track + shape
Blueprint()
Text(common=txt, text="Track: default + shape")
shp = circle(cx=1, cy=1, radius=0.5, label='X-{count}')
Track(rectangle(), shapes=[shp]*4)
PageBreak()

# ---- square track + shape
Blueprint()
Text(common=txt, text="Track: square + shape")
shp = star(cx=1, cy=1, vertices=5, radius=0.5, label='{count}')
Track(square(side=1.5), shapes=[shp]*4)
PageBreak()

# # ---- polygon track + shape
Blueprint()
Text(common=txt, text="Track: polygon + shape")
shp = hexagon(cx=1, cy=1, height=0.5, label='{count}')
Track(polygon(cx=2, cy=3, radius=1.5, sides=8), shapes=[shp]*8)
PageBreak()

# # ---- polygon track + shape
Blueprint()
Text(common=txt, text="Track: polygon + shape + stop")
shp = hexagon(cx=1, cy=1, height=0.5, label='{count}')
Track(polygon(cx=2, cy=3, radius=1.5, sides=8), shapes=[shp]*8, start=2, stop=8)
PageBreak()

# ---- polyline track + shape
Blueprint()
Text(common=txt, text="Track: polyline + shape")
shp = hexagon(cx=1, cy=1, height=0.5, label='{count}')
Track(Polyline(points=[(0, 0), (1, 2), (2, 1), (3, 3), (1, 5)]), shapes=[shp]*8)
PageBreak()

# # ---- circle track + shape
Blueprint()
Text(common=txt, text="Track: circle + shape")
#shp = rhombus(cx=1, cy=1, width=0.25, height=0.5, label='{count}')
shp = hexagon(cx=1, cy=1, height=0.5, label='{count}')
Track(Circle(cx=2, cy=3, radius=1.5), angles=[30,120,210,300], shapes=[shp]*8)
PageBreak()

# ---- polygon track + rotation shape
Blueprint()
Text(common=txt, text="Track: polygon/shape rotate 'i'")
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
Text(common=txt, text="Track: circle/shape rotate 'o'")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{count}', peaks=[("n", 0.25)])
Track(
    Circle(cx=2, cy=3, radius=1.5),
    angles=[30,120,210,300],
    shapes=[shp]*4,
    rotation_style='o',
)
PageBreak()

Blueprint()
Text(common=txt, text="Track: square/shape rotate 'i'")
shp = rectangle(cx=1, cy=1, width=0.5, height=0.5, label='{count}', peaks=[("n", 0.25)])
Track(
    Square(cx=2, cy=3, side=2),
    shapes=[shp]*4,
    rotation_style='i',
)
PageBreak()

# ---- END
Text(common=txt, text="Tracks END...")
PageBreak(footer=True)

Save()
# Save(output='png', dpi=600)
