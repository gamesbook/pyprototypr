"""
Base test for pyprototypr

Written by: Derek Hohls
Created on: 9 March 2024
"""
from pyprototypr.draw import Create, PageBreak, Save, AutoGrid, Dot

Create(margin_left=0.5, margin_top=0.25)
AutoGrid(stroke_width=0.5)
Dot(x=0, y=2)
Dot(x=4, y=4)
PageBreak()
Save()
