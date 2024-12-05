# -*- coding: utf-8 -*-
"""
Global variables for proto (import at top-level)
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

def initialize():
    global cnv
    global deck
    global dataset
    global filename
    global margin
    global margin_left
    global margin_top
    global margin_bottom
    global margin_right
    global footer
    global footer_draw
    global page_count
    global pargs
    global paper
    global font_size
    global units

    cnv = None  # will become a reportlab.canvas object
    deck = None  # will become a shapes.DeckShape object
    filename = None
    dataset = None  # will become a dictionary of data loaded from a file
    margin = 1
    margin_left = margin
    margin_top = margin
    margin_bottom = margin
    margin_right = margin
    footer = None
    footer_draw = False
    page_count = 0
    pargs = None
    paper = A4
    font_size = 12
    units = cm
