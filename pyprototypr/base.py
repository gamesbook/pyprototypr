# -*- coding: utf-8 -*-
"""
Base shape class for pyprototypr

Notes:
    * https://www.a2-size.com/american-paper-sizes/
    * https://en.wikipedia.org/wiki/Paper_size#Overview_of_ISO_paper_sizes
"""
# lib
from collections import namedtuple
import copy
import json
import logging
import math
import os
# third party
from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas as reportlab_canvas
from reportlab.lib.units import cm, inch, mm
from reportlab.lib.pagesizes import (
    A6, A5, A4, A3, A2, A1, A0, LETTER, LEGAL, ELEVENSEVENTEEN,
    letter, legal, elevenSeventeen, B6, B5, B4, B3, B2, B0, landscape)
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
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
from pyprototypr.utils import geoms, tools

log = logging.getLogger(__name__)

DEBUG = False
DEBUG_COLOR = lightsteelblue
# ---- tuples
UnitProperties = namedtuple(
    'UnitProperties', [
        'page_width',
        'page_height',
        'margin_left',
        'margin_right',
        'margin_bottom',
        'margin_top',
        'x',
        'y',
        'cx',
        'cy',
        'height',
        'width',
        'radius',
        'diameter',
        'side',
        'length',
    ]
)
OffsetProperties = namedtuple(
    'OffsetProperties', [
        'off_x',
        'off_y',
        'delta_x',
        'delta_y',
    ]
)
GridShape = namedtuple(
    'GridShape', [
        'label',
        'x',
        'y',
        'shape',
    ]
)

# ---- units
UNITS = {
    "cm": cm,
    "inch": inch,
    "mm": mm,
    "points": "points"
}
# ---- colors (ReportLab; 18xx Games)
COLORS = {
    "aliceblue": aliceblue,
    "antiquewhite": antiquewhite,
    "aqua": aqua,
    "aquamarine": aquamarine,
    "azure": azure,
    "beige": beige,
    "bisque": bisque,
    "black": black,
    "blanchedalmond": blanchedalmond,
    "blue": blue,
    "blueviolet": blueviolet,
    "brown": brown,
    "burlywood": burlywood,
    "cadetblue": cadetblue,
    "chartreuse": chartreuse,
    "chocolate": chocolate,
    "coral": coral,
    "cornflower": cornflower,
    "cornflowerblue": cornflowerblue,
    "cornsilk": cornsilk,
    "crimson": crimson,
    "cyan": cyan,
    "darkblue": darkblue,
    "darkcyan": darkcyan,
    "darkgoldenrod": darkgoldenrod,
    "darkgray": darkgray,
    "darkgreen": darkgreen,
    "darkgrey": darkgrey,
    "darkkhaki": darkkhaki,
    "darkmagenta": darkmagenta,
    "darkolivegreen": darkolivegreen,
    "darkorange": darkorange,
    "darkorchid": darkorchid,
    "darkred": darkred,
    "darksalmon": darksalmon,
    "darkseagreen": darkseagreen,
    "darkslateblue": darkslateblue,
    "darkslategray": darkslategray,
    "darkslategrey": darkslategrey,
    "darkturquoise": darkturquoise,
    "darkviolet": darkviolet,
    "deeppink": deeppink,
    "deepskyblue": deepskyblue,
    "dimgray": dimgray,
    "dimgrey": dimgrey,
    "dodgerblue": dodgerblue,
    "fidblue": fidblue,
    "fidlightblue": fidlightblue,
    "fidred": fidred,
    "firebrick": firebrick,
    "floralwhite": floralwhite,
    "forestgreen": forestgreen,
    "fuchsia": fuchsia,
    "gainsboro": gainsboro,
    "ghostwhite": ghostwhite,
    "goldenrod": goldenrod,
    "gold": gold,
    "gray": gray,
    "green": green,
    "greenyellow": greenyellow,
    "grey": grey,
    "honeydew": honeydew,
    "hotpink": hotpink,
    "indianred": indianred,
    "indigo": indigo,
    "ivory": ivory,
    "khaki": khaki,
    "lavenderblush": lavenderblush,
    "lavender": lavender,
    "lawngreen": lawngreen,
    "lemonchiffon": lemonchiffon,
    "lightblue": lightblue,
    "lightcoral": lightcoral,
    "lightcyan": lightcyan,
    "lightgoldenrodyellow": lightgoldenrodyellow,
    "lightgreen": lightgreen,
    "lightgrey": lightgrey,
    "lightpink": lightpink,
    "lightsalmon": lightsalmon,
    "lightseagreen": lightseagreen,
    "lightskyblue": lightskyblue,
    "lightslategray": lightslategray,
    "lightslategrey": lightslategrey,
    "lightsteelblue": lightsteelblue,
    "lightyellow": lightyellow,
    "limegreen": limegreen,
    "lime": lime,
    "linen": linen,
    "magenta": magenta,
    "maroon": maroon,
    "mediumaquamarine": mediumaquamarine,
    "mediumblue": mediumblue,
    "mediumorchid": mediumorchid,
    "mediumpurple": mediumpurple,
    "mediumseagreen": mediumseagreen,
    "mediumslateblue": mediumslateblue,
    "mediumspringgreen": mediumspringgreen,
    "mediumturquoise": mediumturquoise,
    "mediumvioletred": mediumvioletred,
    "midnightblue": midnightblue,
    "mintcream": mintcream,
    "mistyrose": mistyrose,
    "moccasin": moccasin,
    "navajowhite": navajowhite,
    "navy": navy,
    "oldlace": oldlace,
    "olivedrab": olivedrab,
    "olive": olive,
    "orange": orange,
    "orangered": orangered,
    "orchid": orchid,
    "palegoldenrod": palegoldenrod,
    "palegreen": palegreen,
    "paleturquoise": paleturquoise,
    "palevioletred": palevioletred,
    "papayawhip": papayawhip,
    "peachpuff": peachpuff,
    "peru": peru,
    "pink": pink,
    "plum": plum,
    "powderblue": powderblue,
    "purple": purple,
    "red": red,
    "rosybrown": rosybrown,
    "royalblue": royalblue,
    "saddlebrown": saddlebrown,
    "salmon": salmon,
    "sandybrown": sandybrown,
    "seagreen": seagreen,
    "seashell": seashell,
    "sienna": sienna,
    "silver": silver,
    "skyblue": skyblue,
    "slateblue": slateblue,
    "slategray": slategray,
    "slategrey": slategrey,
    "snow": snow,
    "springgreen": springgreen,
    "steelblue": steelblue,
    "tan": tan,
    "teal": teal,
    "thistle": thistle,
    "tomato": tomato,
    "turquoise": turquoise,
    "violet": violet,
    "wheat": wheat,
    "whitesmoke": whitesmoke,
    "white": white,
    "yellowgreen": yellowgreen,
    "yellow": yellow,
    # 18xx colors from https://github.com/XeryusTC/map18xx/blob/master/src/tile.rs
    "GROUND_18XX": "#FDD9B5",  # Sandy Tan
    "YELLOW_18XX": "#FDEE00",  # Aureolin
    "GREEN_18XX": "#00A550",  # Pigment Green
    "RUSSET_18XX": "#CD7F32",  # Bronze
    "GREY_18XX": "#ACACAC",  # Silver Chalice
    "BROWN_18XX": "#7B3F00",  # Chocolate
    "RED_18XX": "#DC143C",  # Crimson
    "BLUE_18XX": "#007FFF",  # Azure
    "BARRIER_18XX": "#660000",  # Blood Red
    "WHITE_18XX": "#FFFFFF",  # White
}
# ---- page sizes
PAGES = {
    "LETTER": LETTER,
    "landscape": landscape,
    "legal": legal,
    "A1": A1,
    "A0": A0,
    "A3": A3,
    "A2": A2,
    "A5": A5,
    "A4": A4,
    "A6": A6,
    "elevenSeventeen": elevenSeventeen,
    "LEGAL": LEGAL,
    "letter": letter,
    "B4": B4,
    "B5": B5,
    "B6": B6,
    "B0": B0,
    "B2": B2,
    "B3": B3,
    "ELEVENSEVENTEEN": ELEVENSEVENTEEN,
    "tabloid": elevenSeventeen,
}
WIDTH = 0.1


class BaseCanvas:
    """Wrapper/extended class for a ReportLab canvas."""

    def __init__(self, filename=None, pagesize=None, **kwargs):
        self.canvas = reportlab_canvas.Canvas(
            filename=filename, pagesize=pagesize or A4)
        self.jsonfile = kwargs.get('defaults', None)
        self.defaults = {}
        # ---- override
        if self.jsonfile:
            try:
                with open(self.jsonfile) as data_file:
                    self.defaults = json.load(data_file)
            except (IOError, ValueError):
                filepath = tools.script_path()
                _jsonfile = os.path.join(filepath, self.jsonfile)
                try:
                    with open(_jsonfile) as data_file:
                        self.defaults = json.load(data_file)
                except (IOError, ValueError):
                    tools.feedback(
                        f'Unable to find or load the file "{self.jsonfile}"'
                        f' - also checked in "{filepath}".')
        # ---- constants
        self.default_length = 1
        self.show_id = False  # True
        # ---- general
        self.shape = self.defaults.get('shape', 'rectangle')
        self.shape_id = None
        self.sequence = self.defaults.get('sequence', [])
        self.dataset = []
        self.members = []  # card IDs, of which current card is a member
        self._object = None
        self.kwargs = kwargs
        self.run_debug = False
        self.units = self.get_units(self.defaults.get('units'), cm)
        # ---- page
        self.pagesize = self.get_page(self.defaults.get('pagesize'), A4)
        self.page_width = self.pagesize[0] / self.units
        self.page_height = self.pagesize[1] / self.units
        self.margin = self.defaults.get('margin', 1)
        self.margin_top = self.defaults.get('margin_top', self.margin)
        self.margin_bottom = self.defaults.get('margin_bottom', self.margin)
        self.margin_left = self.defaults.get('margin_left', self.margin)
        self.margin_right = self.defaults.get('margin_right', self.margin)
        # ---- grid cut marks
        self.grid_marks = self.defaults.get('grid_marks', 0)
        self.grid_color = self.get_color(self.defaults.get('grid_color'), grey)
        self.grid_stroke_width = self.defaults.get('grid_stroke_width', WIDTH)
        self.grid_length = self.defaults.get('grid_length', 0.85)  # 1/3 inch
        self.grid_offset = self.defaults.get('grid_offset', 0)
        # ---- sizes and positions
        self.row = self.defaults.get('row', None)
        self.col = self.defaults.get('col', self.defaults.get('column', None))
        self.height = self.defaults.get('height', 1)
        self.width = self.defaults.get('width', 1)
        self.size = self.defaults.get('size', None)  # proxy for equal H/W
        self.x = self.defaults.get('x', self.defaults.get('left', 1))
        self.y = self.defaults.get('y', self.defaults.get('bottom', 1))
        self.cx = self.defaults.get('cx', None)
        self.cy = self.defaults.get('cy', None)
        self.scaling = self.defaults.get('scaling', None)
        self.dot_point = self.defaults.get('dot_point', 3.0)  # points
        # ---- to be calculated ...
        self.area = None
        self.vertices = []
        # ---- repeats
        self.pattern = self.defaults.get('pattern', None)
        self.repeat = self.defaults.get('repeat', True)
        self.offset = self.defaults.get('offset', 0)
        self.offset_across = self.defaults.get('offset_across', self.offset)
        self.offset_down = self.defaults.get('offset_down', self.offset)
        self.gap = self.defaults.get('gap', 0)
        self.gap_x = self.defaults.get('gap_x', self.gap)
        self.gap_y = self.defaults.get('gap_y', self.gap)
        # ---- rotate in degrees
        self.rotate = self.defaults.get('rotate',
                                        self.defaults.get('rotation', 0))
        self.orientation = self.defaults.get('orientation', 'vertical')
        self.position = self.defaults.get('position', None)
        self.flip = self.defaults.get('flip', 'up')
        # ---- line
        self.line_color = self.defaults.get('line_color', WIDTH)
        self.line_width = self.defaults.get('line_width', WIDTH)
        self.line_cap = self.defaults.get('line_cap', None)
        self.line_dots = self.defaults.get(
            'line_dots', self.defaults.get('dots', False))
        self.dashes = self.defaults.get('dashes', None)
        # ---- color and transparency
        fill = self.defaults.get('fill', self.defaults.get('fill_color'))
        self.fill = self.get_color(fill, white)
        self.transparency = self.defaults.get('transparency', None)
        self.debug_color = self.get_color(
            self.defaults.get('debug_color'), DEBUG_COLOR)
        # ---- stroke
        stroke = self.defaults.get('stroke', self.defaults.get('stroke_color'))
        self.stroke = self.get_color(stroke, black)
        self.stroke_width = self.defaults.get('stroke_width', WIDTH)
        # ---- font
        self.font_face = self.defaults.get('font_face', 'Helvetica')
        self.font_size = self.defaults.get('font_size', 12)
        self.style = self.defaults.get('style', None)  # Normal? from reportlab
        self.wrap = self.defaults.get('wrap', False)
        self.align = self.defaults.get('align', 'centre')  # left,right,justify
        self._alignment = TA_LEFT  # see to_alignment()
        # ---- text: base
        self.text = self.defaults.get('text', '')
        self.text_size = self.defaults.get('text_size', self.font_size)
        self.text_stroke = self.get_color(
            self.defaults.get('text_stroke'), self.stroke)
        self.text_stroke_width = self.get_color(
            self.defaults.get('text_stroke_width'), self.stroke_width)
        # ---- text: label
        self.label = self.defaults.get('label', '')
        self.label_size = self.defaults.get('label_size', self.font_size)
        self.label_stroke = self.get_color(
            self.defaults.get('label_stroke'), self.stroke)
        self.label_stroke_width = self.get_color(
            self.defaults.get('label_stroke_width'), self.stroke_width)
        # ---- text: title
        self.title = self.defaults.get('title', '')
        self.title_size = self.defaults.get('title_size', self.font_size)
        self.title_stroke = self.get_color(
            self.defaults.get('title_stroke'), self.stroke)
        self.title_stroke_width = self.get_color(
            self.defaults.get('title_stroke_width'), self.stroke_width)
        # ---- text: heading
        self.heading = self.defaults.get('heading', '')
        self.heading_size = self.defaults.get('heading_size', self.font_size)
        self.heading_stroke = self.get_color(
            self.defaults.get('heading_stroke'), self.stroke)
        self.heading_stroke_width = self.get_color(
            self.defaults.get('heading_stroke_width'), self.stroke_width)
        # ---- text block
        self.outline_color = self.defaults.get('outline_color', self.fill)
        self.outline_width = self.defaults.get('outline_width', 0)
        self.leading = self.defaults.get('leading', 12)
        # ---- image / file
        self.source = self.defaults.get('source', None)  # file or http://
        # ---- line / ellipse / bezier / sector
        self.length = self.defaults.get('length', self.default_length)
        self.angle = self.defaults.get('angle', 0)
        self.angle_width = self.defaults.get('angle_width', 90)
        # ---- chord
        self.angle_1 = self.defaults.get('angle1', 0)
        self.xe = self.defaults.get('xe', 0)  # second point for ellipse
        self.ye = self.defaults.get('ye', 0)
        # ---- arrow: head and tail
        self.head_style = self.defaults.get('head_style', 'triangle')
        self.tail_style = self.defaults.get('tail_style', None)
        self.head_fraction = self.defaults.get('head_fraction', 0.1)
        self.tail_fraction = self.defaults.get('tail_fraction', 0.1)
        self.head_height = self.defaults.get('head_height', None)
        self.tail_height = self.defaults.get('tail_height', None)
        self.head_width = self.defaults.get('head_width', None)
        self.tail_width = self.defaults.get('tail_width', None)
        self.tail_fill = self.defaults.get('tail_fill', self.fill)
        self.head_fill = self.defaults.get('head_fill', self.fill)
        self.head_stroke = self.defaults.get('head_stroke', self.stroke)
        self.tail_stroke = self.defaults.get('tail_stroke', self.stroke)
        self.head_stroke_width = self.defaults.get(
            'head_stroke_width', self.stroke_width)
        self.tail_stroke_width = self.defaults.get(
            'tail_stroke_width', self.stroke_width)
        # ---- line / bezier
        self.x_1 = self.defaults.get('x1', 0)
        self.y_1 = self.defaults.get('y1', 0)
        # ---- bezier
        self.x_2 = self.defaults.get('x2', 1)
        self.y_2 = self.defaults.get('y2', 1)
        self.x_3 = self.defaults.get('x3', 1)
        self.y_3 = self.defaults.get('y3', 1)
        # ---- rect / card
        self.rounding = self.defaults.get('rounding', 0)
        self.rounded = self.defaults.get('rounded', False)
        self.notch = self.defaults.get('notch', 0)
        self.notch_corners = self.defaults.get('notch_corners', 'SW NW NE SE')
        self.notch_x = self.defaults.get('notch_x', 0)
        self.notch_y = self.defaults.get('notch_y', 0)
        # ---- stadium
        self.edges = self.defaults.get('edges', 'L R')
        # ---- grid / card layout
        self.rows = self.defaults.get('rows', 0)
        self.cols = self.defaults.get('cols', self.defaults.get('columns', 0))
        self.offset_x = self.defaults.get('offset_x', 0)
        self.offset_y = self.defaults.get('offset_y', 0)
        # ---- circle / star / polygon
        self.diameter = self.defaults.get('diameter', 1)
        self.radius = self.defaults.get('radius', self.diameter / 2.0)
        self.vertices = self.defaults.get('vertices', 5)
        self.sides = self.defaults.get('sides', 6)
        self.points = self.defaults.get('points', [])
        # ---- compass
        self.perimeter = self.defaults.get('perimeter', 'circle')
        self.directions = self.defaults.get('directions', None)
        # ---- triangle
        self.flip = self.defaults.get('flip', 'up')
        self.hand = self.defaults.get('hand', 'right')
        # ---- hexagon / circle / octagon
        self.side = self.defaults.get('side', 0)  # length of sides
        self.centre_shape = self.defaults.get('centre_shape', '')
        self.centre_shape_x = self.defaults.get('centre_shape_x', 0)
        self.centre_shape_y = self.defaults.get('centre_shape_y', 0)
        self.dot_size = self.defaults.get('dot_size', 0)
        self.dot_color = self.get_color(self.defaults.get('dot_color'), black)
        self.cross_size = self.defaults.get('cross_size', 0)
        self.cross_stroke = self.get_color(self.defaults.get('cross_stroke'), black)
        self.cross_stroke_width = self.defaults.get('cross_stroke_width', self.stroke_width)
        # ---- hexagon
        self.hex_top = self.defaults.get('hex_top', 'flat')  # flat|pointy
        self.caltrops = self.defaults.get('caltrops', None)
        self.caltrops_fraction = self.defaults.get('caltrops_fraction', None)
        self.caltrops_invert = kwargs.get('caltrops_invert', False)
        self.links = self.defaults.get('links', None)
        self.link_width = self.defaults.get('link_width', self.stroke_width)
        self.link_stroke = self.defaults.get('link_stroke', self.stroke)
        self.link_cap = self.defaults.get('link_cap', self.line_cap)
        # ---- hexagons
        self.hid = self.defaults.get('id', '')  # HEX ID
        self.hex_rows = self.defaults.get('hex_rows', 0)
        self.hex_cols = self.defaults.get('hex_cols', 0)
        self.hex_offset = self.defaults.get('hex_offset', 'even')  # even|odd
        self.hex_layout = self.defaults.get('hex_layout', 'rectangle')  # rectangle
        self.coord_type_x = self.defaults.get('coord_type_x', 'number')  # number|letter
        self.coord_type_y = self.defaults.get('coord_type_y', 'number')  # number|letter
        self.coord_start_x = self.defaults.get('coord_start_x', 0)
        self.coord_start_y = self.defaults.get('coord_start_y', 0)
        self.coord_position = self.defaults.get('coord_position', None)  # top|middle|bottom
        self.coord_offset = self.defaults.get('coord_offset', 0)
        self.coord_font_face = self.defaults.get('coord_font_face', 'Helvetica')
        self.coord_font_size = self.defaults.get('coord_font_size',
                                                 int(self.font_size * 0.5))
        self.coord_stroke = self.get_color(self.defaults.get('coord_stroke'), black)
        self.coord_padding = self.defaults.get('coord_padding', 2)
        self.coord_separator = self.defaults.get('coord_separator', '')
        self.coord_prefix = self.defaults.get('coord_prefix', '')
        self.coord_style = self.defaults.get('coord_style', '')
        self.masked = self.defaults.get('masked', [])
        # ---- starfield
        self.enclosure = None
        self.colors = [white]
        self.sizes = [self.defaults.get('stroke_width', WIDTH)]
        self.density = 10
        self.star_pattern = 'random'
        # ---- hatches
        self.hatch = self.defaults.get('hatch', 0)
        self.hatch_directions = self.defaults.get('hatch_directions', 'n ne e se')
        self.hatch_width = self.defaults.get('hatch_width', self.stroke_width)
        self.hatch_stroke = self.defaults.get('hatch_stroke', self.stroke)
        self.hatch_dots = self.defaults.get('hatch_dots', None)
        self.hatch_cap = self.defaults.get('hatch_cap', self.line_cap)
        self.hatch_dashes = self.defaults.get('hatch_dashes', None)

    def get_canvas(self):
        """Return reportlab canvas object"""
        return self.canvas

    def get_color(self, name=None, default=black):
        """Get a color by name from a pre-defined dictionary."""
        if name:
            return COLORS.get(name, default)
        return default

    def get_units(self, name=None, default=cm):
        """Get units by name from a pre-defined dictionary."""
        if name:
            return UNITS.get(name, default)
        return default

    def get_page(self, name=None, default=A4):
        """Get a page-size by name from a pre-defined dictionary."""
        if name:
            return PAGES.get(name, default)
        return default


class BaseShape:
    """Base class for objects that are drawn on a given canvas."""

    def __init__(self, _object=None, canvas=None, **kwargs):
        self.kwargs = kwargs
        # tools.feedback(f'*** BaseShape {kwargs=}')
        # ---- constants
        self.default_length = 1
        self.show_id = False  # True
        # ---- KEY
        self.canvas = canvas or BaseCanvas()  # BaseCanvas object
        cnv = self.canvas  # shortcut for use in getting defaults
        # log.debug("BaseShape types %s %s %s",type(self.canvas),type(canvas),type(cnv))
        self._object = _object  # placeholder for an incoming Shape object
        self.shape_id = None
        self.stylesheet = getSampleStyleSheet()
        self.sequence = kwargs.get('sequence', [])  # e.g. card numbers
        self.dataset = []  # list of dict data (loaded from file)
        self.members = []  # card IDs, of which current card is a member
        # ---- general
        self.common = kwargs.get('common', None)
        self.shape = kwargs.get('shape', cnv.shape)
        self.run_debug = kwargs.get("debug", cnv.run_debug)
        self.units = kwargs.get('units', cnv.units)
        # ---- page
        self.pagesize = kwargs.get('pagesize', cnv.pagesize)
        self.margin = kwargs.get('margin', cnv.margin)
        self.margin_top = kwargs.get('margin_top', cnv.margin_top)
        self.margin_bottom = kwargs.get('margin_bottom', cnv.margin_bottom)
        self.margin_left = kwargs.get('margin_left', cnv.margin_left)
        self.margin_right = kwargs.get('margin_right', cnv.margin_right)
        self.grid_marks = kwargs.get('grid_marks', cnv.grid_marks)
        self.grid_color = kwargs.get('grid_color', cnv.grid_color)
        self.grid_stroke_width = kwargs.get('grid_stroke_width', cnv.grid_stroke_width)
        self.grid_length = kwargs.get('grid_length', cnv.grid_length)
        self.page_width = self.pagesize[0] / self.units
        self.page_height = self.pagesize[1] / self.units
        # ---- sizes and positions
        self.row = kwargs.get('row', cnv.row)
        self.col = kwargs.get('col', kwargs.get('column', cnv.col))
        self.height = kwargs.get('height', cnv.height)
        self.width = kwargs.get('width', cnv.width)
        self.size = kwargs.get('size', cnv.size)  # for equal height/width
        self.x = kwargs.get('x', kwargs.get('left', cnv.x))
        self.y = kwargs.get('y', kwargs.get('bottom', cnv.y))
        self.cx = kwargs.get('cx', cnv.cx)  # centre (for some shapes)
        self.cy = kwargs.get('cy', cnv.cy)  # centre (for some shapes)
        self.scaling = kwargs.get('scaling', None)  # SVG images
        self.dot_point = kwargs.get('dot_point', cnv.dot_point)  # points
        # ---- to be calculated ...
        self.area = cnv.area
        self.vertices = cnv.vertices
        # ---- repeats
        self.pattern = kwargs.get('pattern', cnv.pattern)
        self.repeat = kwargs.get('repeat', cnv.repeat)
        self.offset = kwargs.get('offset', cnv.offset)
        self.offset_across = kwargs.get('offset_down', cnv.offset_down)
        self.offset_down = kwargs.get('offset_across', cnv.offset_across)
        self.gap = kwargs.get('gap', cnv.gap)
        self.gap_x = kwargs.get('gap_x', cnv.gap_x)
        self.gap_y = kwargs.get('gap_y', cnv.gap_y)
        # ---- rotate in degrees / radians
        self.rotate = kwargs.get('rotate', kwargs.get('rotation', cnv.rotate))
        self._rotate_theta = math.radians(self.rotate)  # radians
        self.orientation = kwargs.get('orientation', cnv.orientation)
        self.position = kwargs.get('position', cnv.position)
        # ---- line
        self.line_width = kwargs.get('line_width', cnv.line_width)
        self.line_cap = kwargs.get('line_cap', cnv.line_cap)
        self.line_dots = kwargs.get('line_dots',
                                    kwargs.get('dots', cnv.line_dots))
        self.dashes = kwargs.get('dashes', None)
        # ---- color and transparency
        self.debug_color = kwargs.get('debug_color', cnv.debug_color)
        self.transparency = kwargs.get('transparency', cnv.transparency)
        # ---- stroke
        self.stroke = kwargs.get('stroke', kwargs.get('stroke_color', cnv.stroke))
        self.stroke_width = kwargs.get('stroke_width', cnv.stroke_width)
        # ---- font
        self.font_face = kwargs.get('font_face', cnv.font_face)
        self.font_size = kwargs.get('font_size', cnv.font_size)
        self.style = kwargs.get('style', cnv.style)  # Normal? from reportlab
        self.wrap = kwargs.get('wrap', cnv.wrap)
        self.align = kwargs.get('align', cnv.align)  # left, right, justify
        self._alignment = TA_LEFT  # see to_alignment()
        # ---- text: base
        self.text = kwargs.get('text', cnv.text)
        self.text_size = kwargs.get('text_size', cnv.text_size)
        self.text_stroke = kwargs.get('text_stroke', cnv.text_stroke)
        self.text_stroke_width = kwargs.get('text_stroke_width', cnv.text_stroke_width)
        # ---- text: label
        self.label = kwargs.get('label', cnv.label)
        self.label_size = kwargs.get('label_size', cnv.label_size)
        self.label_stroke = kwargs.get('label_stroke', cnv.label_stroke)
        self.label_stroke_width = kwargs.get('label_stroke_width', cnv.label_stroke_width)
        # ---- text: title
        self.title = kwargs.get('title', cnv.title)
        self.title_size = kwargs.get('title_size', cnv.title_size)
        self.title_stroke = kwargs.get('title_stroke', cnv.title_stroke)
        self.title_stroke_width = kwargs.get('title_stroke_width', cnv.title_stroke_width)
        # ---- text: heading
        self.heading = kwargs.get('heading', cnv.heading)
        self.heading_size = kwargs.get('heading_size', cnv.heading_size)
        self.heading_stroke = kwargs.get('heading_stroke', cnv.heading_stroke)
        self.heading_stroke_width = kwargs.get('heading_stroke_width', cnv.heading_stroke_width)
        # ---- text block
        self.outline_color = kwargs.get('outline_color', cnv.outline_color)
        self.outline_width = kwargs.get('outline_width', cnv.outline_width)
        self.leading = kwargs.get('leading', cnv.leading)
        # ---- fill color
        self.fill = kwargs.get('fill', kwargs.get('fill_color', cnv.fill))
        # tools.feedback(f"+++  BShp:{self} init {kwargs.get('fill')=} {self.fill=} {kwargs.get('fill_color')=}")
        # ---- image / file
        self.source = kwargs.get('source', cnv.source)  # file or http://
        # ---- line / ellipse / bezier / arc
        self.length = kwargs.get('length', cnv.length)
        self.angle = kwargs.get('angle', cnv.angle)  # anti-clock from flat
        self.angle_width = kwargs.get('angle_width', cnv.angle_width)  # delta degrees
        self._angle_theta = math.radians(self.angle)
        # ---- chord
        self.angle_1 = kwargs.get('angle1', cnv.angle_1)  # anti-clock from flat
        self._angle_1_theta = math.radians(self.angle_1)
        self.xe = kwargs.get('xe', cnv.xe)
        self.ye = kwargs.get('ye', cnv.ye)
        # ---- arrow: head and tail
        self.head_style = kwargs.get('head_style', cnv.head_style)
        self.tail_style = kwargs.get('tail_style', cnv.tail_style)
        self.head_fraction = kwargs.get('head_fraction', cnv.head_fraction)
        self.tail_fraction = kwargs.get('tail_fraction', cnv.tail_fraction)
        self.head_height = kwargs.get('head_height', cnv.head_height)
        self.tail_height = kwargs.get('tail_height', cnv.tail_width)
        self.head_width = kwargs.get('head_width', cnv.head_width)
        self.tail_width = kwargs.get('tail_width', cnv.tail_width)
        self.tail_fill = kwargs.get('tail_fill', cnv.tail_fill)
        self.head_fill = kwargs.get('head_fill', cnv.head_fill)
        self.head_stroke = kwargs.get('head_stroke', cnv.stroke)
        self.tail_stroke = kwargs.get('tail_stroke', cnv.stroke)
        self.head_stroke_width = kwargs.get('head_stroke_width', cnv.stroke_width)
        self.tail_stroke_width = kwargs.get('tail_stroke_width', cnv.stroke_width)
        # ---- line / bezier / sector
        self.x_1 = kwargs.get('x1', cnv.x_1)
        self.y_1 = kwargs.get('y1', cnv.y_1)
        # ---- bezier / sector
        self.x_2 = kwargs.get('x2', cnv.x_2)
        self.y_2 = kwargs.get('y2', cnv.y_2)
        self.x_3 = kwargs.get('x3', cnv.x_3)
        self.y_3 = kwargs.get('y3', cnv.y_3)
        # ---- rect / card
        self.rounding = kwargs.get('rounding', cnv.rounding)
        self.rounded = kwargs.get('rounded', cnv.rounded)
        self.notch = kwargs.get('notch', cnv.notch)
        self.notch_corners = kwargs.get('notch_corners', cnv.notch_corners)
        self.notch_x = kwargs.get('notch_x', cnv.notch_x)
        self.notch_y = kwargs.get('notch_y', cnv.notch_y)
        # ---- stadium
        self.edges = kwargs.get('edges', cnv.edges)
        # ---- grid / card layout
        self.rows = kwargs.get('rows', cnv.rows)
        self.cols = kwargs.get('cols', kwargs.get('columns', cnv.cols))
        self.offset_x = kwargs.get('offset_x', cnv.offset_x)
        self.offset_y = kwargs.get('offset_y', cnv.offset_y)
        # ---- circle / star / polygon
        self.diameter = kwargs.get('diameter', cnv.diameter)
        self.radius = kwargs.get('radius', cnv.radius)
        self.vertices = kwargs.get('vertices', cnv.vertices)
        self.sides = kwargs.get('sides', cnv.sides)
        self.points = kwargs.get('points', cnv.points)
        # ---- compass
        self.perimeter = kwargs.get('perimeter', 'circle')  # circle|rectangle|hexagon
        self.directions = kwargs.get('directions', None)
        # ---- triangle
        self.flip = kwargs.get('flip', 'up')
        self.hand = kwargs.get('hand', 'right')
        # ---- hexagon / circle / octagon
        self.side = kwargs.get('side', 0)  # length of sides
        self.centre_shape = kwargs.get('centre_shape', '')
        self.centre_shape_x = kwargs.get('centre_shape_x', cnv.centre_shape_x)
        self.centre_shape_y = kwargs.get('centre_shape_y', cnv.centre_shape_y)
        self.dot_color = kwargs.get('dot_color', cnv.dot_color)
        self.dot_size = kwargs.get('dot_size', cnv.dot_size)
        self.cross_stroke = kwargs.get('cross_stroke', cnv.cross_stroke)
        self.cross_stroke_width = kwargs.get('cross_stroke_width', cnv.cross_stroke_width)
        self.cross_size = kwargs.get('cross_size', cnv.cross_size)
        # ---- hexagon
        self.hex_top = kwargs.get('hex_top', cnv.hex_top)
        self.caltrops = kwargs.get('caltrops', cnv.caltrops)
        self.caltrops_fraction = kwargs.get('caltrops_fraction', cnv.caltrops_fraction)
        self.caltrops_invert = kwargs.get('caltrops_invert', cnv.caltrops_invert)
        self.links = kwargs.get('links', cnv.links)
        self.link_width = kwargs.get('link_width', cnv.link_width)
        self.link_stroke = kwargs.get('link_stroke', cnv.stroke)
        self.link_cap = kwargs.get('link_cap', cnv.link_cap)
        # ---- hexagons
        self.hid = kwargs.get('id', cnv.hid)  # HEX ID
        self.hex_rows = kwargs.get('hex_rows', cnv.hex_rows)
        self.hex_cols = kwargs.get('hex_cols', cnv.hex_cols)
        self.hex_layout = kwargs.get('hex_layout', cnv.hex_layout)  # rectangle|circle|diamond|triangle
        self.hex_offset = kwargs.get('hex_offset', cnv.hex_offset)  # even|odd
        self.coord_type_x = kwargs.get('coord_type_x', cnv.coord_type_x)  # number|letter
        self.coord_type_y = kwargs.get('coord_type_y', cnv.coord_type_y)  # number|letter
        self.coord_start_x = kwargs.get('coord_start_x', cnv.coord_start_x)
        self.coord_start_y = kwargs.get('coord_start_y', cnv.coord_start_y)
        self.coord_position = kwargs.get('coord_position', cnv.coord_position)  # top|middle|bottom
        self.coord_offset = kwargs.get('coord_offset', cnv.coord_offset)
        self.coord_font_face = kwargs.get('coord_font_face', cnv.coord_font_face)
        self.coord_font_size = kwargs.get('coord_font_size', cnv.coord_font_size)
        self.coord_stroke = kwargs.get('coord_stroke', cnv.coord_stroke)
        self.coord_padding = kwargs.get('coord_padding', cnv.coord_padding)
        self.coord_separator = kwargs.get('coord_separator', cnv.coord_separator)
        self.coord_prefix = kwargs.get('coord_prefix', cnv.coord_prefix)
        self.coord_style = kwargs.get('coord_style', '') # linear|diagonal
        self.masked = kwargs.get('masked', cnv.masked)
        # ---- starfield
        self.enclosure = kwargs.get('enclosure', cnv.enclosure)
        self.colors = kwargs.get('colors', cnv.colors)
        self.sizes = kwargs.get('sizes', cnv.sizes)
        self.density = kwargs.get('density', cnv.density)
        self.star_pattern = kwargs.get('star_pattern', cnv.star_pattern)
        # ---- hatches
        self.hatch = kwargs.get('hatch', cnv.hatch)
        self.hatch_directions = kwargs.get('hatch_directions', cnv.hatch_directions)
        self.hatch_width = kwargs.get('hatch_width', cnv.hatch_width)
        self.hatch_stroke = kwargs.get('hatch_stroke', cnv.stroke)
        self.hatch_cap = kwargs.get('hatch_cap', cnv.hatch_cap)
        self.hatch_dots = kwargs.get('hatch_dots', cnv.line_dots)
        self.hatch_dashes = kwargs.get('hatch_dashes', cnv.dashes)

        # ---- CHECK ALL
        correct, issue = self.check_settings()
        if not correct:
            tools.feedback("Problem with settings: %s." % '; '.join(issue))
        # ---- UPDATE SELF WITH COMMON
        if self.common:
            try:
                attrs = vars(self.common)
            except TypeError:
                tools.feedback(f'Cannot process the Common property "{self.common}"'
                               ' - please check!', True)
            for attr in attrs.keys():
                if attr not in ['canvas', 'common', 'stylesheet', 'kwargs'] and \
                        attr[0] != '_':
                    # tools.feedback(f'{attr=}')
                    common_attr = getattr(self.common, attr)
                    base_attr = getattr(BaseCanvas(), attr)
                    if common_attr != base_attr:
                        setattr(self, attr, common_attr)

        # ---- SET offset properties to correct units
        self._o = self.set_offset_props()
        # ---- SET UNIT PROPS (last!)
        self.set_unit_properties()

    def __str__(self):
        return f'{self.__class__.__name__}::{self.kwargs}'

    def unit(self, item, units=None, skip_none=False):
        """Convert an item into the appropriate unit system."""
        log.debug("units %s %s", units, self.units)
        if item is None and skip_none:
            return None
        if not units:
            units = self.units
        try:
            return item * units
        except (TypeError, ValueError):
            tools.feedback(
                f'Unable to set units: "{item}".'
                ' Please check that this is a valid value.',
                stop=True)

    def set_unit_properties(self):
        """Convert base properties into unit-based values."""
        # set a "width" value for use in calculations e.g. Track
        if self.radius and not self.width:
            self.width = 2.0 * self.radius
        if self.diameter and not self.width:
            self.width = self.diameter
        if self.side and not self.width:
            self.width = self.side  # square

        self._u = UnitProperties(
            self.pagesize[0],
            self.pagesize[1],
            self.unit(self.margin_left) if self.margin_left is not None else None,
            self.unit(self.margin_right) if self.margin_right is not None else None,
            self.unit(self.margin_bottom) if self.margin_bottom is not None else None,
            self.unit(self.margin_top) if self.margin_top else None,
            self.unit(self.x) if self.x is not None else None,
            self.unit(self.y) if self.y is not None else None,
            self.unit(self.cx) if self.cx is not None else None,
            self.unit(self.cy) if self.cy is not None else None,
            self.unit(self.height) if self.height is not None else None,
            self.unit(self.width) if self.width is not None else None,
            self.unit(self.radius) if self.radius is not None else None,
            self.unit(self.diameter) if self.diameter is not None else None,
            self.unit(self.side) if self.side is not None else None,
            self.unit(self.length) if self.length is not None else None)

    def set_offset_props(self, off_x=0, off_y=0):
        """Get OffsetProperties for a Shape."""
        margin_left = self.unit(self.margin_left) if self.margin_left is not None else None
        margin_bottom = self.unit(self.margin_bottom) if self.margin_bottom is not None else None
        off_x = self.unit(off_x) if off_x is not None else None
        off_y = self.unit(off_y) if off_y is not None else None
        return OffsetProperties(
            off_x,
            off_y,
            off_x + margin_left,
            off_y + margin_bottom)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an element on a given canvas."""
        self._o = self.set_offset_props(off_x, off_y)
        # self.abs... variable are absolute page locations in native units
        #  they are for internal use only and are not expected to be called by the user
        #  if set, they should be used to ignore/bypass any other values for calculating
        #  the starting point or centre point for drawing a shape
        self._abs_x = kwargs.get('_abs_x', None)
        self._abs_y = kwargs.get('_abs_y', None)
        self._abs_x1 = kwargs.get('_abs_x1', None)
        self._abs_y1= kwargs.get('_abs_y1', None)
        self._abs_cx = kwargs.get('_abs_cx', None)
        self._abs_cy = kwargs.get('_abs_cy', None)
        self.use_abs = True if self._abs_x and self._abs_y else False
        self.use_abs_1 = True if self._abs_x1 and self._abs_y1 else False
        self.use_abs_c = True if self._abs_cx and self._abs_cy else False

    def set_canvas_props(
            self,
            cnv=None,
            fill=None,  # reserve None for 'no fill at all'
            stroke=None,
            stroke_width=None,
            stroke_cap=None,
            line_dots=None,
            dashes=None,
            debug=False):
        """Set reportlab canvas properties for font, line and colors"""
        canvas = cnv if cnv else self.canvas.canvas
        try:
            canvas.setFont(self.font_face, self.font_size)
        except AttributeError:
            pass
        except KeyError:
            tools.feedback(
                f'Unable to find font: "{self.font_face}".'
                ' Please check that this is installed on your system.',
                stop=True)
        try:
            if fill is None and self.fill is None:
                canvas.setFillColor(white, 0)  # full transparency
                if debug:
                    tools.feedback('~~~ NO fill color set!')
            else:
                _fill = fill or self.fill
                if self.transparency:
                    try:
                        alpha = float(self.transparency) / 100.0
                    except Exception:
                        tools.feedback(
                            f'Unable to use "{self.transparency}" as the transparency'
                            ' - must be from 1 to 100', True)
                    z = Color(_fill.red, _fill.green, _fill.blue, alpha)
                    # tools.feedback(f'~~~ Transp. color set: {z} vs. {_fill}')
                    _fill = z
                canvas.setFillColor(_fill)
                if debug:
                    tools.feedback(f'~~~ Fill color set: {_fill}')
        except AttributeError:
            tools.feedback('Unable to set fill color ')
        try:
            canvas.setStrokeColor(stroke or self.stroke)
        except TypeError:
            tools.feedback('Please check your stroke setting; should be a color value')
        except AttributeError:
            pass
        try:
            canvas.setLineWidth(stroke_width or self.stroke_width)
        except TypeError:
            tools.feedback('Please check your stroke_width setting; should be a number')
        except AttributeError:
            pass
        # ---- line cap
        if stroke_cap:
            if stroke_cap in ['r', 'rounded']:
                canvas.setLineCap(1)
            elif stroke_cap in ['s', 'square']:
                canvas.setLineCap(2)
            else:
                tools.feedback(f'Line cap type "{stroke_cap}" cannot be used.', False)
        # ---- set line dots / dashes
        if line_dots or self.line_dots:
            _dots = self.values_to_points([0.03, 0.03])
            canvas.setDash(array=_dots)
        elif dashes or self.dashes:
            dash_values = dashes or self.dashes
            _dashes = self.values_to_points(dash_values)
            canvas.setDash(array=_dashes)
        else:
            canvas.setDash(array=[])

    def check_settings(self):
        """Check that the user-supplied parameters are correct"""
        correct = True
        issue = []
        if self.align:
            if str(self.align).lower() not in \
                    ['left', 'right', 'justify', 'centre', 'l', 'r', 'j', 'c', ]:
                issue.append(f'"{self.align}" is an invalid align!')
                correct = False
        if self.caltrops:
            if str(self.caltrops).lower() not in \
                    ['large', 'medium', 'small', 's', 'm', 'l', ]:
                issue.append(f'"{self.caltrops}" is an invalid caltrops sie!')
                correct = False
        if self.edges:
            if not isinstance(self.edges, list):
                _edges = self.edges.split()
            else:
                _edges = self.edges
            for edge in _edges:
                if str(edge).lower() not in \
                        ['left', 'right', 'top', 'bottom', 'l', 'r', 't', 'b', ]:
                    issue.append(f'"{edge}" is an invalid option in {self.edges}!')
                    correct = False
        if self.flip:
            if str(self.flip).lower() not in \
                    ['up', 'down', 'u', 'd', ]:
                issue.append(f'"{self.flip}" is an invalid flip!')
                correct = False
        if self.hand:
            if str(self.hand).lower() not in \
                    ['left', 'right', 'l', 'r', ]:
                issue.append(f'"{self.hand}" is an invalid hand!')
                correct = False
        if self.orientation:
            if str(self.orientation).lower() not in \
                    ['vertical', 'horizontal', 'v', 'h', ]:
                issue.append(f'"{self.orientation}" is an invalid orientation!')
                correct = False
        if self.perimeter:
            if str(self.perimeter).lower() not in \
                    ['circle', 'rectangle', 'hexagon', 'octagon', 'c', 'r', 'h', 'o', ]:
                issue.append(f'"{self.perimeter}" is an invalid perimeter!')
                correct = False
        if self.position:
            if str(self.position).lower() not in \
                    ['top', 'bottom', 'center', 'middle',  't', 'b', 'c', 'm', ]:
                issue.append(f'"{self.position}" is an invalid position!')
                correct = False
        # ---- hexagons
        if self.coord_style:
            if str(self.coord_style).lower() not in \
                    ['l', 'linear', 'd', 'diagonal', ]:
                issue.append(f'"{self.coord_style}" is an invalid coord style!')
                correct = False
        # ---- arrows
        if self.head_style:
            if str(self.head_style).lower() not in \
                    ['line', 'l', 'line2', 'l2', 'line3', 'l3', 'triangle', 't',
                     'diamond', 'd', 'notch', 'n', 'spear', 's', 'circle', 'c', ]:
                issue.append(f'"{self.head_style}" is an invalid arrow head_style!')
                correct = False
        if self.tail_style:
            if str(self.tail_style).lower() not in \
                    ['line', 'l', 'line2', 'l2', 'line3', 'l3', 'feather', 'f',
                     'circle', 'c', ]:
                issue.append(f'"{self.tail_style}" is an invalid arrow tail_style!')
                correct = False
        # ---- starfield
        if self.star_pattern:
            if str(self.star_pattern).lower() not in \
                    ['random', 'r', 'cluster', 'c', ]:
                issue.append(f'"{self.pattern}" is an invalid starfield pattern!')
                correct = False

        return correct, issue

    def to_alignment(self):
        """Convert local, English-friendly alignments to Reportlab enums."""
        if self.align == 'centre' or self.align == 'center':
            self._alignment = TA_CENTER
        elif self.align == 'right':
            self._alignment = TA_RIGHT
        elif self.align == 'justify':
            self._alignment = TA_JUSTIFY
        else:
            self._alignment = TA_LEFT
        return self._alignment

    def load_image(self, source=None, scaling=None) -> tuple:
        """Load an image from file or website.

        If source not found; try path in which script located.

        Returns:
            tuple: Image or SVG; boolean (True if file type is SVG)

        Notes:
            * https://www.blog.pythonlibrary.org/2018/04/12/adding-svg-files-in-reportlab/
        """

        def scale_image(drawing, scaling_factor):
            """Scale a shapes.Drawing() while maintaining aspect ratio
            """
            try:
                _scaling_factor = float(scaling_factor)
            except Exception:
                tools.feedback(
                    f'Cannot scale an image with a value of {scaling_factor}', True)
            scaling_x = _scaling_factor
            scaling_y = _scaling_factor
            drawing.width = drawing.minWidth() * scaling_x
            drawing.height = drawing.height * scaling_y
            drawing.scale(scaling_x, scaling_y)
            return drawing

        img = None
        try:
            svg = False
            source_ext = source.strip()[-3:]
            # tools.feedback(f'Loading type: {source_ext}')
            if source_ext.lower() == 'svg':
                svg = True
        except Exception:
            pass
        if source:
            try:
                if svg:
                    if not os.path.exists(source):
                        raise IOError
                    img = svg2rlg(source)
                    if scaling:
                        img = scale_image(img, scaling)
                else:
                    img = ImageReader(source)
                return img, svg
            except IOError:
                filepath = tools.script_path()
                _source = os.path.join(filepath, source)
                try:
                    if svg:
                        if not os.path.exists(_source):
                            raise IOError
                        img = svg2rlg(_source)
                        if scaling:
                            img = scale_image(img, scaling_factor=scaling)
                    else:
                        img = ImageReader(_source)
                    return img, svg
                except IOError:
                    ftype = 'SVG ' if svg else ''
                    tools.feedback(
                        f'Unable to find or open {ftype}image "{_source}";'
                        f' including {filepath}.')
        return img, svg

    def process_template(self, _dict):
        """Set values for properties based on those defined in a dictionary."""
        if _dict.get('x'):
            self.x = _dict.get('x', 1)
        if _dict.get('y'):
            self.y = _dict.get('y', 1)
        if _dict.get('height'):
            self.height = _dict.get('height', 1)
        if _dict.get('width'):
            self.width = _dict.get('width', 1)
        if _dict.get('diameter'):
            self.diameter = _dict.get('diameter', 1)
        if _dict.get('radius'):
            self.radius = _dict.get('radius', self.diameter / 2.0 or 1)
        if _dict.get('rounding'):
            self.rounding = _dict.get('rounding', None)
        # if _dict.get('x'):
        #    self.x = _dict.get('x', 1)

    def get_center(self):
        """Attempt to get centre (x,y) tuple for a shape."""
        if self.cx and self.cy:
            return (self.cx, self.cy)
        if self.x and self.y and self.width and self.height:
            return (self.x + self.width / 2.0, self.y + self.height / 2.0)
        return None

    def get_edges(self):
        """Attempt to get edges of rectangle."""
        if self.x and self.y and self.width and self.height:
            edges = {
                'left': self.x,
                'right': self.x + self.width,
                'bottom': self.y,
                'top': self.y + self.height
            }
            return edges
        return {}

    def make_path_points(self, cnv, p1: geoms.Point, p2: geoms.Point):
        """Draw line between two Points"""
        pth = cnv.beginPath()
        pth.moveTo(p1.x, p1.y)
        pth.lineTo(p2.x, p2.y)
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)

    def make_path_vertices(self, cnv, vertices: list, v1: int, v2: int):
        """Draw line between two vertices"""
        self.make_path_points(cnv, vertices[v1], vertices[v2])

    def textify(self, index=None, text=None):
        """Extract text from a list, or create string, based on index & type."""
        _text = text or self.text
        log.debug("text %s %s %s %s", index, text, _text, type(_text))
        if not _text:
            return
        if hasattr(_text, 'lower'):
            return _text
        try:
            return _text[index]
        except TypeError:
            return _text

    def points_to_value(self, value: float) -> float:
        """Convert a point value to a units-based value."""
        try:
            if self.units == cm:
                return float(value) / cm
            if self.units == mm:
                return float(value) / mm
            elif self.units == inch:
                return float(value) / inch
            else:
                return float(value)
        except Exception as err:
            log.exception(err)
            tools.feedback(f'Unable to convert "{value}" to {self.units}!', True)

    def values_to_points(self, items: list) -> list:
        """Convert a list of values to point units."""
        try:
            if self.units == cm:
                return [float(item) * cm for item in items]
            elif self.units == mm:
                return [float(item) * mm for item in items]
            elif self.units == inch:
                return [float(item) * inch for item in items]
            else:
                tools.feedback(f'Unable to convert "{self.units}" to points!', True)
        except Exception as err:
            log.exception(err)
            tools.feedback(f'Unable to convert "{items}" to points!', True)

    def draw_multi_string(self, canvas, x, y, string, align=None, rotate=0, **kwargs):
        """Low-level text drawing, split string (\n) if needed, with align and rotate.

        Args:
            * canvas (reportlab.pdfgen.canvas.Canvas): usually the calling
              function should access cnv.canvas i.e. an attribute of BaseCanvas
            * x (float) and y (float): must be in native units (i.e. points)!
            * string (str): the text to draw/write
            * align (str): one of [centre|right|left|None] alignment of text
            * rotate (float): an angle in degrees; anti-clockwise from East
        """
        if not string:
            return
        # ---- replace {PLACEHOLDER} with a value
        _sequence = kwargs.get('text_sequence', '')
        string = string.format(SEQUENCE=_sequence)
        # align
        align = align or self.align
        mvy = copy.copy(y)
        # tools.feedback("string %s %s rotate:%s" % (type(string), string, rotate))
        for ln in string.split('\n'):
            if rotate:
                canvas.saveState()
                canvas.translate(x, mvy)
                canvas.rotate(rotate)
                if align == 'centre':
                    canvas.drawCentredString(0, 0, ln)
                elif align == 'right':
                    canvas.drawRightString(0, 0, ln)
                else:
                    canvas.drawString(0, 0, ln)
                canvas.restoreState()
            else:
                if align == 'centre':
                    canvas.drawCentredString(x, mvy, ln)
                elif align == 'right':
                    canvas.drawRightString(x, mvy, ln)
                else:
                    canvas.drawString(x, mvy, ln)
            mvy -= canvas._leading

    def draw_string(self, canvas, x, y, string, align=None, rotate=0, **kwargs):
        """Draw a multi-string on the canvas.
        """
        self.draw_multi_string(
            canvas=canvas, x=x, y=y, string=string, align=align, rotate=rotate)

    def draw_heading(self, canvas, x, y, y_offset=0, rotate=0, **kwargs):
        """Draw the heading for a shape (normally above the shape).

        Requires native units (i.e. points)!
        """
        if self.heading:
            y_off = y_offset or self.title_size
            canvas.setFont(self.font_face, self.heading_size)
            canvas.setFillColor(self.heading_stroke)
            self.draw_multi_string(
                canvas, x, y + y_off, self.heading, rotate=rotate, **kwargs)

    def draw_label(self, canvas, x, y, align=None, rotate=0, centred=True, **kwargs):
        """Draw the label for a shape (usually at the centre).

        Requires native units (i.e. points)!
        """
        if self.label:
            y = y - (self.label_size / 3.0) if centred else y
            canvas.setFont(self.font_face, self.label_size)
            canvas.setFillColor(self.label_stroke)
            self.draw_multi_string(
                canvas, x, y, self.label, align=align, rotate=rotate, **kwargs)

    def draw_title(self, canvas, x, y, y_offset=0, align=None, rotate=0, **kwargs):
        """Draw the title for a shape (normally below the shape).

        Requires native units (i.e. points)!
        """
        if self.title:
            y_off = y_offset or self.title_size
            canvas.setFont(self.font_face, self.title_size)
            canvas.setFillColor(self.title_stroke)
            self.draw_multi_string(
                canvas, x, y - y_off, self.title, align=align, rotate=rotate, **kwargs)

    def draw_dot(self, canvas, x, y):
        """Draw a small dot on a shape (normally the centre).

        Requires native units (i.e. points)!
        """
        if self.dot_size:
            dot_size = self.unit(self.dot_size)
            canvas.setFillColor(self.dot_color)
            canvas.setStrokeColor(self.dot_color)
            canvas.circle(x, y, dot_size, stroke=1, fill=1)

    def draw_cross(self, canvas, x, y):
        """Draw a cross on a shape (normally the centre).

        Requires native units (i.e. points)!
        """
        if self.cross_size:
            cross_size = self.unit(self.cross_size)
            canvas.setFillColor(self.cross_stroke)
            canvas.setStrokeColor(self.cross_stroke)
            canvas.setLineWidth(self.cross_stroke_width)
            # horizontal
            pt1 = geoms.Point(x - cross_size / 2.0, y)
            pt2 = geoms.Point(x + cross_size / 2.0, y)
            self.make_path_points(canvas, pt1, pt2)
            # vertical
            pt1 = geoms.Point(x, y - cross_size / 2.0)
            pt2 = geoms.Point(x, y + cross_size / 2.0)
            self.make_path_points(canvas, pt1, pt2)

    def lines_between_sides(
            self,
            cnv,
            side: float,
            lines: int,
            vertices: list,
            left_nodes: tuple,
            right_nodes: tuple,
            ):
        """Draw lines between opposing (left and right) sides of a shape

        Args:
            side: length of a side
            lines: number of lines extending from the side
            vertices: list of the Points making up the shape
            left_nodes: ID's of vertices on either end of the left side
            right_nodes: ID's of vertices on either end of the right side

        Note:
            * Vertices normally go clockwise from bottom/lower left
            * Direction of vertex indices in left- and right-nodes must be the same
        """
        delta = side / lines
        # tools.feedback(f'{side=} {lines=} {delta=}')
        for number in range(0, lines + 1):
            left_pt = geoms.point_on_line(
                 vertices[left_nodes[0]], vertices[left_nodes[1]], delta * number)
            right_pt = geoms.point_on_line(
                 vertices[right_nodes[0]], vertices[right_nodes[1]], delta * number)
            self.make_path_points(cnv, left_pt, right_pt)

    def debug(self, canvas, **kwargs):
        """Execute any debug statements."""
        if self.run_debug:
            if kwargs.get('vertices', []):  # display vertex index number next to vertex
                canvas.setFillColor(self.debug_color)
                canvas.setFont(self.font_face, 4)
                for key, vert in enumerate(kwargs.get('vertices')):
                    x = self.points_to_value(vert.x)
                    y = self.points_to_value(vert.y)
                    self.draw_multi_string(
                        canvas, vert.x, vert.y, f'{key}:{x:.2f},{y:.2f}')

    def debug_point(self, canvas, point: geoms.Point, label=''):
        """Display a labelled point."""
        canvas.setFillColor(DEBUG_COLOR)
        canvas.setStrokeColor(DEBUG_COLOR)
        canvas.setLineWidth(0.1)
        canvas.setFont(self.font_face, 6)
        x = self.points_to_value(point.x)
        y = self.points_to_value(point.y)
        self.draw_multi_string(
            canvas, point.x, point.y, f'{label} {point.x:.2f},{point.y:.2f}')
        canvas.circle(point.x, point.y, 2, stroke=1, fill=1)

    def V(self, *args):
        """Placeholder for value evaluator."""
        try:
            return self.dataset[self.shape_id].get(args[0], '')
        except Exception:
            if not self.shape_id:
                tools.feedback('No ID - unable to locate item!')
            elif self.dataset[self.shape_id]:
                tools.feedback(f'Unable to locate item #{self.shape_id} in dataset!')
            else:
                tools.feedback(f'Unable to locate column {args[0]}!')
        return ''

    def Q(self, *args):
        """Placeholder for query evaluator."""
        tools.feedback('NOT YET AVAILABLE')


class GroupBase(list):
    """Class for group base."""

    def __init__(self, *args, **kwargs):
        list.__init__(self, *args)
        self.kwargs = kwargs
