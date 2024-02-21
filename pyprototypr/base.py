#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base shape class for pyprototypr
"""
# lib
import copy
import json
import logging
import math
import os
# third party
from reportlab.pdfgen import canvas as reportlab_canvas
from reportlab.lib.units import cm, inch
from reportlab.lib.pagesizes import (
    A6, A5, A4, A3, A2, A1, A0, LETTER, LEGAL, ELEVENSEVENTEEN,
    letter, legal, elevenSeventeen, B6, B5, B4, B3, B2, B0, landscape)
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import (
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
from pyprototypr.utils import tools

log = logging.getLogger(__name__)

DEBUG = False
UNITS = {
    "cm": cm,
    "inch": inch
}
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
}
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
}
WIDTH = 0.1


class BaseCanvas:
    """Wrapper/extended class for a ReportLab canvas."""

    def __init__(self, filename=None, pagesize=None, **kwargs):
        self.canvas = reportlab_canvas.Canvas(
            filename=filename, pagesize=pagesize or A4)
        self.jsonfile = kwargs.get('defaults', None)
        self.defaults = {}
        # override
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
        # constants
        self.default_length = 1
        self.show_id = False  # True
        # general
        self.shape = self.defaults.get('shape', 'rectangle')
        self.shape_id = None
        self.sequence = self.defaults.get('sequence', [])
        self.dataset = []
        self.members = []  # card IDs, of which current card is a member
        self._object = None
        self.kwargs = kwargs
        # page
        self.pagesize = self.get_page(self.defaults.get('pagesize'), A4)
        self.margin = self.defaults.get('margin', 1)
        self.margin_top = self.defaults.get('margin_top', self.margin)
        self.margin_bottom = self.defaults.get('margin_bottom', self.margin)
        self.margin_left = self.defaults.get('margin_left', self.margin)
        self.margin_right = self.defaults.get('margin_right', self.margin)
        self.grid_marks = self.defaults.get('grid_marks', 0)
        self.grid_color = self.get_color(
            self.defaults.get('grid_color'), grey)
        self.grid_stroke_width = self.defaults.get('grid_stroke_width', WIDTH)
        self.grid_length = self.defaults.get('grid_length', 0.33)
        # sizes and positions
        self.units = self.get_units(self.defaults.get('units'), cm)
        self.row = self.defaults.get('row', None)
        self.col = self.defaults.get('col', self.defaults.get('column', None))
        self.height = self.defaults.get('height', 1)
        self.width = self.defaults.get('width', 1)
        self.size = self.defaults.get('size', None)  # proxy for equal H/W
        self.x = self.defaults.get('x', self.defaults.get('left', 1))
        self.y = self.defaults.get('y', self.defaults.get('bottom', 1))
        self.cx = self.defaults.get('cx', None)
        self.cy = self.defaults.get('cy', None)
        # repeats
        self.offset = self.defaults.get('offset', 0)
        self.offset_across = self.defaults.get('offset_across', self.offset)
        self.offset_down = self.defaults.get('offset_down', self.offset)
        self.gap = self.defaults.get('gap', 0)
        self.gap_across = self.defaults.get('gap_across', self.gap)
        self.gap_down = self.defaults.get('gap_down', self.gap)
        # rotate in degrees
        self.rotate = self.defaults.get('rotate',
                                        self.defaults.get('rotation', 0))
        self.orientation = self.defaults.get('orientation', 'vertical')
        self.position = self.defaults.get('position', None)
        # line
        self.line_color = self.defaults.get('line_color', WIDTH)
        self.line_width = self.defaults.get('line_width', WIDTH)
        self.line_dots = self.defaults.get('line_dots',
                                           self.defaults.get('dots',
                                                             False))
        self.line_dashes = self.defaults.get('line_dashes',
                                             self.defaults.get('dashes',
                                                               False))
        self.line_dotdash = self.defaults.get('line_dotdash',
                                              self.defaults.get('dotdash',
                                                                None))
        # color and fill
        fill = self.defaults.get('fill', self.defaults.get('fill_color'))
        self.fill = self.get_color(fill, white)
        self.pattern = self.defaults.get('pattern', None)
        self.repeat = self.defaults.get('repeat', True)
        # text
        self.align = self.defaults.get('align', 'centre')  # left,right,justify
        self._alignment = TA_LEFT  # see to_alignment()
        self.font_face = self.defaults.get('font_face', 'Helvetica')
        self.font_size = self.defaults.get('font_size', 12)
        self.label_size = self.defaults.get('label_size', self.font_size)
        self.title_size = self.defaults.get('title_size', self.font_size)
        self.heading_size = self.defaults.get('heading_size', self.font_size)
        self.text = self.defaults.get('text', '')
        self.label = self.defaults.get('label', '')
        self.title = self.defaults.get('title', '')
        self.heading = self.defaults.get('heading', '')
        self.style = self.defaults.get('style', None)  # Normal? from reportlab
        self.wrap = self.defaults.get('wrap', False)
        # text block
        self.outline_color = self.defaults.get('outline_color', self.fill)
        self.outline_width = self.defaults.get('outline_width', 0)
        self.leading = self.defaults.get('leading', 12)
        # line colors
        stroke = self.defaults.get('stroke', self.defaults.get('stroke_color'))
        self.stroke = self.get_color(stroke, black)
        self.stroke_width = self.defaults.get('stroke_width', WIDTH)
        self.stroke_text = self.get_color(
            self.defaults.get('stroke_text'), self.stroke)
        self.stroke_label = self.get_color(
            self.defaults.get('stroke_label'), self.stroke)
        self.stroke_title = self.get_color(
            self.defaults.get('stroke_title'), self.stroke)
        self.stroke_heading = self.get_color(
            self.defaults.get('stroke_heading'), self.stroke)
        # line and fill
        self.transparent = self.defaults.get('transparent', False)
        # image / file
        self.source = self.defaults.get('source', None)  # file or http://
        # line / ellipse / bezier
        self.length = self.defaults.get('length', 0)
        self.angle = self.defaults.get('angle', 0)
        self.x_1 = self.defaults.get('x1', 1)
        self.y_1 = self.defaults.get('y1', 1)
        # bezier
        self.x_2 = self.defaults.get('x2', 1)
        self.y_2 = self.defaults.get('y2', 1)
        self.x_3 = self.defaults.get('x3', 1)
        self.y_3 = self.defaults.get('y3', 1)
        # rect / card
        self.rounding = self.defaults.get('rounding', 0)
        self.rounded = self.defaults.get('rounded', False)
        # grid / card layout
        self.rows = self.defaults.get('rows', 1)
        self.cols = self.defaults.get('cols', self.defaults.get('columns', 1))
        # circle / star / poly
        self.radius = self.defaults.get('radius', 1)
        self.vertices = self.defaults.get('vertices', 5)
        self.sides = self.defaults.get('sides', 6)
        self.points = self.defaults.get('points', [])
        # hexes
        self.side = self.defaults.get('side', 1)  # length of sides
        self.dot_color = self.get_color(self.defaults.get('dot_color'), black)
        self.dot_size = self.defaults.get('dot_size', 0)
        self.hid = self.defaults.get('id', '')  # HEX ID

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
        # constants
        self.default_length = 1
        self.show_id = False  # True
        # KEY
        self.canvas = canvas or BaseCanvas()  # BaseCanvas object
        cnv = self.canvas  # shortcut for use in getting defaults
        log.debug("Base types %s %s %s", type(self.canvas), type(canvas), type(cnv))
        self._object = _object  # placeholder for an incoming Shape object
        self.kwargs = kwargs
        self.shape_id = None
        self.stylesheet = getSampleStyleSheet()
        self.sequence = kwargs.get('sequence', [])  # e.g. card numbers
        self.dataset = []  # list of dict data (loaded from file)
        self.members = []  # card IDs, of which current card is a member
        # general
        self.common = kwargs.get('common', None)
        self.shape = kwargs.get('shape', cnv.shape)
        # page
        self.pagesize = kwargs.get('pagesize', cnv.pagesize)
        self.margin = kwargs.get('margin', cnv.margin)
        self.margin_top = kwargs.get('margin_top', cnv.margin_top)
        self.margin_bottom = kwargs.get('margin_bottom', cnv.margin_bottom)
        self.margin_left = kwargs.get('margin_left', cnv.margin_left)
        self.margin_right = kwargs.get('margin_right', cnv.margin_right)
        self.grid_marks = kwargs.get('grid_marks', cnv.grid_marks)
        self.grid_color = kwargs.get('grid_color', cnv.grid_color)
        self.grid_stroke_width = kwargs.get('grid_stroke_width',
                                            cnv.grid_stroke_width)
        self.grid_length = kwargs.get('grid_length', cnv.grid_length)
        # sizes and positions
        self.units = kwargs.get('units', cnv.units)
        self.row = kwargs.get('row', cnv.row)
        self.col = kwargs.get('col', kwargs.get('column', cnv.col))
        self.height = kwargs.get('height', cnv.height)
        self.width = kwargs.get('width', cnv.width)
        self.size = kwargs.get('size', cnv.size)  # for equal height/width
        self.x = kwargs.get('x', kwargs.get('left', cnv.x))
        self.y = kwargs.get('y', kwargs.get('bottom', cnv.y))
        self.cx = kwargs.get('cx', cnv.cx)
        self.cy = kwargs.get('cy', cnv.cy)
        # repeats
        self.offset = kwargs.get('offset', cnv.offset)
        self.offset_across = kwargs.get('offset_down', cnv.offset_down)
        self.offset_down = kwargs.get('offset_across', cnv.offset_across)
        self.gap = kwargs.get('gap', cnv.gap)
        self.gap_across = kwargs.get('gap_down', cnv.gap_down)
        self.gap_down = kwargs.get('gap_across', cnv.gap_across)
        # rotate in degrees
        self.rotate = kwargs.get('rotate', kwargs.get('rotation', cnv.rotate))
        self._rotate_theta = self.rotate * math.pi / 180.0  # radians
        self.orientation = kwargs.get('orientation', cnv.orientation)
        self.position = kwargs.get('position', cnv.position)
        # line
        self.line_width = kwargs.get('line_width', cnv.line_width)
        self.line_dots = kwargs.get('line_dots',
                                    kwargs.get('dots', cnv.line_dots))
        self.line_dashes = kwargs.get('line_dashes',
                                      kwargs.get('dashes', cnv.line_dashes))
        self.line_dotdash = kwargs.get('line_dotdash',
                                       kwargs.get('dotdash', cnv.line_dotdash))
        # text
        self.align = kwargs.get('align', cnv.align)  # left, right, justify
        self._alignment = TA_LEFT  # see to_alignment()
        self.font_face = kwargs.get('font_face', cnv.font_face)
        self.font_size = kwargs.get('font_size', cnv.font_size)
        self.label_size = kwargs.get('label_size', cnv.label_size)
        self.title_size = kwargs.get('title_size', cnv.title_size)
        self.heading_size = kwargs.get('heading_size', cnv.heading_size)
        self.text = kwargs.get('text', cnv.text)
        self.label = kwargs.get('label', cnv.label)
        self.title = kwargs.get('title', cnv.title)
        self.heading = kwargs.get('heading', cnv.heading)
        self.style = kwargs.get('style', cnv.style)  # Normal? from reportlab
        self.wrap = kwargs.get('wrap', cnv.wrap)
        # text block
        self.outline_color = kwargs.get('outline_color', cnv.outline_color)
        self.outline_width = kwargs.get('outline_width', cnv.outline_width)
        self.leading = kwargs.get('leading', cnv.leading)
        # color and fill
        self.fill = kwargs.get('fill', kwargs.get('fill_color', cnv.fill))
        self.pattern = kwargs.get('pattern', cnv.pattern)
        self.repeat = kwargs.get('repeat', cnv.repeat)
        # lines
        self.stroke = kwargs.get('stroke', kwargs.get('stroke_color',
                                                      cnv.stroke))
        self.stroke_width = kwargs.get('stroke_width', cnv.stroke_width)
        self.stroke_text = kwargs.get('stroke_text', cnv.stroke_text)
        self.stroke_label = kwargs.get('stroke_label', cnv.stroke_label)
        self.stroke_title = kwargs.get('stroke_title', cnv.stroke_title)
        self.stroke_heading = kwargs.get('stroke_heading', cnv.stroke_heading)
        # line and fill
        self.transparent = kwargs.get('transparent', cnv.transparent)
        # image / file
        self.source = kwargs.get('source', cnv.source)  # file or http://
        # line / ellipse / bezier
        self.length = kwargs.get('length', cnv.length)
        self.angle = kwargs.get('angle', cnv.angle)  # anti-clock from flat
        self._angle_theta = self.angle * math.pi / 180.0  # radians
        self.x_1 = kwargs.get('x1', cnv.x_1)
        self.y_1 = kwargs.get('y1', cnv.y_1)
        # bezier
        self.x_2 = kwargs.get('x2', cnv.x_2)
        self.y_2 = kwargs.get('y2', cnv.y_2)
        self.x_3 = kwargs.get('x3', cnv.x_3)
        self.y_3 = kwargs.get('y3', cnv.y_3)
        # rect / card
        self.rounding = kwargs.get('rounding', cnv.rounding)
        self.rounded = kwargs.get('rounded', cnv.rounded)
        # grid / card layout
        self.rows = kwargs.get('rows', cnv.rows)
        self.cols = kwargs.get('cols', kwargs.get('columns', cnv.cols))
        # circle / star / poly
        self.radius = kwargs.get('radius', cnv.radius)
        self.vertices = kwargs.get('vertices', cnv.vertices)
        self.sides = kwargs.get('sides', cnv.sides)
        self.points = kwargs.get('points', cnv.points)
        # hexes
        self.side = kwargs.get('side', cnv.side)  # length of sides
        self.dot_color = kwargs.get('dot_color', cnv.dot_color)
        self.dot_size = kwargs.get('dot_size', cnv.dot_size)
        self.hid = kwargs.get('id', cnv.hid)  # HEX ID
        # CHECK
        correct, issue = self.check_settings()
        if not correct:
            tools.feedback(f"Problem with settings: {issue}.")
        # UPDATE SELF WITH COMMON
        if self.common:
            attrs = vars(self.common)
            for attr in attrs.keys():
                if attr not in ['canvas', 'common', 'stylesheet'] and \
                        attr[0] != '_':
                    common_attr = getattr(self.common, attr)
                    base_attr = getattr(BaseCanvas(), attr)
                    if common_attr != base_attr:
                        setattr(self, attr, common_attr)

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

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an element on a given canvas."""
        raise NotImplementedError

    def set_canvas_props(self, cnv=None, fill=None,
                         stroke=None, stroke_width=None):
        """Set reportlab canvas properties for font and colors"""
        canvas = cnv if cnv else self.canvas.canvas
        log.debug('scp: %s %s', self.font_face, self.font_size)
        log.debug('scp: stroke %s / self.stroke %s', stroke, self.stroke)
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
            canvas.setFillColor(fill or self.fill)
        except AttributeError:
            pass
        try:
            canvas.setStrokeColor(stroke or self.stroke)
        except AttributeError:
            pass
        try:
            canvas.setLineWidth(stroke_width or self.stroke_width)
        except AttributeError:
            pass
        if self.line_dashes:
            canvas.setDash(array=[6, 2])
        if self.line_dots:
            canvas.setDash(array=[1, 1])
        if self.line_dotdash:
            canvas.setDash(array=self.line_dotdash)

    def check_settings(self):
        """Check that the user-supplied parameters are correct"""
        correct = True
        issue = []
        if self.position:
            if str(self.position).lower() not in \
                    ['top', 'bottom', 'center', 'middle']:
                issue.append('Invalid position!')
                correct = False
        if self.align:
            if str(self.align).lower() not in \
                    ['left', 'right', 'justify', 'centre']:
                issue.append('Invalid align!')
                correct = False
        if self.orientation:
            if str(self.orientation).lower() not in \
                    ['vertical', 'horizontal']:
                issue.append('Invalid orientation!')
                correct = False
        return correct, issue

    def to_alignment(self):
        """Convert local, English-friendly alignments to reportlab enums."""
        if self.align == 'centre':
            self._alignment = TA_CENTER
        elif self.align == 'right':
            self._alignment = TA_RIGHT
        elif self.align == 'justify':
            self._alignment = TA_JUSTIFY
        else:
            self._alignment = TA_LEFT
        return self._alignment

    def load_image(self, source=None):
        """Load an image from file or website.

        If source not found; try path in which script located"""
        img = None
        if source:
            try:
                img = ImageReader(source)
                return img
            except IOError:
                filepath = tools.script_path()
                _source = os.path.join(filepath, source)
                try:
                    img = ImageReader(_source)
                    return img
                except IOError:
                    tools.feedback(
                        f'Unable to find or open image "{_source}"; including {filepath}.')
        return img

    def process_template(self, _dict):
        """Set values for properties based on those defined in a dictionary."""
        if _dict.get('x'):
            self.x = _dict.get('x', 1)
        if _dict.get('y'):
            self.y = _dict.get('x', 1)
        if _dict.get('height'):
            self.height = _dict.get('height', 1)
        if _dict.get('width'):
            self.width = _dict.get('width', 1)
        if _dict.get('radius'):
            self.radius = _dict.get('radius', 1)
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

    def textify(self, index=None, text=None):
        """Extract text from a list, or create string, based on index & type"""
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

    def draw_multi_string(self, canvas, x, y, string, align=None):
        """Draw a string, split if needed, with a given alignment."""
        if not string:
            return
        align = align or self.align
        mvy = copy.copy(y)
        log.debug("string %s %s", type(string), string)
        for ln in string.split('\n'):
            if align == 'centre':
                canvas.drawCentredString(x, mvy, ln)
            elif align == 'right':
                canvas.drawRightString(x, mvy, ln)
            else:
                canvas.drawString(x, mvy, ln)
            mvy -= canvas._leading

    def draw_label(self, canvas, x, y, string, align=None):
        """Draw a multi-string on the canvas"""
        self.draw_multi_string(canvas=canvas, x=x, y=y, string=string, align=align)

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
        tools.feedback(f'TO DO! {args}')


class GroupBase(list):
    """Class for group base."""

    def __init__(self, *args):
        list.__init__(self, *args)
