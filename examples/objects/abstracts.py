# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: Derek Hohls
Created on: 27 September 2026
"""
from protograf import *

Create(
    filename="abstracts.pdf",
    paper_height=10,
    paper_width=10,
    margin=1,
    page_grid=1)

header = Common(x=0, y=0, font_size=12, align="left")
footer = Common(x=0, y=8.5, font_size=12, align="left")
thick = Default(stroke_width=0.5)

# ---- default Abstract Game Grid
Text("Abstract Game: Default Board", common=header)
agd = AbstractGame(default=thick)
AbstractState(board=agd)

# ---- Abstract Game Grids: Size and Position
PageBreak()
Text("Abstract Game: Default Board", common=header)
agsp = AbstractGame(
    x=0, y=0,
    height=1.25,
    rows=3, cols=3,
    default=thick
)
AbstractState(board=agsp)
ahsp = AbstractGame(
    name="hexagons",
    x=4, y=4,
    height=1.25,
    rows=3, cols=3,
    default=thick
)
AbstractState(board=ahsp)

# ---- Abstract Game Grid - styled
PageBreak()
ags = AbstractGame(
    name="grid",
    fills=["gold"],
    stroke="red",
    stroke_width=2,
    frame=True,
    frame_width=15,
    frame_stroke="limegreen",
    label=True,
    label_stroke="blue")
AbstractState(board=ags)
Text("Abstract Game: Styled Board", common=header)

# ---- Chess - setup
PageBreak()
Text("Chess Game: Setup", common=header)
agcs = AbstractGame(name="chess")
AbstractState(board=agcs, setup=True)

# ---- Chess - customised board
PageBreak()
agcs = AbstractGame(
    name="chess",
    fills=["#FFCE9E", "#D18B47"],  # browns
    frame=True,
    frame_width=15,
    frame_stroke="brown",
    label=True,
    label_stroke="#FFCE9E",
    label_offset_row=0.275,
    label_offset_col=0.25,
)
AbstractState(board=agcs, setup=True)
Text("Chess Game: Frame, Colors & Labels", common=header)

# ---- Chess - positions
PageBreak()
Text("Chess Game: Positions", common=header)
agcp = AbstractGame(name="chess")
AbstractState(
    board=agcp,
    positions="""
    r..qr.k.
    p....pbp
    bp...np.
    ...p....
    ........
    BPN.P.P.
    P.Q.NnBP
    R..R..K.
    """
)
Text("Fischer(B) vs Byrne(W);"
     " 1963/64 USA Chess Championship;"
     " end move 15",
     x=0, y=8.5, font_size=7, align="left")

# ---- Chess Grid - custom board areas
PageBreak()
Text("Grid (Chess): Custom Squares", common=header)
htch = Default(
    hatches='ne',
    hatches_count=15,
    hatches_stroke_width=1,
    hatches_stroke="dimgray")
sqr = Default(
    fill="white",
    stroke=None,
    height=1,
    width=1)
sqDark = rectangle(default=[sqr, htch])
sqLite = rectangle(default=sqr)

agcb = AbstractGame(
    name="chess",
    areas=[sqLite, sqDark],
)
AbstractState(board=agcb)


# ---- Shogi - setup
PageBreak()
Text("Shogi Game: Setup", common=footer)
agss = AbstractGame(name="shogi", label=True, default=thick)
AbstractState(board=agss, setup=True)

# ---- Shogi - positions
PageBreak()
Text("Shogi Game: Positions (International)", common=footer)
agcp = AbstractGame(
    name="shogi",
    fills=['#D8A300'],
    stroke_width=1.5,
    stroke="white",
    pieces_type="shogi-int")
AbstractState(
    board=agcp,
    positions="""
    L..R....K
    P.S.NnB.P
    B..PN.P.P
    .........
    ...s.....
    ....p....
    p....pb.p
    bp...n.p.
    l...r.k..
    """
)

# ---- Go- positions
PageBreak()
Text("Go Game: Positions", common=header)
aggp = AbstractGame(default=thick,
    name="go",
    label=True,
    fill='#D8A300')
AbstractState(
    board=aggp,
    positions="99/"*7 + ".B.B.W..W.BBB..B.W/" + "99/"*10
)

# ---- Checkers - setup
PageBreak()
Text("Checkers Game: Setup", common=header)
agks = AbstractGame(name="checkers")
AbstractState(board=agks, setup=True)


# ---- Hexagons - default
PageBreak()
Text("Hexagons: default with labels", common=header)
aghd = AbstractGame(name="hexagons", label=True, default=thick)
AbstractState(board=aghd)

# ---- Hexagons - hex game
PageBreak()
Text("Hexagons: Hex Game", common=header)
aghg = AbstractGame(name="hex", label=True, label_size=7, default=thick)
AbstractState(board=aghg)

# ---- Hexagons - hex game
PageBreak()
Text("Hexagons: hexhex", common=header)
aghh = AbstractGame(default=thick,
    name="hexhex",
    hexes=4,
    label_font='Courier',
    label_size=16,
)
AbstractState(board=aghh)

# ---- Hexagons - pattern
PageBreak()
Text("Hexagons: pattern", common=header)
agha = AbstractGame(default=thick,
    name="hexagons",
    rows=5,
    cols=7,
    fills=['lawngreen'],
    pattern = """
    . O O . O O .
     O O O O O O .
    O O . O . O O
     O O O O O O .
    . O O . O O .
    """)
AbstractState(board=agha)

# ---- Hexagons - pattern + pieces
PageBreak()
Text("Hexagons: pattern & pieces", common=header)
aghpp = AbstractGame(default=thick,
    name="hexagons",
    rows=5,
    cols=7,
    fills='lawngreen',
    label=True,
    pattern = """
    . O O . O O .
     O O O O O O .
    O O . O . O O
     O O O O O O .
    . O O . O O .
    """)
AbstractState(
    board=aghpp,
    positions="B2W/B4W/B3W/B4W/B2W")  # SHOULD ignore blank cells!!


# ---- Hexagons - cell shape
PageBreak()
Text("Hexagons: custom cell shape", common=header)
ags = AbstractGame(
    name="hexhex",
    hexes=4,
    label=True,
    cell_shape=circle(radius=0.56, stroke="red", stroke_width=1),
    stroke="white",
    label_stroke="grey",
)
AbstractState(board=ags)

# ---- Grid - reuse Chess pieces
PageBreak()
Text("Abstract Game: Chess Pieces", common=header)
knights = [
    ('K', 'chess_white_knight'),
    ('J', 'chess_black_knight')]
agcp = AbstractGame(default=thick,
    rows=4, cols=4,
    pieces=knights,
    )
AbstractState(
    board=agcp,
    positions="""
    .
    KKKK
    JJJJ
    .
    """)

# ---- Hexagons - custom pieces
PageBreak()
Text(common=header, text="Grid: custom pieces")

red_pieces = Common(
    radius=0.4, fill="red",
    radii_stroke_width=4, radii_stroke="black",
    dot_stroke="black")
blu_pieces = Common(
    radius=0.4, fill="blue",
    radii_stroke_width=4, radii_stroke="silver",
    dot_stroke="silver")

angles = [60, 120, 180, 240, 300, 360]

RA = circle(common=red_pieces, radii=angles, radii_dotted=True)
RL = circle(common=red_pieces, radii=angles)
RC = circle(common=red_pieces, dot=0.1)

BA = circle(common=blu_pieces, radii=angles, radii_dotted=True)
BL = circle(common=blu_pieces, radii=angles)
BC = circle(common=blu_pieces, dot=0.1)

all_pieces = [
    ('A', RA), ('L', RL), ('C', RC),
    ('a', BA), ('l', BL), ('c', BC),
]

agpi = AbstractGame(default=thick,
    name="hexhex",
    y=1,
    height=1,
    hexes=4,
    pieces=all_pieces)
AbstractState(
    board=agpi,
    positions="4/lacal/6/7/6/LACAL/4"
)

# ---- Grid - stacked pieces
PageBreak()
Text(common=header, text='Grid: "stacked" pieces')
blak_pieces = Common(
    radius=0.4, fill="black",
    label_size=14,
    label_stroke="white")
wite_pieces = Common(
    radius=0.4, fill="white",
    label_size=14,
    label_stroke="black")

B1 = circle(common=blak_pieces, label="1")
B2 = circle(common=blak_pieces, label="2")
B3 = circle(common=blak_pieces, label="3")
B4 = circle(common=blak_pieces, label="4")
B5 = circle(common=blak_pieces, label="5")
B6 = circle(common=blak_pieces, label="6")
B7 = circle(common=blak_pieces, label="7")
B8 = circle(common=blak_pieces, label="8")
B9 = circle(common=blak_pieces, label="9")
W1 = circle(common=wite_pieces, label="1")
W2 = circle(common=wite_pieces, label="2")
W3 = circle(common=wite_pieces, label="3")
W4 = circle(common=wite_pieces, label="4")
W5 = circle(common=wite_pieces, label="5")
W6 = circle(common=wite_pieces, label="6")
W7 = circle(common=wite_pieces, label="7")
W8 = circle(common=wite_pieces, label="8")
W9 = circle(common=wite_pieces, label="9")

num_pieces = [
    ('q', B1), ('w', B2), ('e', B3), ('r', B4), ('t', B5),
    ('y', B6), ('u', B7), ('i', B8), ('o', B9), #'p', B2),
    ('1', W1), ('2', W2), ('3', W3), ('4', W4), ('5', W5),
    ('6', W6), ('7', W7), ('8', W8), ('9', W9), #'p', W2),
]

aggi = AbstractGame(default=thick,
    name="grid",
    y=1,
    height=1,
    rows=5, cols=5,
    pieces=num_pieces)
AbstractState(
    board=aggi,
    positions="""
    qwert
    yuio.
    .....
    6789.
    12345"""
)

# ---- Abstract Game Grid - markers
PageBreak()
Text(common=header, text="Grid Board: markers and annotations")
agm = AbstractGame(
    x=2, y=1,
    height=1,
    label=True,
    rows=5, cols=5,
    default=thick
)
markers = [
    line(xy=agm.b2.c, xy1=agm.d4.c, stroke_width=2, arrow=True),
    text(agm.d4.name, xy=agm.d4.c),
]
annotations = [
    circle(cxy=agm.c3.c, fill_stroke="green")
]
AbstractState(
    board=agm,
    annotations=annotations,
    markers=markers,
)

# ---- Abstract Game Grid - annotations
PageBreak()
Text(common=header, text="Grid Board: annotations")
aga = AbstractGame(
    label=True,
    rows=6, cols=6,
    default=thick
)
cross = Common(
    side=aga.a6.ht,
    stroke_width=0.5,
    hatches='d',
    hatches_count=2,
    hatches_stroke='red',
    hatches_stroke_width=1.5)
annotations = [
    square(cxy=aga.a6.c, common=cross),
    square(cxy=aga.f6.c, common=cross),
    square(cxy=aga.a1.c, common=cross),
    square(cxy=aga.f1.c, common=cross),
    circle(cxy=aga.c3.ne, fill_stroke="red", transparency=50),
]
AbstractState(
    board=aga,
    annotations=annotations,
)



Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/objects",
    names=[
        'abstracts_default',
        'abstracts_size_position',
        'abstracts_styled',
        'abstracts_chess_setup',
        'abstracts_chess_customised',
        'abstracts_chess_positions',
        'abstracts_chess_custom_board',
        'abstracts_shogi_setup',
        'abstracts_shogi_positions',
        'abstracts_go_positions',
        'abstracts_checkers_setup',
        'abstracts_hexagons_default',
        'abstracts_hexagons_hexgame',
        'abstracts_hexagons_hexhex',
        'abstracts_hexagons_pattern',
        'abstracts_hexagons_pattern_pieces',
        'abstracts_hexagons_cell_shape',
        'abstracts_grid_chess_pieces',
        'abstracts_grid_pieces',
        'abstracts_grid_pieces_numbered',
        'abstracts_grid_markers',
        'abstracts_grid_annotations',
    ]
)
