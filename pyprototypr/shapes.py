# -*- coding: utf-8 -*-
"""
Create custom shapes for pyprototypr
"""
# lib
import codecs
import copy
import logging
import math
import random

# third party
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import (
    A8, A7, A6, A5, A4, A3, A2, A1, A0, LETTER, LEGAL, ELEVENSEVENTEEN,
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
    'CircleShape', 'CompassShape', 'DotShape', 'HexShape', 'PolygonShape',
    'RectangleShape', 'RhombusShape', 'SquareShape', 'StadiumShape', ] # EllipseShape ???
GRID_SHAPES_NO_CENTRE = [
     'TextShape', 'StarShape', ]
# NOT GRID:  ArcShape, BezierShape, PolylineShape, ChordShape


class ImageShape(BaseShape):
    """
    Image (bitmap or SVG) on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Show an image on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        img = None
        # ---- check for Card usage
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
        # ---- load image
        # tools.feedback(f'*** IMAGE {ID=} {_source=} {x=} {y=} {self.scaling=} ')
        img, is_svg = self.load_image(_source, self.scaling)
        if not img:
            tools.feedback(
                f'Unable to load image "{_source}!" - please check name and location',
                True)
        rotation = kwargs.get('rotation', self.rotation)
        # assumes 1 pt == 1 pixel ?
        if rotation:
            # ---- rotated image
            # tools.feedback(f'*** IMAGE {ID=} {rotation=} {self._u.x=}, {self._u.y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                dx, dy = self._u.margin_left, self._u.margin_bottom
                cnv.translate(x + dx, y + dy)
            else:
                cnv.translate(x + self._o.delta_x, y + self._o.delta_y)
            cnv.rotate(rotation)
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
            # ---- normal image
            if is_svg:
                from reportlab.graphics import renderPDF
                renderPDF.draw(img, cnv, x=x, y=y)
            else:
                # TODO -> use height=10 OR width=12 AND preserveAspectRatio=True,
                cnv.drawImage(img, x=x, y=y, width=width, height=height, mask="auto")
        # ---- text
        xc = x + width / 2.0
        yc = y + height / 2.0
        if self.heading:
            cnv.setFont(self.font_face, self.heading_size)
            cnv.setFillColor(self.heading_stroke)
            self.draw_multi_string(cnv, xc, y + height + cnv._leading, self.heading)
        if self.label:
            cnv.setFont(self.font_face, self.label_size)
            cnv.setFillColor(self.label_stroke)
            self.draw_multi_string(cnv, xc, yc, self.label)
        if self.title:
            cnv.setFont(self.font_face, self.title_size)
            cnv.setFillColor(self.title_stroke)
            self.draw_multi_string(cnv, xc, y - cnv._leading, self.title)


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
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- head
        self.arrow_head()
        # ---- tail
        self.arrow_tail()
        # ---- calculate line rotation
        compass, rotation = geoms.angles_from_points(x, y, x_1, y_1)
        # ---- dot
        self.draw_dot(cnv, (x_1 + x) / 2.0, (y_1 + y) / 2.0)
        # ---- text
        self.draw_label(
            cnv, ID, (x_1 + x) / 2.0, (y_1 + y) / 2.0, rotation=rotation, centred=False, **kwargs)


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
        if lines < 0:
            tools.feedback('Cannot draw negative number of lines!', True)
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
            if 'e' in _dirs or 'w' in _dirs or 'o' in _dirs:  # horizontal
                self.draw_line_between_points(
                    cnv,
                    Point(x_c + self._u.radius, y_c),
                    Point(x_c - self._u.radius, y_c))
            if 'n' in _dirs or 's' in _dirs or 'o' in _dirs:  # vertical
                self.draw_line_between_points(
                    cnv,
                    Point(x_c, y_c + self._u.radius),
                    Point(x_c, y_c - self._u.radius))
            if 'se' in _dirs or 'nw' in _dirs or 'd' in _dirs:  # diagonal  "down"
                poc_top_d = geoms.point_on_circle(Point(x_c, y_c), self._u.radius, 135)
                poc_btm_d = geoms.point_on_circle(Point(x_c, y_c), self._u.radius, 315)
                self.draw_line_between_points(cnv, poc_top_d, poc_btm_d)
            if 'ne' in _dirs or 'sw' in _dirs or 'd' in _dirs:  # diagonal  "up"
                poc_top_u = geoms.point_on_circle(Point(x_c, y_c), self._u.radius, 45)
                poc_btm_u = geoms.point_on_circle(Point(x_c, y_c), self._u.radius, 225)
                self.draw_line_between_points(cnv, poc_top_u, poc_btm_u)

        if num <= 1:
            return

        if 'e' in _dirs or 'w' in _dirs or 'o' in _dirs:  # horizontal
            for dist in horizontal_distances:
                self.draw_line_between_points(  # "above" diameter
                    cnv,
                    Point(x_c - dist[0], y_c + dist[1]),
                    Point(x_c + dist[0], y_c + dist[1]))
                self.draw_line_between_points(  # "below" diameter
                    cnv,
                    Point(x_c - dist[0], y_c - dist[1]),
                    Point(x_c + dist[0], y_c - dist[1]))

        if 'n' in _dirs or 's' in _dirs or 'o' in _dirs:  # vertical
            for dist in vertical_distances:
                self.draw_line_between_points(  # "right" of diameter
                    cnv,
                    Point(x_c + dist[0], y_c + dist[1]),
                    Point(x_c + dist[0], y_c - dist[1]))
                self.draw_line_between_points(  # "left" of diameter
                    cnv,
                    Point(x_c - dist[0], y_c + dist[1]),
                    Point(x_c - dist[0], y_c - dist[1]))

        if 'se' in _dirs or 'nw' in _dirs or 'd' in _dirs:  # diagonal  "down"
            for dist in horizontal_distances:
                _angle = math.degrees(math.asin(dist[0] / self._u.radius))
                # "above right" of diameter
                dal = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 45. + _angle)
                dar = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 45. - _angle)# + 45.)
                self.draw_line_between_points(cnv, dar, dal)
                # "below left" of diameter
                dbl = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 225. - _angle)
                dbr = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 225. + _angle)
                self.draw_line_between_points(cnv, dbr, dbl)
                # TEST cnv.circle(dal.x, dal.y, 2, stroke=1, fill=1 if self.fill else 0)

        if 'ne' in _dirs or 'sw' in _dirs or 'd' in _dirs:  # diagonal  "up"
            for dist in vertical_distances:
                _angle = math.degrees(math.asin(dist[0] / self._u.radius))
                # "above left" of diameter
                poc_top = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, _angle + 45.)
                poc_btm = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 180. - _angle + 45.)
                self.draw_line_between_points(cnv, poc_top, poc_btm)
                # "below right" of diameter
                poc_top = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 45 - _angle)
                poc_btm = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 180. + _angle + 45.)
                self.draw_line_between_points(cnv, poc_top, poc_btm)

    def draw_radii(self, cnv, ID, x_c: float, y_c: float):
        """Draw radius lines from the centre outwards to the circumference.

        The offset will start the line a certain distance away; and the length will
        determine how long the radial line is.  By default it stretches from centre
        to circumference.

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
            rad_offset = self.unit(self.radii_offset) or 0
            rad_length = self.unit(_radius, label='radius length')
            self.set_canvas_props(
                index=ID,
                stroke=self.radii_stroke,
                stroke_width=self.radii_stroke_width,
                dashes=self.radii_dashes,
                line_dots=self.radii_line_dots)
            for rad_angle in _radii:
                # points based on length of line, offset and the angle in degrees
                diam_pt = geoms.point_on_circle(Point(x_c, y_c), rad_length, rad_angle)
                pth = cnv.beginPath()
                if rad_offset is not None and rad_offset != 0:
                    offset_pt = geoms.point_on_circle(Point(x_c, y_c), rad_offset, rad_angle)
                    end_pt = geoms.point_on_line(offset_pt, diam_pt, rad_length)
                    # print(rad_angle, offset_pt, f'{x_c=}, {y_c=}')
                    pth.moveTo(offset_pt.x, offset_pt.y)
                    pth.lineTo(end_pt.x, end_pt.y)
                else:
                    pth.moveTo(x_c, y_c)
                    pth.lineTo(diam_pt.x, diam_pt.y)
                cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)

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
            if self.rotation:
                # tools.feedback(f'*** {self.hatch=}, {self.rotation=}, {type(cnv)}')
                cnv.saveState()
                cnv.translate(self.x_c, self.y_c)
                self.draw_hatch(cnv, ID, self.hatch, 0, 0)
                cnv.rotate(self.rotation)
                cnv.restoreState()
            else:
                self.draw_hatch(cnv, ID, self.hatch, self.x_c, self.y_c)
        # ---- draw radii
        if self.radii:
            if self.rotation:
                # tools.feedback(f'*** {self.hatch=}, {self.rotation=}, {type(cnv)}')
                cnv.saveState()
                cnv.translate(self.x_c, self.y_c)
                self.draw_radii(cnv, ID, 0, 0)
                cnv.rotate(self.rotation)
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
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- calculate line rotation
        compass, rotation = geoms.angles_from_points(x, y, x_1, y_1)
        # tools.feedback(f"*** {compass=} {rotation=}")
        # ---- dot
        self.draw_dot(cnv, (x_1 + x) / 2.0, (y_1 + y) / 2.0)
        # ---- text
        self.draw_label(
            cnv, ID, (x_1 + x) / 2.0, (y_1 + y) / 2.0, rotation=rotation, centred=False, **kwargs)


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
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)

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
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)

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
        if self.perimeter == 'circle':
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
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- calculate line rotation
        compass, rotation = geoms.angles_from_points(x, y, x_1, y_1)
        # tools.feedback(f"*** {compass=} {rotation=}")
        # ---- dot
        self.draw_dot(cnv, (x_1 + x) / 2.0, (y_1 + y) / 2.0)
        # ---- text
        self.draw_label(
            cnv, ID, (x_1 + x) / 2.0, (y_1 + y) / 2.0, rotation=rotation, centred=False, **kwargs)


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
                self.draw_lines_between_sides(
                    cnv, side, lines, vertices, (0, 1), (2, 1))
            if 'se' in _dirs or 'nw' in _dirs:  # slope down to the right
                self.draw_lines_between_sides(
                    cnv, side, lines, vertices, (0, 2), (0, 1))
            if 'e' in _dirs or 'w' in _dirs:  # horizontal
                self.draw_lines_between_sides(
                    cnv, side, lines, vertices, (0, 2), (1, 2))

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an equilateraltriangle on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # calculate points
        x, y = self._u.x, self._u.y
        hand = self.hand.lower() if self.hand else 'east'
        flip = self.flip.lower() if self.flip else 'north'
        angle = self.angle
        side = self._u.side if self._u.side else self._u.width
        height = 0.5 * math.sqrt(3) * side  # ½√3(a)
        # tools.feedback(f'*** {hand=} {flip=} {side=} {height=} {self.fill=} {self.stroke=}')
        self.vertices = []
        pt0 = Point(x + self._o.delta_x, y + self._o.delta_y)
        self.vertices.append(pt0)
        if hand == 'west' or hand == 'w':
            x2 = pt0.x - side
            y2 = pt0.y
            x3 = pt0.x - 0.5 * side
        elif hand == 'east' or hand == 'e':
            x2 = pt0.x + side
            y2 = pt0.y
            x3 = x2 - 0.5 * side
        if flip == 'north' or flip == 'n':
            y3 = pt0.y + height
        elif flip == 'south' or flip == 's':
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
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- calculate centroid
        x_c = (self.vertices[0].x + self.vertices[1].x + self.vertices[2].x) / 3.0
        y_c = (self.vertices[0].y + self.vertices[1].y + self.vertices[2].y) / 3.0
        # tools.feedback(f'*** {x_c=} {y_c=}')
        # ---- debug
        self._debug(cnv, vertices=self.vertices)
        # ---- draw hatch
        if self.hatch:
            self.draw_hatch(cnv, ID, side, self.vertices, self.hatch)
        # ---- dot
        self.draw_dot(cnv, x_c, y_c)
        # ---- text
        self.draw_heading(cnv, ID, x_c, y_c + height * 2.0 / 3.0, **kwargs)
        self.draw_label(cnv, ID, x_c, y_c, **kwargs)
        self.draw_title(cnv, ID, x_c, y_c - height / 3.0, **kwargs)


class HexShape(BaseShape):
    """
    Hexagon on a given canvas.

    See: http://powerfield-software.com/?p=851
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(HexShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.use_diameter = True if self.is_kwarg('diameter') else False
        self.use_height = True if self.is_kwarg('height') else False
        self.use_radius = True if self.is_kwarg('radius') else False
        self.use_side = False
        if 'side' in kwargs:
            self.use_side = True
            if 'radius' in kwargs or 'height' in kwargs or 'diameter' in kwargs:
                self.use_side = False
        # fallback / default
        if not self.use_diameter and not self.use_radius and not self.use_side:
            self.use_height = True

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

    def draw_links(self, cnv, ID, side: float, vertices: list, links: list):
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

    def draw_radii(self, cnv, ID, centre: Point, vertices: list):
        """Draw line(s) connecting the hexagon centre to a vertex.
        """
        self.set_canvas_props(
            index=ID,
            stroke=self.radii_stroke or self.stroke,
            stroke_width=self.radii_stroke_width or self.stroke_width,
            stroke_cap=self.radii_cap or self.line_cap)
        _dirs = self.radii.lower().split()
        if 'ne' in _dirs:  # slope UP to the right
            self.draw_line_between_points(cnv, centre, vertices[2])
        if 'sw' in _dirs:  # slope DOWN to the left
            if self.orientation in ['p', 'pointy']:
                self.draw_line_between_points(cnv, centre, vertices[0])
            else:
                self.draw_line_between_points(cnv, centre, vertices[5])
        if 'se' in _dirs:  # slope DOWN to the right
            self.draw_line_between_points(cnv, centre, vertices[4])
        if 'nw' in _dirs:  # slope UP to the left
            self.draw_line_between_points(cnv, centre, vertices[1])
        if 'n' in _dirs and self.orientation in ['p', 'pointy']:  # vertical UP
            self.draw_line_between_points(cnv, centre, vertices[2])
        if 's' in _dirs and self.orientation in ['p', 'pointy']:  # vertical DOWN
            self.draw_line_between_points(cnv, centre, vertices[5])
        if 'e' in _dirs and self.orientation in ['f', 'flat']:  # horizontal RIGHT
            self.draw_line_between_points(cnv, centre, vertices[3])
        if 'w' in _dirs and self.orientation in ['f', 'flat']:  # horizontal LEFT
            self.draw_line_between_points(cnv, centre, vertices[0])

    def draw_hatch(self, cnv, ID, side: float, vertices: list, num: int):
        """Draw lines connecting two opposite sides and parallel to adjacent side.
        """
        self.set_canvas_props(
            index=ID,
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_width,
            stroke_cap=self.hatch_cap)
        _dirs = self.hatch_directions.lower().split()
        lines = int((num - 1) / 2 + 1)

        if num >= 1:
            # tools.feedback(f'*** {vertices=} {num=} {_dirs=}')
            if self.orientation in ['p', 'pointy']:
                if 'ne' in _dirs or 'sw' in _dirs:  # slope UP to the right
                    self.make_path_vertices(cnv, vertices, 0, 3)
                if 'se' in _dirs or 'nw' in _dirs:  # slope down to the right
                    self.make_path_vertices(cnv, vertices, 1, 4)
                if 'n' in _dirs or 's' in _dirs:  # vertical
                    self.make_path_vertices(cnv, vertices, 2, 5)
            if self.orientation in ['f', 'flat']:
                if 'ne' in _dirs or 'sw' in _dirs:  # slope UP to the right
                    self.make_path_vertices(cnv, vertices, 2, 5)
                if 'se' in _dirs or 'nw' in _dirs:  # slope down to the right
                    self.make_path_vertices(cnv, vertices, 1, 4)
                if 'e' in _dirs or 'w' in _dirs:  # horizontal
                    self.make_path_vertices(cnv, vertices, 0, 3)
        if num >= 3:
            if self.orientation in ['p', 'pointy']:
                if 'ne' in _dirs or 'sw' in _dirs:  # slope UP to the right
                    self.draw_lines_between_sides(cnv, side, lines, vertices, (2, 3), (1, 0))
                    self.draw_lines_between_sides(cnv, side, lines, vertices, (3, 4), (0, 5))
                if 'se' in _dirs or 'nw' in _dirs:  # slope down to the right
                    self.draw_lines_between_sides(cnv, side, lines, vertices, (0, 1), (5, 4))
                    self.draw_lines_between_sides(cnv, side, lines, vertices, (1, 2), (4, 3))
                if 'n' in _dirs or 's' in _dirs:  # vertical
                    self.draw_lines_between_sides(cnv, side, lines, vertices, (1, 2), (0, 5))
                    self.draw_lines_between_sides(cnv, side, lines, vertices, (2, 3), (5, 4))
            if self.orientation in ['f', 'flat']:
                if 'ne' in _dirs or 'sw' in _dirs:  # slope UP to the right
                    self.draw_lines_between_sides(cnv, side, lines, vertices, (2, 1), (5, 0))
                    self.draw_lines_between_sides(cnv, side, lines, vertices, (2, 3), (5, 4))
                if 'se' in _dirs or 'nw' in _dirs:  # slope down to the right
                    self.draw_lines_between_sides(cnv, side, lines, vertices, (4, 5), (1, 0))
                    self.draw_lines_between_sides(cnv, side, lines, vertices, (1, 2), (4, 3))
                if 'e' in _dirs or 'w' in _dirs:  # horizontal
                    self.draw_lines_between_sides(cnv, side, lines, vertices, (0, 1), (3, 2))
                    self.draw_lines_between_sides(cnv, side, lines, vertices, (0, 5), (3, 4))

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a hexagon on a given canvas."""
        # tools.feedback(f'*** draw hexshape: {kwargs} {off_x} {off_y} {ID}')
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        is_cards = kwargs.get("is_cards", False)
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # ---- calculate half_flat & half_side
        if self.height and self.use_height:
            side = self._u.height / math.sqrt(3)
            half_flat = self._u.height / 2.0
        elif self.diameter and self.use_diameter:
            side = self._u.diameter / 2.0
            half_flat = side * math.sqrt(3) / 2.0
        elif self.radius and self.use_radius:
            side = self._u.radius
            half_flat = side * math.sqrt(3) / 2.0
        else:
            pass
        if self.side and self.use_side:
            side = self._u.side
            half_flat = side * math.sqrt(3) / 2.0
        if not self.radius and not self.height and not self.diameter and not self.side:
            tools.feedback(
                'No value for side or height or diameter or radius supplied for hexagon.',
                True)

        half_side = side / 2.0
        height_flat = 2 * half_flat
        diameter = 2.0 * side
        radius = side
        z_fraction = (diameter - side) / 2.0

        # ---- POINTY^
        if self.orientation.lower() in ['p', 'pointy']:
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
            # tools.feedback(f"*** P^: {x=} {y=} {x_d=} {y_d=} {half_flat=} {side=}")

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
            # tools.feedback(f"*** F~: {x=} {y=} {x_d=} {y_d=} {half_flat=} {side=}")

        # ---- calculate area
        self.area = self.calculate_area()
        # ---- canvas
        self.set_canvas_props(index=ID)
        if self.caltrops or self.caltrops_fraction:
            line_dashes = self.calculate_caltrops(
                self.side, self.caltrops, self.caltrops_fraction, self.caltrops_invert)
            cnv.setDash(array=line_dashes)
        # ---- calculate vertical hexagon (clockwise)
        if self.orientation.lower() in ['p', 'pointy']:
            self.vertices = [  # clockwise from bottom-left; relative to centre
                Point(x, y + z_fraction),
                Point(x, y + z_fraction + side),
                Point(x + half_flat, y + diameter),
                Point(x + height_flat, y + z_fraction + side),
                Point(x + height_flat, y + z_fraction),
                Point(x + half_flat, y),
            ]
        # ---- calculate horizontal hexagon (clockwise)
        else:   # self.orientation.lower() in ['f',  'flat']:
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
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- debug
        # self._debug(cnv, Point(x, y), 'start')
        # self._debug(cnv, Point(x_d, y_d), 'centre')
        self._debug(cnv, vertices=self.vertices)
        # ---- draw hatch
        if self.hatch:
            if not self.hatch & 1:
                tools.feedback('Hatch must be an odd number for a Hexagon', True)
            self.draw_hatch(cnv, ID, side, self.vertices, self.hatch)
        # ---- draw links
        if self.links:
            self.draw_links(cnv, ID, side, self.vertices, self.links)
        # ---- draw radii
        if self.radii:
            self.draw_radii(cnv, ID, Point(x_d, y_d), self.vertices)
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
        if self.orientation.lower() in ['p', 'pointy']:
            offset = side  # == radius
        else:
            offset = half_flat
        self.draw_heading(cnv, ID, x_d, y_d + offset, **kwargs)
        self.draw_label(cnv, ID, x_d, y_d, **kwargs)
        self.draw_title(cnv, ID, x_d, y_d - offset, **kwargs)
        # ----  numbering
        self.set_coord(cnv, x_d, y_d, half_flat)
        # ---- set grid property
        self.grid = GridShape(label=self.coord_text, x=x_d, y=y_d, shape=self)


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
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- calculate line rotation
        compass, rotation = geoms.angles_from_points(x, y, x_1, y_1)
        # ---- dot
        self.draw_dot(cnv, (x_1 + x) / 2.0, (y_1 + y) / 2.0)
        # ---- text
        self.draw_label(
            cnv, ID, (x_1 + x) / 2.0, (y_1 + y) / 2.0, rotation=rotation, centred=False, **kwargs)


class PolygonShape(BaseShape):
    """
    Regular polygon on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(PolygonShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.use_diameter = True if self.is_kwarg('diameter') else False
        self.use_height = True if self.is_kwarg('height') else False
        self.use_radius = True if self.is_kwarg('radius') else False
        # ---- perform overrides
        if self.cx and self.cy:
            self.x, self.y = self.cx, self.cy
        # ---- RESET UNIT PROPS (last!)
        self.set_unit_properties()

    def get_radius(self):
        if self.radius and self.use_radius:
            radius = self._u.radius
        elif self.diameter and self.use_diameter:
            radius = self._u.diameter / 2.0
        elif self.height and self.use_height:
            radius = self._u.height / 2.0
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

    def draw_mesh(self, cnv, ID, vertices: list):
        """Draw lines connecting each of the vertices to mid-points of other sides.
        """
        tools.feedback('Sorry, mesh for Polygon is not yet implemented.', True)
        ''' TODO - autodraw (without dirs)
        self.set_canvas_props(
            index=ID,
            stroke=self.mesh_stroke or self.stroke,
            stroke_width=self.mesh_stroke_width or self.stroke_width,
            stroke_cap=self.mesh_cap or self.line_cap)
        _dirs = self.hatch_directions.lower().split()
        lines = int(num)
        if num >= 1:
            if 'ne' in _dirs or 'sw' in _dirs:  # slope UP to the right
                self.draw_lines_between_sides(cnv, side, lines, vertices, (0, 1), (5, 4))
            if 'se' in _dirs or 'nw' in _dirs:  # slope down to the right
                self.draw_lines_between_sides(cnv, side, lines, vertices, (2, 3), (7, 6))
            if 'n' in _dirs or 's' in _dirs:  # vertical
                self.draw_lines_between_sides(cnv, side, lines, vertices, (3, 4), (0, 7))
            if 'e' in _dirs or 'w' in _dirs:  # horizontal
                self.draw_lines_between_sides(cnv, side, lines, vertices, (1, 2), (6, 5))
        '''

    def draw_radii(self, cnv, ID, centre: Point, vertices: list):
        """Draw lines connecting the polygon centre to each of the vertices.
        """
        _radii = []
        for vertex in vertices:
            _, angle = geoms.angles_from_points(centre.x, centre.y, vertex.x, vertex.y)
            _radii.append(angle)
        rad_offset = self.unit(self.radii_offset, label='radii offset') or 0
        rad_length = self.unit(self.radii_length, label='radii length') if self.radii_length \
            else self.get_radius()
        self.set_canvas_props(
            index=ID,
            stroke=self.radii_stroke,
            stroke_width=self.radii_stroke_width,
            dashes=self.radii_dashes,
            line_dots=self.radii_line_dots)
        for rad_angle in _radii:
            # points based on length of line, offset and the angle in degrees
            diam_pt = geoms.point_on_circle(centre, rad_length, rad_angle)
            pth = cnv.beginPath()
            if rad_offset is not None and rad_offset != 0:
                offset_pt = geoms.point_on_circle(centre, rad_offset, rad_angle)
                end_pt = geoms.point_on_line(offset_pt, diam_pt, rad_length)
                # print(rad_angle, offset_pt, f'{x_c=}, {y_c=}')
                pth.moveTo(offset_pt.x, offset_pt.y)
                pth.lineTo(end_pt.x, end_pt.y)
            else:
                pth.moveTo(centre.x, centre.y)
                pth.lineTo(diam_pt.x, diam_pt.y)
            cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)

    def get_vertices(self, rotation: float = 0, is_rotated: bool = False):
        """Calculate centre, radius and vertices of polygon.
        """
        # convert to using units
        if is_rotated:
            x, y = 0., 0.  # centre for now-rotated canvas
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        # calculate vertices - assumes x,y marks the centre point
        radius = self.get_radius()
        vertices = geoms.polygon_vertices(self.sides, radius, Point(x, y), rotation)
        return x, y, radius, vertices

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a regular polygon on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- set canvas
        cnv = cnv.canvas if cnv else self.canvas.canvas
        self.set_canvas_props(index=ID)
        if self.height:
            side = self._u.height / math.sqrt(3)
            half_flat = self._u.height / 2.0
        elif self.diameter:
            side = self._u.diameter / 2.0
            self._u.side = side
            half_flat = self._u.side * math.sqrt(3) / 2.0
        elif self.radius:
            side = self.u_radius
        # ---- calc centre in units
        if self.cx and self.cy:
            x = self._u.cx + self._o.delta_x
            y = self._u.cy + self._o.delta_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        # ---- handle rotation: START
        is_rotated = False
        rotation = kwargs.get('rotation', self.rotation)
        if rotation:
            is_rotated = True
            # tools.feedback(f'*** Rect {ID=} {rotation=} {self._u.x=}, {self._u.y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                cnv.translate(x + self._u.margin_left, y + self._u.margin_bottom)
            else:
                cnv.translate(x, y)
            cnv.rotate(rotation)
        # --- handle 'orientation' (flat vs pointy)
        flatten = 0
        if (self.orientation.lower() == 'flat' and not (self.sides - 2) % 4 == 0) or \
                (self.orientation.lower() == 'pointy' and (self.sides - 2) % 4 == 0):
            interior = ((self.sides - 2) * 180.0) / self.sides
            flatten = (180 - interior) / 2.0
        x, y, radius, vertices = self.get_vertices(
            rotation=flatten, is_rotated=is_rotated)
        # ---- invalid polygon?
        if not vertices or len(vertices) == 0:
            if rotation:
                cnv.restoreState()
            return
        # ---- draw polygon
        pth = cnv.beginPath()
        pth.moveTo(*vertices[0])
        for vertex in vertices:
            pth.lineTo(vertex.x, vertex.y)
        pth.close()
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- draw radii
        if self.radii:
            self.draw_radii(cnv, ID, Point(x, y), vertices)
        # ---- draw mesh
        if self.mesh:
            self.draw_mesh(cnv, ID, vertices)
        # ---- debug
        self._debug(cnv, vertices=vertices)  # needs: self.run_debug = True
        # ---- dot
        self.draw_dot(cnv, x, y)
        # ---- cross
        self.draw_cross(cnv, x, y)
        # ---- text
        self.draw_heading(cnv, ID, x, y, 1.3 * radius, **kwargs)
        self.draw_label(cnv, ID, x, y, **kwargs)
        self.draw_title(cnv, ID, x, y, 1.4 * radius, **kwargs)
        # ---- handle rotation: END
        if rotation:
            cnv.restoreState()


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

    def set_vertices(self, rotation=0, **kwargs):
        """Set vertices for rectangle without hatches."""
        if rotation:
            kwargs['rotation'] = rotation
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
        rotation = kwargs.get('rotation', None)
        if rotation:
            x = -self._u.width / 2.0
            y = -self._u.height / 2.0
        return x, y

    def draw_hatch(self, cnv, ID, vertices: list, num: int):
        _dirs = self.hatch_directions.lower().split()
        # ---- check dirs
        if self.rounding or self.rounded:
            if 'ne' in _dirs or 'sw' in _dirs or 'se' in _dirs or 'nw' in _dirs \
                    or 'd' in _dirs:
                tools.feedback(
                    'No diagonal hatching permissible with rounding in the rectangle',
                    True)
        # ---- check spacing
        if self.rounding or self.rounded:
            spacing = max(self._u.width / (num + 1), self._u.height / (num + 1))
            if self.rounding:
                _rounding = self.unit(self.rounding)
            elif self.rounded:
                _rounding = self._u.width * 0.08
            if spacing < _rounding:
                tools.feedback(
                    'No hatching permissible with this size rounding in the rectangle',
                    True)
        if self.notch or self.notch_x or self.notch_y:
            tools.feedback('No hatching permissible with a notched Rectangle', True)
        # ---- set canvas
        self.set_canvas_props(
            index=ID,
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_width,
            stroke_cap=self.hatch_cap)
        # ---- draw items
        if num >= 1:
            # breakpoint()
            if 'ne' in _dirs or 'sw' in _dirs or 'd' in _dirs:  # UP to the right
                pth = cnv.beginPath()
                pth.moveTo(vertices[0].x, vertices[0].y)
                pth.lineTo(vertices[2].x, vertices[2].y)
                cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
            if 'se' in _dirs or 'nw' in _dirs or 'd' in _dirs:  # DOWN to the right
                pth = cnv.beginPath()
                pth.moveTo(vertices[1].x, vertices[1].y)
                pth.lineTo(vertices[3].x, vertices[3].y)
                cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
            if 'n' in _dirs or 's' in _dirs or 'o' in _dirs:  # vertical
                x_dist = self._u.width / (num + 1)
                for i in range(1, num + 1):
                    pth = cnv.beginPath()
                    pth.moveTo(vertices[0].x + i * x_dist, vertices[1].y)
                    pth.lineTo(vertices[0].x + i * x_dist, vertices[0].y)
                    cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
            if 'e' in _dirs or 'w' in _dirs or 'o' in _dirs:  # horizontal
                y_dist = self._u.height / (num + 1)
                for i in range(1, num + 1):
                    pth = cnv.beginPath()
                    pth.moveTo(vertices[0].x, vertices[0].y + i * y_dist)
                    pth.lineTo(vertices[0].x + self._u.width, vertices[0].y + i * y_dist)
                    cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
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

        if 'ne' in _dirs or 'sw' in _dirs or 'd' in _dirs:  # slope UP to the right
            for i in range(1, diag_num):  # top-left side
                j = diag_num - i
                pth = cnv.beginPath()
                pth.moveTo(left_pt[i].x, left_pt[i].y)
                pth.lineTo(top_pt[j].x, top_pt[j].y)
                cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
            for i in range(1, diag_num):  # bottom-right side
                j = diag_num - i
                pth = cnv.beginPath()
                pth.moveTo(btm_pt[i].x, btm_pt[i].y)
                pth.lineTo(rite_pt[j].x, rite_pt[j].y)
                cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        if 'se' in _dirs or 'nw' in _dirs or 'd' in _dirs:  # slope down to the right
            for i in range(1, diag_num):  # bottom-left side
                pth = cnv.beginPath()
                pth.moveTo(left_pt[i].x, left_pt[i].y)
                pth.lineTo(btm_pt[i].x, btm_pt[i].y)
                cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
            for i in range(1, diag_num):  # top-right side
                pth = cnv.beginPath()
                pth.moveTo(top_pt[i].x, top_pt[i].y)
                pth.lineTo(rite_pt[i].x, rite_pt[i].y)
                cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a rectangle on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- set canvas
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # ---- validate properties
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
        # ---- calculate properties
        x, y = self.calculate_xy()
        # ---- overrides for grid layout
        if self.use_abs_c:
            x = self._abs_cx - self._u.width / 2.0
            y = self._abs_cy - self._u.height / 2.0
        x_d = x + self._u.width / 2.0  # centre
        y_d = y + self._u.height / 2.0  # centre
        self.area = self.calculate_area()
        delta_m_up, delta_m_down = 0.0, 0.0  # potential text offset from chevron
        # ---- handle rotation: START
        rotation = kwargs.get('rotation', self.rotation)
        # print(self.label, rotation)
        if rotation:
            # tools.feedback(f'*** Rect {ID=} {rotation=} {self._u.x=}, {self._u.y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                cnv.translate(x + self._u.margin_left, y + self._u.margin_bottom)
            else:
                cnv.translate(x + self._u.width / 2.0, y + self._u.height / 2.0)
            cnv.rotate(rotation)
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
            cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
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
            vertices = self.set_vertices(rotation=rotation, **kwargs)
            self.draw_hatch(cnv, ID, vertices, self.hatch)
        # ---- grid marks
        self.set_canvas_props(
            index=ID,
            stroke=self.grid_stroke,
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
        if kwargs and kwargs.get('rotation'):
            kwargs.pop('rotation')  # otherwise labels rotate again!
        self.draw_heading(cnv, ID, x_d, y_d + 0.5 * self._u.height + delta_m_up, **kwargs)
        self.draw_label(cnv, ID, x_d, y_d, **kwargs)
        self.draw_title(cnv, ID, x_d, y_d - 0.5 * self._u.height - delta_m_down, **kwargs)
        # ----  numbering
        self.set_coord(cnv, x_d, y_d)
        # ---- handle rotation: END
        if rotation:
            cnv.restoreState()
        # ---- set grid property
        self.grid = GridShape(label=self.coord_text, x=x_d, y=y_d, shape=self)


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
        cx = x + self._u.width / 2.0
        cy = y + self._u.height / 2.0
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- calculated properties
        self.area = (self._u.width * self._u.height) / 2.0
        # ---- handle rotation: START
        rotation = kwargs.get('rotation', self.rotation)
        if rotation:
            # tools.feedback(f'*** IMAGE {ID=} {rotation=} {self._u.x=}, {self._u.y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                #cnv.translate(cx + self._u.margin_left, cy + self._u.margin_bottom)
                cnv.translate(cx, cy)
            else:
                cnv.translate(cx, cy)
            cnv.rotate(rotation)
            # reset centre and "bottom left"
            cx, cy = 0, 0
            x = -self._u.width / 2.0
            y = -self._u.height / 2.0
        # ---- draw rhombus
        x_s, y_s = x, y + self._u.height / 2.0
        pth = cnv.beginPath()
        pth.moveTo(x_s, y_s)
        pth.lineTo(x_s + self._u.width / 2.0, y_s + self._u.height / 2.0)
        pth.lineTo(x_s + self._u.width, y_s)
        pth.lineTo(x_s + self._u.width / 2.0, y_s - self._u.height / 2.0)
        pth.lineTo(x_s, y_s)
        pth.close()
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- dot
        self.draw_dot(cnv, x + self._u.width / 2.0, y + self._u.height / 2.0)
        # ---- text
        self.draw_heading(cnv, ID, x + self._u.width / 2.0, y + self._u.height, **kwargs)
        self.draw_label(cnv, ID, x + self._u.width / 2.0, y + self._u.height / 2.0, **kwargs)
        self.draw_title(cnv, ID, x + self._u.width / 2.0, y, **kwargs)
        # ---- handle rotation: END
        if rotation:
            cnv.restoreState()


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
        if hand == 'west':
            x2 = x - self._u.width
        elif hand == 'east':
            x2 = x + self._u.width
        if flip == 'north':
            y2 = y + self._u.height
        elif flip == 'south':
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
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        x_c, y_c = x_sum / 3.0, y_sum / 3.0  # centroid
        # ---- dot
        self.draw_dot(cnv, x_c, y_c)
        # ---- text
        self.draw_label(cnv, ID, x_c, y_c, **kwargs)


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
            cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)


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
        # tools.feedback(f'@Square@ {self.label=} // {off_x=}, {off_y=} {kwargs=}')
        return super().draw(cnv, off_x, off_y, ID, **kwargs)


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
        cx = x + self._u.width / 2.0
        cy = y + self._u.height / 2.0
        # ---- handle rotation: START
        rotation = kwargs.get('rotation', self.rotation)
        if rotation:
            # tools.feedback(f'*** IMAGE {ID=} {rotation=} {self._u.x=}, {self._u.y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                #cnv.translate(cx + self._u.margin_left, cy + self._u.margin_bottom)
                cnv.translate(cx, cy)
            else:
                cnv.translate(cx, cy)
            cnv.rotate(rotation)
            # reset centre and "bottom left"
            cx, cy = 0, 0
            x = -self._u.width / 2.0
            y = -self._u.height / 2.0
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
            if count == 2 and ('w' in _edges or 'west' in _edges):
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
            elif count == 1 and ('n' in _edges or 'north' in _edges):
                cx, cy = vertex.x - 0.5 * self._u.width, vertex.y
                right_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_tb, radius_tb, 0, 90)
                left_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_tb, radius_tb, 90, 180)
                pth.moveTo(*vertex)
                pth.curveTo(*right_curve[1])
                pth.curveTo(*left_curve[1])
            elif count == 3 and ('s' in _edges or 'south' in _edges):
                cx, cy = vertex.x + 0.5 * self._u.width, vertex.y
                left_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_tb, radius_tb, 180, 270)
                right_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_tb, radius_tb, 270, 360)
                pth.moveTo(*vertex)
                pth.curveTo(*left_curve[1])
                pth.curveTo(*right_curve[1])
                pth.moveTo(*self.vertices[3])
            elif count == 0 and ('e' in _edges or 'east' in _edges):
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
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- cross
        self.draw_cross(cnv,  x + self._u.width / 2.0, y + self._u.height / 2.0)
        # ---- dot
        self.draw_dot(cnv, x + self._u.width / 2.0, y + self._u.height / 2.0)
        # ---- text
        delta = radius_tb if 'n' in _edges or 'north' in _edges else 0.
        self.draw_heading(cnv, ID, x + self._u.width / 2.0, y + self._u.height + delta, **kwargs)
        self.draw_label(cnv, ID, x + self._u.width / 2.0, y + self._u.height / 2.0, **kwargs)
        self.draw_title(cnv, ID, x + self._u.width / 2.0, y - delta, **kwargs)
        # ---- handle rotation: END
        if rotation:
            cnv.restoreState()


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
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- dot
        self.draw_dot(cnv, x, y)
        # ---- text
        self.draw_heading(cnv, ID, x,  y + radius, **kwargs)
        self.draw_label(cnv, ID, x, y, **kwargs)
        self.draw_title(cnv, ID, x, y - radius, **kwargs)


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
        rotation = kwargs.get('rotation', self.rotation)
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- overrides for text value
        _sequence = kwargs.get('text_sequence', '')
        # tools.feedback(f'*** {_sequence=} {self.text=}')
        if self.text == '' or self.text is None:
            self.text = f'{_sequence}'
        _text = self.textify(ID)
        if _text is None:
            return
        _text = str(_text)  # card data could be numeric
        #tools.feedback(f'*** {_sequence=} {self.text=} {_text}')
        if '\\u' in _text:
             _text = codecs.decode(_text, 'unicode_escape')
        _text = _text.format(SEQUENCE=_sequence)
        # ---- text style
        if self.wrap:
            _style = ParagraphStyle(name="sc")
            _style.textColor = self.stroke
            _style.backColor = self.fill
            _style.borderColor = self.outline_stroke
            _style.borderWidth = self.outline_width
            _style.alignment = self.to_alignment()
            _style.fontSize = self.font_size
            _style.fontName = self.font_face
            _style.leading = self.leading
            """
            # potential other properties
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Times-Roman',
            bulletFontSize=10,
            bulletIndent=0,
            borderPadding= 0,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,
            splitLongWords=1,
            """
            # tools.feedback(f'*** LONG-{ID} => text:{_text}')
            para = Paragraph(_text, style=_style)
            w, h = para.wrap(width, height)
            para.drawOn(cnv, x_t, y_t - h)  # start text from top of 'box'
        else:
            # tools.feedback(f"*** {x_t=} {y_t=} {_text=} {_sequence} {rotation=}")
            cnv.setFillColor(self.stroke)
            self.draw_multi_string(cnv, x_t, y_t, _text, rotation=rotation)

# ---- Other


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
