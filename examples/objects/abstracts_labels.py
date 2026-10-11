"""
Written by: Derek Hohls
Created on: 9 Oct 2026
"""
from protograf import *
from protograf.shapes import HexHexLocations

Create(
    paper_height=20,
    paper_width=20,
    margin=1,
    stroke_width=0.5,
    page_grid=1,
    page_grid_dark=5,
    show_margins=True,
)
txt = Common(x=0, y=0, font_size=12, align="left")
header = Common(x=0, y=0, font_size=12, align="left")
diagram= Common(font_size=12, align="centre")


# ---- HexHex Grid Labels
games = Common(
    name="hexhex",
    height=1.5,
    hexes=4,
    label=True,
    label_size=12,
)

abl = AbstractGame(
    common=games,
    x=0, y=0,
    label_start='BL',
    )
AbstractState(
    board=abl,
    annotations=[
        text(abl.a1.name, xy=abl.a1.c),
        text(abl.g6.name, xy=abl.g6.c)]
)
Text("HexHex: label BL", x=4, y=8, common=diagram)

abr = AbstractGame(
    common=games,
    x=10, y=0,
    label_start='BR',
    )
AbstractState(
    board=abr,
    annotations=[
        text(abr.a1.name, xy=abr.a1.c),
        text(abr.g6.name, xy=abr.g6.c)]
)
Text("HexHex: label BR", x=14, y=8, common=diagram)

atl = AbstractGame(
    common=games,
    x=0, y=10,
    label_start='TL',
    )
AbstractState(
    board=atl,
    annotations=[
        text(atl.a1.name, xy=atl.a1.c),
        text(atl.g6.name, xy=atl.g6.c)]
)
Text("HexHex: label TL", x=4, y=18, common=diagram)

atr = AbstractGame(
    common=games,
    x=10, y=10,
    label_start='TR',
    )
AbstractState(
    board=atr,
    annotations=[
        text(atr.a1.name, xy=atr.a1.c),
        text(atr.g6.name, xy=atr.g6.c)]
)
Text("HexHex: label TR", x=14, y=18, common=diagram)

PageBreak()

# ---- Hexagonal Grid Labels ==================================================
games = Common(
    name="hexagonal",
    height=1.5,
    hexes=4,
    label=True,
    label_size=12,
)

abl = AbstractGame(
    common=games,
    x=0, y=0,
    label_start='BL',
    )
AbstractState(
    board=abl,
    annotations=[
        text(abl.a1.name, xy=abl.a1.c),
        text(abl.g6.name, xy=abl.g6.c)]
)
Text("Hexagonal: label BL", x=4, y=8, common=diagram)

abr = AbstractGame(
    common=games,
    x=10, y=0,
    label_start='BR',
    )
AbstractState(
    board=abr,
    annotations=[
        text(abr.a1.name, xy=abr.a1.c),
        text(abr.g6.name, xy=abr.g6.c)]
)
Text("Hexagonal: label BR", x=14, y=8, common=diagram)

atl = AbstractGame(
    common=games,
    x=0, y=10,
    label_start='TL',
    )
AbstractState(
    board=atl,
    annotations=[
        text(atl.a1.name, xy=atl.a1.c),
        text(atl.g6.name, xy=atl.g6.c)]
)
Text("Hexagonal: label TL", x=4, y=18, common=diagram)

atr = AbstractGame(
    common=games,
    x=10, y=10,
    label_start='TR',
    )
AbstractState(
    board=atr,
    annotations=[
        text(atr.a1.name, xy=atr.a1.c),
        text(atr.g6.name, xy=atr.g6.c)]
)
Text("Hexagonal: label TR", x=14, y=18, common=diagram)

PageBreak()

# ---- Rectangular Grid Labels ================================================
gridded = Common(
    name="grid",
    height=1.5,
    rows=6,
    cols=7,
    label=True,
    label_size=12,
)

agbl = AbstractGame(
    common=gridded,
    x=1, y=0,
    label_start='BL',
    )
AbstractState(
    board=agbl,
    annotations=[
        text(agbl.a1.name, xy=agbl.a1.c),
        text(agbl.g6.name, xy=agbl.g6.c)]
)
Text("Grid: label BL", x=4, y=8, common=diagram)

agbr = AbstractGame(
    common=gridded,
    x=11, y=0,
    label_start='BR',
    )
AbstractState(
    board=agbr,
    annotations=[
        text(agbr.a1.name, xy=agbr.a1.c),
        text(agbr.g6.name, xy=agbr.g6.c)]
)
Text("Grid: label BR", x=14, y=8, common=diagram)

agtl = AbstractGame(
    common=gridded,
    x=1, y=11,
    label_start='TL',
    )
AbstractState(
    board=agtl,
    annotations=[
        text(agtl.a1.name, xy=agtl.a1.c),
        text(agtl.g6.name, xy=agtl.g6.c)]
)
Text("Grid: label TL", x=4, y=18, common=diagram)

agtr = AbstractGame(
    common=gridded,
    x=11, y=11,
    label_start='TR',
    )
AbstractState(
    board=agtr,
    annotations=[
        text(agtr.a1.name, xy=agtr.a1.c),
        text(agtr.g6.name, xy=agtr.g6.c)]
)
Text("Grid: label TR", x=14, y=18, common=diagram)


Save()
