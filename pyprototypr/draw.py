# -*- coding: utf-8 -*-
"""
Primary drawing interface for pyprototypr
"""
# future
from __future__ import division
import logging
# lib
from copy import copy
import os
import sys
# third party
from reportlab.lib.pagesizes import *
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import *
from reportlab.lib.units import cm, inch
# local
from .bgg import BGGGame, BGGGameList
from .base import BaseCanvas, GroupBase, COLORS
from .dice import (
    Dice, DiceD4, DiceD6, DiceD8, DiceD10, DiceD12, DiceD20, DiceD100)
from .shapes import (
    ArcShape, ArrowShape, BezierShape, CircleShape, CommonShape, ConnectShape,
    CompassShape, DeckShape, DotShape, DotGridShape, EllipseShape,
    EquilateralTriangleShape, FooterShape, GridShape, HexShape, ImageShape, LineShape,
    OctagonShape, PolygonShape, PolylineShape, Query, RectangleShape, RepeatShape,
    RhombusShape, RightAngledTriangleShape, SectorShape, ShapeShape,
    SquareShape, StadiumShape, StarShape, StarFieldShape, TextShape)
from ._version import __version__
from pyprototypr.utils.support import base_fonts
from pyprototypr.utils import tools
from pyprototypr.utils.tools import Point


log = logging.getLogger(__name__)

cnv = None  # will become a reportlab.canvas object
deck = None  # will become a shapes.DeckShape object
dataset = None  # will become a dictionary of data loaded from a file
# default margins
margin = 1
margin_left = margin
margin_top = margin
margin_bottom = margin
margin_right = margin
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
    # ---- margin
    margin = kwargs.get('margin', margin)
    margin_left = kwargs.get('margin_left', margin)
    margin_top = kwargs.get('margin_top', margin)
    margin_bottom = kwargs.get('margin_bottom', margin)
    margin_right = kwargs.get('margin_right', margin)
    # ---- cards and page
    _cards = kwargs.get('cards', 0)
    fonts = kwargs.get('fonts', [])
    landscape = kwargs.get('landscape', False)
    kwargs = margins(**kwargs)
    pagesize = kwargs.get('pagesize', A4)
    defaults = kwargs.get('defaults', None)
    # ---- fonts
    base_fonts()
    for _font in fonts:
        pdfmetrics.registerFont(TTFont(_font[0], _font[1]))
    # ---- filename and fallback
    filename = kwargs.get('filename', None)
    if not filename:
        basename = 'test'
        # log.debug('basename: "%s" sys.argv[0]: "%s"', basename, sys.argv[0])
        if sys.argv[0]:
            basename = os.path.basename(sys.argv[0]).split('.')[0]
        else:
            if _cards:
                basename = 'cards'
        filename = f'{basename}.pdf'
    # ---- canvas and deck
    cnv = BaseCanvas(filename, pagesize=pagesize, defaults=defaults)
    page_width = pagesize[0]  # units = 1/72 of an inch
    page_height = pagesize[1]  # units = 1/72 of an inch
    if landscape:
        cnv.canvas.setPageSize(landscape(pagesize))
        page_width = pagesize[1]  # units = 1/72 of an inch
        page_height = pagesize[0]  # units = 1/72 of an inch
    if kwargs.get('fill'):
        cnv.setFillColor(kwargs.get('fill'))
        cnv.rect(
            0, 0, page_width, page_height, stroke=0, fill=1)
    if _cards:
        Deck(canvas=cnv, sequence=range(1, _cards + 1), **kwargs)  # deck variable


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
    global footer

    kwargs['pagesize'] = pagesize
    footer = FooterShape(_object=None, canvas=cnv, **kwargs)


def Header(**kwargs):
    global cnv
    global margin
    global margin_left
    global margin_bottom
    global margin_right


def PageBreak(**kwargs):
    global cnv
    global deck
    global page_count
    global pagesize
    global footer

    page_count += 1
    kwargs = margins(**kwargs)
    # tools.feedback(f'PageBreak {type(cnv)=}')
    if kwargs.get("footer", False):
        kwargs['pagesize'] = pagesize
        footer = FooterShape(_object=None, canvas=cnv, **kwargs)
        footer.draw(cnv=cnv, ID=page_count, **kwargs)
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
    """Add margins to a set of kwargs, if not present."""
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


def Font(face=None, **kwargs):
    global cnv

    cnv.font_face = face or 'Helvetica'
    cnv.font_size = kwargs.get('size', 12)
    cnv.stroke = COLORS.get(kwargs.get('color', 'black'))


def Version():
    global cnv
    tools.feedback(f'Running pyprototyper version {__version__}.')


def Feedback(msg):
    global cnv
    tools.feedback(msg)

# ---- cards =====


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
    except Exception:
        pass
    # string - either 'all' or a range: '1', '1-2', '1-3,5-6'
    if not _cards:
        try:
            if sequence.lower() == 'all':
                _cards = range(1, len(dataset) + 1)
            else:
                _cards = tools.sequence_split(sequence)
        except Exception:
            tools.feedback(
                f'Unable to convert "{sequence}"" into a card or range or cards.')
    for _card in _cards:
        card = deck.get(_card - 1)  # cards internally number from ZERO
        if card:
            for element in elements:
                element.members = _cards  # track all related cards
                card.members = _cards
                card.elements.append(element)  # may be Group or Shape or Query
        else:
            tools.feedback(f'Cannot find card#{_card}.'
                           ' (Check "cards" setting in Deck)')


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

# ---- data and functions  =====


def Data(source=None, **kwargs):
    """Load data from file into a dictionary for shared access."""
    global cnv
    global deck
    global dataset
    dataset = tools.load_data(source, **kwargs)
    log.debug("dataset loaded: %s", dataset)
    if len(dataset) == 0:
        tools.feedback("Dataset is empty or cannot be loaded!")
    else:
        deck.create(len(dataset))
        deck.dataset = dataset


def V(*args):
    """Expect args[0] to be the name (string) of a column in the dataset."""
    global dataset
    log.debug("V %s %s %s", args, type(dataset), len(dataset))
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
        log.debug("Set: %s %s %s", kw, kwargs[kw], type(kwargs[kw]))
        setattr(_object, kw, kwargs[kw])
    return _object

# ---- shapes ====


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


def Arrow(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    arr = arrow(row=row, col=col, **kwargs)
    arr.draw()
    return arr


def arrow(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    return ArrowShape(canvas=cnv, **kwargs)


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


def Compass(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    cmpss = compass(row=row, col=col, **kwargs)
    cmpss.draw()
    return cmpss


def compass(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    return CompassShape(canvas=cnv, **kwargs)


def Dot(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    dtt = dot(row=row, col=col, **kwargs)
    dtt.draw()
    return dtt


def dot(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    return DotShape(canvas=cnv, **kwargs)


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


def EquilateralTriangle(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    eqt = EquilateralTriangleShape(canvas=cnv, **kwargs)
    eqt.draw()
    return eqt


def equilateraltriangle(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    return EquilateralTriangleShape(canvas=cnv, **kwargs)


def DotGrid(**kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    # override defaults ... otherwise grid not "next" to margins
    kwargs['x'] = kwargs.get('x', 0)
    kwargs['y'] = kwargs.get('y', 0)
    dgrd = DotGridShape(canvas=cnv, **kwargs)
    dgrd.draw()
    return dgrd


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
    if kwargs.get('common'):
        tools.feedback('The "common" property cannot be used with AutoGrid.', True)
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
    kwargs['stroke_width'] = kwargs.get('stroke_width', 0.2)  # fine line
    kwargs['font_size'] = kwargs.get('font_size', 10)
    # ---- numbering
    if numbering:
        _common = Common(
            font_size=kwargs['font_size'],
            stroke=kwargs['stroke'],
            units=kwargs['units'])
        for x in range(1, kwargs['cols'] + 1):
            Text(x=x*size,
                 y=kwargs['y'] - kwargs['size'] / 2.0,
                 text=str(x*size),
                 common=_common)
        for y in range(1, kwargs['rows'] + 1):
            Text(x=kwargs['x'] - kwargs['size'] / 2.0,
                 y=y*size - _common.points_to_value(kwargs['font_size']) / 2.0,
                 text=str(y*size),
                 common=_common)
        # draw "zero" number
        z_x, z_y = kwargs['units'] * margin_left, kwargs['units'] * margin_bottom
        corner_dist = tools.length_of_line(Point(0, 0), Point(z_x, z_y))
        corner_frac = corner_dist * 0.66 / kwargs['units']
        # tools.feedback(f'*** {z_x=} {z_y=} {corner_dist=}')
        zero_pt = tools.point_on_line(Point(0, 0), Point(z_x, z_y), corner_frac)
        Text(x=zero_pt.x / kwargs['units'] - kwargs['size'] / 4.0,
             y=zero_pt.y / kwargs['units'] - kwargs['size'] / 4.0,
             text="0",
             common=_common)

    # ---- subgrid
    if kwargs.get('subdivisions'):
        local_kwargs = copy(kwargs)
        local_kwargs['size'] = size / int(kwargs.get('subdivisions'))
        for col in range(0, cols):
            for row in range(0, rows):
                off_x = float(kwargs['size']) * col
                off_y = float(kwargs['size']) * row
                # log.warning("col:%s row:%s off_x:%s off_y:%s", col, row, off_x, off_y)
                local_kwargs['rows'] = int(kwargs.get('subdivisions'))
                local_kwargs['cols'] = int(kwargs.get('subdivisions'))
                local_kwargs['stroke_width'] = kwargs.get('stroke_width') / 2.0
                subgrid = GridShape(canvas=cnv, **local_kwargs)
                subgrid.draw(off_x=off_x, off_y=off_y)
    # ---- draw AutoGrid
    grid = GridShape(canvas=cnv, **kwargs)
    grid.draw()
    return grid


def Hexagon(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    # tools.feedback(f'Will draw HexShape: {kwargs}')
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


def Octagon(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    octg = octagon(row=row, col=col, **kwargs)
    octg.draw()
    return octg


def octagon(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    return OctagonShape(canvas=cnv, **kwargs)


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


def RightAngledTriangle(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    rat = RightAngledTriangleShape(canvas=cnv, **kwargs)
    rat.draw()
    return rat


def rightangledtriangle(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    return RightAngledTriangleShape(canvas=cnv, **kwargs)


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
    return RectangleShape(canvas=cnv, **kwargs)


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


def Sector(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    sct = sector(row=row, col=col, **kwargs)
    sct.draw()
    return sct


def sector(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    return SectorShape(canvas=cnv, **kwargs)


def Square(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    sqr = square(row=row, col=col, **kwargs)
    sqr.draw()
    return sqr


def square(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    return SquareShape(canvas=cnv, **kwargs)


def Stadium(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    std = stadium(row=row, col=col, **kwargs)
    std.draw()
    return std


def stadium(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    return StadiumShape(canvas=cnv, **kwargs)


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


def StarField(**kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    starfield = StarFieldShape(canvas=cnv, **kwargs)
    starfield.draw()
    return starfield


def starfield(**kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    return StarFieldShape(canvas=cnv, **kwargs)


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

# ---- connect ====


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

# ---- repeats ====


def Repeat(_object, **kwargs):
    """Initialise a deck with all its settings, including source of data."""
    global cnv
    global deck
    repeat = RepeatShape(_object=_object, **kwargs)
    repeat.draw()

# ---- patterns ====


def Hexagons(rows=1, cols=1, sides=None, **kwargs):
    global cnv
    global deck
    kwargs = kwargs

    def draw_hexagons(rows: int, cols: int, stop: int, the_cols: list, odd_mid: bool = True):
        """Draw rows of hexagons for each column in `the_cols`"""
        top_row = 0
        end_row = rows - 1
        if not odd_mid:
            end_row = rows
            top_row = 1
        for ccol in the_cols:
            top_row = top_row + 1 if ccol & 1 != 0 else top_row  # odd col
            end_row = end_row - 1 if ccol & 1 == 0 else end_row  # even col
            # print('ccol, top_row, end_row', ccol, top_row, end_row)
            for row in range(top_row - 1, end_row + 1):
                _row = row + 1
                # tools.feedback(f'{ccol=}, {_row=}')
                if kwargs.get('masked') and [_row, ccol] in kwargs.get('masked'):
                    pass
                else:
                    Hexagon(row=row, col=ccol - 1, hex_rows=rows, hex_cols=cols, **kwargs)
            if ccol - 1 == stop:  # reached "leftmost" -> reset counters
                top_row = 1
                end_row = rows - 1

    if kwargs.get('hex_layout') and kwargs.get('hex_top'):
        if kwargs.get('hex_top').lower() in ['p', 'pointy'] and \
            kwargs.get('hex_layout') not in ['r', 'rec', 'rect', 'rectangle']:
                tools.feedback(
                    f'Cannot use this custom hex_layout with pointy hexagons!',
                    True)

    if kwargs.get('hex_layout') in ['c', 'cir', 'circle']:
        if not sides and (
            (rows is not None and rows < 3) and
            (cols is not None and cols < 3)):
            tools.feedback(f'The minimum values for rows/cols is 3!', True)
        if rows and rows > 1:
            cols = rows
        if cols and cols > 1:
            rows = cols
        if rows != cols:
            rows = cols
        if sides:
            if sides < 2:
                tools.feedback(f'The minimum value for sides is 2!', True)
            rows = 2 * sides - 1
            cols = rows
        else:
            if rows & 1 == 0:
                tools.feedback(f'An odd number is needed for rows!', True)
            if cols & 1 == 0:
                tools.feedback(f'An odd number is needed for cols!', True)
            sides = rows // 2 + 1
        the_cols = list(range(sides, 0, -1 )) + list(range(sides + 1, rows + 1))
        draw_hexagons(rows, cols, 0, the_cols, odd_mid=False)

    elif kwargs.get('hex_layout') in ['d', 'dia', 'diamond']:
        cols = rows * 2 - 1
        the_cols = list(range(rows, 0, -1 )) + list(range(rows + 1, cols + 1))
        draw_hexagons(rows, cols, 0, the_cols)

    elif kwargs.get('hex_layout') in ['t', 'tri', 'triangle']:
        tools.feedback(f'Cannot draw diamond-pattern hexagons: {kwargs}', True)

    elif kwargs.get('hex_layout') in ['l', 'loz', 'stadium']:
        tools.feedback(f'Cannot draw stadium-pattern hexagons: {kwargs}', True)

    else:  # default to rectangular layout
        for row in range(rows):
            for col in range(cols):
                if kwargs.get('masked') and [row + 1, col + 1] in kwargs.get('masked'):
                    pass
                else:
                    Hexagon(row=row, col=col, hex_rows=rows, hex_cols=cols, **kwargs)


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

# ---- BGG ====


def BGG(ids=None, user=None, progress=False, short=500):
    gamelist = BGGGameList()
    if user:
        tools.feedback("Sorry - BGG user collection function is not available yet!")
    if ids:
        for game_id in ids:
            if progress:
                tools.feedback(f"Retrieving game '{game_id}' from BoardGameGeek...")
            _game = BGGGame(game_id=game_id, short=short)
            gamelist.set_values(_game)
    return gamelist

# ---- dice ====


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
    except Exception:
        tools.feedback(f'Unable to determine dice type/roll for "{dice}"')
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


def named(variable):
    return f'{variable=}'.split('=')[0]
