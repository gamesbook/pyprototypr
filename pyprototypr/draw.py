# -*- coding: utf-8 -*-
"""
Primary drawing interface for pyprototypr
"""
# future
from __future__ import division
# lib
import argparse
from copy import copy
from datetime import datetime
import itertools
import logging
import math
import os
import pathlib
import random
import sys
from typing import Union, Any
# third party
from reportlab.lib.pagesizes import *
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
# from reportlab.lib.colors import black, white
from reportlab.lib.units import cm, inch
from reportlab.lib.colors import (
    Color,
    aliceblue, antiquewhite, aqua, aquamarine, azure, beige, bisque, black,
    blanchedalmond, blue, blueviolet, brown, burlywood, cadetblue, chartreuse,
    chocolate, coral, cornflowerblue, cornsilk, crimson, cyan, darkblue,
    darkcyan, darkgoldenrod, darkgray, darkgrey, darkgreen, darkkhaki,
    darkmagenta, darkolivegreen, darkorange, darkorchid, darkred, darksalmon,
    darkseagreen, darkslateblue, darkslategray, darkslategrey, darkturquoise,
    darkviolet, deeppink, deepskyblue, dimgray, dimgrey, dodgerblue,
    floralwhite, forestgreen, fuchsia, gainsboro, ghostwhite, gold, goldenrod,
    gray, grey, green, greenyellow, honeydew, hotpink, indianred, indigo,
    ivory, khaki, lavender, lavenderblush, lawngreen, lemonchiffon, lightblue,
    lightcoral, lightcyan, lightgoldenrodyellow, lightgreen, lightgrey,
    lightpink, lightsalmon, lightseagreen, lightskyblue, lightslategray,
    lightslategrey, lightsteelblue, lightyellow, lime, limegreen, linen,
    magenta, maroon, mediumaquamarine, mediumblue, mediumorchid, mediumpurple,
    mediumseagreen, mediumslateblue, mediumspringgreen, mediumturquoise,
    mediumvioletred, midnightblue, mintcream, mistyrose, moccasin,
    navajowhite, navy, oldlace, olive, olivedrab, orange, orangered, orchid,
    palegoldenrod, palegreen, paleturquoise, palevioletred, papayawhip,
    peachpuff, peru, pink, plum, powderblue, purple, red, rosybrown,
    royalblue, saddlebrown, salmon, sandybrown, seagreen, seashell, sienna,
    silver, skyblue, slateblue, slategray, slategrey, snow, springgreen,
    steelblue, tan, teal, thistle, tomato, turquoise, violet, wheat, white,
    whitesmoke, yellow, yellowgreen, fidblue, fidred, fidlightblue,
    cornflower, firebrick)
# local
from .bgg import BGGGame, BGGGameList
from .base import BaseCanvas, GroupBase, COLORS, DEBUG_COLOR
from .dice import (
    Dice, DiceD4, DiceD6, DiceD8, DiceD10, DiceD12, DiceD20, DiceD100)
from .shapes import (
    BaseShape,
    ArcShape, ArrowShape, BezierShape, ChordShape, CircleShape, CommonShape,
    CompassShape, DotShape, EllipseShape,
    EquilateralTriangleShape, FooterShape, HexShape, ImageShape, LineShape,
    OctagonShape, PolygonShape, PolylineShape, RectangleShape,
    RhombusShape, RightAngledTriangleShape, SectorShape, ShapeShape,
    SquareShape, StadiumShape, StarShape, StarFieldShape, TextShape,
    GRID_SHAPES_WITH_CENTRE, GRID_SHAPES_NO_CENTRE)
from .layouts import (
    GridShape, DotGridShape, VirtualGrid, RectangleGrid,
    VirtualTrack, RectangleTrack,
    ConnectShape, RepeatShape, SequenceShape)
from .groups import DeckShape, Query, Lookup, LookupType
from ._version import __version__
from pyprototypr.utils.support import steps, excel_column
from pyprototypr.utils.tools import base_fonts
from pyprototypr.utils import geoms, tools, support
from pyprototypr.utils.geoms import Point

log = logging.getLogger(__name__)

cnv = None  # will become a reportlab.canvas object
deck = None  # will become a shapes.DeckShape object
filename = None
dataset = None  # will become a dictionary of data loaded from a file
# default margins
margin = 1
margin_left = margin
margin_top = margin
margin_bottom = margin
margin_right = margin
footer = None
page_count = 0
pargs = None


def Create(**kwargs):
    """Initialisation of page and canvas.

    Allows shortcut creation of cards.
    """
    global cnv
    global filename
    global deck
    global margin
    global margin_left
    global margin_top
    global margin_bottom
    global margin_right
    global pagesize
    global font_size
    global pargs
    global footer
    global footer_draw
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
    footer = None
    footer_draw = False
    # ---- fonts
    base_fonts()
    for _font in fonts:
        pdfmetrics.registerFont(TTFont(_font[0], _font[1]))
    font_size = kwargs.get('font_size', 12)
    # ---- command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Specify output directory", default='')
    parser.add_argument("-p", "--pages", help="Specify which pages to process", default='')
    pargs = parser.parse_args()
    # NB - pages does not work - see notes in PageBreak()
    if pargs.pages:
        tools.feedback('Pages is not an implemented feature - sorry!')
    # ---- filename and fallback
    _filename = kwargs.get('filename', '')
    if not _filename:
        basename = 'test'
        # log.debug('basename: "%s" sys.argv[0]: "%s"', basename, sys.argv[0])
        if sys.argv[0]:
            basename = os.path.basename(sys.argv[0]).split('.')[0]
        else:
            if _cards:
                basename = 'cards'
        _filename = f'{basename}.pdf'
    filename = os.path.join(pargs.directory, _filename)
    # tools.feedback(f"output: {filename}", False)
    # ---- canvas and deck
    cnv = BaseCanvas(filename, pagesize=pagesize, defaults=defaults)
    if landscape:
        cnv.canvas.setPageSize(landscape(cnv.pagesize))
        page_width = cnv.pagesize[1]  # point units (1/72 of an inch)
        page_height = cnv.pagesize[0]  # point units (1/72 of an inch)
    else:
        page_width = cnv.pagesize[0]  # point units (1/72 of an inch)
        page_height = cnv.pagesize[1]  # point units (1/72 of an inch)
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
    global font_size
    global footer
    global footer_draw  # always draw
    global page_count

    kwargs['pagesize'] = pagesize
    if not kwargs.get('font_size'):
        kwargs['font_size'] = font_size
    footer_draw = kwargs.get('draw', False)
    footer = FooterShape(_object=None, canvas=cnv, **kwargs)
    # footer.draw() - this is called via PageBreak()


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
    global font_size
    global footer
    global footer_draw
    global pargs

    page_count += 1
    kwargs = margins(**kwargs)
    if kwargs.get("footer", footer_draw):
        if footer is None:
            kwargs['pagesize'] = pagesize
            kwargs['font_size'] = font_size
            footer = FooterShape(_object=None, canvas=cnv, **kwargs)
        footer.draw(cnv=cnv, ID=page_count, text=None, **kwargs)
    # If count not in the required pargs.pages then do NOT show!
    # Note: this code does not work; seems there is no way to clear or hide the canvas
    #       in ReportLab that would support this operation
    # try:
    #     pages = tools.sequence_split(pargs.pages) if pargs.pages else None
    # except:
    #     tools.feedback(
    #         f'Cannot process "pages" value {pargs.pages} - please check and try again!',
    #         True)
    # if pages and page_count not in pages:
    #     pass
    # else:
    #     cnv.canvas.showPage()
    cnv.canvas.showPage()


def page_break():
    PageBreak()


def Save(**kwargs):
    global cnv
    global filename
    global deck

    if deck and len(deck.deck) > 1:
        deck.draw(cnv, cards=deck.cards, image_list=deck.image_list)
        cnv.canvas.showPage()
    try:
        cnv.canvas.save()
    except FileNotFoundError as err:
        tools.feedback(f'Unable to save "{filename}" - {err}', True)

    output = kwargs.get('output', None)
    dpi = support.to_int(kwargs.get('dpi', 300), 'dpi')
    if output:
        support.pdf_to_png(filename, dpi)


def save(**kwargs):
    Save(**kwargs)


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
    tools.feedback(f'Running pyprototypr version {__version__}.')


def Feedback(msg):
    global cnv
    tools.feedback(msg)


def Today(details: str = 'datetime', style: str = 'iso'):
    """Return string-formatted current date / datetime in a pre-defined style
    """
    current = datetime.now()
    if details == 'date' and style == 'usa':
        return current.strftime('%B %d %Y')  # USA
    if details == 'date' and style == 'eur':
        return current.strftime('%Y-%m-%d')  # Eur
    if details == 'datetime' and style == 'eur':
        return current.strftime('%Y-%m-%d %H:%m')  # Eur
    if details == 'datetime' and style == 'usa':
        return current.strftime('%B %d %Y %I:%m%p')  # USA
    return current.isoformat(timespec='seconds')  # ISO


def Random(end: int = 1, start: int = 0, decimals: int = 2):
    """Return a random number, in a range (`start` to `end`), rounded to `decimals`.
    """
    rrr = random.random() * end + start
    if decimals == 0:
        return int(rrr)
    return round(rrr, decimals)


def Matrix(labels: list = None, data: list = None) -> list:
    """Return list of dicts; each element is a unique combo of all the items in `data`
    """
    if data is None:
        return []
    combos = list(itertools.product(*data))
    # check labels
    data_length = len(combos[0])
    if labels == []:
        labels = [f'VALUE{item+1}' for item in range(0, data_length)]
    else:
        if len(labels) != data_length:
            tools.feedback(
                "The number of labels must equal the number of combinations!", True)
    result = []
    for item in combos:
        entry = {}
        for key, value in enumerate(item):
            entry[labels[key]] = value
        result.append(entry)
    return result

# ---- Cards ====


def Card(sequence, *elements):
    """Add one or more elements to a card or cards.

    NOTE: A Card receives its `draw()` command via Save()!
    """
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
    # string - either 'all'/'*' .OR. a range: '1', '1-2', '1-3,5-6'
    if not _cards:
        try:
            card_count = len(dataset) if dataset else len(deck.image_list)
            if sequence.lower() == 'all' or sequence.lower() == '*':
                _cards = range(1, card_count + 1)
            else:
                _cards = tools.sequence_split(sequence)
        except Exception as err:
            log.error('Handling sequence:%s with dataset:%s & images:%s - %s',
                      sequence, dataset, deck.image_list, err)
            tools.feedback(
                f'Unable to convert "{sequence}" into a card or range or cards {deck}.')
    for index, _card in enumerate(_cards):
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
    """Initialise a deck with all its settings, including source(s) of data.

    NOTE: A Deck receives its `draw()` command from Save()!
    """
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


def group(*args, **kwargs):
    global cnv
    global deck
    gb = GroupBase(kwargs)
    for arg in args:
        gb.append(arg)
    return gb

# ---- data and functions


def Data(**kwargs):
    """Load data from file, dictionary or directory for access by a Deck."""
    global cnv
    global deck
    global dataset

    filename = kwargs.get('filename', None)
    matrix = kwargs.get('matrix', None)
    images = kwargs.get('images', None)
    filters = kwargs.get('image_filters', None)
    _extra = kwargs.get('extra', 0)  # extra cards (not part of normal dataset)
    try:
        extra = int(_extra)
    except:
        tools.feedback(f'Extra must be a whole number, not "{_extra}"!', True)

    if filename:  # handle excel and CSV
        dataset = tools.load_data(filename, **kwargs)
        log.debug("dataset loaded: %s", dataset)
        if len(dataset) == 0:
            tools.feedback("Dataset is empty or cannot be loaded!", True)
        else:
            deck.create(len(dataset) + extra)
            deck.dataset = dataset
    elif matrix:  # handle pre-built dict
        dataset = matrix
        log.debug("dataset loaded: %s", dataset)
        if len(dataset) == 0:
            tools.feedback("Matrix data is empty or cannot be loaded!", True)
        else:
            deck.create(len(dataset) + extra)
            deck.dataset = dataset
    elif images:  # handle images
        src = pathlib.Path(images)
        if not src.is_dir():
            # look relative to script's location
            script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
            full_path = os.path.join(script_dir, images)
            src = pathlib.Path(full_path)
            if not src.is_dir():
                tools.feedback(
                    f'Cannot locate or access directory: {images} or {full_path}', True)
        if filters:
            src = src.glob(filters)  # glob('*.[tx][xl][ts]')
        for child in src.iterdir():
            deck.image_list.append(child)
        if len(deck.image_list) == 0:
            tools.feedback(
                f'Directory "{src}" has no relevant files or cannot be loaded!', True)
        deck.cards = len(deck.image_list)  + extra  # OVERWRITE total number of cards
        deck.create(deck.cards)  # resize deck based on images

    else:
        tools.feedback("You must provide a source of data for Data!", True)
    return dataset


def V(*args):
    """Expect args[0] to be the name (string) of a column in the dataset."""
    global dataset
    log.debug("V %s %s %s", args, type(dataset), len(dataset))
    if dataset and isinstance(dataset, list):
        return [item.get(args[0], '') for item in dataset]
    return []


def Q(query='', result=None, alternate=None):
    """
    Enable querying/selection of data from a dataset list

        query: str
            boolean-type expression which can be evaluated to return a True
            e.g. 'name`=`fred' filters item for dataset['name'] == 'fred'
        result: str or element
            returned if query is True
        alternate: str or element
            OPTIONAL; returned if query is False; if not supplied, then None
    """
    global dataset

    if dataset and isinstance(dataset, list):
        query_list = tools.query_construct(query)
        # [[key, operator, target, LINKER], ...]
        for query_item in query_list:
            vals = [item.get(query_item[0], '') for item in dataset]
            query_item[0] = vals
            # [(list_of_possible_targets, operator, target, LINKER), ...]
        return Query(query=query_list, result=result, alternate=alternate)
    return None


def L(lookup: str, target: str, result: str, default: Any = '') -> LookupType:
    """Enable lookup of data in a record of a dataset

        lookup: Any
            the lookup column whose value must be used for the match
        target: str
            the name of the column of the data being searched
        result: str
            name of result column containing the data to be returned
        default: Any
            the data to be returned if no match is made

    In short:
        lookup and target enable finding a matching record in the dataset;
        the data in the 'result' column of that record is stored as an
        `lookup: result` entry in the returned lookups dictionary of the LookupType
    """
    global dataset
    print(f"L {lookup=} {target=} {result=}")

    lookups = {}
    if dataset and isinstance(dataset, list):
        # validate the lookup column
        if lookup not in dataset[0].keys():
            tools.feedback(f'The "{lookup}" column is not available.', True)
        for key, record in enumerate(dataset):
            if target in record.keys():
                if result in record.keys():
                    lookups[record[target]] = record[result]
                else:
                    tools.feedback(f'The "{result}" column is not available.', True)
            else:
                tools.feedback(f'The "{target}" column is not available.', True)
    result = LookupType(column=lookup, lookups=lookups)
    return result


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



def Chord(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    chd = chord(row=row, col=col, **kwargs)
    chd.draw()
    return chd


def chord(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    kwargs['row'] = row
    kwargs['col'] = col
    return ChordShape(canvas=cnv, **kwargs)


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


def Hexagon(row=None, col=None, **kwargs):
    global cnv
    global deck
    kwargs = margins(**kwargs)
    # tools.feedback(f'Will draw HexShape: {kwargs}')
    kwargs['row'] = row
    kwargs['col'] = col
    hexagon = HexShape(canvas=cnv, **kwargs)
    grid_shape = hexagon.draw()
    return grid_shape


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
    grid_shape = rect.draw()
    return grid_shape


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
    grid_shape = sqr.draw()
    return grid_shape


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
    kwargs['row'] = row
    kwargs['col'] = col
    std = StadiumShape(canvas=cnv, **kwargs)
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


# ---- Grids ====

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


def Blueprint(**kwargs):
    global cnv
    global deck
    global pagesize
    global margin_left
    global margin_top
    global margin_bottom
    global margin_right

    def set_style(style_name):
        """Set blueprint color and fill."""
        match style_name:
            case 'green':
                color, fill = "#CECE2C", "#35705E"
            case 'grey' | 'gray':
                color, fill =  white, "#A1969C"
            case 'blue' | 'invert' | 'inverted':
                color, fill = honeydew, '#3085AC'
            case _:
                color, fill = '#3085AC', None
                if style_name is not None:
                    tools.feedback(
                        f'The Blueprint style "{style_name}" is unknown', False, True)
        return color, fill

    kwargs = margins(**kwargs)
    if kwargs.get('common'):
        tools.feedback('The "common" property cannot be used with a Blueprint.', True)
    kwargs['units'] = kwargs.get('units', cm)
    size = 1.0
    if kwargs['units'] == inch:
        size = 0.5
    # override defaults ... otherwise grid not "next" to margins
    numbering = kwargs.get('numbering', True)
    kwargs['size'] = kwargs.get('size', size)
    kwargs['x'] = kwargs.get('x', 0)
    kwargs['y'] = kwargs.get('y', 0)
    m_x = kwargs['units'] * (margin_left + margin_right)
    m_y = kwargs['units'] * (margin_top + margin_bottom)
    _cols = (pagesize[0] - m_x) / (kwargs['units'] * float(kwargs['size']))
    _rows = (pagesize[1] - m_y) / (kwargs['units'] * float(kwargs['size']))
    rows = int(_rows)
    cols = int(_cols)
    kwargs['rows'] = kwargs.get('rows', rows)
    kwargs['cols'] = kwargs.get('cols', cols)
    kwargs['stroke_width'] = kwargs.get('stroke_width', 0.2)  # fine line
    default_font_size = 10 * math.sqrt(pagesize[0]) / math.sqrt(A4[0])
    line_dots = kwargs.get('line_dots', False)
    kwargs['font_size'] = kwargs.get('font_size', default_font_size)
    line_color, page_fill = set_style(kwargs.get('style', None))
    kwargs['stroke'] = kwargs.get('stroke', line_color)
    kwargs['fill'] = kwargs.get('fill', page_fill)
    # ---- page color (optional)
    if kwargs['fill'] is not None:
        cnv.canvas.setFillColor(kwargs['fill'])
        cnv.canvas.rect(0, 0, pagesize[0], pagesize[1], stroke=0, fill=1)
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
        corner_dist = geoms.length_of_line(Point(0, 0), Point(z_x, z_y))
        corner_frac = corner_dist * 0.66 / kwargs['units']
        # tools.feedback(f'*** {z_x=} {z_y=} {corner_dist=}')
        zero_pt = geoms.point_on_line(Point(0, 0), Point(z_x, z_y), corner_frac)
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
                local_kwargs['stroke'] = kwargs.get('subdivisions_stroke', kwargs['stroke'])
                local_kwargs['dashes'] = kwargs.get('subdivisions_dashes')
                local_kwargs['dots'] = kwargs.get('subdivisions_dots')
                subgrid = GridShape(canvas=cnv, **local_kwargs)
                subgrid.draw(off_x=off_x, off_y=off_y)
    # ---- draw Blueprint grid
    grid = GridShape(canvas=cnv, line_dots=line_dots, **kwargs)
    grid.draw()
    return grid

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


def Lines(rows=1, cols=1, **kwargs):
    global cnv
    global deck
    kwargs = kwargs
    for row in range(rows):
        for col in range(cols):
            Line(row=row, col=col, **kwargs)

# ---- sequence ====


def Sequence(_object=None, **kwargs):
    """Draw a set of objects in a line."""
    global cnv
    global deck
    sequence = SequenceShape(_object=_object, **kwargs)
    sequence.draw()


def sequence(_object=None, **kwargs):
    """Draw a set of objects in a line."""
    global cnv
    global deck
    return SequenceShape(_object=_object, **kwargs)

# ---- patterns (grid)


def Hexagons(rows=1, cols=1, sides=None, **kwargs):
    """Draw a set of hexagons in a pattern."""
    global cnv
    global deck
    kwargs = kwargs
    locations = []

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
                    grid_location = Hexagon(
                        row=row, col=ccol - 1, hex_rows=rows, hex_cols=cols, **kwargs)
                    locations.append(grid_location)
            if ccol - 1 == stop:  # reached "leftmost" -> reset counters
                top_row = 1
                end_row = rows - 1
        return locations

    if kwargs.get('hex_layout') and kwargs.get('hex_top'):
        if kwargs.get('hex_top').lower() in ['p', 'pointy'] and \
                kwargs.get('hex_layout') not in ['r', 'rec', 'rect', 'rectangle']:
            tools.feedback(
                'Cannot use this custom hex_layout with pointy hexagons!',
                True)

    if kwargs.get('hex_layout') in ['c', 'cir', 'circle']:
        if not sides and ((rows is not None and rows < 3) and (
                cols is not None and cols < 3)):
            tools.feedback('The minimum values for rows/cols is 3!', True)
        if rows and rows > 1:
            cols = rows
        if cols and cols > 1:
            rows = cols
        if rows != cols:
            rows = cols
        if sides:
            if sides < 2:
                tools.feedback('The minimum value for sides is 2!', True)
            rows = 2 * sides - 1
            cols = rows
        else:
            if rows & 1 == 0:
                tools.feedback('An odd number is needed for rows!', True)
            if cols & 1 == 0:
                tools.feedback('An odd number is needed for cols!', True)
            sides = rows // 2 + 1
        the_cols = list(range(sides, 0, -1)) + list(range(sides + 1, rows + 1))
        locations = draw_hexagons(rows, cols, 0, the_cols, odd_mid=False)

    elif kwargs.get('hex_layout') in ['d', 'dia', 'diamond']:
        cols = rows * 2 - 1
        the_cols = list(range(rows, 0, -1)) + list(range(rows + 1, cols + 1))
        locations = draw_hexagons(rows, cols, 0, the_cols)

    elif kwargs.get('hex_layout') in ['t', 'tri', 'triangle']:
        tools.feedback(f'Cannot draw triangle-pattern hexagons: {kwargs}', True)

    elif kwargs.get('hex_layout') in ['l', 'loz', 'stadium']:
        tools.feedback(f'Cannot draw stadium-pattern hexagons: {kwargs}', True)

    else:  # default to rectangular layout
        for row in range(rows):
            for col in range(cols):
                if kwargs.get('masked') and [row + 1, col + 1] in kwargs.get('masked'):
                    pass
                else:
                    grid_location = Hexagon(
                        row=row, col=col, hex_rows=rows, hex_cols=cols, **kwargs)
                    locations.append(grid_location)

    return locations


def Rectangles(rows=1, cols=1, **kwargs):
    """Draw a set of rectangles in a pattern."""
    global cnv
    global deck
    kwargs = kwargs
    locations = []

    for row in range(rows):
        for col in range(cols):
            if kwargs.get('masked') and [row + 1, col + 1] in kwargs.get('masked'):
                pass
            else:
                grid_location = Rectangle(row=row, col=col, **kwargs)
                locations.append(grid_location)

    return locations


def Squares(rows=1, cols=1, **kwargs):
    """Draw a set of squares in a pattern."""
    global cnv
    global deck
    kwargs = kwargs
    locations = []

    for row in range(rows):
        for col in range(cols):
            if kwargs.get('masked') and [row + 1, col + 1] in kwargs.get('masked'):
                pass
            else:
                grid_location = Square(row=row, col=col, **kwargs)
                locations.append(grid_location)

    return locations


def Location(grid: list, label: str, shapes: list, **kwargs):
    global cnv
    kwargs = kwargs

    def draw_shape(shape: BaseShape, loc: Point):
        shape_name = shape.__class__.__name__
        shape_abbr = shape_name.replace('Shape', '')
        # shape.debug_point(cnv.canvas, point=loc)
        dx = shape.kwargs.get('dx', 0)  # user-units
        dy = shape.kwargs.get('dy', 0)  # user-units
        pts = shape.values_to_points([dx, dy])  # absolute units (points)
        try:
            x = loc.x + pts[0]
            y = loc.y + pts[1]
            # tools.feedback(f"{shape=} :: {loc.x=}, {loc.y=} // {dx=}, {dy=}")
            # tools.feedback(f"{kwargs=}")
            # tools.feedback(f"{label} :: {shape_name=}")
            if shape_name in GRID_SHAPES_WITH_CENTRE:
                shape.draw(_abs_cx=x, _abs_cy=y, **kwargs)
            elif shape_name in GRID_SHAPES_NO_CENTRE:
                shape.draw(_abs_x=x, _abs_y=y, **kwargs)
            else:
                tools.feedback(f"Unable to draw {shape_abbr}s in Locations!", True)
        except Exception as err:
            tools.feedback(err, False)
            tools.feedback(
                f"Unable to draw the '{shape_abbr} - please check its settings!", True)

    # checks
    if grid is None or not isinstance(grid, list):
        tools.feedback("The grid (as a list) must be supplied!", True)

    # get location centre from grid via the label
    loc = None
    for position in grid:
        if position.label.lower() == str(label).lower():
            loc = Point(position.x, position.y)
            break
    if loc is None:
        tools.feedback(f"The location '{label}' is not in the grid!", True)

    if shapes:
        for shape in shapes:
            if shape.__class__.__name__ == 'GroupBase':
                tools.feedback(f"Group drawing ({shape}) NOT IMPLEMENTED YET", True)
            else:
                draw_shape(shape, loc)


def Locations(grid: list, labels: Union[str, list], shapes: list, **kwargs):
    global cnv
    kwargs = kwargs

    if grid is None or not isinstance(grid, list):
        tools.feedback("The grid (as a list) must be supplied!", True)
    if labels is None:
        tools.feedback("No grid location labels supplied!", True)
    if shapes is None:
        tools.feedback("No list of shapes supplied!", True)
    if isinstance(labels, str):
        _labels = labels.split(',')
        if labels.lower() == 'all':
           _labels = []
           for loc in grid:
               if isinstance(loc, GridLocation):
                   _labels.append(loc.label)
    elif isinstance(labels, list):
        _labels = labels
    else:
        tools.feedback("Grid location labels must a list or a comma-delimited string!", True)

    if not isinstance(shapes, list):
        tools.feedback("Shapes must contain a list of shapes!", True)

    for label in _labels:
        # tools.feedback(f'{label=} :: {shapes=}')
        Location(grid, label, shapes)


def LinkLine(grid: list, locations: list, **kwargs):
    """Enable a line link between one or more locations in a grid."""
    global cnv
    global margin
    global margin_left
    global margin_top
    global margin_bottom
    global margin_right
    kwargs = kwargs

    if not isinstance(locations, list):
        tools.feedback(f"'{locations} is not a list - please check!", True)
    if len(locations) < 2:
        tools.feedback(f"There should be at least 2 locations to create links!", True)
    dummy = shape()
    for index, location in enumerate(locations):
        # precheck
        if not isinstance(location, tuple) or len(location) != 3:
            tools.feedback(f"The location '{location} is not valid - please check its syntax!", True)
        # get location centre from grid via the label
        loc = None
        for position in grid:
            if location[0] == position.label:
                loc = Point(position.x, position.y)
                break
        if loc is None:
            tools.feedback(f"The location '{location[0]}' is not in the grid!", True)
        # new line?
        if index + 1 < len(locations):
            # location #2
            location_2 = locations[index + 1]
            if not isinstance(location_2, tuple) or len(location_2) != 3:
                tools.feedback(f"The location '{location_2} is not valid -"
                               " please check its syntax!", True)
            loc_2 = None
            for position in grid:
                if location_2[0] == position.label:
                    loc_2 = Point(position.x, position.y)
                    break
            if loc_2 is None:
                tools.feedback(f"The location '{location_2[0]}' is not in the grid!", True)
            if location[0] == location_2[0]:
                tools.feedback(f"Locations must differ!", True)
            # line start/end
            x = dummy.points_to_value(loc.x) + location[1]
            y = dummy.points_to_value(loc.y) + location[2]
            x1 = dummy.points_to_value(loc_2.x) + location_2[1]
            y1 = dummy.points_to_value(loc_2.y) + location_2[2]

            _line = line(x=x, y=y, x1=x1, y1=y1, **kwargs)
            # tools.feedback(f"{x=}, {y=}, {x1=}, {y1=}")
            delta_x = margin_left
            delta_y = margin_bottom
            # tools.feedback(f"{delta_x=}, {delta_y=}")
            _line.draw(
                off_x=-delta_x,
                off_y=-delta_y,
            )

# ---- layout & tracks ====


def Layout(grid, **kwargs):
    global cnv

    kwargs = kwargs
    shapes = kwargs.get('shapes', [])
    if not isinstance(grid, VirtualGrid):
        tools.feedback(f"The value '{grid}' is not a valid grid!", True)
    # ---- iterate through grid & draw shape(s)
    shape_id = 0
    locations = enumerate(grid.next_location())
    for count, loc in locations:
        if grid.stop and count + 1 >= grid.stop:
            break
        if grid.pattern in ['o', 'outer']:
            if count + 1 > grid.rows * 2 + (grid.cols - 2) * 2:
                break
        shape = copy(shapes[shape_id])  # enable overwrite/change of properties
        # ---- supply data to shape's text fields
        data = {
            'col': loc.col, 'row': loc.row, 'x': loc.x, 'y': loc.y, 'count': count + 1}
        # tools.feedback(f'{data=}')
        try:
            shape.label = shapes[shape_id].label.format(**data)  # replace {xyz} entries
            shape.title = shapes[shape_id].title.format(**data)
            shape.heading = shapes[shape_id].heading.format(**data)
        except KeyError as err:
            text = str(err).split()
            tools.feedback(
                f'You cannot use {text[0]} as a special field; remove the {{ }} brackets',
                True)
        # ---- execute the draw()
        shape.draw(off_x=loc.x, off_y=loc.y)
        shape_id += 1
        if shape_id > len(shapes) - 1:
            shape_id = 0  # reset and start again


def Track(track=None, **kwargs):
    global cnv

    kwargs = kwargs
    _spaces = kwargs.get('spaces', 8)
    spaces = tools.as_int(_spaces, 'spaces', minimum=4)  # number of spaces around track
    # breakpoint()
    shapes = kwargs.get('shapes', [])  # shape(s) to draw at the locations
    if not track:
        track = RectangleTrack(fill_color=DEBUG_COLOR)
    if not isinstance(track, VirtualTrack):
        tools.feedback(f"The value '{track}' is not a valid track!", True)
    if not shapes:
        # create a default shape
        side = track.calculate_perimeter(units=True) / spaces
        # tools.feedback(f'*** default square: {side=} {spaces=}')
        shapes = [square(side=side, label="{count}")]
    # ---- validate shape type(s)
    for shp in shapes:
        if not isinstance(shp, (SquareShape, CircleShape, OctagonShape)):
            tools.feedback("Only square, circle, or octagon shapes allowed!", True)
    # ---- walk the track & draw shape(s)
    shape_id = 0
    track_points = enumerate(track.next_location(shapes=shapes, spaces=spaces))
    for count, t_pt in track_points:
        if track.final and count + 1 >= track.final:
            break  # stop early
        # ---- execute the draw()
        shape = copy(shapes[shape_id])  # enable overwrite/change of properties
        # ---- supply data to text fields
        data = {'x': t_pt.x, 'y': t_pt.y, 'count': count + 1}
        try:
            shape.label = shapes[shape_id].label.format(**data)  # replace {xyz} entries
            shape.title = shapes[shape_id].title.format(**data)
            shape.heading = shapes[shape_id].heading.format(**data)
        except KeyError as err:
            text = str(err).split()
            tools.feedback(
                f'You cannot use {text[0]} as a special field; remove the {{ }} brackets',
                True)
        # ---- supply data to change shape's location
        shape.cx = shape.points_to_value(t_pt.x - track._o.delta_x)
        shape.cy = shape.points_to_value(t_pt.y - track._o.delta_y)
        # shape.width = t_pt.width  # recalculated to fit on track
        # tools.feedback(f'*** {shape.cx}, {shape.cy}')
        shape.set_unit_properties()
        shape.draw(cnv)
        shape_id += 1
        if shape_id > len(shapes) - 1:
            shape_id = 0  # reset and start again

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
