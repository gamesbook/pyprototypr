"""
MR Hex for pyprototypr

Written by: Derek Hohls
Created on: 19 April 2024
"""
from pyprototypr.draw import *

Create(filename="plain_grid.pdf",
       pagesize=A4,
       margins=0.5)

Grid(size=0.85, stroke=gray)  # 1/3"

Save()
