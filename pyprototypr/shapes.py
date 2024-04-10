#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create custom shapes for pyprototypr
"""
# lib
import logging
import math
import random

# third party
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

# local
from pyprototypr.utils.tools import Point
from pyprototypr.utils import tools
from pyprototypr.base import BaseShape, BaseCanvas, UNITS, COLORS, PAGES

log = logging.getLogger(__name__)


DEBUG = False


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


class ImageShape(BaseShape):
    """
    Image (bitmap or SVG) on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Show an image on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        img = None
        # convert to using units
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
        # tools.feedback(f'{self.scaling} scaling')
        img, is_svg = self.load_image(self.source, self.scaling)
        if img:
            # assumes 1 pt == 1 pixel ?
            if is_svg:
                from reportlab.graphics import renderPDF
                renderPDF.draw(img, cnv, x=x, y=y)
            else:
                cnv.drawImage(img, x=x, y=y, width=width, height=height, mask="auto")
        # ---- text
        xc = x + width / 2.0
        if self.label:
            cnv.setFont(self.font_face, self.label_size)
            cnv.setFillColor(self.label_stroke)
            self.draw_multi_string(cnv, xc, y + height / 2.0, self.label)
        if self.title:
            cnv.setFont(self.font_face, self.title_size)
            cnv.setFillColor(self.title_stroke)
            self.draw_multi_string(cnv, xc, y - cnv._leading, self.title)
        if self.heading:
            cnv.setFont(self.font_face, self.heading_size)
            cnv.setFillColor(self.heading_stroke)
            self.draw_multi_string(cnv, xc, y + height + cnv._leading, self.heading)


class LineShape(BaseShape):
    """
    Line on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a line on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        x = self._u.x + self._o.delta_x
        y = self._u.y + self._o.delta_y
        if self.x_1 and self.y_1:
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
        # canvas
        self.set_canvas_props()
        # ---- draw line
        pth = cnv.beginPath()
        pth.moveTo(x, y)
        pth.lineTo(x_1, y_1)
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        # ----  text
        self.draw_label(cnv, (x_1 + x) / 2.0, (y_1 + y) / 2.0)
        # ----  dot
        self.draw_dot(cnv, (x_1 + x) / 2.0, (y_1 + y) / 2.0)


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
        x = self._u.x + self._o.delta_x
        y = self._u.y + self._o.delta_y
        if self.x_1 and self.y_1:
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
        # canvas
        self.set_canvas_props()
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
        # ---- text
        self.draw_label(cnv, (x_1 + x) / 2.0, (y_1 + y) / 2.0)
        # ---- dot
        self.draw_dot(cnv, (x_1 + x) / 2.0, (y_1 + y) / 2.0)


class RhombusShape(BaseShape):
    """
    Rhombus on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a rhombus (diamond) on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        if self.cx and self.cy:
            x = self._u.cx - self._u.width / 2.0 + self._o.delta_x
            y = self._u.cy - self._u.height / 2.0 + self._o.delta_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        # canvas
        self.set_canvas_props()
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
        # ---- text
        self.draw_label(cnv, x + self._u.width / 2.0, y + self._u.height / 2.0)
        # ---- dot
        self.draw_dot(cnv, x + self._u.width / 2.0, y + self._u.height / 2.0)


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

    def draw_hatching(self, cnv, vertices: list, num: int):
        from reportlab.lib.colors import black, blue, red
        if self.rounding or self.rounded:
            tools.feedback('No hatching permissible with a rounded Rectangle', True)
        self.set_canvas_props(
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_width,
            stroke_cap=self.hatch_cap)
        _dirs = self.hatch_directions.lower().split()
        if num >=1:
            if 'ne' or 'sw' in _dirs:  # slope UP to the right
                pth = cnv.beginPath()
                pth.moveTo(vertices[0].x, vertices[0].y)
                pth.lineTo(vertices[2].x, vertices[2].y)
                cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
            if 'se' or 'nw' in _dirs:  # slope down to the right
                pth = cnv.beginPath()
                pth.moveTo(vertices[1].x, vertices[1].y)
                pth.lineTo(vertices[3].x, vertices[3].y)
                cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
            if 'n' or 's' in _dirs:  # vertical
                x_dist = self._u.width / (num + 1)
                for i in range(1, num + 1):
                    pth = cnv.beginPath()
                    pth.moveTo(vertices[0].x + i * x_dist, vertices[1].y)
                    pth.lineTo(vertices[0].x + i * x_dist, vertices[0].y)
                    cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
            if 'e' or 'w' in _dirs:  # horizontal
                y_dist = self._u.height / (num + 1)
                for i in range(1, num + 1):
                    pth = cnv.beginPath()
                    pth.moveTo(vertices[0].x, vertices[0].y + i * y_dist)
                    pth.lineTo(vertices[0].x + self._u.width, vertices[0].y + i * y_dist)
                    cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        if num >= 2:
            diag_num = int((num - 1) / 2 + 1)
            x_dist = self._u.width / diag_num
            y_dist = self._u.height / diag_num
            top_pt, btm_pt, left_pt, rite_pt = [], [],[], []
            for number in range(0, diag_num + 1):
                left_pt.append(
                    tools.point_on_line(vertices[0], vertices[1], y_dist * number))
                top_pt.append(
                    tools.point_on_line(vertices[1], vertices[2], x_dist * number))
                rite_pt.append(
                    tools.point_on_line(vertices[3], vertices[2], y_dist * number))
                btm_pt.append(
                    tools.point_on_line(vertices[0], vertices[3], x_dist * number))

        if 'ne' or 'sw' in _dirs:  # slope UP to the right
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

        if 'se' or 'nw' in _dirs:  # slope down to the right
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
        # ---- adjust start
        if self.row is not None and self.col is not None:
            x = self.col * self._u.width + self._o.delta_x
            y = self.row * self._u.height + self._o.delta_y
        elif self.cx and self.cy:
            x = self._u.cx - self._u.width / 2.0 + self._o.delta_x
            y = self._u.cy + self._u.height / 2.0 + self._o.delta_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        # ---- overrides to centre the shape
        if kwargs.get("cx") and kwargs.get("cy"):
            x = self._u.cx - self._u.width / 2.0
            y = self._u.cy - self._u.height / 2.0
        # ---- calculated properties
        self.area = self.calculate_area()
        self.vertices = [  # clockwise from bottom-left; relative to centre
            Point(x, y),
            Point(x, y + self._u.height),
            Point(x + self._u.width, y + self._u.height),
            Point(x + self._u.width, y),
        ]
        # canvas
        self.set_canvas_props()
        # ---- draw rectangle
        if self.rounding:
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
        # ---- draw hatches
        if self.hatch:
            self.draw_hatching(cnv, self.vertices, self.hatch)
        # ---- grid marks
        self.set_canvas_props(
            stroke=self.grid_color, stroke_width=self.grid_stroke_width)
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
        # ---- text
        self.draw_label(cnv, x + self._u.width / 2.0, y + self._u.height / 2.0)
        # ---- dot
        self.draw_dot(cnv, x + self._u.width / 2.0, y + self._u.height / 2.0)


# class SquareShape(BaseShape):
#     pass

#     def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
#         """Draw a square on a given canvas."""
#         pass

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

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a square on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)


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
        if kwargs.get("cx") and kwargs.get("cy"):
            x = self.unit(kwargs.get("cx")) - self._u.width / 2.0 + self._o.delta_x
            y = self.unit(kwargs.get("cy")) + self._u.height / 2.0 + self._o.delta_y
            c_x = self.unit(kwargs.get("cx")) + self._o.delta_x
            c_y = self.unit(kwargs.get("cy")) + self._o.delta_y
        # ---- calculated properties
        side = self._u.height / (1 + math.sqrt(2.0))
        self.area = self.calculate_area()
        zzz = math.sqrt((side * side) / 2.0)
        self.vertices = [  # clockwise from bottom-left; relative to centre
            (c_x - side / 2.0, c_y - self._u.height / 2.0),  # 1
            (c_x - self._u.width / 2.0, c_y - self._u.height / 2.0 + zzz),  # 2
            (c_x - self._u.width / 2.0, c_y - self._u.height / 2.0 + zzz + side),  # 3
            (c_x - side / 2.0, c_y + self._u.height / 2.0),  # 4
            (c_x + side / 2.0, c_y + self._u.height / 2.0),  # 5
            (c_x + self._u.width / 2.0, c_y - self._u.height / 2.0 + zzz + side),  # 6
            (c_x + self._u.width / 2.0, c_y - self._u.height / 2.0 + zzz),  # 7
            (c_x + side / 2.0, c_y - self._u.height / 2.0),  # 8
        ]
        # canvas
        self.set_canvas_props()
        # ---- draw octagon
        pth = cnv.beginPath()
        pth.moveTo(*self.vertices[0])
        for vertex in self.vertices:
            pth.lineTo(*vertex)
        pth.close()
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        # ---- text
        self.draw_label(cnv, x + self._u.width / 2.0, y + self._u.height / 2.0)
        # ---- dot
        self.draw_dot(cnv, x + self._u.width / 2.0, y + self._u.height / 2.0)


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
        # canvas
        self.set_canvas_props()
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
        # convert to using units
        x_1 = self._u.x + self._o.delta_x
        y_1 = self._u.y + self._o.delta_y
        if not self.x_1:
            self.x_1 = self.x + self.default_length
        if not self.y_1:
            self.y_1 = self.y + self.default_length
        x_2 = self.unit(self.x_1) + self._o.delta_x
        y_2 = self.unit(self.y_1) + self._o.delta_y
        # canvas
        self.set_canvas_props()
        # ---- draw arc
        cnv.arc(x_1, y_1, x_2, y_2)


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
            self.y_1 = self.y + self.default_length
        x_2 = self.unit(self.x_1) + self._o.delta_x
        y_2 = self.unit(self.y_1) + self._o.delta_y
        x_3 = self.unit(self.x_2) + self._o.delta_x
        y_3 = self.unit(self.y_2) + self._o.delta_y
        x_4 = self.unit(self.x_3) + self._o.delta_x
        y_4 = self.unit(self.y_3) + self._o.delta_y
        # canvas
        self.set_canvas_props()
        # ---- draw bezier
        cnv.bezier(x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4)


class PolygonShape(BaseShape):
    """
    Regular polygon on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a regular polygon on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # convert to using units
        x = self._u.x + self._o.delta_x
        y = self._u.y + self._o.delta_y
        # calc - assumes x and y are the centre
        if self.radius:
            radius = self._u.radius
        else:
            side = self._u.side
            sides = int(self.sides)
            # 180 degrees is math.pi radians
            radius = side / (2.0 * math.sin(math.pi / sides))
        vertices = tools.polygon_vertices(self.sides, radius, self.rotate, (x, y))
        if not vertices or len(vertices) == 0:
            return
        # canvas
        self.set_canvas_props()
        # ---- draw polygon
        pth = cnv.beginPath()
        pth.moveTo(*vertices[0])
        for vertex in vertices:
            pth.lineTo(*vertex)
        pth.close()
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        # ---- text
        self.draw_label(cnv, x, y)
        self.draw_title(cnv, x, y, 1.4 * radius)
        self.draw_heading(cnv, x, y, 1.3 * radius)
        # ---- dot
        self.draw_dot(cnv, x, y)


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
        # canvas
        self.set_canvas_props()
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

    def draw_coord(self, cnv, x_d, y_d, half_flat):
        """Draw the coord inside the hexagon."""
        if self.coord_position:
            # ---- set coord value
            _row = self.hex_rows - self.row + self.coord_start_y
            _col = self.col + 1 if not self.coord_start_x else self.col + self.coord_start_x
            _x = tools.sheet_column(_col, True) \
                if self.coord_type_x in ['l', 'lower'] else tools.sheet_column(_col)
            _y = tools.sheet_column(_row, True) \
                if self.coord_type_y in ['l', 'lower'] else tools.sheet_column(_row)
            if self.coord_type_x in ['n', 'number']:
                _x = str(_col).zfill(self.coord_padding)
            if self.coord_type_y in ['n', 'number']:
                _y = str(_row).zfill(self.coord_padding)
            _coord_text = str(self.coord_prefix) + _x + str(self.coord_separator) + _y
            # ---- set coord props
            cnv.setFont(self.coord_font_face, self.coord_font_size)
            cnv.setFillColor(self.coord_stroke)
            # ---- draw coord
            coord_offset = self.unit(self.coord_offset)
            if self.coord_position in ['t', 'top']:
                self.draw_multi_string(
                    cnv, x_d, y_d + half_flat * 0.7 + coord_offset, _coord_text)
            elif self.coord_position in ['m', 'middle', 'mid']:
                self.draw_multi_string(
                    cnv, x_d, y_d + coord_offset - self.coord_font_size / 2.0, _coord_text)
            elif self.coord_position in ['b', 'bottom', 'bot']:
                self.draw_multi_string(
                    cnv, x_d, y_d - half_flat * 0.9 + coord_offset, _coord_text)
            else:
                tools.feedback(
                    f'Cannot handle a coord_position of "{self.coord_position}"')

    def calculate_area(self):
        if self.side:
            side = self._u.side
        elif self.height:
            side = self._u.height / math.sqrt(3)
        return (3.0 * math.sqrt(3.0) * side * side) / 2.0

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a hexagon on a given canvas."""
        # tools.feedback(f'Will draw a hex shape: {kwargs} {off_x} {off_y} {ID}')
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        is_cards = kwargs.get("is_cards", False)
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # ---- calculate half_flat & half_side from self.side, self.diameter, self.height
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
        # ---- POINTY
        if self.hex_orientation.lower() in ['p', 'pointy']:
            #         /\
            # x,y .. | |
            #        \/
            # x and y are at the bottom-left corner of the box around the hex
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
            # ---- + draw pointy by row/col
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
                    if (self.row + 1) & 1:  # odd row; row are 0-base numbered!
                        x = self.col * height_flat + half_flat + self._u.x + self._o.delta_x
                    else:  # even row
                        x = self.col * height_flat  + self._u.x + self._o.delta_x
                else:  # self.hex_offset in ['e', 'E', 'even']
                    # downshift applies from first even row - NOT the very first one!
                    downshift = diameter - z_fraction if self.row >=1 else 0
                    downshift = downshift * self.row if self.row >=2 else downshift
                    y = self.row * (diameter + side) - downshift + self._u.y + self._o.delta_y
                    if (self.row + 1) & 1:  # odd row; row are 0-base numbered!
                        x = self.col * height_flat + self._u.x + self._o.delta_x
                    else:  # even row
                        x = self.col * height_flat + half_flat + self._u.x + self._o.delta_x

            # ---- + calculate hex centre
            x_d = x + half_flat
            y_d = y + side
            # tools.feedback(f"{x=} {y=} {half_flat=} {side=} ")
            if self.cx and self.cy:
                # cx,cy are centred; create x_d,y_d as the unit-formatted hex centre
                x_d = self._u.cx
                y_d = self._u.cy
                x = x_d - half_flat + self._o.delta_x
                y = y_d - side + self._o.delta_y
            # ---- FLAT
        else:
            #         __
            # x,y .. /  \
            #        \__/
            # x and y are at the bottom-left corner of the box around the hex
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
            # tools.feedback(f"{x=} {y=} {half_flat=} {side=} {self.row=} {self.col=}")
            # ---- + draw flat by row/col
            if self.row is not None and self.col is not None and is_cards:
                x = self.col * 2.0 * side + self._o.delta_x
                y = half_flat + self.row * 2.0 * half_flat + self._o.delta_x
            elif self.row is not None and self.col is not None:
                if self.hex_offset in ['o', 'O', 'odd']:
                    x = self.col * (half_side + side) + self._u.x + self._o.delta_x
                    y = self.row * half_flat * 2.0 + self._u.y + self._o.delta_y
                    if (self.col + 1) & 1:  # odd
                        y = y + half_flat
                else:  # self.hex_offset in ['e', 'E', 'even']
                    x = self.col * (half_side + side) + self._u.x + self._o.delta_x
                    y = self.row * half_flat * 2.0 + self._u.y + self._o.delta_y
                    if (self.col + 1) & 1:  # odd
                        pass
                    else:
                        y = y + half_flat
            # ----  + calculate hex centre
            x_d = x + side
            y_d = y + half_flat
            # ----  + recalculate centre if preset
            if self.cx and self.cy:
                # cx,cy are centred; create x_d,y_d as the unit-formatted hex centre
                x_d = self._u.cx
                y_d = self._u.cy
                x = x_d - half_side - side / 2.0 + self._o.delta_x
                y = y_d + self._o.delta_y
            # log.debug("x:%s y:%s hh:%s hs:%s s:%s ", x, y, half_flat, half_side, side)
        # ---- calculate area
        self.area = self.calculate_area()
        # ---- canvas
        self.set_canvas_props()
        if self.caltrops or self.caltrops_fraction:
            line_dashes = self.calculate_caltrops(
                self.side, self.caltrops, self.caltrops_fraction, self.caltrops_invert)
            cnv.setDash(array=line_dashes)
        # ---- calculate vertical hexagon (clockwise)
        if self.hex_orientation.lower() in ['p', 'pointy']:
            self.vertices = [  # clockwise from bottom-left; relative to centre
                Point(x, y + z_fraction),
                Point(x, y + z_fraction + side),
                Point(x + half_flat, y + diameter),
                Point(x + height_flat, y + z_fraction + side),
                Point(x + height_flat, y + z_fraction),
                Point(x + half_flat, y),
            ]
        # ---- calculate horizontal hexagon (clockwise)
        else:   # self.hex_orientation.lower() in ['f',  'flat']:
            self.vertices = [  # clockwise from left; relative to centre
                Point(x, y + half_flat),
                Point(x + z_fraction, y + height_flat),
                Point(x + z_fraction + side, y + height_flat),
                Point(x + diameter, y + half_flat),
                Point(x + z_fraction + side, y),
                Point(x + z_fraction, y),
            ]
        # ---- draw hexagon
        # tools.feedback(f'{x=} {y=} {self.vertices=}')
        pth = cnv.beginPath()
        pth.moveTo(*self.vertices[0])
        for vertex in self.vertices:
            pth.lineTo(*vertex)
        pth.close()
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        # ---- centred shape (with offset)
        if self.centre_shape:
            # tools.feedback(f'DRAW shape:{self.dot_shape} at ({x_d=},{y_d=})')
            self.centre_shape.draw(
                cx=x_d + self.unit(self.centre_shape_x),
                cy=y_d + self.unit(self.centre_shape_y))
        # ---- text
        self.draw_label(cnv, x_d, y_d)
        self.draw_title(cnv, x_d, y_d, 1.4 * diameter / 2.0)
        self.draw_heading(cnv, x_d, y_d, 1.3 * diameter / 2.0)
        # ---- dot
        self.draw_dot(cnv, x_d, y_d)
        # ----  numbering
        self.draw_coord(cnv, x_d, y_d, half_flat)


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
        # calc - assumes x and y are the centre
        radius = self._u.radius
        # canvas
        self.set_canvas_props()
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
        # ---- text
        self.draw_label(cnv, x, y)
        if self.title:
            cnv.setFont(self.font_face, self.title_size)
            cnv.setFillColor(self.title_stroke)
            self.draw_multi_string(cnv, x, y - 1.4 * radius, self.title)
        if self.heading:
            cnv.setFont(self.font_face, self.heading_size)
            cnv.setFillColor(self.heading_stroke)
            self.draw_multi_string(cnv, x, y + 1.3 * radius, self.heading)
        # ---- dot
        self.draw_dot(cnv, x, y)


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
        points = []
        points.append((x, y))
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
        points.append((x2, y2))
        points.append((x2, y))
        # canvas
        self.set_canvas_props()
        # ---- draw RA triangle
        x_sum, y_sum = 0, 0
        pth = cnv.beginPath()
        for key, vertex in enumerate(points):
            x, y = vertex
            # shift to relative position
            x = x + self._o.delta_x
            y = y + self._o.delta_y
            x_sum += x
            y_sum += y
            if key == 0:
                pth.moveTo(x, y)
            pth.lineTo(x, y)
        pth.close()
        cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
        x_c, y_c = x_sum / 3.0, y_sum / 3.0  # centroid
        # ---- text
        self.draw_label(cnv, x_c, y_c)
        # ---- dot
        self.draw_dot(cnv, x_c, y_c)


class EquilateralTriangleShape(BaseShape):
    pass

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an equilateraltriangle on a given canvas."""
        pass


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
        # convert to using units
        x_t = self._u.x + self._o.delta_x
        y_t = self._u.y + self._o.delta_y
        if self.height:
            height = self._u.height
        if self.width:
            width = self._u.width
        # canvas
        self.set_canvas_props(cnv)
        # text
        _text = self.textify(ID)
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
            leading=12,
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
            para.wrapOn(cnv, width, height)
            para.drawOn(cnv, x_t, y_t)
        else:
            cnv.setFillColor(self.stroke)
            self.draw_multi_string(cnv, x_t, y_t, _text)


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
            self.width = 2.0 * self.radius
            self.height = 2.0 * self.radius
        # ---- calcuate centre
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

    def __str__(self):
        return f'{self.__class__.__name__}::{self.kwargs}'

    def calculate_area(self):
        return math.pi * self._u.radius * self._u.radius

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw circle on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # ---- calculated properties
        self.area = self.calculate_area()
        if self._o.delta_x or self._o.delta_y:
            self.x_c = self.x_c + self._o.delta_x
            self.y_c = self.y_c + self._o.delta_y
        # canvas
        self.set_canvas_props()
        # ---- draw circle
        cnv.circle(
            self.x_c, self.y_c, self._u.radius, stroke=1, fill=1 if self.fill else 0)
        # ---- text
        self.draw_label(cnv, self.x_c, self.y_c)
        self.draw_title(cnv, self.x_c, self.y_c, 1.4 * self._u.radius)
        self.draw_heading(cnv, self.x_c, self.y_c, 1.3 * self._u.radius)
        # ---- dot
        self.draw_dot(cnv, self.x_c, self.y_c)


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
        # tools.feedback(f'{ranges=}')
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
        # tools.feedback(f'{self.x_c=}, {self.y_c=}')
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
        if self.row is not None and self.col is not None:
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
        # canvas
        self.set_canvas_props()
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

        # ---- text
        self.draw_label(cnv, self.x_c, self.y_c)
        self.draw_title(cnv, self.x_c, self.y_c, 1.4 * radius)
        self.draw_heading(cnv, self.x_c, self.y_c, 1.3 * radius)
        # ---- dot
        self.draw_dot(cnv, self.x_c, self.y_c)


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
        # canvas
        self.set_canvas_props()
        # ---- draw ellipse
        cnv.ellipse(x_1, y_1, x_2, y_2, stroke=1, fill=1 if self.fill else 0)
        x_c = (x_2 - x_1) / 2.0 + x_1
        y_c = (y_2 - y_1) / 2.0 + y_1
        # ---- text
        self.draw_label(cnv, x_c, y_c)
        # ---- dot
        self.draw_dot(cnv, x_c, y_c)


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
        # tools.feedback(f'{color=} {size=} {position=}')
        cnv.setFillColor(color)
        cnv.setStrokeColor(color)
        cnv.circle(position.x, position.y, size, stroke=1, fill=1)

    def cluster_stars(self, cnv):
        tools.feedback('CLUSTER NOT IMPLEMENTED', True)
        for star in range(0, self.star_count):
            pass

    def random_stars(self, cnv):
        # tools.feedback(f'{self.enclosure=}')
        for star in range(0, self.star_count):
            if isinstance(self.enclosure, RectangleShape):
                x_y = Point(
                    random.random() * self.enclosure._u.width + self._o.delta_x,
                    random.random() * self.enclosure._u.height + self._o.delta_y
                    )
            elif isinstance(self.enclosure, CircleShape):
                r_fraction = random.random() * self.enclosure._u.radius
                angle = math.radians(random.random() * 360.0)
                x = r_fraction * math.cos(angle) + self.enclosure.x_c + self._o.delta_x
                y = r_fraction * math.sin(angle) + self.enclosure.y_c + self._o.delta_y
                x_y = Point(x, y)
            else:
                tools.feedback(f'{self.enclosure} IS NOT IMPLEMENTED', True)
            self.draw_star(cnv, x_y)

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
        # tools.feedback(f'{self.star_pattern =} {self.enclosure}')
        # tools.feedback(f'{area=} {self.density=} {self.star_count=}')
        # ---- set canvas
        self.set_canvas_props()
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
        # convert to using units
        x = self._u.x + self._o.delta_x
        y = self._u.y + self._o.delta_y
        height = self._u.height  # of each grid item
        width = self._u.width  # of each grid item
        if self.size:  # square grid
            size = self.unit(self.size)
            height, width = size, size
        y_cols, x_cols = [], []
        for y_col in range(0, self.rows + 1):
            y_cols.append(y + y_col * height)
        for x_col in range(0, self.cols + 1):
            x_cols.append(x + x_col * width)
        # canvas
        self.set_canvas_props()
        # ---- draw grid
        cnv.grid(x_cols, y_cols)  # , stroke=1, fill=1)


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


# ---- deck/card related-----


class CardShape(BaseShape):
    """
    Card shape on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(CardShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.elements = []  # container for objects which get added to the card
        self.height = kwargs.get("height", 8.8)
        self.width = kwargs.get("width", 6.3)
        self.kwargs.pop("width", None)
        self.kwargs.pop("height", None)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an element on a given canvas."""
        raise NotImplementedError

    def draw_card(self, cnv, row, col, cid):
        """Draw a card on a given canvas."""
        log.debug("Card cnv:%s r:%s c:%s id:%s shp:%s", cnv, row, col, cid, self.shape)
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
        for flat_ele in flat_elements:
            log.debug("flat_ele %s", flat_ele)
            members = flat_ele.members or self.members
            try:  # - normal element
                iid = members.index(cid + 1)
                flat_ele.draw(
                    cnv=cnv, off_x=col * self.width, off_y=row * self.height, ID=iid
                )
            except AttributeError:
                # query ... get a new element ... or not!?
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
            except ValueError:
                tools.feedback(f"Unable to draw card #{cid + 1}.")
            except Exception as err:
                tools.feedback(f"Unable to draw card #{cid + 1}. (Error:{err})")


class DeckShape(BaseShape):
    """
    Placeholder for the deck design; list of CardShapes and Shapes.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(DeckShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # page
        self.page_width = self.pagesize[0] / self.units
        self.page_height = self.pagesize[1] / self.units
        # cards
        self.deck = []  # container for CardShape objects
        self.cards = kwargs.get("cards", 9)  # default total number of cards
        self.height = kwargs.get("height", 8.8)  # OVERWRITE
        self.width = kwargs.get("width", 6.3)  # OVERWRITE
        self.sequence = kwargs.get("sequence", [])  # e.g. "1-2" or "1-5,8,10"
        self.template = kwargs.get("template", None)
        # user provided-rows and -columns
        self.card_rows = kwargs.get("rows", None)
        self.card_cols = kwargs.get("cols", kwargs.get("columns", None))
        # data file
        self.data_file = kwargs.get("data", None)
        self.data_cols = kwargs.get("data_cols", None)
        self.data_rows = kwargs.get("data_rows", None)
        self.data_header = kwargs.get("data_header", True)
        # GO!
        self.create(self.cards)

    def create(self, cards):
        """Create a new deck, based on number of `cards`"""
        log.debug("Cards are: %s", self.sequence)
        self.deck = []
        log.debug("deck %s cards with kwargs %s", cards, self.kwargs)
        for card in range(0, cards):
            _card = CardShape(**self.kwargs)
            _card.shape_id = card
            self.deck.append(_card)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        cnv = cnv if cnv else self.canvas
        log.debug("Deck cnv:%s type:%s", type(self.canvas), type(cnv))
        # user-defined rows and cols
        max_rows = self.card_rows
        max_cols = self.card_cols
        # calculate rows/cols based on page size and margins
        if not max_rows:
            row_space = float(self.page_height) - self.margin_bottom - self.margin_top
            max_rows = int(row_space / float(self.height))
        if not max_cols:
            col_space = float(self.page_width) - self.margin_left - self.margin_right
            max_cols = int(col_space / float(self.width))
        log.debug("w:%s cs:%s mc:%s", self.page_width, col_space, max_cols)
        log.debug("h:%s rs:%s mr:%s", self.page_height, row_space, max_rows)
        row, col = 0, 0
        # generate cards
        for key, card in enumerate(self.deck):
            card.draw_card(cnv, row=row, col=col, cid=card.shape_id)
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


### repeats ===================================================================


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
        self.gap_across = self.gap_across or self.gap
        self.gap_down = self.gap_down or self.gap
        if self.repeat:
            (
                self.repeat_across,
                self.repeat_down,
                self.gap_down,
                self.gap_across,
                self.gap_across,
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
        log.debug("ga:%s gd:%s", self.gap_across, self.gap_down)

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
                    log.debug("fes:%s", flat_elements)
                    for flat_ele in flat_elements:
                        log.debug("fe:%s", flat_ele)
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

# ---- Other ----


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
        # overrides
        page_width = self.pagesize[0]
        self.kwargs["x"] = self.kwargs.get("x", page_width / 2.0)
        self.kwargs["y"] = self.margin_bottom / 2.0

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw footer on a given canvas page."""
        cnv = cnv if cnv else self.canvas
        if not self.kwargs.get("text"):
            self.kwargs["text"] = "Page %s" % ID
        text = TextShape(_object=None, canvas=cnv, kwargs=self.kwargs)
        text.draw()
