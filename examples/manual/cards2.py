"""
`cards2` example for pyprototypr

Written by: Derek Hohls
Created on: 29 February 2016
"""
from pyprototypr.draw import *

Create(pagesize=A3,
       filename="example2.pdf")
Deck(cards=9)
Save()
