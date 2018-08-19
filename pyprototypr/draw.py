#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Drawing interface for pyprototypr
"""
# future
from __future__ import division
# lib
# third party
from reportlab.lib.pagesizes import *
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import *
# local
from bgg import BGGGame, BGGGameList
from base import BaseShape, BaseCanvas, GroupBase, UNITS, COLORS
from shapes import \
    BezierShape, CardShape, CircleShape, CommonShape, \
    ConnectShape, DeckShape, EllipseShape, FooterShape, GridShape, HexShape, \
    ArcShape, ImageShape, LineShape,PolygonShape, \
    PolylineShape, Query, RectShape, RepeatShape, RhombusShape, ShapeShape, \
    StarShape, TextShape, Value
from dice import Dice, DiceD4, DiceD6, DiceD8, DiceD10, DiceD12, DiceD20, \
    DiceD100
from utils.support import numbers, letters, split, combinations, base_fonts
from utils import tools


cnv = None  # will become a reportlab.canvas object
deck = None  # will become a shapes.DeckShape object
dataset = None  # will become a dictionary of data loaded from a file
# default margins
margin = 1
margin_left = margin
margin_top = margin
margin_bottom = margin
margin_right = margin
is_footer = False
footer = None
page_count = 0


def Create(**kwargs):
    """Initialisation of page and canvas.

    Allows shortcut creation of cards.
    """
    global cnv
    global deck
    global margin
    global margin_left
    global margin_top
    global margin_bottom
    global margin_right
    global pagesize
    # margin
    margin = kwargs.get('margin', margin)
    margin_left = kwargs.get('margin_left', margin)
    margin_top = kwargs.get('margin_top', margin)
    margin_bottom = kwargs.get('margin_bottom', margin)
    margin_right = kwargs.get('margin_right', margin)
    # cards etc
    _cards = kwargs.get('cards', 0)
    filename = kwargs.get('filename', None)
    fonts = kwargs.get('fonts', [])
    landscape = kwargs.get('landscape', False)
    kwargs = margins(**kwargs)
    base_fonts()
    for _font in fonts:
        pdfmetrics.registerFont(TTFont(_font[0], _font[1]))
    if not filename:
        if _cards:
            filename = 'cards.pdf'
        else:
            filename = 'test.pdf'
    pagesize = kwargs.get('pagesize', A4)
    defaults = kwargs.get('defaults', None)
    cnv = BaseCanvas(filename, pagesize=pagesize, defaults=defaults)
    if landscape:
        cnv.canvas.setPageSize(landscape(pagesize))
    if _cards:
        Deck(canvas=cnv, sequence=range(1, _cards + 1),
             **kwargs)  # set deck variable


def create(**kwargs):
    global cnv
    global deck
    Create(**kwargs)


def Footer(**kwargs):
    global cnv
    global margin
    global margin_left
    global margin_bottom
    global margin_right
    global pagesize
    global is_footer
    global footer
    is_footer = True
    footer = FooterShape(_object=None, canvas=cnv, **kwargs)


def Header(**kwargs):
    global cnv
    global margin
    global margin_left
    global margin_bottom
    global margin_right


def PageBreak():
    global cnv
    global deck
    global is_footer
    global page_count
    global footer

    if is_footer is True:
        page_count += 1
        footer.draw(cnv=cnv, ID=page_count)
    cnv.canvas.showPage()


def page_break():
    PageBreak()


def Save():
    global cnv
    global deck
    if deck and len(deck.deck) > 1:
        deck.draw(cnv)
        cnv.canvas.showPage()
    cnv.canvas.save()


def save():
    Save()


def margins(**kwargs):
    global margin
    global margin_left
    global margin_top
    global margin_bottom
    global margin_right
    kwargs['margin'] = kwargs.get('margin', margin)
    kwargs['margin_left'] = kwargs.get('margin_left', margin)
    kwargs['margin_top'] = kwargs.get('margin_top', margin)
    kwargs['margin_bottom'] = kwargs.get('margin_bottom', margin)
    kwargs['margin_right'] = kwargs.get('margin_right', margin)
    return kwargs

### cards ====================================================================


def Card(sequence, *elements):
    """Add one or more elements to a card or cards."""
    global cnv
    global deck
    global dataset
    _cards = []
    # int - single card
    try:
        _card = int(sequence)
        _cards = range(_card, _card + 1)
    except:
        pass
    # string - either 'all' or a range: '1', '1-2', '1-3,5-6'
    if not _cards:
        try:
            if sequence.lower() == 'all':
                _cards = range(1, len(dataset) + 1)
            else:
                _cards = tools.sequence_split(sequence)
        except:
            tools.feedback(
                'Unable to convert "%s"" into a card or range or cards' %
                sequence)
    for _card in _cards:
        card = deck.get(_card - 1)  # cards internally number from ZERO
        if card:
            for element in elements:
                element.members = _cards  # track all related cards
                card.members = _cards
                card.elements.append(element)  # may be Group or Shape or Query
        else:
            tools.feedback("Cannot find card# %s" % _card)


def Deck(**kwargs):
    """Initialise a deck with all its settings, including source of data."""
    global cnv
    global deck
    global margin
    global margin_left
    global margin_top
    global margin_bottom
    global margin_right
    margin = kwargs.get('margin', margin)
    margin_left = kwargs.get('margin_left', margin)
    margin_top = kwargs.get('margin_top', margin)
    margin_bottom = kwargs.get('margin_bottom', margin)
    margin_right = kwargs.get('margin_right', margin)
    deck = DeckShape(**kwargs)


def group(*args):
    global cnv
    global deck
    g = GroupBase()
    for arg in args:
        g.append(arg)
    return g

### data and functions  ======================================================


def Data(source=None, **kwargs):
    """Load data from file into a dictionary for shared access."""
    global cnv
    global deck
    global dataset
    dataset = tools.load_data(source, **kwargs)
    #print "draw_142:dataset loaded", dataset
    if len(dataset) == 0:
        tools.feedback("Dataset is empty or cannot be loaded!")
    else:
        deck.create(len(dataset))
        deck.dataset = dataset


def V(*args):
    """Expect args[0] to be the name (string) of a column in the dataset."""
    global dataset
    #print "draw_239 ... V", args, type(dataset), len(dataset)
    if dataset and len(dataset) > 0:
        return [item.get(args[0], '') for item in dataset]
    return []


def Q(query='', result=None, alternate=None):
    """
    Enable querying/selction of data from a dataset list

        query: str
            boolean-type expression which can be evaluated to return a True
            e.g. 'name`=`fred' filters item for dataset['name'] == 'fred'
        result: str or element
            returned if query is True
        alternate: str or element
            OPTIONAL; returned if query is False; if not supplied, then None
    """
    global dataset
    if dataset and len(dataset) > 0:
        query_list = tools.query_construct(query)
        # [[key, operator, target, LINKER], ...]
        for query_item in query_list:
            vals = [item.get(query_item[0], '') for item in dataset]
            query_item[0] = vals
            # [(list_of_possible_targets, operator, target, LINKER), ...]
        return Query(query=query_list, result=result, alternate=alternate)
    return None


def Set(_object, **kwargs):
    """Overwrite one or more properties for a Shape/object with new value(s)"""
    for kw in kwargs.keys():
        #print "draw_271", kw, kwargs[kw], type(kwargs[kw])
        setattr(_object, kw, kwargs[kw])
    return _object

### shapes ===================================================================


def Common(source=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['source'] = source
    cshape = CommonShape(canvas=cnv, **kwargs)
    return cshape


def common(source=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['source'] = source
    cshape = CommonShape(canvas=cnv, **kwargs)
    return cshape


def Image(source=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['source'] = source
    image = ImageShape(canvas=cnv, **kwargs)
    image.draw()
    return image


def image(source=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['source'] = source
    return ImageShape(canvas=cnv, **kwargs)


def Arc(**kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    arc = ArcShape(canvas=cnv, **kwargs)
    arc.draw()
    return arc


def arc(**kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    return ArcShape(canvas=cnv, **kwargs)


def Bezier(**kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    bezier = BezierShape(canvas=cnv, **kwargs)
    bezier.draw()
    return bezier


def bezier(**kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    return BezierShape(canvas=cnv, **kwargs)


def Circle(**kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    circle = CircleShape(canvas=cnv, **kwargs)
    circle.draw()
    return circle


def circle(**kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    return CircleShape(canvas=cnv, **kwargs)


def Ellipse(**kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    ellipse = EllipseShape(canvas=cnv, **kwargs)
    ellipse.draw()
    return ellipse


def ellipse(**kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    return EllipseShape(canvas=cnv, **kwargs)


def Grid(**kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    # override defaults ... otherwise grid not "next" to margins
    kwargs['x'] = kwargs.get('x', 0)
    kwargs['y'] = kwargs.get('y', 0)
    grid = GridShape(canvas=cnv, **kwargs)
    grid.draw()
    return grid


def AutoGrid(**kwargs):
    global cnv
    global deck
    global pagesize
    global margin_left
    global margin_top
    global margin_bottom
    global margin_right
    kwargs = margins(**kwargs)
    kwargs['units'] = kwargs.get('units', cm)
    size = 1.0
    if kwargs['units'] == inch:
        size = 0.5
    # override defaults ... otherwise grid not "next" to margins
    numbering = kwargs.get('numbering', True)
    kwargs['size'] = kwargs.get('size', size)
    kwargs['x'] = kwargs.get('x', 0)
    kwargs['y'] = kwargs.get('y', 0)
    kwargs['stroke'] = kwargs.get('stroke', lightsteelblue)
    m_x = kwargs['units'] * (margin_left + margin_right)
    m_y = kwargs['units'] * (margin_top + margin_bottom)
    _cols = (pagesize[0] - m_x) / (kwargs['units'] * float(kwargs['size']))
    _rows = (pagesize[1] - m_y) / (kwargs['units'] * float(kwargs['size']))
    rows = int(_rows)
    cols = int(_cols)
    kwargs['rows'] = kwargs.get('rows', rows)
    kwargs['cols'] = kwargs.get('cols', cols)
    kwargs['stroke_width'] = kwargs.get('stroke_width', 0.33)
    kwargs['font_size'] = kwargs.get('font_size', 10)
    grid = GridShape(canvas=cnv, **kwargs)
    grid.draw()
    if numbering:
        common = Common(font_size=kwargs['font_size'],
                        stroke=kwargs['stroke'],
                        units=kwargs['units'])
        for x in range(0, kwargs['cols'] + 1):
            Text(x=x*size,
                 y=kwargs['y'] - kwargs['size'] / 2.0,
                 text=str(x*size),
                 common=common)
        for y in range(0, kwargs['rows'] + 1):
            Text(x=kwargs['x'] - kwargs['size'] / 2.0,
                 y=y*size,
                 text=str(y*size),
                 common=common)
    return grid


def Hexagon(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    hexagon = HexShape(canvas=cnv, **kwargs)
    hexagon.draw()
    return hexagon


def hexagon(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    return HexShape(canvas=cnv, **kwargs)


def Line(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    lin = line(row=row, col=col, **kwargs)
    lin.draw()
    return lin


def line(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    return LineShape(canvas=cnv, **kwargs)


def Polygon(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    poly = polygon(row=row, col=col, **kwargs)
    poly.draw()
    return poly


def polygon(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    return PolygonShape(canvas=cnv, **kwargs)


def Polyline(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    polylin = polyline(row=row, col=col, **kwargs)
    polylin.draw()
    return polylin


def polyline(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    return PolylineShape(canvas=cnv, **kwargs)


def Rhombus(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    rhomb = rhombus(row=row, col=col, **kwargs)
    rhomb.draw()
    return rhomb


def rhombus(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    return RhombusShape(canvas=cnv, **kwargs)


def Rectangle(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    rect = rectangle(row=row, col=col, **kwargs)
    rect.draw()
    return rect


def rectangle(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    return RectShape(canvas=cnv, **kwargs)


def Shape(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    shapeshape = shape(row=row, col=col, **kwargs)
    shapeshape.draw()
    return shapeshape


def shape(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    return ShapeShape(canvas=cnv, **kwargs)


def Star(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    star = StarShape(canvas=cnv, **kwargs)
    star.draw()
    return star


def star(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    return StarShape(canvas=cnv, **kwargs)


def Text(**kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    text = TextShape(canvas=cnv, **kwargs)
    text.draw()
    return text


def text(*args, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    _obj = args[0] if args else None
    return TextShape(_object=_obj, canvas=cnv, **kwargs)

### connect===================================================================


def Connect(shape_from, shape_to, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['shape_from'] = shape_from
    kwargs['shape_to'] = shape_to
    connect = ConnectShape(canvas=cnv, **kwargs)
    connect.draw(cnv=cnv)
    return connect


def connect(shape_from, shape_to, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['shape_from'] = shape_from
    kwargs['shape_to'] = shape_to
    return ConnectShape(canvas=cnv, **kwargs)

### repeats ==================================================================


def Repeat(_object, **kwargs):
    """Initialise a deck with all its settings, including source of data."""
    global cnv
    global deck
    repeat = RepeatShape(_object=_object, **kwargs)
    repeat.draw()

### patterns =================================================================


def Hexagons(rows=1, cols=1, **kwargs):
    global cnv
    global deck
    kwargs = kwargs
    for row in range(rows):
        for col in range(cols):
            Hexagon(row=row, col=col, **kwargs)


def Rectangles(rows=1, cols=1, **kwargs):
    global cnv
    global deck
    kwargs = kwargs
    for row in range(rows):
        for col in range(cols):
            Rectangle(row=row, col=col, **kwargs)


def Lines(rows=1, cols=1, **kwargs):
    global cnv
    global deck
    kwargs = kwargs
    for row in range(rows):
        for col in range(cols):
            Line(row=row, col=col, **kwargs)

### BGG ======================================================================


def BGG(ids=None, user=None, progress=False):
    gamelist = BGGGameList()
    if user:
        tools.feedback("Sorry - user collection function is not available yet!")
    if ids:
        for game_id in ids:
            if progress:
                tools.feedback("Retrieving game '%s' from BoardGameGeek..." % game_id)
            _game = BGGGame(game_id=game_id)
            gamelist.set_values(_game)
    return gamelist

### dice =====================================================================


def dice(dice='1d6', rolls=None):
    """Roll multiple totals for a kind of die.

    Examples:
    >>> dice('2d6')  # Catan dice roll
    [9]
    >>> dice('3D6', 6)  # D&D Basic Character Attributes
    [14, 11, 8, 10, 9, 7]
    >>> dice()  # single D6 roll
    [3]
    """
    if not dice:
        dice = '1d6'
    try:
        dice = dice.replace(' ', '').replace('D', 'd')
        _list = dice.split('d')
        _type, pips = int(_list[0]), int(_list[1])
    except:
        tools.feedback('Unable to determine dice type/roll for "%s"' % dice)
        return None
    return Dice().multi_roll(count=rolls, pips=pips, dice=_type)


def d4(rolls=None):
    return DiceD4().roll(count=rolls)


def d6(rolls=None):
    return DiceD6().roll(count=rolls)


def d8(rolls=None):
    return DiceD8().roll(count=rolls)


def d10(rolls=None):
    return DiceD10().roll(count=rolls)


def d12(rolls=None):
    return DiceD12().roll(count=rolls)


def d20(rolls=None):
    return DiceD20().roll(count=rolls)


def d100(rolls=None):
    return DiceD100().roll(count=rolls)
