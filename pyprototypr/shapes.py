# -*- coding: utf-8 -*-
"""
Create custom shapes for pyprototypr
"""
# lib
import copy
import logging
import math
import random

# third party
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import (
    A6, A5, A4, A3, A2, A1, A0, LETTER, LEGAL, ELEVENSEVENTEEN,
    letter, legal, elevenSeventeen, B6, B5, B4, B3, B2, B0, landscape)

# local
from pyprototypr.utils.geoms import (
    Point, Link, Location, TrackPoint)  # named tuples
from pyprototypr.utils import geoms, tools
from pyprototypr.base import (
    BaseShape, BaseCanvas, GridShape, UNITS, COLORS, PAGES, DEBUG_COLOR)

log = logging.getLogger(__name__)

DEBUG = False
GRID_SHAPES_WITH_CENTRE = [
    'CircleShape', 'CompassShape', 'DotShape', 'HexShape', 'OctagonShape',
    'RectangleShape', 'RhombusShape', 'SquareShape', 'StadiumShape', ] # EllipseShape ???
GRID_SHAPES_NO_CENTRE = [
     'TextShape', 'StarShape', ]
# NOT GRID:  ArcShape, BezierShape, PolylineShape, ChordShape


# ---- Functions =====

class Value:
    """
    Class wrapper for a list of values possible for a card attribute.
    """

    def __init__(self, **kwargs):
        self.datalist = kwargs.get("datalist", [])
        self.members = []  # card IDs, of which affected card is a member

    def __call__(self, cid):
        """Return datalist item number 'ID' (card number)."""
        log.debug("datalist:%s cid:%s", self.datalist, cid)
        try:
            x = self.datalist[cid]
            return x
        except (ValueError, TypeError, IndexError):
            return None


class Query:
    """
    Query to select an element or a value for a card attribute.
    """

    def __init__(self, **kwargs):
        self.query = kwargs.get("query", [])
        self.result = kwargs.get("result", None)
        self.alternate = kwargs.get("alternate", None)
        self.members = []  # card IDs, of which affected card is a member

    def __call__(self, cid):
        """Process the query, for a given card 'ID' in the dataset."""
        result = None
        results = []
        for _query in self.query:
            log.debug("_query %s %s", len(_query), _query)
            if _query and len(_query) >= 4:
                result = tools.comparer(
                    val=_query[0][cid], operator=_query[1], target=_query[2]
                )
            results.append(result)
            results.append(_query[3])
        # compare across all
        result = tools.boolean_join(results)
        log.debug("cid %s Results %s", cid, results)
        if result is not None:
            if result:
                return self.result
            else:
                return self.alternate
        else:
            tools.feedback(f'Query "{self.query}" is incorrectly constructed.')

# ---- Core Shapes =====


class ImageShape(BaseShape):
    """
    Image (bitmap or SVG) on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Show an image on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        img = None
        # ---- check for usage via Card ID
        # tools.feedback(f'*** {ID=} {self.source=}')
        if ID is not None and isinstance(self.source, list):
            _source = self.source[ID]
        else:
            _source = self.source
        if not _source:
            return
        # ---- convert to using units
        height = self._u.height
        width = self._u.width
        if self.cx and self.cy and width and height:
            x = self._u.cx - width / 2.0 + self._o.delta_x
            y = self._u.cy - height / 2.0 + self._o.delta_y
        elif self.cx and self.cy and not (width or height):
            tools.feedback(
                "Must supply width and height for use with cx and cy.", stop=True
            )
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        # ---- draw image
        # tools.feedback(f'*** IMAGE {ID=} {_source=} {x=} {y=} {self.scaling=} ')
        img, is_svg = self.load_image(_source, self.scaling)
        if not img:
            tools.feedback("Unable to load that image!", True)
        rotate = kwargs.get('rotate', self.rotate)
        # assumes 1 pt == 1 pixel ?
        # ---- handle rotation
        if rotate:
            # tools.feedback(f'*** IMAGE {ID=} {rotate=} {self._u.x=}, {self._u.y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                dx, dy = self._u.margin_left, self._u.margin_bottom
                cnv.translate(x + dx, y + dy)
            else:
                cnv.translate(x + self._o.delta_x, y + self._o.delta_y)
            cnv.rotate(rotate)
            # draw the image relative to the origin
            if is_svg:
                from reportlab.graphics import renderPDF
                renderPDF.draw(img, cnv, x=-width / 2.0, y=-height / 2.0)
            else:
                cnv.drawImage(
                    img,
                    x=-width / 2.0,
                    y=-height / 2.0,
                    width=width,
                    height=height,
                    mask="auto")
            cnv.restoreState()
        else:
            if is_svg:
                from reportlab.graphics import renderPDF
                renderPDF.draw(img, cnv, x=x, y=y)
            else:
                cnv.drawImage(img, x=x, y=y, width=width, height=height, mask="auto")
        # ---- text
        xc = x + width / 2.0
        if self.heading:
            cnv.setFont(self.font_face, self.heading_size)
            cnv.setFillColor(self.heading_stroke)
            self.draw_multi_string(cnv, xc, y + height + cnv._leading, self.heading)
        if self.label:
            cnv.setFont(self.font_face, self.label_size)
            cnv.setFillColor(self.label_stroke)
            self.draw_multi_string(cnv, xc, y + height / 2.0, self.label)
        if self.title:
            cnv.setFont(self.font_face, self.title_size)
            cnv.setFillColor(self.title_stroke)
            self.draw_multi_string(cnv, xc, y - cnv._leading, self.title)


class DotShape(BaseShape):
    """
    Dot of fixed radius on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a dot on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # tools.feedback(f"Dot {self._o.delta_x=} {self._o.delta_y=}")
        cnv = cnv.canvas if cnv else self.canvas.canvas
        if self.use_abs_c:
            x = self._abs_cx
            y = self._abs_cy
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        size = self.dot_point / 2.0  # diameter is 3 points ~ 1mm or 1/32"
        self.fill = self.stroke
        self.set_canvas_props(index=ID)
        # ---- draw dot
        # tools.feedback(f'*** Dot {size=} {x=} {y=}')
        cnv.circle(x, y, size, stroke=0, fill=1 if self.fill else 0)
        # ---- text
        self.draw_heading(cnv, ID, x, y, **kwargs)
        self.draw_label(cnv, ID, x, y, **kwargs)
        self.draw_title(cnv, ID, x, y, **kwargs)


class LineShape(BaseShape):
    """
    Line on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a line on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        if self.use_abs:
            x = self._abs_x
            y = self._abs_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        if self.use_abs_1:
            x_1 = self._abs_x1
            y_1 = self._abs_y1
        elif self.x_1 or self.y_1:
            x_1 = self.unit(self.x_1) + self._o.delta_x
            y_1 = self.unit(self.y_1) + self._o.delta_y
        else:
            if self.angle > 0:
                angle = math.radians(self.angle)
                x_1 = x + (self._u.length * math.cos(angle))
                y_1 = y + (self._u.length * math.sin(angle))
            else:
                x_1 = x + self._u.length
                y_1 = y
        if self.row is not None and self.row >= 0:
            y = y + self.row * self._u.height
            y_1 = y_1 + self.row * self._u.height  # - self._u.margin_bottom
        if self.col is not None and self.col >= 0:
            x = x + self.col * self._u.width
            x_1 = x_1 + self.col * self._u.width  # - self._u.margin_left
        # tools.feedback(f"{x=} {x_1=} {y=} {y_1=}")
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw line
        pth = cnv.beginPath()
        pth.moveTo(x, y)
        pth.lineTo(x_1, y_1)
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        # ---- calculate line rotation
        compass, rotate = geoms.angles_from_points(x, y, x_1, y_1)
        # ---- dot
        self.draw_dot(cnv, (x_1 + x) / 2.0, (y_1 + y) / 2.0)
        # ---- text
        self.draw_label(
            cnv, ID, (x_1 + x) / 2.0, (y_1 + y) / 2.0, rotate=rotate, centred=False, **kwargs)


class ChordShape(BaseShape):
    """
    Chord line on a Circle on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a chord on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        if not isinstance(self.shape, CircleShape):
            tools.feedback('Shape must be a circle!', True)
        circle = self.shape
        x_c, y_c = circle.calculate_centre()
        centre = Point(circle.cx, circle.cy)
        pt0 = geoms.point_on_circle(centre, circle.radius, self.angle)
        pt1 = geoms.point_on_circle(centre, circle.radius, self.angle_1)
        # tools.feedback(f"*** {circle.radius=} {pt0=} {pt1=}")
        x = self.unit(pt0.x) + self._o.delta_x
        y = self.unit(pt0.y) + self._o.delta_y
        x_1 = self.unit(pt1.x) + self._o.delta_x
        y_1 = self.unit(pt1.y) + self._o.delta_y
        # tools.feedback(f"*** {x=} {x_1=} {y=} {y_1=}")
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw line
        pth = cnv.beginPath()
        pth.moveTo(x, y)
        pth.lineTo(x_1, y_1)
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        # ---- calculate line rotation
        compass, rotate = geoms.angles_from_points(x, y, x_1, y_1)
        # tools.feedback(f"*** {compass=} {rotate=}")
        # ---- dot
        self.draw_dot(cnv, (x_1 + x) / 2.0, (y_1 + y) / 2.0)
        # ---- text
        self.draw_label(
            cnv, ID, (x_1 + x) / 2.0, (y_1 + y) / 2.0, rotate=rotate, centred=False, **kwargs)


class ArrowShape(BaseShape):
    """
    Arrow on a given canvas.
    """

    def arrow_head(self):
        """Draw head of arrow."""

    def arrow_tail(self):
        """Draw head of arrow."""

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an arrow on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        if self.use_abs:
            x = self._abs_x
            y = self._abs_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        if self.use_abs_1:
            x_1 = self._abs_x1
            y_1 = self._abs_y1
        elif self.x_1 or self.y_1:
            x_1 = self.unit(self.x_1) + self._o.delta_x
            y_1 = self.unit(self.y_1) + self._o.delta_y
        else:
            if self.angle > 0:
                angle = math.radians(self.angle)
                x_1 = x + (self._u.length * math.cos(angle))
                y_1 = y + (self._u.length * math.sin(angle))
            else:
                x_1 = x + self._u.length
                y_1 = y
        if self.row is not None and self.row >= 0:
            y = y + self.row * self._u.height
            y_1 = y_1 + self.row * self._u.height - self._u.margin_bottom
        if self.col is not None and self.col >= 0:
            x = x + self.col * self._u.width
            x_1 = x_1 + self.col * self._u.width - self._u.margin_left
        log.debug("x:%s x1:%s y:%s y1:%s", x, x_1, y, y_1)
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw arrow
        log.debug("angle:%s length:%s x:%s y:%s x_1:%s y_1:%s",
                  self.angle, self._u.length, x, y, x_1, y_1)
        pth = cnv.beginPath()
        pth.moveTo(x, y)
        pth.lineTo(x_1, y_1)
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        # ---- head
        self.arrow_head()
        # ---- tail
        self.arrow_tail()
        # ---- calculate line rotation
        compass, rotate = geoms.angles_from_points(x, y, x_1, y_1)
        # ---- dot
        self.draw_dot(cnv, (x_1 + x) / 2.0, (y_1 + y) / 2.0)
        # ---- text
        self.draw_label(
            cnv, ID, (x_1 + x) / 2.0, (y_1 + y) / 2.0, rotate=rotate, centred=False, **kwargs)


class RhombusShape(BaseShape):
    """
    Rhombus on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a rhombus (diamond) on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        if self.use_abs_c:
            x = self._abs_cx
            y = self._abs_cy
        elif self.cx and self.cy:
            x = self._u.cx - self._u.width / 2.0 + self._o.delta_x
            y = self._u.cy - self._u.height / 2.0 + self._o.delta_y
        elif self.use_abs:
            x = self._abs_x
            y = self._abs_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- calculated properties
        self.area = (self._u.width * self._u.height) / 2.0
        # ---- draw rhombus
        x_s, y_s = x, y + self._u.height / 2.0
        pth = cnv.beginPath()
        pth.moveTo(x_s, y_s)
        pth.lineTo(x_s + self._u.width / 2.0, y_s + self._u.height / 2.0)
        pth.lineTo(x_s + self._u.width, y_s)
        pth.lineTo(x_s + self._u.width / 2.0, y_s - self._u.height / 2.0)
        pth.lineTo(x_s, y_s)
        pth.close()
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        # ---- dot
        self.draw_dot(cnv, x + self._u.width / 2.0, y + self._u.height / 2.0)
        # ---- text
        self.draw_heading(cnv, ID, x + self._u.width / 2.0, y + self._u.height, **kwargs)
        self.draw_label(cnv, ID, x + self._u.width / 2.0, y + self._u.height / 2.0, **kwargs)
        self.draw_title(cnv, ID, x + self._u.width / 2.0, y - self._u.height, **kwargs)


class StadiumShape(BaseShape):
    """
    Stadium ("pill") on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(StadiumShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides to centre shape
        if self.cx and self.cy:
            self.x = self.cx - self.width / 2.0
            self.y = self.cy - self.height / 2.0
            # tools.feedback(f"INIT Old x:{x} Old y:{y} New X:{self.x} New Y:{self.y}")
        self.kwargs = kwargs

    def __str__(self):
        return f'{self.__class__.__name__}::{self.kwargs}'

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a stadium on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- adjust start
        if self.row is not None and self.col is not None:
            x = self.col * self._u.width + self._o.delta_x
            y = self.row * self._u.height + self._o.delta_y
        elif self.cx and self.cy:
            x = self._u.cx - self._u.width / 2.0 + self._o.delta_x
            y = self._u.cy - self._u.height / 2.0 + self._o.delta_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        # ---- overrides to centre the shape
        if self.use_abs_c:
            x = self._abs_cx
            y = self._abs_cy
        elif kwargs.get("cx") and kwargs.get("cy"):
            x = self._u.cx - self._u.width / 2.0
            y = self._u.cy - self._u.height / 2.0
        # ---- vertices
        self.vertices = [  # clockwise from bottom-left; relative to centre
            Point(x, y),
            Point(x, y + self._u.height),
            Point(x + self._u.width, y + self._u.height),
            Point(x + self._u.width, y),
        ]
        # tools.feedback(f'*** {len(self.vertices)=}')
        # ---- edges
        _edges = []
        if self.edges:
            if not isinstance(self.edges, list):
                __edges = self.edges.split()
            else:
                __edges = self.edges
            _edges = [edge.lower() for edge in __edges]
            # reverse order of vertices because curves are drawn anti-clockwise
            self.vertices = list(reversed(self.vertices))
            self.vertices.append(self.vertices[0])
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw rect fill only
        pth = cnv.beginPath()
        pth.moveTo(*self.vertices[0])
        for vertex in self.vertices:
            pth.lineTo(*vertex)
        pth.close()
        cnv.drawPath(pth, stroke=0, fill=1 if self.fill else 0)

        # ---- draw stadium
        pth = cnv.beginPath()
        pth.moveTo(*self.vertices[0])
        radius_lr = self._u.height / 2.0
        radius_tb = self._u.width / 2.0
        for count, vertex in enumerate(self.vertices):
            # draw half-circle at chosen stadium self.edges;
            # using Bezier, cannot get half-circle - need to use two quarter circles

            # vx, vy = self.points_to_value(vertex.x) - 1, self.points_to_value(vertex.y) - 1
            # tools.feedback(f'*** {count=} vx={vx:.2f} vy={vy:.2f}')
            if count == 2 and ('l' in _edges or 'left' in _edges):
                cx, cy = vertex.x, vertex.y - 0.5 * self._u.height
                # _cx, _cy = self.points_to_value(cx) - 1, self.points_to_value(cy) - 1
                # tools.feedback(f'***  cx={_cx:.2f} cy={_cy:.2f}')
                top_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_lr, radius_lr, 90, 180)
                bottom_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_lr, radius_lr, 180, 270)
                pth.moveTo(*vertex)
                pth.curveTo(*top_curve[1])
                pth.curveTo(*bottom_curve[1])
            elif count == 1 and ('t' in _edges or 'top' in _edges):
                cx, cy = vertex.x - 0.5 * self._u.width, vertex.y
                right_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_tb, radius_tb, 0, 90)
                left_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_tb, radius_tb, 90, 180)
                pth.moveTo(*vertex)
                pth.curveTo(*right_curve[1])
                pth.curveTo(*left_curve[1])
            elif count == 3 and ('b' in _edges or 'bottom' in _edges):
                cx, cy = vertex.x + 0.5 * self._u.width, vertex.y
                left_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_tb, radius_tb, 180, 270)
                right_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_tb, radius_tb, 270, 360)
                pth.moveTo(*vertex)
                pth.curveTo(*left_curve[1])
                pth.curveTo(*right_curve[1])
                pth.moveTo(*self.vertices[3])
            elif count == 0 and ('r' in _edges or 'right' in _edges):
                cx, cy = vertex.x, vertex.y + 0.5 * self._u.height
                bottom_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_lr, radius_lr, 270, 360)
                top_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_lr, radius_lr, 0, 90)
                pth.moveTo(*vertex)
                pth.curveTo(*bottom_curve[1])
                pth.curveTo(*top_curve[1])
            # no curve; use a regular line
            else:
                if count + 1 < len(self.vertices):
                    pth.lineTo(*self.vertices[count + 1])
        # pth.close()
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        # ---- cross
        self.draw_cross(cnv,  x + self._u.width / 2.0, y + self._u.height / 2.0)
        # ---- dot
        self.draw_dot(cnv, x + self._u.width / 2.0, y + self._u.height / 2.0)
        # ---- text
        self.draw_heading(cnv, ID, x + self._u.width / 2.0, y + self._u.height, **kwargs)
        self.draw_label(cnv, ID, x + self._u.width / 2.0, y + self._u.height / 2.0, **kwargs)
        self.draw_title(cnv, ID, x + self._u.width / 2.0, y, **kwargs)


class RectangleShape(BaseShape):
    """
    Rectangle on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(RectangleShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides to centre shape
        if self.cx and self.cy:
            self.x = self.cx - self.width / 2.0
            self.y = self.cy - self.height / 2.0
            # tools.feedback(f"INIT Old x:{x} Old y:{y} New X:{self.x} New Y:{self.y}")
        self.kwargs = kwargs

    def __str__(self):
        return f'{self.__class__.__name__}::{self.kwargs}'

    def calculate_area(self):
        return self._u.width * self._u.height

    def calculate_perimeter(self, units=False):
        """Total length of bounding perimeter."""
        length = 2.0 * (self._u.width + self._u.height)
        if units:
            return self.points_to_value(length)
        else:
            return length

    def set_vertices(self, rotate=0, **kwargs):
        """Set vertices for rectangle without hatches."""
        if rotate:
            kwargs['rotate'] = rotate
        x, y = self.calculate_xy(**kwargs)
        return [  # clockwise from bottom-left; relative to centre
            Point(x, y),
            Point(x, y + self._u.height),
            Point(x + self._u.width, y + self._u.height),
            Point(x + self._u.width, y),
        ]

    def set_coord(self, cnv, x_d, y_d):
        """Set (optionally draw) the coords of the rectangle."""
        the_row = self.row or 0
        the_col = self.col or 0
        #_row = self.rows - the_row + self.coord_start_y
        _row = the_row + 1 if not self.coord_start_y else the_row + self.coord_start_y
        _col = the_col + 1 if not self.coord_start_x else the_col + self.coord_start_x
        # tools.feedback(f'*** # ---- {_row=},{_col=}')
        # ---- set coord x,y values
        if self.coord_type_x in ['l', 'lower']:
            _x = tools.sheet_column(_col, True)
        elif self.coord_type_x in ['l-m', 'lower-multiple']:
            _x = tools.alpha_column(_col, True)
        elif self.coord_type_x in ['u', 'upper']:
            _x = tools.sheet_column(_col)
        elif self.coord_type_x in ['u-m', 'upper-multiple']:
            _x = tools.alpha_column(_col)
        else:
            _x = str(_col).zfill(self.coord_padding)  # numeric
        if self.coord_type_y in ['l', 'lower']:
            _y = tools.sheet_column(_row, True)
        elif self.coord_type_y in ['l-m', 'lower-multiple']:
            _y = tools.alpha_column(_row, True)
        elif self.coord_type_y in ['u', 'upper']:
            _y = tools.sheet_column(_row)
        elif self.coord_type_y in ['u-m', 'upper-multiple']:
            _y = tools.alpha_column(_row)
        else:
            _y = str(_row).zfill(self.coord_padding)  # numeric
        # ---- set coord label
        self.coord_text = str(self.coord_prefix) + _x + str(self.coord_separator) + _y
        # ---- draw coord (optional)
        if self.coord_position:
            # ---- * set coord props
            cnv.setFont(self.coord_font_face, self.coord_font_size)
            cnv.setFillColor(self.coord_stroke)
            coord_offset = self.unit(self.coord_offset)
            if self.coord_position in ['t', 'top']:
                self.draw_multi_string(
                    cnv, x_d, y_d + coord_offset, self.coord_text)
            elif self.coord_position in ['m', 'middle', 'mid']:
                self.draw_multi_string(
                    cnv, x_d, y_d + coord_offset - self.coord_font_size / 2.0, self.coord_text)
            elif self.coord_position in ['b', 'bottom', 'bot']:
                self.draw_multi_string(
                    cnv, x_d, y_d + coord_offset, self.coord_text)
            else:
                tools.feedback(
                    f'Cannot handle a coord_position of "{self.coord_position}"')


    def calculate_xy(self, **kwargs):
        # ---- adjust start
        if self.row is not None and self.col is not None:
            x = self.col * self._u.width + self._o.delta_x
            y = self.row * self._u.height + self._o.delta_y
        elif self.cx and self.cy:
            x = self._u.cx - self._u.width / 2.0 + self._o.delta_x
            y = self._u.cy - self._u.height / 2.0 + self._o.delta_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        # ---- overrides to centre the shape
        if kwargs.get("cx") and kwargs.get("cy"):
            x = kwargs.get("cx") - self._u.width / 2.0
            y = kwargs.get("cy") - self._u.height / 2.0
        # ---- overrides for centering
        rotate = kwargs.get('rotate', None)
        if rotate:
            x = -self._u.width / 2.0
            y = -self._u.height / 2.0
        return x, y

    def draw_hatch(self, cnv, ID, vertices: list, num: int):
        if self.rounding or self.rounded:
            tools.feedback('No hatching permissible with a rounded Rectangle', True)
        if self.notch or self.notch_x or self.notch_y:
            tools.feedback('No hatching permissible with a notched Rectangle', True)
        self.set_canvas_props(
            index=ID,
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_width,
            stroke_cap=self.hatch_cap)
        _dirs = self.hatch_directions.lower().split()
        if num >= 1:
            # breakpoint()
            if 'ne' in _dirs or 'sw' in _dirs:  # slope UP to the right
                pth = cnv.beginPath()
                pth.moveTo(vertices[0].x, vertices[0].y)
                pth.lineTo(vertices[2].x, vertices[2].y)
                cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
            if 'se' in _dirs or 'nw' in _dirs:  # slope down to the right
                pth = cnv.beginPath()
                pth.moveTo(vertices[1].x, vertices[1].y)
                pth.lineTo(vertices[3].x, vertices[3].y)
                cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
            if 'n' in _dirs or 's' in _dirs:  # vertical
                x_dist = self._u.width / (num + 1)
                for i in range(1, num + 1):
                    pth = cnv.beginPath()
                    pth.moveTo(vertices[0].x + i * x_dist, vertices[1].y)
                    pth.lineTo(vertices[0].x + i * x_dist, vertices[0].y)
                    cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
            if 'e' in _dirs or 'w' in _dirs:  # horizontal
                y_dist = self._u.height / (num + 1)
                for i in range(1, num + 1):
                    pth = cnv.beginPath()
                    pth.moveTo(vertices[0].x, vertices[0].y + i * y_dist)
                    pth.lineTo(vertices[0].x + self._u.width, vertices[0].y + i * y_dist)
                    cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        if num >= 1:
            diag_num = int((num - 1) / 2 + 1)
            x_dist = self._u.width / diag_num
            y_dist = self._u.height / diag_num
            top_pt, btm_pt, left_pt, rite_pt = [], [], [], []
            for number in range(0, diag_num + 1):
                left_pt.append(
                    geoms.point_on_line(vertices[0], vertices[1], y_dist * number))
                top_pt.append(
                    geoms.point_on_line(vertices[1], vertices[2], x_dist * number))
                rite_pt.append(
                    geoms.point_on_line(vertices[3], vertices[2], y_dist * number))
                btm_pt.append(
                    geoms.point_on_line(vertices[0], vertices[3], x_dist * number))

        if 'ne' in _dirs or 'sw' in _dirs:  # slope UP to the right
            for i in range(1, diag_num):  # top-left side
                j = diag_num - i
                pth = cnv.beginPath()
                pth.moveTo(left_pt[i].x, left_pt[i].y)
                pth.lineTo(top_pt[j].x, top_pt[j].y)
                cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
            for i in range(1, diag_num):  # bottom-right side
                j = diag_num - i
                pth = cnv.beginPath()
                pth.moveTo(btm_pt[i].x, btm_pt[i].y)
                pth.lineTo(rite_pt[j].x, rite_pt[j].y)
                cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        if 'se' in _dirs or 'nw' in _dirs:  # slope down to the right
            for i in range(1, diag_num):  # bottom-left side
                pth = cnv.beginPath()
                pth.moveTo(left_pt[i].x, left_pt[i].y)
                pth.lineTo(btm_pt[i].x, btm_pt[i].y)
                cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
            for i in range(1, diag_num):  # top-right side
                pth = cnv.beginPath()
                pth.moveTo(top_pt[i].x, top_pt[i].y)
                pth.lineTo(rite_pt[i].x, rite_pt[i].y)
                cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a rectangle on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # ---- check properties
        is_notched = True if (self.notch or self.notch_x or self.notch_y) else False
        is_chevron = True if (self.chevron or self.chevron_height) else False
        if (self.rounding or self.rounded) and is_notched:
            tools.feedback("Cannot use rounding or rounded with notch.", True)
        if (self.rounding or self.rounded) and is_chevron:
            tools.feedback("Cannot use rounding or rounded with chevron.", True)
        if self.hatch and is_notched:
            tools.feedback("Cannot use hatch with notch.", True)
        if self.hatch and is_chevron:
            tools.feedback("Cannot use hatch with chevron.", True)
        if is_notched and is_chevron:
            tools.feedback("Cannot use notch and chevron together.", True)
        # ---- calculated properties
        x, y = self.calculate_xy()
        # ---- overrides for grid
        if self.use_abs_c:
            x = self._abs_cx - self._u.width / 2.0
            y = self._abs_cy - self._u.height / 2.0
        x_d = x + self._u.width / 2.0  # centre
        y_d = y + self._u.height / 2.0  # centre
        self.area = self.calculate_area()
        delta_m_up, delta_m_down = 0.0, 0.0  # potential text offset from chevron

        # ---- handle rotation: START
        rotate = kwargs.get('rotate', self.rotate)
        if rotate:
            # tools.feedback(f'*** Rect {ID=} {rotate=} {self._u.x=}, {self._u.y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                cnv.translate(x + self._u.margin_left, y + self._u.margin_bottom)
            else:
                cnv.translate(x + self._u.width / 2.0, y + self._u.height / 2.0)
            cnv.rotate(rotate)
            # reset centre and "bottom left"
            x_d, y_d = 0, 0
            x = -self._u.width / 2.0
            y = -self._u.height / 2.0

        # ---- notch vertices
        if is_notched:
            if self.notch_corners:
                _ntches = self.notch_corners.split()
                _notches = [str(ntc).upper() for ntc in _ntches]
            # tools.feedback(f'*** {self.notch_x=} {self.notch_y=} {_notches=} ')
            n_x = self.unit(self.notch_x) if self.notch_x else self.unit(self.notch)
            n_y = self.unit(self.notch_y) if self.notch_y else self.unit(self.notch)
            self.vertices = []
            if 'SW' in _notches:
                self.vertices.append(Point(x, y + n_y))
            else:
                self.vertices.append(Point(x, y))
            if 'NW' in _notches:
                self.vertices.append(Point(x, y + self._u.height - n_y))
                self.vertices.append(Point(x + n_x, y + self._u.height))
            else:
                self.vertices.append(Point(x, y + self._u.height))
            if 'NE' in _notches:
                self.vertices.append(Point(x + self._u.width - n_x, y + self._u.height))
                self.vertices.append(Point(x + self._u.width, y + self._u.height - n_y))
            else:
                self.vertices.append(Point(x + self._u.width, y + self._u.height))
            if 'SE' in _notches:
                self.vertices.append(Point(x + self._u.width, y + n_y))
                self.vertices.append(Point(x + self._u.width - n_x, y))
            else:
                self.vertices.append(Point(x + self._u.width, y))
            if 'SW' in _notches:
                self.vertices.append(Point(x + n_x, y))
            else:
                self.vertices.append(Point(x, y))
        # ---- chevron vertices
        elif is_chevron:
            try:
                _chevron_height = float(self.chevron_height)
            except:
                tools.feedback(
                    f"A chevron_height of {self.chevron_height} is not valid!", True)
            if _chevron_height <= 0:
                tools.feedback(
                    "The chevron_height must be greater than zero; "
                    f"not {self.chevron_height}.", True)
            delta_m = self.unit(_chevron_height)
            if not self.chevron:
                self.chevron = 'N'
            self.vertices = []
            if self.chevron.upper() == 'N':
                delta_m_up = delta_m
                self.vertices.append(Point(x, y))
                self.vertices.append(Point(x, y + self._u.height))
                self.vertices.append(Point(x + self._u.width / 2.0, y + self._u.height + delta_m))
                self.vertices.append(Point(x + self._u.width, y + self._u.height))
                self.vertices.append(Point(x + self._u.width, y))
                self.vertices.append(Point(x + self._u.width / 2.0, y + delta_m))
            elif self.chevron.upper() == 'S':
                delta_m_down = delta_m
                self.vertices.append(Point(x, y))
                self.vertices.append(Point(x, y + self._u.height))
                self.vertices.append(Point(x + self._u.width / 2.0, y + self._u.height - delta_m))
                self.vertices.append(Point(x + self._u.width, y + self._u.height))
                self.vertices.append(Point(x + self._u.width, y))
                self.vertices.append(Point(x + self._u.width / 2.0, y - delta_m))
            elif self.chevron.upper() == 'W':
                self.vertices.append(Point(x, y))
                self.vertices.append(Point(x - delta_m, y + self._u.height / 2.0))
                self.vertices.append(Point(x, y + self._u.height))
                self.vertices.append(Point(x + self._u.width, y + self._u.height))
                self.vertices.append(Point(x  + self._u.width - delta_m, y + self._u.height / 2.0))
                self.vertices.append(Point(x + self._u.width, y))
            elif self.chevron.upper() == 'E':
                self.vertices.append(Point(x, y))
                self.vertices.append(Point(x + delta_m, y + self._u.height / 2.0))
                self.vertices.append(Point(x, y + self._u.height))
                self.vertices.append(Point(x + self._u.width, y + self._u.height))
                self.vertices.append(Point(x + self._u.width + delta_m, y + self._u.height / 2.0))
                self.vertices.append(Point(x + self._u.width, y))
            else:
                self.vertices = self.set_vertices(**kwargs)
        else:
            self.vertices = self.set_vertices(**kwargs)
        # tools.feedback(f'*** {len(self.vertices)=}')
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw rectangle
        if is_notched or is_chevron:
            pth = cnv.beginPath()
            pth.moveTo(*self.vertices[0])
            for vertex in self.vertices:
                pth.lineTo(*vertex)
            pth.close()
            cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        elif self.rounding:
            rounding = self.unit(self.rounding)
            cnv.roundRect(
                x,
                y,
                self._u.width,
                self._u.height,
                rounding,
                stroke=1,
                fill=1 if self.fill else 0,
            )
        elif self.rounded:
            _rounding = self._u.width * 0.08
            cnv.roundRect(
                x,
                y,
                self._u.width,
                self._u.height,
                _rounding,
                stroke=1,
                fill=1 if self.fill else 0,
            )
        else:
            cnv.rect(
                x,
                y,
                self._u.width,
                self._u.height,
                stroke=1,
                fill=1 if self.fill else 0,
            )
        # ---- draw hatch
        if self.hatch:
            vertices = self.set_vertices(rotate=rotate, **kwargs)
            self.draw_hatch(cnv, ID, vertices, self.hatch)
        # ---- grid marks
        self.set_canvas_props(
            index=ID,
            stroke=self.grid_color,
            stroke_width=self.grid_stroke_width)
        if self.grid_marks:
            deltag = self.unit(self.grid_length)
            pth = cnv.beginPath()
            gx, gy = 0, y  # left-side
            pth.moveTo(gx, gy)
            pth.lineTo(deltag, gy)
            pth.moveTo(0, gy + self._u.height)
            pth.lineTo(deltag, gy + self._u.height)
            gx, gy = x, self.pagesize[1]  # top-side
            pth.moveTo(gx, gy)
            pth.lineTo(gx, gy - deltag)
            pth.moveTo(gx + self._u.width, gy)
            pth.lineTo(gx + self._u.width, gy - deltag)
            gx, gy = self.pagesize[0], y  # right-side
            pth.moveTo(gx, gy)
            pth.lineTo(gx - deltag, gy)
            pth.moveTo(gx, gy + self._u.height)
            pth.lineTo(gx - deltag, gy + self._u.height)
            gx, gy = x, 0  # bottom-side
            pth.moveTo(gx, gy)
            pth.lineTo(gx, gy + deltag)
            pth.moveTo(gx + self._u.width, gy)
            pth.lineTo(gx + self._u.width, gy + deltag)
            # done
            cnv.drawPath(pth, stroke=1, fill=1)
        # ---- fill pattern?
        img, is_svg = self.load_image(self.pattern)
        if img:
            log.debug("IMG %s s%s %s", type(img._image), img._image.size)
            iwidth = img._image.size[0]
            iheight = img._image.size[1]
            # repeat?
            if self.repeat:
                cnv.drawImage(img, x=x, y=y, width=iwidth, height=iheight, mask="auto")
            else:
                # stretch
                # TODO - work out how to (a) fill and (b) cut off -- mask?
                # assume DPI = 300?  72pt = 1" = 300px -see
                # http://two.pairlist.net/pipermail/reportlab-users/2006-January/004670.html
                # w, h = yourImage.size
                # yourImage.crop((0, 30, w, h-30)).save(...)
                cnv.drawImage(
                        img,
                        x=x,
                        y=y,
                        width=self._u.width,
                        height=self._u.height,
                        mask="auto",
                    )
        # ---- cross
        self.draw_cross(cnv, x_d, y_d)
        # ---- dot
        self.draw_dot(cnv, x_d, y_d)
        # ---- text
        self.draw_heading(cnv, ID, x_d, y_d + 0.5 * self._u.height + delta_m_up, **kwargs)
        self.draw_label(cnv, ID, x_d, y_d, **kwargs)
        self.draw_title(cnv, ID, x_d, y_d - 0.5 * self._u.height - delta_m_down, **kwargs)
        # ----  numbering
        self.set_coord(cnv, x_d, y_d)
        # ***TEMP ***
        # cnv.setFont(self.font_face, 24)
        # self.draw_multi_string(cnv, x_d, y_d, self.coord_text)

        # ---- handle rotation: END
        if rotate:
            cnv.restoreState()

        # ---- return key settings
        return GridShape(label=self.coord_text, x=x_d, y=y_d, shape=self)


class SquareShape(RectangleShape):
    """
    Square on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(SquareShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides to make a "square rectangle"
        if self.width and not self.side:
            self.side = self.width
        if self.height and not self.side:
            self.side = self.height
        self.height, self.width = self.side, self.side
        self.set_unit_properties()
        self.kwargs = kwargs

    def __str__(self):
        return f'{self.__class__.__name__}::{self.kwargs}'

    def calculate_area(self):
        return self._u.width * self._u.height

    def calculate_perimeter(self, units=False):
        """Total length of bounding line."""
        length = 2.0 * (self._u.width + self._u.height)
        if units:
            return self.points_to_value(length)
        else:
            return length

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a square on a given canvas."""
        # tools.feedback(f'@Square@ {self.label=} // {off_x=}, {off_y=}')
        return super().draw(cnv, off_x, off_y, ID, **kwargs)


class OctagonShape(BaseShape):
    """
    Octagon on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(OctagonShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides to centre shape
        if self.cx and self.cy:
            self.x = self.cx - self.width / 2.0
            self.y = self.cy - self.height / 2.0
            # tools.feedback(f"INIT Old x:{x} Old y:{y} New X:{self.x} New Y:{self.y}")

    def calculate_area(self):
        side = self._u.height / (1 + math.sqrt(2.0))
        return 2 * side * side * (1 + math.sqrt(2))

    def draw_hatch(self, cnv, ID, side: float, vertices: list, num: int):
        self.set_canvas_props(
            index=ID,
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_width,
            stroke_cap=self.hatch_cap)
        _dirs = self.hatch_directions.lower().split()
        lines = int(num)
        if num >= 1:
            if 'ne' in _dirs or 'sw' in _dirs:  # slope UP to the right
                self.lines_between_sides(cnv, side, lines, vertices, (0, 1), (5, 4))
            if 'se' in _dirs or 'nw' in _dirs:  # slope down to the right
                self.lines_between_sides(cnv, side, lines, vertices, (2, 3), (7, 6))
            if 'n' in _dirs or 's' in _dirs:  # vertical
                self.lines_between_sides(cnv, side, lines, vertices, (3, 4), (0, 7))
            if 'e' in _dirs or 'w' in _dirs:  # horizontal
                self.lines_between_sides(cnv, side, lines, vertices, (1, 2), (6, 5))

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an octagon on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        if self.row is not None and self.col is not None:
            x = self.col * self._u.width + self._o.delta_x
            y = self.row * self._u.height + self._o.delta_y
            c_x, c_y = x + self._u.width / 2.0, y + self._u.height / 2.0
        elif self.cx and self.cy:
            x = self._u.cx - self._u.width / 2.0 + self._o.delta_x
            y = self._u.cy - self._u.height / 2.0 + self._o.delta_y
            c_x = self._u.cx + self._o.delta_x
            c_y = self._u.cy + self._o.delta_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
            c_x, c_y = x + self._u.width / 2.0, y + self._u.height / 2.0
        # tools.feedback(f"DRAW Old {x=} {y=} {cx=} {cy=}")
        # ---- overrides to centre the shape
        if self.use_abs_c:
            c_x = self._abs_cx
            c_y = self._abs_cy
        elif kwargs.get("cx") and kwargs.get("cy"):
            x = self.unit(kwargs.get("cx")) - self._u.width / 2.0 + self._o.delta_x
            y = self.unit(kwargs.get("cy")) + self._u.height / 2.0 + self._o.delta_y
            c_x = self.unit(kwargs.get("cx")) + self._o.delta_x
            c_y = self.unit(kwargs.get("cy")) + self._o.delta_y
        # ---- calculated properties
        side = self._u.height / (1 + math.sqrt(2.0))
        self.area = self.calculate_area()
        zzz = math.sqrt((side * side) / 2.0)
        self.vertices = [  # Points clockwise from bottom-left; relative to centre
            Point(c_x - side / 2.0, c_y - self._u.height / 2.0),  # 1
            Point(c_x - self._u.width / 2.0, c_y - self._u.height / 2.0 + zzz),  # 2
            Point(c_x - self._u.width / 2.0, c_y - self._u.height / 2.0 + zzz + side),  # 3
            Point(c_x - side / 2.0, c_y + self._u.height / 2.0),  # 4
            Point(c_x + side / 2.0, c_y + self._u.height / 2.0),  # 5
            Point(c_x + self._u.width / 2.0, c_y - self._u.height / 2.0 + zzz + side),  # 6
            Point(c_x + self._u.width / 2.0, c_y - self._u.height / 2.0 + zzz),  # 7
            Point(c_x + side / 2.0, c_y - self._u.height / 2.0),  # 8
        ]
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw octagon
        pth = cnv.beginPath()
        pth.moveTo(*self.vertices[0])
        for vertex in self.vertices:
            pth.lineTo(vertex.x, vertex.y)
        pth.close()
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        cx = x + self._u.width / 2.0
        cy = y + self._u.height / 2.0
        # ---- debug
        self.debug(cnv, vertices=self.vertices)
        # ---- draw hatch
        if self.hatch:
            self.draw_hatch(cnv, ID, side, self.vertices, self.hatch)
        # ---- cross
        self.draw_cross(cnv, cx, cy)
        # ---- dot
        self.draw_dot(cnv, cx, cy)
        # ---- text
        self.draw_heading(cnv, ID, cx, cy + 0.5 * self._u.height, **kwargs)
        self.draw_label(cnv, ID,cx, cy, **kwargs)
        self.draw_title(cnv, ID, cx, cy - 0.5 * self._u.height, **kwargs)


class ShapeShape(BaseShape):
    """
    Irregular polygon, based on a set of points, on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(ShapeShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides
        self.x = kwargs.get("x", kwargs.get("left", 0))
        self.y = kwargs.get("y", kwargs.get("bottom", 0))

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an irregular polygon on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw Shape
        if isinstance(self.points, str):
            # SPLIT STRING e.g. "1,2  3,4  4.5,8.8"
            _points = self.points.split(" ")
            points = [_point.split(",") for _point in _points]
        else:
            points = self.points
        if points and len(points) > 0:
            pth = cnv.beginPath()
            for key, vertex in enumerate(points):
                _x0, _y0 = float(vertex[0]), float(vertex[1])
                # convert to using units
                x = self.unit(_x0) + self._o.delta_x
                y = self.unit(_y0) + self._o.delta_y
                if key == 0:
                    pth.moveTo(x, y)
                pth.lineTo(x, y)
            pth.close()
            cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)


class ArcShape(BaseShape):
    """
    Arc on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw arc on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # tools.feedback(f'*** ARC {self.x=} {self.y=} {self.x_1=} {self.y_1=} {self.angle_width=} ')
        # convert to using units
        x_1 = self._u.x + self._o.delta_x
        y_1 = self._u.y + self._o.delta_y
        if not self.x_1:
            self.x_1 = self.x + self.default_length
        if not self.y_1:
            self.y_1 = self.y + self.default_length
        x_2 = self.unit(self.x_1) + self._o.delta_x
        y_2 = self.unit(self.y_1) + self._o.delta_y
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw arc
        # tools.feedback(f'*** Arc: {x_1=}, {y_1=}, {x_2=}, {y_2=}')
        cnv.arc(x_1, y_1, x_2, y_2, startAng=self.angle, extent=self.angle_width) # anti-clock from flat; 90°


class BezierShape(BaseShape):
    """
    Bezier curve on a given canvas.

    A Bezier curve is specified by four control points:
        (x1,y1), (x2,y2), (x3,y3), (x4,y4).
    The curve starts at (x1,y1) and ends at (x4,y4) with a line segment
    from (x1,y1) to (x2,y2) and a line segment from (x3,y3) to (x4,y4)
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw Bezier curve on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # convert to using units
        x_1 = self._u.x + self._o.delta_x
        y_1 = self._u.y + self._o.delta_y
        if not self.x_1:
            self.x_1 = self.x + self.default_length
        if not self.y_1:
            self.y1 = self.y + self.default_length
        x_2 = self.unit(self.x_1) + self._o.delta_x
        y_2 = self.unit(self.y_1) + self._o.delta_y
        x_3 = self.unit(self.x_2) + self._o.delta_x
        y_3 = self.unit(self.y_2) + self._o.delta_y
        x_4 = self.unit(self.x_3) + self._o.delta_x
        y_4 = self.unit(self.y_3) + self._o.delta_y
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw bezier
        cnv.bezier(x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4)


class SectorShape(BaseShape):
    """
    Sector on a given canvas. Aka "wedge". Aka "slice" or "pie slice".

    Note:
        * User supplies a "compass" angle i.e. degrees clockwise from North - but this
          must be converted to a "reportlab" angle i.e. degrees anti-clockwise from East
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(SectorShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # ---- perform overrides
        self.radius = self.radius or self.diameter / 2.0
        if self.cx is None and self.x is None:
            tools.feedback('Either provide x or cx for Sector', True)
        if self.cy is None and self.y is None:
            tools.feedback('Either provide y or cy for Sector', True)
        if self.cx and self.cy:
            self.x = self.cx - self.radius
            self.y = self.cy - self.radius
            self.x_1 = self.cx + self.radius
            self.y_1 = self.cy + self.radius
            # tools.feedback(f'*** {self.x=} {self.y=} {self.x1=} {self.y1=}')
        else:
            self.x_1 = self.x + 2.0 * self.radius
            self.y_1 = self.y + 2.0 * self.radius
        # ---- calculate centre
        radius = self._u.radius
        if self.row is not None and self.col is not None:
            self.x_c = self.col * 2.0 * radius + radius
            self.y_c = self.row * 2.0 * radius + radius
            # log.debug(f"{self.col=}, {self.row=}, {self.x_c=}, {self.y_c=}")
        elif self.cx and self.cy:
            self.x_c = self._u.cx
            self.y_c = self._u.cy
        else:
            self.x_c = self._u.x + radius
            self.y_c = self._u.y + radius

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw sector on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        if self.use_abs_c:
            self.x_c = self._abs_cx
            self.y_c = self._abs_cy
        # convert to using units
        x_1 = self.unit(self.x) + self._o.delta_x
        y_1 = self.unit(self.y) + self._o.delta_y
        x_2 = self.unit(self.x_1) + self._o.delta_x
        y_2 = self.unit(self.y_1) + self._o.delta_y
        # angles
        start = (450 - self.angle) % 360.0 - self.angle_width
        width = self.angle_width
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw sector
        cnv.wedge(
            x_1, y_1, x_2, y_2, start, width, stroke=1, fill=1 if self.fill else 0)


class PolygonShape(BaseShape):
    """
    Regular polygon on a given canvas.
    """

    def get_radius(self):
        if self.radius:
            radius = self._u.radius
        else:
            side = self._u.side
            sides = int(self.sides)
            # 180 degrees is math.pi radians
            radius = side / (2.0 * math.sin(math.pi / sides))
        return radius

    def calculate_area(self):
        sides = int(self.sides)
        radius = self.get_radius()
        area = (sides * radius * radius / 2.0) * math.sin(2.0 * math.pi / sides)
        return area

    def get_vertices(self):
        """Calculate centre, radius and vertices of polygon.
        """
        # convert to using units
        x = self._u.x + self._o.delta_x
        y = self._u.y + self._o.delta_y
        # calc - assumes x and y are the centre
        radius = self.get_radius()
        vertices = geoms.polygon_vertices(self.sides, radius, self.rotate, Point(x, y))
        return x, y, radius, vertices

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a regular polygon on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        x, y, radius, vertices = self.get_vertices()
        if not vertices or len(vertices) == 0:
            return
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw polygon
        pth = cnv.beginPath()
        pth.moveTo(*vertices[0])
        for vertex in vertices:
            pth.lineTo(vertex.x, vertex.y)
        pth.close()
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        # ---- dot
        self.draw_dot(cnv, x, y)
        # ---- text
        self.draw_heading(cnv, ID, x, y, 1.3 * radius, **kwargs)
        self.draw_label(cnv, ID, x, y, **kwargs)
        self.draw_title(cnv, ID, x, y, 1.4 * radius, **kwargs)


class PolylineShape(BaseShape):
    """
    Multi-part line on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a polyline on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        points = tools.tuple_split(self.points)
        if not points:
            points = self.points
        if not points or len(points) == 0:
            tools.feedback("No Polyline points to draw - or points are incorrect!")
            return
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw polyline
        pth = cnv.beginPath()
        for key, vertex in enumerate(points):
            x, y = vertex
            # convert to using units
            x = self.unit(x) + self._o.delta_x
            y = self.unit(y) + self._o.delta_y
            if key == 0:
                pth.moveTo(x, y)
            pth.lineTo(x, y)
        cnv.drawPath(pth, stroke=1, fill=0)


class HexShape(BaseShape):
    """
    Hexagon on a given canvas.

    See: http://powerfield-software.com/?p=851
    """

    def calculate_caltrops(self, side, size=None, fraction=None, invert=False):
        """Calculate settings for caltrops (the hex "corner").

        Note: `side` must be in unconverted (user) form e.g. cm or inches
        """
        # tools.feedback(f'*** {side=} {size=} {fraction=}')
        array = []
        match size:
            case "large" | "l":
                part = side / 3.0
                array = [part, part, part]
            case "medium" | "m":
                part = side / 5.0
                array = [part, part * 3.0, part]
            case "small" | "s":
                part = side / 7.0
                array = [part, part * 5.0, part]
            case _:
                pass
        if fraction:
            try:
                float(fraction)
            except Exception:
                tools.feedback(f'Cannot use "{fraction}" for a caltrops fraction', True)
            fraction = min(fraction, 0.5)  # caltrops might meet in the middle
            if fraction < 1.0:
                part = fraction * side
                middle = (1.0 - 2.0 * fraction) * side
                array = [part, middle, part]
        array.insert(0, 0) if invert else array.append(0)
        # convert to points!
        points = self.values_to_points(array)
        return points

    def set_coord(self, cnv, x_d, y_d, half_flat):
        """Set and draw the coords of the hexagon."""
        the_row = self.row or 0
        the_col = self.col or 0
        _row = self.hex_rows - the_row + self.coord_start_y
        _col = the_col + 1 if not self.coord_start_x else the_col + self.coord_start_x
        # ---- set coord label value
        if self.coord_style:
            if str(self.coord_style).lower() in ['d', 'diagonal']:
                col_group = (_col - 1) // 2
                _row += col_group
        # ---- set coord x,y values
        if self.coord_type_x in ['l', 'lower']:
            _x = tools.sheet_column(_col, True)
        elif self.coord_type_x in ['l-m', 'lower-multiple']:
            _x = tools.alpha_column(_col, True)
        elif self.coord_type_x in ['u', 'upper']:
            _x = tools.sheet_column(_col)
        elif self.coord_type_x in ['u-m', 'upper-multiple']:
            _x = tools.alpha_column(_col)
        else:
            _x = str(_col).zfill(self.coord_padding)  # numeric
        if self.coord_type_y in ['l', 'lower']:
            _y = tools.sheet_column(_row, True)
        elif self.coord_type_y in ['l-m', 'lower-multiple']:
            _y = tools.alpha_column(_row, True)
        elif self.coord_type_y in ['u', 'upper']:
            _y = tools.sheet_column(_row)
        elif self.coord_type_y in ['u-m', 'upper-multiple']:
            _y = tools.alpha_column(_row)
        else:
            _y = str(_row).zfill(self.coord_padding)  # numeric
        # ---- set coord label
        self.coord_text = str(self.coord_prefix) + _x + str(self.coord_separator) + _y
        # ---- draw coord (optional)
        if self.coord_position:
            # ---- * set coord props
            cnv.setFont(self.coord_font_face, self.coord_font_size)
            cnv.setFillColor(self.coord_stroke)

            coord_offset = self.unit(self.coord_offset)
            if self.coord_position in ['t', 'top']:
                self.draw_multi_string(
                    cnv, x_d, y_d + half_flat * 0.7 + coord_offset, self.coord_text)
            elif self.coord_position in ['m', 'middle', 'mid']:
                self.draw_multi_string(
                    cnv, x_d, y_d + coord_offset - self.coord_font_size / 2.0, self.coord_text)
            elif self.coord_position in ['b', 'bottom', 'bot']:
                self.draw_multi_string(
                    cnv, x_d, y_d - half_flat * 0.9 + coord_offset, self.coord_text)
            else:
                tools.feedback(
                    f'Cannot handle a coord_position of "{self.coord_position}"')

    def calculate_area(self):
        if self.side:
            side = self._u.side
        elif self.height:
            side = self._u.height / math.sqrt(3)
        return (3.0 * math.sqrt(3.0) * side * side) / 2.0

    def draw_links(self, cnv, side: float, vertices: list, links: list):
        """Draw arcs or lines to link two sides of a hexagon."""
        self.set_canvas_props(
            index=ID,
            stroke=self.link_stroke,
            stroke_width=self.link_width,
            stroke_cap=self.link_cap)
        _links = links.split(",")
        for _link in _links:
            parts = _link.split()
            try:
                the_link = Link(
                    a=int(parts[0]),
                    b=int(parts[1]),
                    style=parts[2] if len(parts) > 2 else None)
                # tools.feedback(f'*** {the_link=}')
            except TypeError:
                tools.feedback(
                    f'Cannot use {parts[0]} and/or {parts[1]} as hex side numbers.',
                    True)

            va_start = the_link.a - 1
            va_end = the_link.a % 6
            vb_start = the_link.b - 1
            vb_end = the_link.b % 6
            tools.feedback(f'a:{va_start}-{va_end} b:{vb_start}-{vb_end}')

            separation = geoms.separation_between_hexsides(the_link.a, the_link.b)
            match separation:
                case 0:
                    pass  # no line
                case 1:  # adjacent; small arc
                    if va_start in [5, 0] and vb_start in [4, 5]:
                        lower_corner = Point(vertices[vb_end].x - side / 2.0,
                                             vertices[vb_end].y - side / 2.0)
                        top_corner = Point(vertices[vb_end].x + side / 2.0,
                                           vertices[vb_end].y + side / 2.0)
                        cnv.arc(
                            lower_corner.x, lower_corner.y,
                            top_corner.x, top_corner.y,
                            startAng=0,
                            extent=120)  # anti-clockwise from "east"

                    if va_start in [0, 5] and vb_start in [0, 1]:
                        lower_corner = Point(vertices[vb_end].x - side / 2.0,
                                             vertices[vb_end].y - side / 2.0)
                        top_corner = Point(vertices[vb_end].x + side / 2.0,
                                           vertices[vb_end].y + side / 2.0)
                        cnv.arc(
                            lower_corner.x, lower_corner.y,
                            top_corner.x, top_corner.y,
                            startAng=-60,
                            extent=120)  # anti-clockwise from "east"

                    # tools.feedback(
                    #     f'arc *** x_1={lower_corner.x}, y_1={lower_corner.y}'
                    #     f' x_2={top_corner.x}, y_2={top_corner.y}')

                case 2:  # non-adjacent; large arc
                    pass
                case 3:  # opposite sides; straight line
                    a_mid = geoms.point_on_line(
                        vertices[va_start], vertices[va_end], side / 2.0)
                    b_mid = geoms.point_on_line(
                        vertices[vb_start], vertices[vb_end], side / 2.0)
                    pth = cnv.beginPath()
                    pth.moveTo(*a_mid)
                    pth.lineTo(*b_mid)
                    cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
                case _:
                    raise NotImplementedError(
                        f'Unable to handle hex "{separation=}"')

    def draw_hatch(self, cnv, ID, side: float, vertices: list, num: int):

        self.set_canvas_props(
            index=ID,
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_width,
            stroke_cap=self.hatch_cap)
        _dirs = self.hatch_directions.lower().split()
        lines = int((num - 1) / 2 + 1)

        if num >= 1:
            # tools.feedback(f'*** {vertices=} {num=} {_dirs=}')
            if self.hex_top in ['p', 'pointy']:
                if 'ne' in _dirs or 'sw' in _dirs:  # slope UP to the right
                    self.make_path_vertices(cnv, vertices, 0, 3)
                if 'se' in _dirs or 'nw' in _dirs:  # slope down to the right
                    self.make_path_vertices(cnv, vertices, 1, 4)
                if 'n' in _dirs or 's' in _dirs:  # vertical
                    self.make_path_vertices(cnv, vertices, 2, 5)
            if self.hex_top in ['f', 'flat']:
                if 'ne' in _dirs or 'sw' in _dirs:  # slope UP to the right
                    self.make_path_vertices(cnv, vertices, 2, 5)
                if 'se' in _dirs or 'nw' in _dirs:  # slope down to the right
                    self.make_path_vertices(cnv, vertices, 1, 4)
                if 'e' in _dirs or 'w' in _dirs:  # horizontal
                    self.make_path_vertices(cnv, vertices, 0, 3)
        if num >= 3:
            if self.hex_top in ['p', 'pointy']:
                if 'ne' in _dirs or 'sw' in _dirs:  # slope UP to the right
                    self.lines_between_sides(cnv, side, lines, vertices, (2, 3), (1, 0))
                    self.lines_between_sides(cnv, side, lines, vertices, (3, 4), (0, 5))
                if 'se' in _dirs or 'nw' in _dirs:  # slope down to the right
                    self.lines_between_sides(cnv, side, lines, vertices, (0, 1), (5, 4))
                    self.lines_between_sides(cnv, side, lines, vertices, (1, 2), (4, 3))
                if 'n' in _dirs or 's' in _dirs:  # vertical
                    self.lines_between_sides(cnv, side, lines, vertices, (1, 2), (0, 5))
                    self.lines_between_sides(cnv, side, lines, vertices, (2, 3), (5, 4))
            if self.hex_top in ['f', 'flat']:
                if 'ne' in _dirs or 'sw' in _dirs:  # slope UP to the right
                    self.lines_between_sides(cnv, side, lines, vertices, (2, 1), (5, 0))
                    self.lines_between_sides(cnv, side, lines, vertices, (2, 3), (5, 4))
                if 'se' in _dirs or 'nw' in _dirs:  # slope down to the right
                    self.lines_between_sides(cnv, side, lines, vertices, (4, 5), (1, 0))
                    self.lines_between_sides(cnv, side, lines, vertices, (1, 2), (4, 3))
                if 'e' in _dirs or 'w' in _dirs:  # horizontal
                    self.lines_between_sides(cnv, side, lines, vertices, (0, 1), (3, 2))
                    self.lines_between_sides(cnv, side, lines, vertices, (0, 5), (3, 4))

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a hexagon on a given canvas."""
        # if self.height < 2.2: breakpoint()
        # print(kwargs, ID, self.height)
        # tools.feedback(f'*** draw hexshape: {kwargs} {off_x} {off_y} {ID}')
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        is_cards = kwargs.get("is_cards", False)
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # ---- calculate half_flat & half_side
        if self.side:
            side = self._u.side
            half_flat = self._u.side * math.sqrt(3) / 2.0
        elif self.height:
            self.side = self.height / math.sqrt(3)
            side = self._u.height / math.sqrt(3)
            half_flat = self._u.height / 2.0
        elif self.diameter:
            self.side = self.diameter / 2.0
            side = self._u.diameter / 2.0
            half_flat = self._u.side * math.sqrt(3) / 2.0
        else:
            tools.feedback(
                'No value for side or height or diameter supplied for hexagon.',
                True)
        half_side = side / 2.0
        height_flat = 2 * half_flat
        diameter = 2.0 * side
        z_fraction = (diameter - side) / 2.0

        # ---- POINTY^
        if self.hex_top.lower() in ['p', 'pointy']:
            #          .
            #         / \`
            # x,y .. |  |
            #        \ /
            #         .
            # x and y are at the bottom-left corner of the box around the hex
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
            # ---- ^ draw pointy by row/col
            if self.row is not None and self.col is not None and is_cards:
                x = self.col * height_flat + self._o.delta_x
                y = self.row * diameter + self._o.delta_x
            elif self.row is not None and self.col is not None:
                if self.hex_offset in ['o', 'O', 'odd']:
                    # TODO => calculate!
                    # downshift applies from first even row - NOT the very first one!
                    downshift = diameter - z_fraction if self.row >=1 else 0
                    downshift = downshift * self.row if self.row >=2 else downshift
                    y = self.row * (diameter + side) - downshift + self._u.y + self._o.delta_y
                    if (self.row + 1) & 1:  # is odd row; row are 0-base numbered!
                        x = self.col * height_flat + half_flat + self._u.x + self._o.delta_x
                    else:  # even row
                        x = self.col * height_flat  + self._u.x + self._o.delta_x
                else:  # self.hex_offset in ['e', 'E', 'even']
                    # downshift applies from first even row - NOT the very first one!
                    downshift = diameter - z_fraction if self.row >=1 else 0
                    downshift = downshift * self.row if self.row >=2 else downshift
                    y = self.row * (diameter + side) - downshift + self._u.y + self._o.delta_y
                    if (self.row + 1) & 1:  # is odd row; row are 0-base numbered!
                        x = self.col * height_flat + self._u.x + self._o.delta_x
                    else:  # even row
                        x = self.col * height_flat + half_flat + self._u.x + self._o.delta_x
            # ----  ^ set hex centre relative to x,y
            x_d = x + half_flat
            y_d = y + side
            # ---- ^ recalculate hex centre
            if self.use_abs_c:
                # create x_d, y_d as the unit-formatted hex centre
                x_d = self._abs_cx
                y_d = self._abs_cy
                # recalculate start x,y
                x = x_d - half_flat
                y = y_d - half_side - side / 2.0
            elif self.cx and self.cy:
                # cx,cy are centre; create x_d, y_d as the unit-formatted hex centre
                x_d = self._u.cx + self._o.delta_y
                y_d = self._u.cy + self._o.delta_x
                # recalculate start x,y
                x = x_d - half_flat
                y = y_d - half_side - side / 2.0
            # tools.feedback(f"***P^: {x=} {y=} {x_d=} {y_d=} {half_flat=} {side=}")

        # ---- FLAT~
        else:
            #         __
            # x,y .. /  \
            #        \__/
            #
            # x and y are at the bottom-left corner of the box around the hex
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
            # tools.feedback(f"{x=} {y=} {half_flat=} {side=} {self.row=} {self.col=}")
            # ---- ~ draw flat by row/col
            if self.row is not None and self.col is not None and is_cards:
                x = self.col * 2.0 * side + self._o.delta_x
                y = half_flat + self.row * 2.0 * half_flat + self._o.delta_x
            elif self.row is not None and self.col is not None:
                if self.hex_offset in ['o', 'O', 'odd']:
                    x = self.col * (half_side + side) + self._u.x + self._o.delta_x
                    y = self.row * half_flat * 2.0 + self._u.y + self._o.delta_y
                    if (self.col + 1) & 1:  # is odd
                        y = y + half_flat
                else:  # self.hex_offset in ['e', 'E', 'even']
                    x = self.col * (half_side + side) + self._u.x + self._o.delta_x
                    y = self.row * half_flat * 2.0 + self._u.y + self._o.delta_y
                    if (self.col + 1) & 1:  # is odd
                        pass
                    else:
                        y = y + half_flat
            # ----  ~ set hex centre relative to x,y
            x_d = x + side
            y_d = y + half_flat
            # ----  ~ recalculate centre if preset
            if self.use_abs_c:
                # create x_d, y_d as the unit-formatted hex centre
                x_d = self._abs_cx
                y_d = self._abs_cy
                # recalculate start x,y
                x = x_d - half_side - side / 2.0
                y = y_d - half_flat
            elif self.cx and self.cy:
                # cx,cy are centre; create x_d, y_d as the unit-formatted hex centre
                x_d = self._u.cx + self._o.delta_x
                y_d = self._u.cy + self._o.delta_y
                # recalculate start x,y
                x = x_d - half_side - side / 2.0
                y = y_d - half_flat
            # tools.feedback(f"***F~: {x=} {y=} {x_d=} {y_d=} {half_flat=} {side=}")

        # ---- calculate area
        self.area = self.calculate_area()
        # ---- canvas
        self.set_canvas_props(index=ID)
        if self.caltrops or self.caltrops_fraction:
            line_dashes = self.calculate_caltrops(
                self.side, self.caltrops, self.caltrops_fraction, self.caltrops_invert)
            cnv.setDash(array=line_dashes)
        # ---- calculate vertical hexagon (clockwise)
        if self.hex_top.lower() in ['p', 'pointy']:
            self.vertices = [  # clockwise from bottom-left; relative to centre
                Point(x, y + z_fraction),
                Point(x, y + z_fraction + side),
                Point(x + half_flat, y + diameter),
                Point(x + height_flat, y + z_fraction + side),
                Point(x + height_flat, y + z_fraction),
                Point(x + half_flat, y),
            ]
        # ---- calculate horizontal hexagon (clockwise)
        else:   # self.hex_top.lower() in ['f',  'flat']:
            self.vertices = [  # clockwise from left; relative to centre
                Point(x, y + half_flat),
                Point(x + z_fraction, y + height_flat),
                Point(x + z_fraction + side, y + height_flat),
                Point(x + diameter, y + half_flat),
                Point(x + z_fraction + side, y),
                Point(x + z_fraction, y),
            ]

        # ---- draw hexagon
        # tools.feedback(f'*** {x=} {y=} {self.vertices=}')
        pth = cnv.beginPath()
        pth.moveTo(*self.vertices[0])
        for vertex in self.vertices:
            # TODO - set side-specific line color/style here
            pth.lineTo(*vertex)
        pth.close()
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        # ---- debug
        # self.debug_point(cnv, Point(x, y), 'start')
        # self.debug_point(cnv, Point(x_d, y_d), 'centre')
        self.debug(cnv, vertices=self.vertices)
        # ---- draw hatch
        if self.hatch:
            if not self.hatch & 1:
                tools.feedback('Hatch must be an odd number for a Hexagon', True)
            self.draw_hatch(cnv, ID, side, self.vertices, self.hatch)
        # ---- draw links
        if self.links:
            self.draw_links(cnv, side, self.vertices, self.links)
        # ---- centred shape (with offset)
        if self.centre_shape:
            cshape_name = self.centre_shape.__class__.__name__
            if cshape_name in GRID_SHAPES_WITH_CENTRE:
                # tools.feedback(f'*** IN-HEX {cshape_name} at ({x_d=},{y_d=}, '
                #               f'{self.centre_shape_x}, {self.centre_shape_y})')
                self.centre_shape.draw(
                    _abs_cx=x_d + self.unit(self.centre_shape_x),
                    _abs_cy=y_d + self.unit(self.centre_shape_y))
            elif cshape_name not in GRID_SHAPES_WITH_CENTRE:
                tools.feedback(f'Cannot draw a centered {cshape_name}!')
        # ---- cross
        self.draw_cross(cnv, x_d, y_d)
        # ---- dot
        self.draw_dot(cnv, x_d, y_d)
        # ---- text
        if self.hex_top.lower() in ['p', 'pointy']:
            offset = side  # == radius
        else:
            offset = half_flat
        self.draw_heading(cnv, ID, x_d, y_d + offset, **kwargs)
        self.draw_label(cnv, ID, x_d, y_d, **kwargs)
        self.draw_title(cnv, ID, x_d, y_d - offset, **kwargs)
        # ----  numbering
        self.set_coord(cnv, x_d, y_d, half_flat)
        # ---- return key settings
        return GridShape(label=self.coord_text, x=x_d, y=y_d, shape=self)


class StarShape(BaseShape):
    """
    Star on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a star on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # convert to using units
        x = self._u.x + self._o.delta_x
        y = self._u.y + self._o.delta_y
        # ---- overrides to centre the shape
        if self.use_abs_c:
            x = self._abs_cx
            y = self._abs_cy
        elif self.cx and self.cy:
            x = self._u.cx + self._o.delta_x
            y = self._u.cy + self._o.delta_y
        # calc - assumes x and y are the centre!
        radius = self._u.radius
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw star
        pth = cnv.beginPath()
        pth.moveTo(x, y + radius)
        angle = (2 * math.pi) * 2.0 / 5.0
        start_angle = math.pi / 2.0
        log.debug("Start self.vertices:%s", self.vertices)
        for vertex in range(self.vertices - 1):
            next_angle = angle * (vertex + 1) + start_angle
            x_1 = x + radius * math.cos(next_angle)
            y_1 = y + radius * math.sin(next_angle)
            pth.lineTo(x_1, y_1)
        pth.close()
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        # ---- dot
        self.draw_dot(cnv, x, y)
        # ---- text
        self.draw_heading(cnv, ID, x,  y + radius, **kwargs)
        self.draw_label(cnv, ID, x, y, **kwargs)
        self.draw_title(cnv, ID, x, y - radius, **kwargs)


class RightAngledTriangleShape(BaseShape):
    """
    Right-angled Triangle on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # set sizes
        if self.height and not self.width:
            self._u.width = self._u.height
        if self.width and not self.height:
            self._u.height = self._u.width
        # calculate points
        x, y = self._u.x, self._u.y
        self.vertices = []
        self.vertices.append(Point(x, y))
        if not self.hand or not self.flip:
            tools.feedback(
                'Need to supply both "flip" and "hand" options! for triangle.',
                stop=True)
        hand = self.hand.lower()
        flip = self.flip.lower()
        if hand == 'left':
            x2 = x - self._u.width
        elif hand == 'right':
            x2 = x + self._u.width
        if flip == 'up':
            y2 = y + self._u.height
        elif flip == 'down':
            y2 = y - self._u.height
        self.vertices.append(Point(x2, y2))
        self.vertices.append(Point(x2, y))
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw RA triangle
        x_sum, y_sum = 0, 0
        pth = cnv.beginPath()
        for key, vertex in enumerate(self.vertices):
            # shift to relative position
            x = vertex.x + self._o.delta_x
            y = vertex.y + self._o.delta_y
            x_sum += x
            y_sum += y
            if key == 0:
                pth.moveTo(x, y)
            pth.lineTo(x, y)
        pth.close()
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        x_c, y_c = x_sum / 3.0, y_sum / 3.0  # centroid
        # ---- dot
        self.draw_dot(cnv, x_c, y_c)
        # ---- text
        self.draw_label(cnv, ID, x_c, y_c, **kwargs)


class EquilateralTriangleShape(BaseShape):

    def draw_hatch(self, cnv, ID, side: float, vertices: list, num: int):
        self.set_canvas_props(
            index=ID,
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_width,
            stroke_cap=self.hatch_cap)
        _dirs = self.hatch_directions.lower().split()
        lines = int(num) + 1
        if num >= 1:
            # v_tl, v_tr, v_bl, v_br
            if 'ne' in _dirs or 'sw' in _dirs:  # slope UP to the right
                self.lines_between_sides(
                    cnv, side, lines, vertices, (0, 1), (2, 1))
            if 'se' in _dirs or 'nw' in _dirs:  # slope down to the right
                self.lines_between_sides(
                    cnv, side, lines, vertices, (0, 2), (0, 1))
            if 'e' in _dirs or 'w' in _dirs:  # horizontal
                self.lines_between_sides(
                    cnv, side, lines, vertices, (0, 2), (1, 2))

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an equilateraltriangle on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # calculate points
        x, y = self._u.x, self._u.y
        hand = self.hand.lower() if self.hand else 'right'
        flip = self.flip.lower() if self.flip else 'up'
        angle = self.angle
        side = self._u.side if self._u.side else self._u.width
        height = 0.5 * math.sqrt(3) * side  # ½√3(a)
        # tools.feedback(f'*** {hand=} {flip=} {side=} {height=} {self.fill=} {self.stroke=}')
        self.vertices = []
        pt0 = Point(x + self._o.delta_x, y + self._o.delta_y)
        self.vertices.append(pt0)
        if hand == 'left':
            x2 = pt0.x - side
            y2 = pt0.y
            x3 = pt0.x - 0.5 * side
        elif hand == 'right':
            x2 = pt0.x + side
            y2 = pt0.y
            x3 = x2 - 0.5 * side
        if flip == 'up':
            y3 = pt0.y + height
        elif flip == 'down':
            y3 = pt0.y - height
        self.vertices.append(Point(x2, y2))
        self.vertices.append(Point(x3, y3))
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw equilateral triangle
        x_sum, y_sum = 0, 0
        pth = cnv.beginPath()
        pth.moveTo(self.vertices[0].x, self.vertices[0].y)
        for key, vertex in enumerate(self.vertices):
            pth.lineTo(vertex.x, vertex.y)
        pth.close()
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        # ---- calculate centroid
        x_c = (self.vertices[0].x + self.vertices[1].x + self.vertices[2].x) / 3.0
        y_c = (self.vertices[0].y + self.vertices[1].y + self.vertices[2].y) / 3.0
        # tools.feedback(f'*** {x_c=} {y_c=}')
        # ---- debug
        self.debug(cnv, vertices=self.vertices)
        # ---- draw hatch
        if self.hatch:
            self.draw_hatch(cnv, ID, side, self.vertices, self.hatch)
        # ---- dot
        self.draw_dot(cnv, x_c, y_c)
        # ---- text
        self.draw_heading(cnv, ID, x_c, y + height, **kwargs)
        self.draw_label(cnv, ID, x_c, y_c, **kwargs)
        self.draw_title(cnv, ID, x_c, y, **kwargs)


class TextShape(BaseShape):
    """
    Text on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(TextShape, self).__init__(_object=_object, canvas=canvas, **kwargs)

    def __call__(self, *args, **kwargs):
        """do something when I'm called"""
        log.debug("calling TextShape...")

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw text on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # ---- convert to using units
        x_t = self._u.x + self._o.delta_x
        y_t = self._u.y + self._o.delta_y
        # ---- position the shape
        if self.use_abs:
            x_t = self._abs_x
            y_t = self._abs_y
        if self.height:
            height = self._u.height
        if self.width:
            width = self._u.width
        rotate = kwargs.get('rotate', self.rotate)
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- overrides for text value
        _sequence = kwargs.get('text_sequence', '')
        # tools.feedback(f'!!! {_sequence=} {self.text=}')
        if self.text == '' or self.text is None:
            self.text = f'{_sequence}'
        _text = self.textify(ID)
        _text = _text.format(SEQUENCE=_sequence)
        # ---- text style
        if self.wrap:
            _style = ParagraphStyle(name="sc")
            _style.textColor = self.stroke
            _style.borderColor = self.outline_color
            _style.borderWidth = self.outline_width
            _style.alignment = self.to_alignment()
            _style.fontSize = self.font_size
            _style.fontName = self.font_face
            _style.leading = self.leading
            """
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Times-Roman',
            bulletFontSize=10,
            bulletIndent=0,
            backColor=None,
            borderPadding= 0,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,
            splitLongWords=1,
            """
            para = Paragraph(_text, style=_style)
            w, h = para.wrap(width, height)
            para.drawOn(cnv, x_t, y_t - h)  # start text from top of 'box'
        else:
            cnv.setFillColor(self.stroke)
            # if _text == '1':
            #     self.debug_point(cnv, Point(x_t, y_t), '    !!!')
            # tools.feedback(f"!!! {x_t=} {y_t=} {_text=} {_sequence} {rotate=}")
            self.draw_multi_string(cnv, x_t, y_t, _text, rotate=rotate)


class CircleShape(BaseShape):
    """
    Circle on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(CircleShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # ---- perform overrides
        self.radius = self.radius or self.diameter / 2.0
        if self.cx and self.cy:
            self.x = self.cx - self.radius
            self.y = self.cy - self.radius
        else:
            self.cx = self.x + self.radius
            self.cy = self.y + self.radius
        self.width = 2.0 * self.radius
        self.height = 2.0 * self.radius
        # ---- RESET UNIT PROPS (last!)
        self.set_unit_properties()

        # # ---- calculate centre
        # radius = self._u.radius
        # if self.row is not None and self.col is not None:
        #     self.x_c = self.col * 2.0 * radius + radius
        #     self.y_c = self.row * 2.0 * radius + radius
        #     # log.debug(f"{self.col=}, {self.row=}, {self.x_c=}, {self.y_c=}")
        # elif self.cx and self.cy:
        #     self.x_c = self._u.cx
        #     self.y_c = self._u.cy
        # else:
        #     self.x_c = self._u.x + self._u.radius
        #     self.y_c = self._u.y + self._u.radius

    def __str__(self):
        return f'{self.__class__.__name__}::{self.kwargs}'

    def calculate_centre(self):
        # ---- calculated centre
        if self.use_abs_c:
            self.x_c = self._abs_cx
            self.y_c = self._abs_cy
        else:
            self.x_c = self._u.cx + self._o.delta_x
            self.y_c = self._u.cy + self._o.delta_y
        return self.x_c, self.y_c

    def calculate_area(self):
        return math.pi * self._u.radius * self._u.radius

    def calculate_perimeter(self, units=False):
        """Total length of bounding line (circumference)."""
        length = math.pi * 2.0 * self._u.radius
        if units:
            return self.points_to_value(length)
        else:
            return length

    def draw_hatch(self, cnv, ID, num: int, x_c: float, y_c: float):
        """Draw hatch lines from one edge to the other.

        Args:
            num: number of lines
            x_c: x-centre of circle
            y_c: y-centre of circle
        """
        self.set_canvas_props(
            index=ID,
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_width,
            stroke_cap=self.hatch_cap)
        _dirs = self.hatch_directions.lower().split()
        lines = int(num)
        dist = (self._u.radius * 2.0) / (lines + 1)
        partial = lines // 2

        # calculate relative distances for each line - (x, y) tuples
        vertical_distances, horizontal_distances = [], []
        for line_no in range(1, partial + 1):
            if lines & 1:
                dist_h = dist * line_no
            else:
                dist_h = dist * 0.5 if line_no == 1 else dist * line_no - dist * 0.5
            dist_v = math.sqrt(self._u.radius * self._u.radius - dist_h * dist_h)
            vertical_distances.append((dist_h, dist_v))
            horizontal_distances.append((dist_v, dist_h))

        if num >= 1 and lines & 1:  # is odd - draw centre lines
            if 'e' in _dirs or 'w' in _dirs:  # horizontal
                self.make_path_points(
                    cnv,
                    Point(x_c + self._u.radius, y_c),
                    Point(x_c - self._u.radius, y_c))
            if 'n' in _dirs or 's' in _dirs:  # vertical
                self.make_path_points(
                    cnv,
                    Point(x_c, y_c + self._u.radius),
                    Point(x_c, y_c - self._u.radius))

        if num <= 1:
            return

        if 'e' in _dirs or 'w' in _dirs:  # horizontal
            for dist in horizontal_distances:
                self.make_path_points(  # "above" diameter
                    cnv,
                    Point(x_c - dist[0], y_c + dist[1]),
                    Point(x_c + dist[0], y_c + dist[1]))
                self.make_path_points(  # "below" diameter
                    cnv,
                    Point(x_c - dist[0], y_c - dist[1]),
                    Point(x_c + dist[0], y_c - dist[1]))

        if 'n' in _dirs or 's' in _dirs:  # vertical
            for dist in vertical_distances:
                self.make_path_points(  # "right" of diameter
                    cnv,
                    Point(x_c + dist[0], y_c + dist[1]),
                    Point(x_c + dist[0], y_c - dist[1]))
                self.make_path_points(  # "left" of diameter
                    cnv,
                    Point(x_c - dist[0], y_c + dist[1]),
                    Point(x_c - dist[0], y_c - dist[1]))

    def draw_radii(self, cnv, ID, x_c: float, y_c: float):
        """Draw radius lines from the centre outwards to the circumference.

        Args:
            x_c: x-centre of circle
            y_c: y-centre of circle
        """
        if self.radii:
            try:
                _radii = [float(angle) for angle in self.radii if angle >= 0 and angle <= 360]
            except:
                tools.feedback(
                    f'The radii {self.radii} are not valid - must be a list of numbers'
                    ' from 0 to 360', True)
            _radius = self.radii_length or self.radius
            rad_length = self.unit(_radius, label='radius length')
            self.set_canvas_props(
                index=ID,
                stroke=self.radii_stroke,
                stroke_width=self.radii_stroke_width,
                dashes=self.radii_dashes,
                line_dots=self.radii_line_dots)

            for rad_angle in _radii:
                # points based on length of line and an angle in degrees
                new_pt = geoms.point_on_circle(Point(x_c, y_c), rad_length, rad_angle)
                pth = cnv.beginPath()
                pth.moveTo(x_c, y_c)
                pth.lineTo(new_pt.x, new_pt.y)
                cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw circle on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # tools.feedback(f"*** Circle: {self._o.delta_x=} {self._o.delta_y=}")
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # ---- set properties
        x, y = self.calculate_centre()
        self.area = self.calculate_area()
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw circle
        # tools.feedback(f'*** Circle: {x=} {y=}')
        cnv.circle(
            x, y, self._u.radius, stroke=1, fill=1 if self.fill else 0)
        # ---- draw hatch
        if self.hatch:
            if self.rotate:
                # tools.feedback(f'*** {self.hatch=}, {self.rotate=}, {type(cnv)}')
                cnv.saveState()
                cnv.translate(self.x_c, self.y_c)
                self.draw_hatch(cnv, ID, self.hatch, 0, 0)
                cnv.rotate(self.rotate)
                cnv.restoreState()
            else:
                self.draw_hatch(cnv, ID, self.hatch, self.x_c, self.y_c)
        # ---- draw radii
        if self.radii:
            if self.rotate:
                # tools.feedback(f'*** {self.hatch=}, {self.rotate=}, {type(cnv)}')
                cnv.saveState()
                cnv.translate(self.x_c, self.y_c)
                self.draw_radii(cnv, ID, 0, 0)
                cnv.rotate(self.rotate)
                cnv.restoreState()
            else:
                self.draw_radii(cnv, ID, self.x_c, self.y_c)
        # ---- cross
        self.draw_cross(cnv, self.x_c, self.y_c)
        # ---- dot
        self.draw_dot(cnv, self.x_c, self.y_c)
        # ---- text
        self.draw_heading(cnv, ID, self.x_c, self.y_c + self._u.radius, **kwargs)
        self.draw_label(cnv, ID, self.x_c, self.y_c, **kwargs)
        self.draw_title(cnv, ID, self.x_c, self.y_c - self._u.radius, **kwargs)


class CompassShape(BaseShape):
    """
    Compass on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(CompassShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides
        self.radius = self.radius or self.diameter / 2.0
        if self.cx and self.cy:
            self.x = self.cx - self.radius
            self.y = self.cy - self.radius
            self.width = 2.0 * self.radius
            self.height = 2.0 * self.radius
        self.x_c = None
        self.y_c = None

    def circle_radius(self, cnv, angle):
        """Calc x,y on circle and draw line from centre to it."""
        x = self._u.radius * math.sin(math.radians(angle))
        y = self._u.radius * math.cos(math.radians(angle))
        pth = cnv.beginPath()
        pth.moveTo(self.x_c, self.y_c)
        pth.lineTo(x + self.x_c, y + self.y_c)
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)

    def rectangle_ranges(self, height, width):
        """Calculate angle ranges inside rectangle."""
        ranges = []
        first = math.degrees(math.atan((width / 2.0) / (height / 2.0)))
        ranges.append((0, first))
        half_second = math.degrees(math.atan((height / 2.0) / (width / 2.0)))
        second = 2 * half_second + first
        ranges.append((first, second))
        third = second + 2 * first
        ranges.append((second, third))
        fourth = third + 2 * half_second
        ranges.append((third, fourth))
        ranges.append((fourth, 360.0))
        # tools.feedback(f'*** {ranges=}')
        return ranges

    def rectangle_radius(self, cnv, ranges, angle, height, width):
        """Calc x,y on rectangle and draw line from centre to it."""
        radians = math.radians(angle)
        if angle == 0:
            radius = 0.5 * height
        elif angle == 90:
            radius = 0.5 * width
        elif angle == 180:
            radius = 0.5 * height
        elif angle == 270:
            radius = 0.5 * width
        elif angle > ranges[0][0] and angle <= ranges[0][1]:
            radius = (0.5 * height) / math.sin(radians)
        else:
            tools.feedback(f'{angle} not in range', True)

        x = radius * math.sin(radians)
        y = radius * math.cos(radians)
        pth = cnv.beginPath()
        # tools.feedback(f'*** {self.x_c=}, {self.y_c=}')
        pth.moveTo(self.x_c, self.y_c)
        pth.lineTo(x + self.x_c, y + self.y_c)
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw compass on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # convert to using units
        height = self._u.height
        width = self._u.width
        radius = self._u.radius
        # ---- overrides to centre the shape
        if self.use_abs_c:
            self.x_c = self._abs_cx
            self.y_c = self._abs_cy
        elif self.row is not None and self.col is not None:
            self.x_c = self.col * 2.0 * radius + radius + self._o.delta_x
            self.y_c = self.row * 2.0 * radius + radius + self._o.delta_y
            log.debug("row:%s col:%s x:%s y:%s", self.col, self.row, self.x_c, self.y_c)
        elif self.cx and self.cy:
            self.x_c = self._u.cx + self._o.delta_x
            self.y_c = self._u.cy + self._o.delta_y
        else:
            if self.perimeter == 'rectangle':
                self.x_c = self._u.x + width / 2.0 + self._o.delta_x
                self.y_c = self._u.y + height / 2.0 + self._o.delta_x
            else:
                self.x_c = self._u.x + self._o.delta_x + radius
                self.y_c = self._u.y + self._o.delta_y + radius
        # ---- set canvas
        self.set_canvas_props(index=ID)
        if self.perimeter == 'circle':
            cnv.circle(self.x_c, self.y_c, radius, stroke=1, fill=1 if self.fill else 0)
        # ---- get directions
        if self.directions:
            if isinstance(self.directions, str):
                _dirs = self.directions.split(' ')
                _directions = [str(_dir).lower() for _dir in _dirs]
            elif isinstance(self.directions, list):
                _directions = [str(_dir).lower() for _dir in self.directions]
            else:
                tools.feedback(
                    f'Unable to process compass directions "{self.directions}"',
                    True)
        else:
            _directions = [str(num) for num in range(0, 9)]  # ALL directions
        # ---- draw compass in circle
        if self.perimeter == 'circle' or self.perimeter == 'octagon':
            for direction in _directions:
                match direction:
                    case 'n' | '0':
                        self.circle_radius(cnv, 0)
                    case 'ne' | '1':
                        self.circle_radius(cnv, 45)
                    case 'e' | '2':
                        self.circle_radius(cnv, 90)
                    case 'se' | '3':
                        self.circle_radius(cnv, 135)
                    case 's' | '4':
                        self.circle_radius(cnv, 180)
                    case 'sw' | '5':
                        self.circle_radius(cnv, 225)
                    case 'w' | '6':
                        self.circle_radius(cnv, 270)
                    case 'nw' | '7':
                        self.circle_radius(cnv, 315)
                    case _:
                        pass
        # ---- draw compass in rect
        if self.perimeter == 'rectangle':
            ranges = self.rectangle_ranges(height, width)
            for direction in _directions:
                match direction:
                    case 'n' | '0':
                        self.rectangle_radius(cnv, ranges, 0, height, width)
                    case 'ne' | '1':
                        self.rectangle_radius(cnv, ranges, 45, height, width)
                    case 'e' | '2':
                        self.rectangle_radius(cnv, ranges, 90, height, width)
                    case 'se' | '3':
                        pass
                    case 's' | '4':
                        self.rectangle_radius(cnv, ranges, 180, height, width)
                    case 'sw' | '5':
                        pass
                    case 'w' | '6':
                        self.rectangle_radius(cnv, ranges, 270, height, width)
                    case 'nw' | '7':
                        pass
                    case _:
                        pass

        # ---- draw compass in hex
        if self.perimeter == 'hexagon':
            for direction in _directions:
                match direction:
                    case 'n' | '0':
                        self.circle_radius(cnv, 0)
                    case 'ne' | '1':
                        self.circle_radius(cnv, 60)
                    case 'e' | '2':
                        pass
                    case 'se' | '3':
                        self.circle_radius(cnv, 120)
                    case 's' | '4':
                        self.circle_radius(cnv, 180)
                    case 'sw' | '5':
                        self.circle_radius(cnv, 240)
                    case 'w' | '6':
                        pass
                    case 'nw' | '7':
                        self.circle_radius(cnv, 300)
                    case _:
                        pass

        # ---- dot
        self.draw_dot(cnv, self.x_c, self.y_c)
        # ---- text
        self.draw_heading(cnv, ID, self.x_c, self.y_c + radius, **kwargs)
        self.draw_label(cnv, ID,self.x_c, self.y_c, **kwargs)
        self.draw_title(cnv, ID, self.x_c, self.y_c - radius, **kwargs)


class EllipseShape(BaseShape):
    """
    Ellipse on a given canvas.
    """

    def calculate_area(self):
        return math.pi * self._u.height * self._u.width

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw ellipse on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # ---- create key points
        x_1 = self._u.x + self._o.delta_x
        y_1 = self._u.y + self._o.delta_y
        if not self.xe:
            self.xe = self.x + self.default_length
        if not self.ye:
            self.ye = self.y + self.default_length
        x_2 = self.unit(self.xe) + self._o.delta_x
        y_2 = self.unit(self.ye) + self._o.delta_y
        x_c = (x_2 - x_1) / 2.0 + x_1
        y_c = (y_2 - y_1) / 2.0 + y_1
        # ---- overrides to centre the shape
        if self.cx and self.cy:
            dx = self._u.cx + self._o.delta_x - x_c
            dy = self._u.cy + self._o.delta_y - y_c
            x_1 = x_1 + dx
            y_1 = y_1 + dy
            x_2 = x_2 + dx
            y_2 = y_2 + dy
        # ---- calculated properties
        self.area = self.calculate_area()
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw ellipse
        cnv.ellipse(x_1, y_1, x_2, y_2, stroke=1, fill=1 if self.fill else 0)
        x_c = (x_2 - x_1) / 2.0 + x_1
        y_c = (y_2 - y_1) / 2.0 + y_1
        # ---- dot
        self.draw_dot(cnv, x_c, y_c)
        # ---- text
        self.draw_heading(cnv, ID, x_c, y_2, **kwargs)
        self.draw_label(cnv, ID, x_c, y_c, **kwargs)
        self.draw_title(cnv, ID, x_c, y_1, **kwargs)

# ---- Grids and Patterns =====


class StarFieldShape(BaseShape):
    """
    StarField pattern on a given canvas.

    A StarField is specified by the following properties:
     * density (average number of stars per square unit; default is 10)
     * colors (list of individual star colors; default is [white])
     * enclosure (regular shape inside which it is drawn; default is a rectangle)
     * sizes (list of individual star sizes; default is [0.1])
     * star_pattern (random | cluster | )

    Ref:
        https://codeboje.de/starfields-and-galaxies-python/

    TODO:
        Implement : createElipticStarfield()
    """

    def __str__(self):
        return f'{self._kwargs}'

    def draw_star(self, cnv, position: Point):
        """Draw a single star at a Point (x,y)."""
        color = self.colors[random.randint(0, len(self.colors) - 1)]
        size = self.sizes[random.randint(0, len(self.sizes) - 1)]
        # tools.feedback(f'*** {color=} {size=} {position=}')
        cnv.setFillColor(color)
        cnv.setStrokeColor(color)
        cnv.circle(position.x, position.y, size, stroke=1, fill=1)

    def cluster_stars(self, cnv):
        tools.feedback('CLUSTER NOT IMPLEMENTED', True)
        for star in range(0, self.star_count):
            pass

    def random_stars(self, cnv):
        # tools.feedback(f'*** {self.enclosure=}')
        if isinstance(self.enclosure, CircleShape):
            x_c, y_c = self.enclosure.calculate_centre()
        if isinstance(self.enclosure, PolygonShape):
            x_c, y_c, radius, vertices = self.enclosure.get_vertices()
        stars = 0
        while stars < self.star_count:
            if isinstance(self.enclosure, RectangleShape):
                x_y = Point(
                    random.random() * self.enclosure._u.width + self._o.delta_x,
                    random.random() * self.enclosure._u.height + self._o.delta_y
                    )
            elif isinstance(self.enclosure, CircleShape):
                r_fraction = random.random() * self.enclosure._u.radius
                angle = math.radians(random.random() * 360.0)
                x = r_fraction * math.cos(angle) + x_c
                y = r_fraction * math.sin(angle) + y_c
                x_y = Point(x, y)
            elif isinstance(self.enclosure, PolygonShape):
                r_fraction = random.random() * radius
                angle = math.radians(random.random() * 360.0)
                x = r_fraction * math.cos(angle) + x_c
                y = r_fraction * math.sin(angle) + y_c
                x_y = Point(x, y)
                if not geoms.point_in_polygon(x_y, vertices):
                    continue
            else:
                tools.feedback(f'{self.enclosure} IS NOT AN IMPLEMENTED SHAPE!', True)
            self.draw_star(cnv, x_y)
            stars += 1

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw StarField pattern on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # ---- settings
        if self.enclosure is None:
            self.enclosure = RectangleShape()
        # ---- calculations
        random.seed()
        area = math.sqrt(self.enclosure.calculate_area())
        self.star_count = round(self.density * self.points_to_value(area))
        # tools.feedback(f'*** {self.star_pattern =} {self.enclosure}')
        # tools.feedback(f'*** {area=} {self.density=} {self.star_count=}')
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw starfield
        if self.star_pattern in ['r', 'random']:
            self.random_stars(cnv)
        if self.star_pattern in ['c', 'cluster']:
            self.cluster_stars(cnv)


class GridShape(BaseShape):
    """
    Grid on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a grid on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # ---- convert to using units
        x = self._u.x + self._o.delta_x
        y = self._u.y + self._o.delta_y
        height = self._u.height  # of each grid item
        width = self._u.width  # of each grid item
        if self.size:  # square grid
            size = self.unit(self.size)
            height, width = size, size
        # ---- number of blocks in grid:
        if self.rows == 0:
            self.rows = int(
                (self.page_height - self.margin_bottom - self.margin_top)
                / self.points_to_value(height))
        if self.cols == 0:
            self.cols = int(
                (self.page_width - self.margin_left - self.margin_right)
                / self.points_to_value(width))
        # tools.feedback(f'*** {self.rows=} {self.cols=}')
        y_cols, x_cols = [], []
        for y_col in range(0, self.rows + 1):
            y_cols.append(y + y_col * height)
        for x_col in range(0, self.cols + 1):
            x_cols.append(x + x_col * width)
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw grid
        cnv.grid(x_cols, y_cols)  # , stroke=1, fill=1)


class DotGridShape(BaseShape):
    """
    Dot Grid on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a dot grid on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # ---- convert to using units
        x = 0 + self.unit(self.offset_x)
        y = 0 + self.unit(self.offset_y)
        height = self._u.height  # of each grid item
        width = self._u.width  # of each grid item
        if self.size:  # square grid
            size = self.unit(self.size)
            height, width = size, size
        # ---- number of blocks in grid:
        if self.rows == 0:
            self.rows = int((
                self.page_height - self.margin_bottom - self.margin_top - self.offset_y)
                / self.points_to_value(height))
        if self.cols == 0:
            self.cols = int((
                self.page_width - self.margin_left - self.margin_right - self.offset_x)
                / self.points_to_value(width))
        # ---- set canvas
        size = self.dot_point / 2.0  # diameter is 3 points ~ 1mm or 1/32"
        self.fill = self.stroke
        self.set_canvas_props(index=ID)
        # ---- draw dot grid
        for y_col in range(0, self.rows + 1):
            for x_col in range(0, self.cols + 1):
                cnv.circle(
                    x + x_col * width,
                    y + y_col * height,
                    size,
                    stroke=0,
                    fill=1 if self.fill else 0)


class CommonShape(BaseShape):
    """
    Attributes common to, or used by, multiple shapes
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        self._kwargs = kwargs
        super(CommonShape, self).__init__(_object=_object, canvas=canvas, **kwargs)

    def __str__(self):
        return f'{self._kwargs}'

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Not applicable."""
        tools.feedback("This shape cannot be drawn.")


# ---- Deck / Card related  =====


class CardShape(BaseShape):
    """
    Card shape on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(CardShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # tools.feedback(f'*** CardShape {kwargs=}')
        self.elements = []  # container for objects which get added to the card
        self.height = kwargs.get("height", 8.8)
        self.width = kwargs.get("width", 6.3)
        self.kwargs.pop("width", None)
        self.kwargs.pop("height", None)
        self.image = kwargs.get('image', None)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an element on a given canvas."""
        raise NotImplementedError

    def draw_card(self, cnv, row, col, cid, **kwargs):
        """Draw a card on a given canvas."""
        # log.debug("Card r:%s c:%s id:%s shp:%s", row, col, cid, self.shape)
        image = kwargs.get('image', None)
        # ---- draw outline
        label = "ID:%s" % cid if self.show_id else ""
        if self.shape == "rectangle":
            outline = RectangleShape(
                label=label,
                height=self.height,
                width=self.width,
                canvas=cnv,
                col=col,
                row=row,
                **self.kwargs,
            )
            outline.draw()
        elif self.shape == "square":
            outline = SquareShape(
                label=label,
                height=self.height,
                width=self.width,
                canvas=cnv,
                col=col,
                row=row,
                **self.kwargs,
            )
            outline.draw()
        elif self.shape == "circle":
            self.height = self.radius * 2.0
            self.width = self.radius * 2.0
            self.kwargs["radius"] = self.radius
            outline = CircleShape(
                label=label, canvas=cnv, col=col, row=row, **self.kwargs
            )
            outline.draw()
        elif self.shape == "hexagon":
            self.height = self.side * math.sqrt(3.0)
            self.width = self.side * 2.0
            self.kwargs["side"] = self.side
            outline = HexShape(label=label, canvas=cnv, col=col, row=row, **self.kwargs)
            outline.draw(is_cards=True)
        else:
            tools.feedback("Unable to draw a {self.shape}-shaped card.", stop=True)
        # ---- draw card elements
        flat_elements = tools.flatten(self.elements)
        for index, flat_ele in enumerate(flat_elements):
            # ---- * replace image source placeholder
            if image and isinstance(flat_ele, ImageShape):
                # tools.feedback(f'*** {image=} {flat_ele=} {flat_ele.kwargs=}')
                if flat_ele.kwargs.get('source', '').lower() in ['*', 'all']:
                    flat_ele.source = image

            members = flat_ele.members or self.members
            try:
                # ---- * normal element
                iid = members.index(cid + 1)
                # tools.feedback(f"*** {iid=} {col=} {self.width=} / {row=} {self.height=}")
                flat_ele.draw(
                    cnv=cnv, off_x=col * self.width, off_y=row * self.height, ID=iid
                )
            except AttributeError:
                # ---- * query ... get a new element ... or not!?
                log.debug("self.shape_id:%s", self.shape_id)
                new_ele = flat_ele(cid=self.shape_id)  # uses __call__ on Query
                if new_ele:
                    flat_new_eles = tools.flatten(new_ele)
                    for flat_new_ele in flat_new_eles:
                        members = flat_new_ele.members or self.members
                        iid = members.index(cid + 1)
                        flat_new_ele.draw(
                            cnv=cnv,
                            off_x=col * self.width,
                            off_y=row * self.height,
                            ID=iid,
                        )
            except Exception as err:
                tools.feedback(f"Unable to draw card #{cid + 1}. (Error:{err})")


class DeckShape(BaseShape):
    """
    Placeholder for the deck design; list of CardShapes and Shapes.

    NOTE: draw() is called by the DeckShape
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(DeckShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # tools.feedback(f'*** DeckShape {kwargs=}')
        # ---- cards
        self.deck = []  # container for CardShape objects
        self.cards = kwargs.get("cards", 9)  # default total number of cards
        self.height = kwargs.get("height", 8.8)  # OVERWRITE
        self.width = kwargs.get("width", 6.3)  # OVERWRITE
        self.sequence = kwargs.get("sequence", [])  # e.g. "1-2" or "1-5,8,10"
        self.template = kwargs.get("template", None)
        # ---- user provided-rows and -columns
        self.card_rows = kwargs.get("rows", None)
        self.card_cols = kwargs.get("cols", kwargs.get("columns", None))
        # ---- data file
        self.data_file = kwargs.get("data", None)
        self.data_cols = kwargs.get("data_cols", None)
        self.data_rows = kwargs.get("data_rows", None)
        self.data_header = kwargs.get("data_header", True)
        # ---- images dir and filter
        self.images = kwargs.get("images", None)
        self.images_filter = kwargs.get("images_filter", None)
        self.image_list = []
        self.create(self.cards)

    def create(self, cards):
        """Create a new deck, based on number of `cards`"""
        log.debug("Cards are: %s", self.sequence)
        self.deck = []
        log.debug("Deck => %s cards with kwargs: %s", cards, self.kwargs)
        for card in range(0, cards):
            _card = CardShape(**self.kwargs)
            _card.shape_id = card
            self.deck.append(_card)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        cnv = cnv if cnv else self.canvas
        log.debug("Deck cnv:%s type:%s", type(self.canvas), type(cnv))
        # ---- handle kwargs
        images = kwargs.get('image_list', [])
        cards = kwargs.get('cards', None)
        # ---- user-defined rows and cols
        max_rows = self.card_rows
        max_cols = self.card_cols
        # ---- calculate rows/cols based on page size and margins
        if not max_rows:
            row_space = float(self.page_height) - self.margin_bottom - self.margin_top
            max_rows = int(row_space / float(self.height))
        if not max_cols:
            col_space = float(self.page_width) - self.margin_left - self.margin_right
            max_cols = int(col_space / float(self.width))
        log.debug("w:%s cs:%s mc:%s", self.page_width, col_space, max_cols)
        log.debug("h:%s rs:%s mr:%s", self.page_height, row_space, max_rows)
        row, col = 0, 0
        # ---- draw cards
        for key, card in enumerate(self.deck):
            image = images[key] if images and key <= len(images) else None
            card.draw_card(
                cnv, row=row, col=col, cid=card.shape_id, image=image)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
            if row >= max_rows:
                row, col = 0, 0
                if key + 1 != len(self.deck):
                    cnv.canvas.showPage()

    def get(self, cid):
        """Return a card based on the internal ID"""
        for card in self.deck:
            if card.shape_id == cid:
                return card
        return None

    def count(self):
        """Return number of cards in the deck"""
        return len(self.deck)

# ---- sequence


class SequenceShape(BaseShape):
    """
    Set of shapes drawn at points
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(SequenceShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self._object = _object or TextShape(_object=None, canvas=canvas, **kwargs)
        # ---- set props
        self.setting_list = []
        self.setting = kwargs.get('setting', (1, 1, 1, 'number'))
        if not isinstance(self.setting, tuple):
            tools.feedback(f"Sequence setting '{self.setting}' must be a set!", True)
        if len(self.setting) < 2:
            tools.feedback(
                f"Sequence setting '{self.setting}' must include start and end values!",
                True)
        self.set_start = self.setting[0]
        self.set_stop = self.setting[1]
        self.set_inc = self.setting[2] if len(self.setting) > 2 else 1
        if len(self.setting) > 3:
            self.set_type = self.setting[3]
        else:
            self.set_type = 'number' \
                if isinstance(self.set_start, (int, float, complex)) \
                else 'letter'
        # ---- calculate sequence values
        try:
            if self.set_type.lower() in ['n', 'number']:
                self.set_stop = self.setting[1] + 1 if self.set_inc > 0 else self.setting[1] - 1
                self.setting_iterator = range(self.set_start, self.set_stop, self.set_inc)
                self.setting_list = list(self.setting_iterator)
            elif self.set_type.lower() in ['l', 'letter']:
                self.setting_list = []
                start, stop = ord(self.set_start), ord(self.set_stop)
                curr = start
                #breakpoint()
                while True:
                    if self.set_inc > 0 and curr > stop:
                        break
                    if self.set_inc < 0 and curr < stop:
                        break
                    self.setting_list.append(chr(curr))
                    curr += self.set_inc
            else:
                tools.feedback(
                    f"'{self.set_type}' must be either number or letter!", True)
        except Exception as err:
            log.info(err)
            tools.feedback(f"Unable to evaluate Sequence setting '{self.setting}';"
                           " - please check and try again!", True)

        self.gap_x = self.gap_x or self.gap
        self.gap_y = self.gap_y or self.gap

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        log.debug("gx:%s gy:%s", self.gap_x, self.gap_y)
        # tools.feedback(f'* @Seqnc@ {self.label=} // {off_x=}, {off_y=}')
        _off_x, _off_y = off_x, off_y

        for key, item in enumerate(self.setting_list):
            _ID = ID if ID is not None else self.shape_id
            # breakpoint()
            kwargs['text_sequence'] = f'{item}'
            # tools.feedback(f'*   @Seqnc@ {self.gap_x=}, {self.gap_y=}')
            off_x = _off_x + key * self.gap_x
            off_y = _off_y + key * self.gap_y
            flat_elements = tools.flatten(self._object)
            log.debug("flat_eles:%s", flat_elements)
            for each_flat_ele in flat_elements:
                flat_ele = copy.copy(each_flat_ele)  # allow props to be reset
                log.debug("flat_ele:%s", flat_ele)
                try:  # normal element
                    flat_ele.draw(off_x=off_x, off_y=off_y, ID=_ID, **kwargs)
                except AttributeError:
                    new_ele = flat_ele(cid=_ID)
                    log.debug("%s %s", new_ele, type(new_ele))
                    if new_ele:
                        flat_new_eles = tools.flatten(new_ele)
                        log.debug("%s", flat_new_eles)
                        for flat_new_ele in flat_new_eles:
                            log.debug("%s", flat_new_ele)
                            flat_new_ele.draw(
                                off_x=off_x, off_y=off_y, ID=_ID, **kwargs
                            )


# ---- repeats =====


class RepeatShape(BaseShape):
    """
    Shape is drawn multiple times.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(RepeatShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # UPDATE SELF WITH COMMON
        if self.common:
            attrs = vars(self.common)
            for attr in list(attrs.keys()):
                if attr not in ["canvas", "common", "stylesheet"] and attr[0] != "_":
                    common_attr = getattr(self.common, attr)
                    base_attr = getattr(BaseCanvas(), attr)
                    if common_attr != base_attr:
                        setattr(self, attr, common_attr)

        self._object = _object  # incoming Shape object
        # repeat
        self.rows = kwargs.get("rows", 1)
        self.cols = kwargs.get("cols", kwargs.get("columns", 1))
        self.repeat = kwargs.get("repeat", None)
        self.offset_across = self.offset_across or self.offset
        self.offset_down = self.offset_down or self.offset
        self.gap_x = self.gap_x or self.gap
        self.gap_y = self.gap_y or self.gap
        if self.repeat:
            (
                self.repeat_across,
                self.repeat_down,
                self.gap_y,
                self.gap_x,
                self.gap_x,
                self.offset_down,
            ) = self.repeat.split(",")
        else:
            self.across = kwargs.get("across", self.cols)
            self.down = kwargs.get("down", self.rows)
            try:
                self.down = list(range(1, self.down + 1))
            except TypeError:
                pass
            try:
                self.across = list(range(1, self.across + 1))
            except TypeError:
                pass
        # self.repeat_ = kwargs.get('repeat_', None)
        # self.repeat_ = kwargs.get('repeat_', None)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        log.debug("oc:%s od:%s", self.offset_across, self.offset_down)
        log.debug("ga:%s gd:%s", self.gap_x, self.gap_y)

        for col in range(self.cols):
            for row in range(self.rows):
                if ((col + 1) in self.across) and ((row + 1) in self.down):
                    off_x = col * self.width + col * (
                        self.offset_across - self.margin_left
                    )
                    off_y = row * self.height + row * (
                        self.offset_down - self.margin_bottom
                    )
                    flat_elements = tools.flatten(self._object)
                    log.debug("flat_eles:%s", flat_elements)
                    for flat_ele in flat_elements:
                        log.debug("flat_ele:%s", flat_ele)
                        try:  # normal element
                            flat_ele.draw(off_x=off_x, off_y=off_y, ID=self.shape_id)
                        except AttributeError:
                            new_ele = flat_ele(cid=self.shape_id)
                            log.debug("%s %s", new_ele, type(new_ele))
                            if new_ele:
                                flat_new_eles = tools.flatten(new_ele)
                                log.debug("%s", flat_new_eles)
                                for flat_new_ele in flat_new_eles:
                                    log.debug("%s", flat_new_ele)
                                    flat_new_ele.draw(
                                        off_x=off_x, off_y=off_y, ID=self.shape_id
                                    )

# ---- Virtual Class


class Virtual():
    """
    Common properties and methods for all virtual shapes (grid and track)
    """
    global cnv

    def to_int(self, value, label, maximum=None, minimum=None) -> int:
        """Set a value to an int; or stop if an invalid value."""
        try:
            int_value = int(value)
            if minimum and int_value < minimum:
                tools.feedback(
                    f"{label} integer is less than the minimum of {minimum}!",
                    True)
            if maximum and int_value > maximum:
                tools.feedback(
                    f"{label} integer is more than the maximum of {maximum}!",
                    True)
            return int_value
        except Exception:
            tools.feedback(f"{value} is not a valid {label} integer!", True)

    def to_float(self, value, label) -> int:
        """Set a value to a float; or stop if an invalid value."""
        try:
            float_value = float(value)
            return float_value
        except Exception:
            tools.feedback(f"{value} is not a valid {label} floating number!", True)

# ---- Virtual Grids & Layout =====


class VirtualGrid(Virtual):
    """
    Common properties and methods to define a virtual grid.

    A virtual grid is not drawn on the canvas; rather it provides locations/points
    where a user-defined shape will be drawn.
    """
    global cnv
    global deck

    def __init__(self, rows=2, cols=2, **kwargs):
        kwargs = kwargs
        self.rows = self.to_int(rows, 'rows')
        self.cols = self.to_int(cols, 'cols')
        self.grid_size = self.rows * self.cols
        self.row_spacing = kwargs.get('y_interval', 1)
        self.col_spacing = kwargs.get('x_interval', 1)
        self.pattern = kwargs.get('pattern', 'default')
        self.direction = kwargs.get('direction', 'right')
        self.flow = None  # used for snake; see validate() for setting
        self.start = kwargs.get('start', 'bl')
        self.stop = kwargs.get('stop', 0)
        self.validate()

    def validate(self):
        """Check for validate settings and combos."""
        self.stop = self.to_int(self.stop, 'stop')
        self.rows = self.to_int(self.rows, 'rows')
        self.cols = self.to_int(self.cols, 'cols')
        self.start = str(self.start)
        self.pattern = str(self.pattern)
        self.direction = str(self.direction)
        if self.cols < 2 or self.rows < 2:
            tools.feedback(
                f"Minimum grid size is 2x2 (cannot use {self.cols }x{self.rows})!",
                True)
        if self.start.lower() not in ['bl', 'br', 'tl', 'tr']:
            tools.feedback(
                f"{self.start} is not a valid start - "
                "use 'bl', 'br', 'tl', or 'tr'", True)
        if self.pattern.lower() not in [
                'default', 'd', 'snake', 's', 'spiral', 'p', 'outer', 'o']:
            tools.feedback(
                f"{self.pattern} is not a valid pattern - "
                "use 'default', 'outer', 'snake', or 'spiral'", True)
        if self.direction.lower() not in ['up', 'u', 'down', 'd', 'left', 'l', 'right', 'r']:
            tools.feedback(
                f"{self.direction} is not a valid direction - "
                "use 'up', down', left', or 'right'", True)
        if 't' in self.start.lower() and 'u' in self.direction.lower() \
                or 'b' in self.start.lower() and 'd' in self.direction.lower() \
                or 'l' in self.start.lower() and 'l' in self.direction.lower() \
                or 'r' in self.start.lower() and 'r' in self.direction.lower():
            tools.feedback(f"Cannot use {self.start} with {self.direction}!", True)
        if self.direction.lower() in ['up', 'u', 'down', 'd']:
            self.flow = 'vert'
        elif self.direction.lower() in ['left', 'l', 'right', 'r']:
            self.flow = 'hori'
        else:
            tools.feedback(f"{self.direction} is not a valid direction!", True)

    def next_location(self) -> Location:
        """Yield next Location for each call."""
        pass


class RectangleGrid(VirtualGrid):
    """
    Common properties and methods to define a virtual rectangular grid.
    """
    global cnv
    global deck

    def next_location(self) -> Location:
        """Yield next Location for each call."""
        match self.start.lower():
            case 'bl':
                row_start = 1
                col_start = 1
            case 'br':
                row_start = 1
                col_start = self.cols
            case 'tl':
                row_start = self.rows
                col_start = 1
            case 'tr':
                row_start = self.rows
                col_start = self.cols
        col, row, count = col_start, row_start, 0
        while True:  # rows <= self.rows and col <= self.cols:
            # calculate point based on row/col
            x = col
            y = row
            count = count + 1
            # set next grid location
            match self.pattern.lower():
                # ---- snake
                case 'snake' | 'snaking' | 's':
                    # tools.feedback(f'*** {count=} {self.grid_size=} {self.stop=}')
                    if count > self.grid_size or (self.stop and count > self.stop):
                        return
                    yield Location(col, row, x, y)
                    # next grid location
                    match self.direction.lower():
                        case 'r' | 'right':
                            col = col + 1
                            if col > self.cols:
                                col = self.cols
                                if row_start == self.rows:
                                    row = row - 1
                                else:
                                    row = row + 1
                                self.direction = 'l'

                        case 'l' | 'left':
                            col = col - 1
                            if col < 1:
                                col = 1
                                if row_start == self.rows:
                                    row = row - 1
                                else:
                                    row = row + 1
                                self.direction = 'r'

                        case 'u' | 'up':
                            row = row + 1
                            if row > self.rows:
                                row = self.rows
                                if col_start == self.cols:
                                    col = col - 1
                                else:
                                    col = col + 1
                                self.direction = 'd'

                        case 'd' | 'down':
                            row = row - 1
                            if row < 1:
                                row = 1
                                if col_start == self.cols:
                                    col = col - 1
                                else:
                                    col = col + 1
                                self.direction = 'u'

                # ---- spiral
                case 'spiral' | 'p':
                    tools.feedback("Spiral grid layout not implemented yet.", True)

                # ---- outer
                case 'outer' | 'o':
                    yield Location(col, row, x, y)
                    # next grid location
                    match self.direction.lower():
                        case 'r' | 'right':
                            col = col + 1
                            if col > self.cols:
                                col = self.cols
                                if row_start == self.rows:
                                    self.direction = 'd'
                                    row = self.rows - 1
                                    if row < 1:
                                        return
                                else:
                                    self.direction = 'u'
                                    row = 2
                                    if row > self.rows:
                                        return
                        case 'l' | 'left':
                            col = col - 1
                            if col < 1:
                                col = col_start
                                if row_start == self.rows:
                                    self.direction = 'u'
                                    row = 2
                                    if row > self.rows:
                                        return
                                else:
                                    self.direction = 'd'
                                    row = self.rows - 1
                                    if row < 1:
                                        return
                        case 'u' | 'up':
                            row = row + 1
                            if row > self.rows:
                                row = self.rows
                                if col_start == self.cols:
                                    self.direction = 'r'
                                    col = 2
                                    if col > self.cols:
                                        return
                                else:
                                    self.direction = 'l'
                                    col = self.cols - 1
                                    if col < 1:
                                        return
                        case 'd' | 'down':
                            row = row - 1
                            if row < 1:
                                row = 1
                                if col_start == self.cols:
                                    self.direction = 'l'
                                    col = self.cols - 1
                                    if col < 1:
                                        return
                                else:
                                    self.direction = 'r'
                                    col = 2
                                    if col > self.cols:
                                        return

                # ---- regular
                case _:  # default pattern
                    yield Location(col, row, x, y)
                    # next grid location
                    match self.direction.lower():
                        case 'r' | 'right':
                            col = col + 1
                            if col > self.cols:
                                col = col_start
                                if row_start == self.rows:
                                    row = row - 1
                                    if row < 1:
                                        return  # end
                                else:
                                    row = row + 1
                                    if row > self.rows:
                                        return  # end
                        case 'l' | 'left':
                            col = col - 1
                            if col < 1:
                                col = col_start
                                if row_start == self.rows:
                                    row = row - 1
                                    if row < 1:
                                        return  # end
                                else:
                                    row = row + 1
                                    if row > self.rows:
                                        return  # end
                        case 'u' | 'up':
                            row = row + 1
                            if row > self.rows:
                                row = row_start
                                if col_start == self.cols:
                                    col = col - 1
                                    if col < 1:
                                        return  # end
                                else:
                                    col = col + 1
                                    if col > self.cols:
                                        return  # end
                        case 'd' | 'down':
                            row = row - 1
                            if row < 1:
                                row = row_start
                                if col_start == self.cols:
                                    col = col - 1
                                    if col < 1:
                                        return  # end
                                else:
                                    col = col + 1
                                    if col > self.cols:
                                        return  # end

# ---- Tracks =====


class VirtualTrack(Virtual):
    """
    Common properties and methods to define a virtual track.

    A virtual track is not drawn on the canvas; rather it provides a set of points
    where a user-defined shape will be drawn.
    """
    global cnv

    def __init__(self, **kwargs):
        kwargs = kwargs
        self.count = kwargs.get('count ', 8)
        self.start = kwargs.get('start', 'BL')
        self.initial = kwargs.get('initial', 0)  # most tracks...
        self.final = kwargs.get('final', 0)
        self.reset = kwargs.get('reset', 0)
        self.spacing = kwargs.get('spacing ', 0)
        self.direction = kwargs.get('direction', 'clockwise')
        self.rotation = kwargs.get('rotation', 'none')
        self.corners = kwargs.get('corners', [])  # use ["","","",""] to skip!
        self.validate()

    def validate(self):
        """Check for validate settings and combos."""
        self.count = self.to_int(self.count, 'count')
        self.initial = self.to_int(self.initial, 'initial')
        self.final = self.to_int(self.final, 'final')
        self.reset = self.to_int(self.reset, 'reset')
        self.spacing = self.to_float(self.spacing, 'spacing')
        self.start = str(self.start)
        self.direction = str(self.direction)
        self.rotation = str(self.rotation)

        if self.start.lower() not in ['bl', 'br', 'tl', 'tr']:
            tools.feedback(
                f"{self.start} is not a valid start - "
                "use 'bl', 'br', 'tl', or 'tr'", True)
        if self.direction.lower() not in [
                'c', 'clock', 'clockwise', 'a', 'anti', 'anticlockwise']:
            tools.feedback(
                f"{self.direction} is not a valid direction - "
                "use 'c', 'clock', 'clockwise', 'a', 'anti', or 'anticlockwise'", True)
        if self.rotation.lower() not in ['i', 'in', 'o', 'out', 'n', 'none']:
            tools.feedback(
                f"{self.rotation} is not a valid rotation - "
                "use 'i', 'in', 'o', 'out', 'n', or 'none'", True)

    def next_location(self, spaces: int, shapes: list) -> Location:
        """Yield next Location for each call."""
        raise NotImplementedError('Overwrite this method in a child class!')


class RectangleTrack(RectangleShape, VirtualTrack):
    """
    Properties and methods to define a rectangular virtual track.
    """
    global cnv

    def __init__(self, _object=None, canvas=None, **kwargs):
        RectangleShape.__init__(self, **kwargs)  # NO super
        VirtualTrack.__init__(self, **kwargs)
        if self.rounding or self.rounded:
            tools.feedback('A rectangular track cannot be rounded', True)
        if self.notch or self.notch_x or self.notch_y:
            tools.feedback('A rectangular track cannot be notched', True)
        self.vertices = RectangleShape.set_vertices(self, **kwargs)
        self._o = self.set_offset_props()
        # derived settings
        match self.start.lower():
            case 'bl':
                if self.direction.lower() in ['c', 'clock', 'clockwise']:
                    self.nodes = [0, 1, 2, 3, 0]
                else:
                    self.nodes = [0, 3, 2, 1, 0]
            case 'tl':
                if self.direction.lower() in ['c', 'clock', 'clockwise']:
                    self.nodes = [1, 2, 3, 0, 1]
                else:
                    self.nodes = [1, 0, 3, 2, 1]
            case 'tr':
                if self.direction.lower() in ['c', 'clock', 'clockwise']:
                    self.nodes = [2, 3, 0, 1, 2]
                else:
                    self.nodes = [2, 1, 0, 3, 2]
            case 'br':
                if self.direction.lower() in ['c', 'clock', 'clockwise']:
                    self.nodes = [3, 0, 1, 2, 3]
                else:
                    self.nodes = [3, 2, 1, 0, 3]

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a rectangle track on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props

    def calculate_params(self, spaces: int, shapes: list) -> tuple:
        """Parameters for calculating Points on perimeter."""
        total_corner_length = 0.0  # TODO calc!!
        perimeter = self.calculate_perimeter() - total_corner_length
        space_size = perimeter / float(spaces)
        spacing = self.unit(self.spacing)  # between each shape
        max_shape_width = space_size - spacing
        increment = space_size + spacing
        # tools.feedback(f'*** RectTrack {perimeter=} {spaces=} {space_size=} {max_shape_width=}')
        return increment, max_shape_width

    def next_location(self, spaces: int, shapes: list) -> TrackPoint:
        """Yield next TrackPoint for each call."""
        increment, max_shape_width = self.calculate_params(spaces, shapes)
        # pre-yield
        counter, node, total_distance = 0, 0, 0.0
        # assuming that no corner shapes are in play...
        the_point = self.vertices[self.nodes[node]]
        point_start = self.vertices[self.nodes[node]]
        point_end = self.vertices[self.nodes[node + 1]]
        # tools.feedback(f'*** +++ NODES {self.vertices=} {self.nodes=}')
        while True:
            # tools.feedback(f'*** NODE {node=} {counter=} start={point_start} end={point_end}')
            yield TrackPoint(the_point.x, the_point.y, max_shape_width)
            counter += 1
            if counter + 1 > spaces:
                return
            # calculate distance along line (or check if next line needed)
            total_distance += increment
            if total_distance > geoms.length_of_line(point_start, point_end):
                node += 1  # next line
                total_distance = 0
                if node + 1 >= len(self.nodes):
                    return  # end of last line ...
                # assuming that no corner shapes are in play...
                point_start = self.vertices[self.nodes[node]]
                point_end = self.vertices[self.nodes[node + 1]]
                # tools.feedback(f'*** *** NODE {node=} ctr={counter} start={point_start} end={point_end}')
                the_point = self.vertices[self.nodes[node]]
            else:
                the_point = geoms.point_on_line(
                    point_start=point_start,
                    point_end=point_end,
                    distance=increment)


class CircleTrack(CircleShape, VirtualTrack):
    """
    Properties and methods to define a circular track.
    """
    global cnv

    def __init__(self, _object=None, canvas=None, **kwargs):
        CircleShape.__init__(self, kwargs)  # NO super
        VirtualTrack.__init__(self, kwargs)

    def next_location(self, spaces: int, shapes: list) -> Point:
        """Yield next Point for each call."""
        return



# ---- Other  =====


class ConnectShape(BaseShape):
    """
    Connect two shapes (Rectangle), based on a position, on a given canvas.

       Q4 | Q1
       -------
       Q3 | Q2

    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(ConnectShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides
        self.shape_from = kwargs.get("shape_from", None)
        self.shape_to = kwargs.get("shape_to", None)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a connection (line) between two shapes on given canvas."""
        cnv = cnv
        ID = ID
        # style
        style = self.style or "direct"
        # shapes and position  - default style
        try:
            shape_from, shape_from_position = self.shape_from  # tuple form
        except Exception:
            shape_from, shape_from_position = self.shape_from, "BC"
        try:
            shape_to, shape_to_position = self.shape_to  # tuple form
        except Exception:
            shape_to, shape_to_position = self.shape_to, "TC"
        # props
        edge_from = shape_from.get_edges()
        edge_to = shape_to.get_edges()
        x_f, y_f = self.key_positions(shape_from, shape_from_position)
        x_t, y_t = self.key_positions(shape_to, shape_to_position)
        xc_f, yc_f = self.shape_from.get_center()
        xc_t, yc_t = self.shape_to.get_center()
        # x,y: use fixed/supplied; or by "name"; or by default; or by "smart"
        if style == "path":
            points = []

            if xc_f == xc_t and yc_f > yc_t:  # above
                points = [
                    self.key_positions(shape_from, "BC"),
                    self.key_positions(shape_to, "TC"),
                ]
            if xc_f == xc_t and yc_f < yc_t:  # below
                points = [
                    self.key_positions(shape_from, "TC"),
                    self.key_positions(shape_to, "BC"),
                ]
            if xc_f > xc_t and yc_f == yc_t:  # left
                points = [
                    self.key_positions(shape_from, "LC"),
                    self.key_positions(shape_to, "RC"),
                ]
            if xc_f < xc_t and yc_f == yc_t:  # right
                points = [
                    self.key_positions(shape_from, "RC"),
                    self.key_positions(shape_to, "LC"),
                ]

            if xc_f < xc_t and yc_f < yc_t:  # Q1
                if edge_from["right"] < edge_to["left"]:
                    if edge_from["top"] < edge_to["bottom"]:
                        log.debug("A t:%s b:%s", edge_from["top"], edge_to["bottom"])
                        delta = (edge_to["bottom"] - edge_from["top"]) / 2.0
                        points = [
                            self.key_positions(shape_from, "TC"),
                            (xc_f, edge_from["top"] + delta),
                            (xc_t, edge_from["top"] + delta),
                            self.key_positions(shape_to, "BC"),
                        ]
                    elif edge_from["top"] > edge_to["bottom"]:
                        log.debug("B t:%s b:%s", edge_from["top"], edge_to["bottom"])
                        points = [
                            self.key_positions(shape_from, "TC"),
                            (xc_f, yc_t),
                            self.key_positions(shape_to, "LC"),
                        ]
                    else:
                        pass
                else:
                    log.debug("C t:%s b:%s", edge_from["top"], edge_to["bottom"])
                    points = [
                        self.key_positions(shape_from, "TC"),
                        (xc_f, yc_t),
                        self.key_positions(shape_to, "LC"),
                    ]
            if xc_f < xc_t and yc_f > yc_t:  # Q2
                log.debug("Q2")

            if xc_f > xc_t and yc_f > yc_t:  # Q3
                log.debug("Q3")

            if xc_f > xc_t and yc_f < yc_t:  # Q4
                log.debug("Q4")
                if edge_from["left"] < edge_to["right"]:
                    if edge_from["top"] < edge_to["bottom"]:
                        log.debug(" A t:%s b:%s", edge_from["top"], edge_to["bottom"])
                        delta = (edge_to["bottom"] - edge_from["top"]) / 2.0
                        points = [
                            self.key_positions(shape_from, "TC"),
                            (xc_f, edge_from["top"] + delta),
                            (xc_t, edge_from["top"] + delta),
                            self.key_positions(shape_to, "BC"),
                        ]
                    elif edge_from["top"] > edge_to["bottom"]:
                        log.debug(" B t:%s b:%s", edge_from["top"], edge_to["bottom"])
                        points = [
                            self.key_positions(shape_from, "TC"),
                            (xc_f, yc_t),
                            self.key_positions(shape_to, "RC"),
                        ]
                    else:
                        pass
                else:
                    log.debug(" C t:%s b:%s", edge_from["top"], edge_to["bottom"])
                    points = [
                        self.key_positions(shape_from, "TC"),
                        (xc_f, yc_t),
                        self.key_positions(shape_to, "RC"),
                    ]

            if xc_f == xc_t and yc_f == yc_t:  # same!
                return
            self.kwargs["points"] = points
            plin = PolylineShape(None, cnv, **self.kwargs)
            plin.draw(ID=ID)
        elif style == "direct":  # straight line
            self.kwargs["x"] = x_f
            self.kwargs["y"] = y_f
            self.kwargs["x1"] = x_t
            self.kwargs["y1"] = y_t
            lin = LineShape(None, cnv, **self.kwargs)
            lin.draw(ID=ID)
        else:
            tools.feedback('Style "{style}" is unknown.')

    def key_positions(self, _shape, location=None):
        """Calculate a dictionary of key positions around a Rectangle.

        T,B,L,R,C = Top, Bottom, Left, Right, Center
        """
        top = _shape.y + _shape.height
        btm = _shape.y
        mid_horizontal = _shape.x + _shape.width / 2.0
        mid_vertical = _shape.y + _shape.height / 2.0
        left = _shape.x
        right = _shape.x + _shape.width
        _positions = {
            "TL": (left, top),
            "TC": (mid_horizontal, top),
            "TR": (right, top),
            "BL": (left, btm),
            "BC": (mid_horizontal, btm),
            "BR": (right, btm),
            "LC": (left, mid_vertical),
            "RC": (right, mid_vertical),
            # '': (),
        }
        if location:
            return _positions.get(location, ())
        else:
            return _positions


class FooterShape(BaseShape):
    """
    Footer for a page.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(FooterShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # self.page_width = kwargs.get('pagesize', (canvas.width, canvas.height))[0]

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw footer on a given canvas page."""
        cnv = cnv if cnv else self.canvas
        #super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        font_size = kwargs.get('font_size', self.font_size)
        # ---- set location and text
        x = self.kwargs.get("x",  self._u.page_width / 2.0)  # centre across page
        y = self.unit(self.margin_bottom) / 2.0   # centre in margin
        text = kwargs.get("text") or "Page %s" % ID
        # tools.feedback(f'*** FooterShape {ID=} {text=} {x=} {y=} {font_size=}')
        # ---- draw footer
        self.draw_multi_string(cnv.canvas, x, y, text, align='centre', font_size=font_size)
