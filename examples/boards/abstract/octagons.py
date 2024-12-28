"""
An Octagons board example for pyprototypr

Written by: Derek Hohls
Created on: 29 December 2024
"""

from pyprototypr import *

Create(filename="octagons.pdf", margin=1.25)

Rectangle(x=1, y=4, height=15, width=15.5, fill=grey)

oct_flat = polygon(
    sides=8, x=1.1, y=4, width=2.35, height=2.35, stroke_width=2, fill=white,
    perbis=True, perbis_directions='1,5', perbis_stroke_width=2)
oct_vert = polygon(
    sides=8, x=1.1, y=4, width=2.35, height=2.35, stroke_width=2, fill=white,
    perbis=True, perbis_directions='3,7', perbis_stroke_width=2)

octos = Common(cols=8, rows=8, gap=2.2)

Repeat(oct_flat, common=octos, across=(1, 3, 5, 7), down=(1, 3, 5, 7), offset_x=2.2)
Repeat(oct_vert, common=octos, across=(1, 3, 5, 7), down=(1, 3, 5, 7), offset_x=0)
Repeat(oct_vert, common=octos, across=(2, 4, 6, 8), down=(2, 4, 6, 8), offset_x=0)
Repeat(oct_flat, common=octos, across=(2, 4, 6, 8), down=(2, 4, 6, 8), offset_x=-2.2)

Save()
