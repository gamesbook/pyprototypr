"""
Show customised BluePrint shape for pyprototypr

Written by: Derek Hohls
Created on: 18 August 2024
"""

from pyprototypr import *

Create(filename="customised_blueprint.pdf",
       pagesize=A8,
       margin_top=0.2,
       margin_left=0.15,
       margin_right=0.2,
       font_size=8)

txt = Common(x=0, y=6, font_size=8, align="left")

Blueprint()
Text(common=txt, text="Blueprint")
PageBreak()

Blueprint(stroke_width=0.8)
Text(common=txt, text="Blueprint: stroke_width=0.8")
PageBreak()

Blueprint(stroke=red)
Text(common=txt, text="Blueprint: stroke=red")
PageBreak()

Blueprint(style='invert')
Text(common=txt, text="Blueprint: style=blue")
PageBreak()

Blueprint(style='green')
Text(common=txt, text="Blueprint: style=green")
PageBreak()

Blueprint(style='grey')
Text(common=txt, text="Blueprint: style=grey")
PageBreak()

Blueprint(style='grey', stroke=purple)
Text(common=txt, text="Blueprint: grey; stroke=purple")
PageBreak()

Blueprint(subdivisions=5)
Text(common=txt, text="Blueprint: subdivisions=5")
PageBreak()

Blueprint(subdivisions=5, subdivisions_dashes=[0.01, 0.01, 0])
Text(common=txt, text="Blueprint: subdivisions as dashes")
PageBreak()


Save()
