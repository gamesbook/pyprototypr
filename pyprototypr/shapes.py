#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create custom shapes for pyprototypr
"""
# future
from __future__ import division
# lib
import math
# third party
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
# local
from pyprototypr.utils import tools
from pyprototypr.base import BaseShape, BaseCanvas, UNITS, COLORS, PAGES


DEBUG = False


class Value(object):
    """Class wrapper for a list of values possible for a card attribute."""

    def __init__(self, **kwargs):
        self.datalist = kwargs.get('datalist', [])
        self.members = []  # card IDs, of which affected card is a member

    def __call__(self, cid):
        """Return datalist item number 'ID' (card number)."""
        #print "shapes_30", self.datalist, ID
        try:
            x = self.datalist[cid]
            return x
        except (ValueError, TypeError, IndexError):
            return None


class Query(object):
    """Query to select an element or a value for a card attribute."""

    def __init__(self, **kwargs):
        self.query = kwargs.get('query', [])
        self.result = kwargs.get('result', None)
        self.alternate = kwargs.get('alternate', None)
        self.members = []  # card IDs, of which affected card is a member

    def __call__(self, cid):
        """Process the query, for a given card 'ID' in the dataset."""
        #raise NotImplementedError
        result = None
        results = []
        for _query in self.query:
            if DEBUG: print "shapes_54 _query", len(_query), '::', _query
            if _query and len(_query) >= 4:
                result = tools.comparer(
                    val=_query[0][cid], operator=_query[1], target=_query[2])
            results.append(result)
            results.append(_query[3])
        # compare across all
        result = tools.boolean_join(results)
        #print "shapes_61 cid %s Results %s" % (cid, results)
        if result is not None:
            if result:
                return self.result
            else:
                return self.alternate
        else:
            tools.feedback('Query "%s" is incorrectly constructed.' %
                           self.query)


class ImageShape(BaseShape):
    """
    Show an image on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Show an image on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        img = None
        # offset
        margin_left = self.unit(self.margin_left)
        margin_bottom = self.unit(self.margin_bottom)
        off_x = self.unit(off_x)
        off_y = self.unit(off_y)
        delta_x = off_x + margin_left
        delta_y = off_y + margin_bottom
        # convert to using units
        height = self.unit(self.height, skip_none=True)
        width = self.unit(self.width, skip_none=True)
        if self.cx and self.cy and width and height:
            x = self.unit(self.cx) - width / 2.0 + delta_x
            y = self.unit(self.cy) - height / 2.0 + delta_y
        elif self.cx and self.cy and not(width or height):
            tools.feedback(
                'Must supply width and height for use with cx and cy',
                stop=True)
        else:
            x = self.unit(self.x) + delta_x
            y = self.unit(self.y) + delta_y
        # draw
        img = self.load_image(self.source)
        if img:
            # assumes 1 pt == 1 pixel ?
            cnv.drawImage(img, x=x, y=y, width=width, height=height,
                          mask='auto')
        # text
        xc = x + width / 2.0
        if self.label:
            cnv.setFont(self.font_face, self.label_size)
            cnv.setFillColor(self.stroke_label)
            self.draw_multi_string(cnv, xc, y + height / 2.0, self.label)
        if self.title:
            cnv.setFont(self.font_face, self.title_size)
            cnv.setFillColor(self.stroke_title)
            self.draw_multi_string(cnv, xc, y - cnv._leading, self.title)
        if self.heading:
            cnv.setFont(self.font_face, self.heading_size)
            cnv.setFillColor(self.stroke_heading)
            self.draw_multi_string(cnv, xc, y + height + cnv._leading,
                                   self.heading)


class LineShape(BaseShape):
    """
    Draw a line on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a line on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # offset
        margin_left = self.unit(self.margin_left)
        margin_bottom = self.unit(self.margin_bottom)
        off_x = self.unit(off_x)
        off_y = self.unit(off_y)
        delta_x = off_x + margin_left
        delta_y = off_y + margin_bottom
        # convert to using units
        x = self.unit(self.x) + delta_x
        y = self.unit(self.y) + delta_y
        height = self.unit(self.height)
        width = self.unit(self.width)
        #print "shapes_126 line", ID, ':margin:', uni, self.margin_left
        if self.length:
            length = self.unit(self.length)
            angle = math.radians(self.angle)
            x_1 = x + (length * math.cos(angle))
            y_1 = y + (length * math.sin(angle))
        else:
            if self.x_1:
                x_1 = self.unit(self.x_1) + delta_x
            else:
                x_1 = x + width
            if self.y_1:
                y_1 = self.unit(self.y_1) + delta_y
            else:
                y_1 = y + height
        if self.row is not None and self.row >= 0:
            y = y + self.row * height
            y_1 = y_1 + self.row * height - margin_bottom
        if self.col is not None and self.col >= 0:
            x = x + self.col * width
            x_1 = x_1 + self.col * width - margin_left
        #if DEBUG: print 165 self.row, self.col, "=", x, x_1, ":", y, y_1
        # canvas
        self.set_canvas_props()
        # draw line
        pth = cnv.beginPath()
        pth.moveTo(x, y)
        pth.lineTo(x_1, y_1)
        cnv.drawPath(pth, stroke=1, fill=1)


class RhombusShape(BaseShape):
    """
    Draw a rhombus on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a rhombus (diamond) on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # offset
        margin_left = self.unit(self.margin_left)
        margin_bottom = self.unit(self.margin_bottom)
        off_x = self.unit(off_x)
        off_y = self.unit(off_y)
        delta_x = off_x + margin_left
        delta_y = off_y + margin_bottom
        # convert to using units
        height = self.unit(self.height)
        width = self.unit(self.width)
        if self.cx and self.cy:
            x = self.unit(self.cx) - width / 2.0 + delta_x
            y = self.unit(self.cy) + height / 2.0 + delta_y
        else:
            x = self.unit(self.x) + delta_x
            y = self.unit(self.y) + delta_y
        # canvas
        self.set_canvas_props()
        fill = 0 if self.transparent else 1
        # draw
        x_s, y_s = x, y + height / 2.0
        pth = cnv.beginPath()
        pth.moveTo(x_s, y_s)
        pth.lineTo(x_s + width / 2.0, y_s + height / 2.0)
        pth.lineTo(x_s + width, y_s)
        pth.lineTo(x_s + width / 2.0, y_s - height / 2.0)
        pth.lineTo(x_s, y_s)
        pth.close()
        cnv.drawPath(pth, stroke=1, fill=fill)
        # text
        if self.label:
            x_c = x + width / 2.0
            y_c = y + height / 2.0
            cnv.setFont(self.font_face, self.label_size)
            cnv.setFillColor(self.stroke_label)
            self.draw_multi_string(cnv, x_c, y_c, self.label)


class RectShape(BaseShape):
    """
    Draw a rectangle on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(RectShape, self).__init__(_object=_object, canvas=canvas,
                                        **kwargs)
        # overrides
        if self.cx and self.cy:
            self.x = self.cx - self.width / 2.0
            self.y = self.cy - self.height / 2.0
        self.kwargs = kwargs

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a rectangle on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # offset
        margin_left = self.unit(self.margin_left)
        margin_bottom = self.unit(self.margin_bottom)
        off_x = self.unit(off_x)
        off_y = self.unit(off_y)
        delta_x = off_x + margin_left
        delta_y = off_y + margin_bottom
        # convert to using units
        #print "shapes_246", self.height, self.width
        height = self.unit(self.height)
        width = self.unit(self.width)
        #print "shapes_249", height, width
        #print "shapes_246 rect", ID, ':margin:', uni, self.margin_left
        if self.row is not None and self.col is not None:
            x = self.col * width + delta_x
            y = self.row * height + delta_y
        elif self.cx and self.cy:
            x = self.unit(self.cx) - width / 2.0 + delta_x
            y = self.unit(self.cy) + height / 2.0 + delta_y
        else:
            x = self.unit(self.x) + delta_x
            y = self.unit(self.y) + delta_y
        # canvas
        self.set_canvas_props()
        fill = 0 if self.transparent else 1
        # draw
        if self.rounding:
            rounding = self.unit(self.rounding)
            cnv.roundRect(
                x, y, width, height, rounding, stroke=1, fill=fill)
        elif self.rounded:
            _rounding = width * 0.08
            cnv.roundRect(
                x, y, width, height, _rounding, stroke=1, fill=fill)
        else:
            cnv.rect(
                x, y, width, height, stroke=1, fill=fill)
        # grid marks
        self.set_canvas_props(stroke=self.grid_color,
                              stroke_width=self.grid_stroke_width)
        if self.grid_marks:
            deltag = self.unit(self.grid_length)
            pth = cnv.beginPath()
            gx, gy = 0, y  # left-side
            pth.moveTo(gx, gy)
            pth.lineTo(deltag, gy)
            pth.moveTo(0, gy + height)
            pth.lineTo(deltag, gy + height)
            gx, gy = x, self.pagesize[1]  # top-side
            pth.moveTo(gx, gy)
            pth.lineTo(gx, gy - deltag)
            pth.moveTo(gx + width, gy)
            pth.lineTo(gx + width, gy - deltag)
            gx, gy = self.pagesize[0], y  # right-side
            pth.moveTo(gx, gy)
            pth.lineTo(gx - deltag, gy)
            pth.moveTo(gx, gy + height)
            pth.lineTo(gx - deltag, gy + height)
            gx, gy = x, 0  # bottom-side
            pth.moveTo(gx, gy)
            pth.lineTo(gx, gy + deltag)
            pth.moveTo(gx + width, gy)
            pth.lineTo(gx + width, gy + deltag)
            # done
            cnv.drawPath(pth, stroke=1, fill=1)
        # pattern
        img = self.load_image(self.pattern)
        if img:
            #print "shapes_355", type(img._image), img._image.size
            iwidth = img._image.size[0]
            iheight = img._image.size[1]
            # repeat?
            if self.repeat:
                cnv.drawImage(img, x=x, y=y, width=iwidth, height=iheight,
                              mask='auto')
            else:
                # stretch
                # TODO - work out how to (a) fill and (b) cut off -- mask?
                # assume DPI = 300?  72pt = 1" = 300px -see
                # http://two.pairlist.net/pipermail/reportlab-users/2006-January/004670.html
                #w, h = yourImage.size
                #yourImage.crop((0, 30, w, h-30)).save(...)
                cnv.drawImage(img, x=x, y=y, width=width, height=height,
                              mask='auto')
        # text
        if self.label:
            cnv.setFont(self.font_face, self.label_size)
            cnv.setFillColor(self.stroke_label)
            x_t = x + width / 2.0
            y_t = y + height / 2.0
            self.draw_multi_string(cnv, x_t, y_t, self.label)


class ShapeShape(BaseShape):
    """
    Draw an irregular polygon, based on a set of points, on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(ShapeShape, self).__init__(_object=_object, canvas=canvas,
                                         **kwargs)
        # overrides
        self.x = kwargs.get('x', kwargs.get('left', 0))
        self.y = kwargs.get('y', kwargs.get('bottom', 0))

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an irregular polygon on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # offset
        margin_left = self.unit(self.margin_left)
        margin_bottom = self.unit(self.margin_bottom)
        off_x = self.unit(off_x)
        off_y = self.unit(off_y)
        x = self.unit(self.x)
        y = self.unit(self.y)
        delta_x = off_x + margin_left + x
        delta_y = off_y + margin_bottom + y
        # canvas
        self.set_canvas_props()
        fill = 0 if self.transparent else 1
        # draw
        if isinstance(self.points, str):
            # SPLIT STRING e.g. "1,2  3,4  4.5,8.8"
            _points = self.points.split(' ')
            points = [_point.split(',') for _point in _points]
        else:
            points = self.points
        if points and len(points) > 0:
            pth = cnv.beginPath()
            for key, vertex in enumerate(points):
                _x0, _y0 = float(vertex[0]), float(vertex[1])
                # convert to using units
                x = self.unit(_x0) + delta_x
                y = self.unit(_y0) + delta_y
                if key == 0:
                    pth.moveTo(x, y)
                pth.lineTo(x, y)
            pth.close()
            cnv.drawPath(pth, stroke=1, fill=fill)


class ArcShape(BaseShape):
    """
    Arc on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw arc on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # offset
        margin_left = self.unit(self.margin_left)
        margin_bottom = self.unit(self.margin_bottom)
        off_x = self.unit(off_x)
        off_y = self.unit(off_y)
        delta_x = off_x + margin_left
        delta_y = off_y + margin_bottom
        # convert to using units
        x_1 = self.unit(self.x) + delta_x
        y_1 = self.unit(self.y) + delta_y
        if not self.x_1:
            self.x_1 = self.x + self.default_length
        if not self.y_1:
            self.y_1 = self.y + self.default_length
        x_2 = self.unit(self.x_1) + delta_x
        y_2 = self.unit(self.y_1) + delta_y
        # canvas
        self.set_canvas_props()
        #draw
        cnv.arc(x_1, y_1, x_2, y_2)


class BezierShape(BaseShape):
    """
    A Bezier curve on a given canvas.

    A Bezier curve is specified by four control points:
        (x1,y1), (x2,y2), (x3,y3), (x4,y4).
    The curve starts at (x1,y1) and ends at (x4,y4) and the line segment
    from (x1,y1) to (x2,y2) and the line segment from (x3,y3) to (x4,y4)
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw Bezier curve on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # offset
        margin_left = self.unit(self.margin_left)
        margin_bottom = self.unit(self.margin_bottom)
        off_x = self.unit(off_x)
        off_y = self.unit(off_y)
        delta_x = off_x + margin_left
        delta_y = off_y + margin_bottom
        # convert to using units
        x_1 = self.unit(self.x) + delta_x
        y_1 = self.unit(self.y) + delta_y
        if not self.x_1:
            self.x_1 = self.x + self.default_length
        if not self.y_1:
            self.y_1 = self.y + self.default_length
        x_2 = self.unit(self.x_1) + delta_x
        y_2 = self.unit(self.y_1) + delta_y
        x_3 = self.unit(self.x_2) + delta_x
        y_3 = self.unit(self.y_2) + delta_y
        x_4 = self.unit(self.x_3) + delta_x
        y_4 = self.unit(self.y_3) + delta_y
        # canvas
        self.set_canvas_props()
        #draw
        cnv.bezier(x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4)


class PolygonShape(BaseShape):
    """
    A regular polygon on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a regular polygon on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # offset
        margin_left = self.unit(self.margin_left)
        margin_bottom = self.unit(self.margin_bottom)
        off_x = self.unit(off_x)
        off_y = self.unit(off_y)
        delta_x = off_x + margin_left
        delta_y = off_y + margin_bottom
        # convert to using units
        x = self.unit(self.x) + delta_x
        y = self.unit(self.y) + delta_y
        # calc - assumes x and y are the centre
        if self.radius:
            radius = self.unit(self.radius)
        else:
            side = self.unit(self.side)
            sides = int(self.sides)
            #180 degrees is math.pi radians
            radius = side / (2.0 * math.sin(math.pi / sides))
        vertices = tools.polygon_vertices(
            self.sides, radius, self.rotate, (x, y))
        if not vertices or len(vertices) == 0:
            return
        # canvas
        self.set_canvas_props()
        fill = 0 if self.transparent else 1
        # draw
        pth = cnv.beginPath()
        pth.moveTo(*vertices[0])
        for vertex in vertices:
            pth.lineTo(*vertex)
        pth.close()
        cnv.drawPath(pth, stroke=1, fill=fill)
        #  text
        if self.label:
            cnv.setFont(self.font_face, self.label_size)
            cnv.setFillColor(self.stroke_label)
            self.draw_multi_string(cnv, x, y, self.label)
        if self.title:
            cnv.setFont(self.font_face, self.title_size)
            cnv.setFillColor(self.stroke_title)
            self.draw_multi_string(cnv, x, y - 1.4 * radius, self.title)
        if self.heading:
            cnv.setFont(self.font_face, self.heading_size)
            cnv.setFillColor(self.stroke_heading)
            self.draw_multi_string(cnv, x, y + 1.3 * radius, self.heading)
        # dot
        if self.dot_size:
            dot_size = self.unit(self.dot_size)
            cnv.setFillColor(self.dot_color)
            cnv.setStrokeColor(self.dot_color)
            cnv.circle(x, y, dot_size, stroke=1, fill=1)


class PolylineShape(BaseShape):
    """
    A multi-part line on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a polyline on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        points = tools.tuple_split(self.points)
        if not points:
            points = self.points
        if not points or len(points) == 0:
            tools.feedback("No points to draw or points are incorrect!")
            return
        # offset
        margin_left = self.unit(self.margin_left)
        margin_bottom = self.unit(self.margin_bottom)
        off_x = self.unit(off_x)
        off_y = self.unit(off_y)
        delta_x = off_x + margin_left
        delta_y = off_y + margin_bottom
        # canvas
        self.set_canvas_props()
        fill = 0 if self.transparent else 1
        # draw
        pth = cnv.beginPath()
        for key, vertex in enumerate(points):
            x, y = vertex
            # convert to using units
            x = self.unit(x) + delta_x
            y = self.unit(y) + delta_y
            if key == 0:
                pth.moveTo(x, y)
            pth.lineTo(x, y)
        cnv.drawPath(pth, stroke=1, fill=fill)


class HexShape(BaseShape):
    """
    A hexagon on a given canvas.

    See: http://powerfield-software.com/?p=851
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an hexagon on a given canvas."""
        is_cards = kwargs.get('is_cards', False)
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # offset
        margin_left = self.unit(self.margin_left)
        margin_bottom = self.unit(self.margin_bottom)
        off_x = self.unit(off_x)
        off_y = self.unit(off_y)
        delta_x = off_x + margin_left
        delta_y = off_y + margin_bottom
        # Calculate half_height and half_side from side
        side = self.unit(self.side)
        half_height = side * math.sqrt(3) / 2.0
        half_side = side / 2.0
        # Get coords for leftmost point
        #         __
        # x,y .. /  \
        #        \__/
        if self.row is not None and self.col is not None and is_cards:
            x = self.col * 2.0 * side + delta_x
            y = half_height + self.row * 2.0 * half_height + delta_x
        elif self.row is not None and self.col is not None:
            x = self.col * (half_side + side) + delta_x
            y = half_height + half_height * self.row * 2.0 + (self.col % 2.0) \
                * half_height + delta_y
        elif self.cx and self.cy:
            # cx and cy are at the centre of the hex
            x_d = self.unit(self.cx)
            y_d = self.unit(self.cy)
            x = x_d - half_side - side / 2.0 + delta_x
            y = y_d + delta_y
        else:
            # x and y are at the bottom-left corner of the box around the hex
            x = self.unit(self.x) + delta_x
            y = self.unit(self.y) + delta_y + half_height
        # hex centre
        x_d = x + half_side + side / 2.0
        y_d = y
        #if DEBUG: print "442", x, y, half_height, half_side, side
        # canvas
        self.set_canvas_props()
        # draw horizontal hexagon (clockwise)
        pth = cnv.beginPath()
        pth.moveTo(x, y)
        pth.lineTo(x + half_side, y + half_height)
        pth.lineTo(x + half_side + side, y + half_height)
        pth.lineTo(x + half_side + side + half_side, y)
        pth.lineTo(x + half_side + side, y - half_height)
        pth.lineTo(x + half_side, y - half_height)
        pth.close()
        cnv.drawPath(pth, stroke=1, fill=1)
        # centre dot
        if self.dot_size:
            dot_size = self.unit(self.dot_size)
            cnv.setFillColor(self.dot_color)
            cnv.setStrokeColor(self.dot_color)
            cnv.circle(x_d, y_d, dot_size, stroke=1, fill=1)
        if DEBUG:
            cnv.setStrokeColorRGB(0, 0, 0)
            cnv.drawCentredString(x - 10, y, '%s.%s' % (self.row, self.col))
        # text
        if self.label:
            cnv.setFont(self.font_face, self.label_size)
            cnv.setFillColor(self.stroke_label)
            self.draw_multi_string(cnv, x_d, y_d, self.label)


class StarShape(BaseShape):
    """
    A star on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a star on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # offset
        margin_left = self.unit(self.margin_left)
        margin_bottom = self.unit(self.margin_bottom)
        off_x = self.unit(off_x)
        off_y = self.unit(off_y)
        delta_x = off_x + margin_left
        delta_y = off_y + margin_bottom
        # convert to using units
        x = self.unit(self.x) + delta_x
        y = self.unit(self.y) + delta_y
        # calc - assumes x and y are the centre
        radius = self.unit(self.radius)
        # canvas
        self.set_canvas_props()
        # draw
        pth = cnv.beginPath()
        pth.moveTo(x, y + radius)
        angle = (2 * math.pi) * 2.0 / 5.0
        start_angle = math.pi / 2.0
        #if DEBUG: print '648 star self.vertices', self.vertices
        for vertex in range(self.vertices - 1):
            next_angle = angle * (vertex + 1) + start_angle
            x_1 = x + radius * math.cos(next_angle)
            y_1 = y + radius * math.sin(next_angle)
            pth.lineTo(x_1, y_1)
        pth.close()
        cnv.drawPath(pth, stroke=1, fill=1)
        # text
        if self.label:
            cnv.setFont(self.font_face, self.label_size)
            cnv.setFillColor(self.stroke_label)
            self.draw_multi_string(cnv, x, y, self.label)
        if self.title:
            cnv.setFont(self.font_face, self.title_size)
            cnv.setFillColor(self.stroke_title)
            self.draw_multi_string(cnv, x, y - 1.4 * radius, self.title)
        if self.heading:
            cnv.setFont(self.font_face, self.heading_size)
            cnv.setFillColor(self.stroke_heading)
            self.draw_multi_string(cnv, x, y + 1.3 * radius, self.heading)


class TextShape(BaseShape):
    """
    Text on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(TextShape, self).__init__(_object=_object, canvas=canvas,
                                        **kwargs)

    def __call__(self, *args, **kwargs):
        """do something when I'm called"""
        if DEBUG: print "shapes_679: calling TextShape..."

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw text on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # offset
        margin_left = self.unit(self.margin_left)
        margin_bottom = self.unit(self.margin_bottom)
        off_x = self.unit(off_x)
        off_y = self.unit(off_y)
        delta_x = off_x + margin_left
        delta_y = off_y + margin_bottom
        # convert to using units
        x_t = self.unit(self.x) + delta_x
        y_t = self.unit(self.y) + delta_y
        if self.height:
            height = self.unit(self.height)
        if self.width:
            width = self.unit(self.width)
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
        super(CircleShape, self).__init__(_object=_object, canvas=canvas,
                                          **kwargs)
        # overrides
        if self.cx and self.cy:
            self.x = self.cx - self.radius
            self.y = self.cy - self.radius
            self.width = 2.0 * self.radius
            self.height = 2.0 * self.radius
        self.kwargs = kwargs

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw circle on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # offset
        margin_left = self.unit(self.margin_left)
        margin_bottom = self.unit(self.margin_bottom)
        off_x = self.unit(off_x)
        off_y = self.unit(off_y)
        delta_x = off_x + margin_left
        delta_y = off_y + margin_bottom
        # convert to using units
        radius = self.unit(self.radius)
        if self.row is not None and self.col is not None:
            x_c = self.col * 2.0 * radius + radius + delta_x
            y_c = self.row * 2.0 * radius + radius + delta_y
            #print "shapes_735", self.col, self.row, "::", x_c, y_c
        elif self.cx and self.cy:
            x_c = self.unit(self.cx) + delta_x
            y_c = self.unit(self.cy) + delta_y
        else:
            x_c = self.unit(self.x) + delta_x + radius
            y_c = self.unit(self.y) + delta_y + radius
        # canvas
        self.set_canvas_props()
        # draw
        cnv.circle(x_c, y_c, radius, stroke=1, fill=1)
        # text
        if self.label:
            cnv.setFont(self.font_face, self.label_size)
            cnv.setFillColor(self.stroke_label)
            self.draw_multi_string(cnv, x_c, y_c, self.label)


class EllipseShape(BaseShape):
    """
    Ellipse on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw ellipse on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # offset
        margin_left = self.unit(self.margin_left)
        margin_bottom = self.unit(self.margin_bottom)
        off_x = self.unit(off_x)
        off_y = self.unit(off_y)
        delta_x = off_x + margin_left
        delta_y = off_y + margin_bottom
        # convert to using units
        x_1 = self.unit(self.x) + delta_x
        y_1 = self.unit(self.y) + delta_y
        if not self.x_1:
            self.x_1 = self.x + self.default_length
        if not self.y_1:
            self.y_1 = self.y + self.default_length
        x_2 = self.unit(self.x_1) + delta_x
        y_2 = self.unit(self.y_1) + delta_y
        # canvas
        self.set_canvas_props()
        #draw
        cnv.ellipse(x_1, y_1, x_2, y_2, stroke=1, fill=1)
        # text
        if self.label:
            cnv.setFont(self.font_face, self.label_size)
            cnv.setFillColor(self.stroke_label)
            x_c = (x_2 - x_1) / 2.0 + x_1
            y_c = (y_2 - y_1) / 2.0 + y_1
            self.draw_multi_string(cnv, x_c, y_c, self.label)


class GridShape(BaseShape):
    """
    A grid on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a grid on a given canvas."""
        cnv = cnv.canvas if cnv else self.canvas.canvas
        # offset
        margin_left = self.unit(self.margin_left)
        margin_bottom = self.unit(self.margin_bottom)
        off_x = self.unit(off_x)
        off_y = self.unit(off_y)
        delta_x = off_x + margin_left
        delta_y = off_y + margin_bottom
        # convert to using units
        x = self.unit(self.x) + delta_x
        y = self.unit(self.y) + delta_y
        height = self.unit(self.height)  # of each grid item
        width = self.unit(self.width)  # of each grid item
        if self.size:  # square grid
            size = self.unit(self.size)
            height, width = size, size
        y_cols, x_cols = [], []
        for y_col in range(0, self.rows + 1):
            y_cols.append(y + y_col*height)
        for x_col in range(0, self.cols + 1):
            x_cols.append(x + x_col*width)
        # canvas
        self.set_canvas_props()
        # draw
        cnv.grid(x_cols, y_cols)  # , stroke=1, fill=1)


class CommonShape(BaseShape):
    """
    Attributes common to, or used by, multiple shapes
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(CommonShape, self).__init__(_object=_object, canvas=canvas,
                                          **kwargs)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Not applicable."""
        tools.feedback('This shape cannot be drawn.')


### deck/card ================================================================


class CardShape(BaseShape):
    """
    Card attributes.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(CardShape, self).__init__(_object=_object, canvas=canvas,
                                        **kwargs)
        self.elements = []  # container for objects which get added to the card
        self.height = kwargs.get('height', 8.8)
        self.width = kwargs.get('width', 6.3)
        self.kwargs.pop('width', None)
        self.kwargs.pop('height', None)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an element on a given canvas."""
        raise NotImplementedError

    def draw_card(self, cnv, row, col, cid):
        """Draw a card on a given canvas."""
        #print "shapes_857  Card cnv", cnv, row, col, cid, self.shape
        # draw outline
        label = "ID:%s" % cid if self.show_id else ''
        if self.shape == 'rectangle':
            outline = RectShape(label=label,
                                height=self.height, width=self.width,
                                canvas=cnv, col=col, row=row, **self.kwargs)
            outline.draw()
        elif self.shape == 'circle':
            self.height = self.radius * 2.0
            self.width = self.radius * 2.0
            self.kwargs['radius'] = self.radius
            outline = CircleShape(label=label,
                                  canvas=cnv, col=col, row=row, **self.kwargs)
            outline.draw()
        elif self.shape == 'hexagon':
            self.height = self.side * math.sqrt(3.0)
            self.width = self.side * 2.0
            self.kwargs['side'] = self.side
            outline = HexShape(label=label,
                               canvas=cnv, col=col, row=row, **self.kwargs)
            outline.draw(is_cards=True)
        else:
            tools.feedback('Unable to draw a %s-shaped card.' % self.shape,
                           stop=True)
        flat_elements = tools.flatten(self.elements)
        for flat_ele in flat_elements:
            #print "shapes_926 flat_ele", flat_ele
            members = flat_ele.members or self.members
            try:  # - normal element
                iid = members.index(cid + 1)
                flat_ele.draw(
                    cnv=cnv,
                    off_x=col*self.width,
                    off_y=row*self.height,
                    ID=iid)
            except AttributeError:
                # query ... get a new element ... or not!?
                #print "shapes_937 self.shape_id", self.shape_id
                new_ele = flat_ele(cid=self.shape_id)  # uses __call__ on Query
                if new_ele:
                    flat_new_eles = tools.flatten(new_ele)
                    for flat_new_ele in flat_new_eles:
                        members = flat_new_ele.members or self.members
                        iid = members.index(cid + 1)
                        flat_new_ele.draw(
                            cnv=cnv,
                            off_x=col*self.width,
                            off_y=row*self.height,
                            ID=iid)
            except ValueError:
                tools.feedback('Unable to draw card #%s' % (cid + 1))
            except Exception as err:
                tools.feedback('Unable to draw card #%s (Error: %s' % ((cid + 1), err))


class DeckShape(BaseShape):
    """Placeholder for the deck design; list of CardShapes and Shapes."""

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(DeckShape, self).__init__(_object=_object, canvas=canvas,
                                        **kwargs)
        # page
        self.page_width = self.pagesize[0] / self.units
        self.page_height = self.pagesize[1] / self.units
        # cards
        self.deck = []  # container for CardShape objects
        self.cards = kwargs.get('cards', 9)  # default total number of cards
        self.height = kwargs.get('height', 8.8)  # OVERWRITE
        self.width = kwargs.get('width', 6.3)  # OVERWRITE
        self.sequence = kwargs.get('sequence', [])  # e.g. "1-2" or "1-5,8,10"
        self.template = kwargs.get('template', None)
        # user provided-rows and -columns
        self.card_rows = kwargs.get('rows', None)
        self.card_cols = kwargs.get('cols', kwargs.get('columns', None))
        # data file
        self.data_file = kwargs.get('data', None)
        self.data_cols = kwargs.get('data_cols', None)
        self.data_rows = kwargs.get('data_rows', None)
        self.data_header = kwargs.get('data_header', True)
        # GO!
        self.create(self.cards)

    def create(self, cards):
        """Create a new deck, based on number of `cards`"""
        #if DEBUG: print "Cards are: %s" % self.sequence
        self.deck = []
        #print "shapes_925:deck %s cards with kwargs %s" % (cards, self.kwargs)
        for card in range(0, cards):
            _card = CardShape(**self.kwargs)
            _card.shape_id = card
            self.deck.append(_card)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        cnv = cnv if cnv else self.canvas
        #print "base_935 Deck cnv", type(self.canvas), type(cnv)
        # user-defined rows and cols
        max_rows = self.card_rows
        max_cols = self.card_cols
        # calculate rows/cols based on page size and margins
        if not max_rows:
            row_space = \
                float(self.page_height) - self.margin_bottom - self.margin_top
            max_rows = int(row_space / float(self.height))
        if not max_cols:
            col_space = \
                float(self.page_width) - self.margin_left - self.margin_right
            max_cols = int(col_space / float(self.width))
        #print "shapes_961:", self.page_width, col_space, max_cols
        #print "shapes_962:", self.page_height, row_space, max_rows
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
    """Draw a Shape multiple times."""

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(RepeatShape, self).__init__(_object=_object, canvas=canvas,
                                          **kwargs)
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

        self._object = _object  # incoming Shape object
        # repeat
        self.rows = kwargs.get('rows', 1)
        self.cols = kwargs.get('cols', kwargs.get('columns', 1))
        self.repeat = kwargs.get('repeat', None)
        self.offset_across = self.offset_across or self.offset
        self.offset_down = self.offset_down or self.offset
        self.gap_across = self.gap_across or self.gap
        self.gap_down = self.gap_down or self.gap
        if self.repeat:
            self.repeat_across, self.repeat_down, \
                self.gap_down, self.gap_across, \
                self.gap_across, self.offset_down = \
                self.repeat.split(',')
        else:
            self.across = kwargs.get('across', self.cols)
            self.down = kwargs.get('down', self.rows)
            try:
                self.down = range(1, self.down + 1)
            except TypeError:
                pass
            try:
                self.across = range(1, self.across + 1)
            except TypeError:
                pass
        #self.repeat_ = kwargs.get('repeat_', None)
        #self.repeat_ = kwargs.get('repeat_', None)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        print "1046", self.offset_across, self.offset_down
        print "1047",self.gap_across, self.gap_down
        for col in range(self.cols):
            for row in range(self.rows):
                if ((col+1) in self.across) and ((row+1) in self.down):
                    off_x = col*self.width + \
                        col*(self.offset_across - self.margin_left)
                    off_y = row*self.height + \
                        row*(self.offset_down - self.margin_bottom)
                    flat_elements = tools.flatten(self._object)
                    #print "shapes_893", flat_elements
                    for flat_ele in flat_elements:
                        #print "shapes_895", flat_ele
                        try:  # normal element
                            flat_ele.draw(off_x=off_x, off_y=off_y,
                                          ID=self.shape_id)
                        except AttributeError:
                            new_ele = flat_ele(cid=self.shape_id)
                            #print "shapes_899", new_ele, type(new_ele)
                            if new_ele:
                                flat_new_eles = tools.flatten(new_ele)
                                #print "shapes_902", flat_new_eles
                                for flat_new_ele in flat_new_eles:
                                    #print "shapes_569", flat_new_ele
                                    flat_new_ele.draw(off_x=off_x, off_y=off_y,
                                                      ID=self.shape_id)

### other ====================================================================


class ConnectShape(BaseShape):
    """
    Connect two shapes (Rectangle), based on a position, on a given canvas.

       Q4 | Q1
       -------
       Q3 | Q2

    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(ConnectShape, self).__init__(_object=_object, canvas=canvas,
                                           **kwargs)
        # overrides
        self.kwargs = kwargs
        self.shape_from = kwargs.get('shape_from', None)
        self.shape_to = kwargs.get('shape_to', None)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a connection (line) between two shapes on given canvas."""
        cnv = cnv
        ID = ID
        # style
        style = self.style or 'direct'
        # shapes and position  - default style
        try:
            shape_from, shape_from_position = self.shape_from  # tuple form
        except:
            shape_from, shape_from_position = self.shape_from, 'BC'
        try:
            shape_to, shape_to_position = self.shape_to  # tuple form
        except:
            shape_to, shape_to_position = self.shape_to, 'TC'
        # props
        edge_from = shape_from.get_edges()
        edge_to = shape_to.get_edges()
        x_f, y_f = self.key_positions(shape_from, shape_from_position)
        x_t, y_t = self.key_positions(shape_to, shape_to_position)
        xc_f, yc_f = self.shape_from.get_center()
        xc_t, yc_t = self.shape_to.get_center()
        # x,y: use fixed/supplied; or by "name"; or by default; or by "smart"
        if style == 'path':
            points = []

            if xc_f == xc_t and yc_f > yc_t:  # above
                points = [
                    self.key_positions(shape_from, 'BC'),
                    self.key_positions(shape_to, 'TC')
                ]
            if xc_f == xc_t and yc_f < yc_t:  # below
                points = [
                    self.key_positions(shape_from, 'TC'),
                    self.key_positions(shape_to, 'BC')
                ]
            if xc_f > xc_t and yc_f == yc_t:  # left
                points = [
                    self.key_positions(shape_from, 'LC'),
                    self.key_positions(shape_to, 'RC')
                ]
            if xc_f < xc_t and yc_f == yc_t:  # right
                points = [
                    self.key_positions(shape_from, 'RC'),
                    self.key_positions(shape_to, 'LC')
                ]

            if xc_f < xc_t and yc_f < yc_t:  # Q1
                print "Q1"
                if edge_from['right'] < edge_to['left']:
                    if edge_from['top'] < edge_to['bottom']:
                        print " A", edge_from['top'], edge_to['bottom']
                        delta = (edge_to['bottom'] - edge_from['top']) / 2.0
                        points = [
                            self.key_positions(shape_from, 'TC'),
                            (xc_f, edge_from['top'] + delta),
                            (xc_t, edge_from['top'] + delta),
                            self.key_positions(shape_to, 'BC')
                        ]
                    elif edge_from['top'] > edge_to['bottom']:
                        print " B", edge_from['top'], edge_to['bottom']
                        points = [
                            self.key_positions(shape_from, 'TC'),
                            (xc_f, yc_t),
                            self.key_positions(shape_to, 'LC')
                        ]
                    else:
                        pass
                else:
                    print " C", edge_from['top'], edge_to['bottom']
                    points = [
                        self.key_positions(shape_from, 'TC'),
                        (xc_f, yc_t),
                        self.key_positions(shape_to, 'LC')
                    ]
            if xc_f < xc_t and yc_f > yc_t:  # Q2
                print "Q2"

            if xc_f > xc_t and yc_f > yc_t:  # Q3
                print "Q3"

            if xc_f > xc_t and yc_f < yc_t:  # Q4
                print "Q4"
                if edge_from['left'] < edge_to['right']:
                    if edge_from['top'] < edge_to['bottom']:
                        print " A", edge_from['top'], edge_to['bottom']
                        delta = (edge_to['bottom'] - edge_from['top']) / 2.0
                        points = [
                            self.key_positions(shape_from, 'TC'),
                            (xc_f, edge_from['top'] + delta),
                            (xc_t, edge_from['top'] + delta),
                            self.key_positions(shape_to, 'BC')
                        ]
                    elif edge_from['top'] > edge_to['bottom']:
                        print " B", edge_from['top'], edge_to['bottom']
                        points = [
                            self.key_positions(shape_from, 'TC'),
                            (xc_f, yc_t),
                            self.key_positions(shape_to, 'RC')
                        ]
                    else:
                        pass
                else:
                    print " C", edge_from['top'], edge_to['bottom']
                    points = [
                        self.key_positions(shape_from, 'TC'),
                        (xc_f, yc_t),
                        self.key_positions(shape_to, 'RC')
                    ]

            if xc_f == xc_t and yc_f == yc_t:  # same!
                return
            self.kwargs['points'] = points
            plin = PolylineShape(None, cnv, **self.kwargs)
            plin.draw(ID=ID)
        elif style == 'direct':  # straight line
            self.kwargs['x'] = x_f
            self.kwargs['y'] = y_f
            self.kwargs['x1'] = x_t
            self.kwargs['y1'] = y_t
            lin = LineShape(None, cnv, **self.kwargs)
            lin.draw(ID=ID)
        else:
            tools.feedback('Style "%s" is not known.' % style)

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
            'TL': (left, top),
            'TC': (mid_horizontal, top),
            'TR': (right, top),
            'BL': (left, btm),
            'BC': (mid_horizontal, btm),
            'BR': (right, btm),
            'LC': (left, mid_vertical),
            'RC': (right, mid_vertical),
            #'': (),
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
        super(FooterShape, self).__init__(_object=_object, canvas=canvas,
                                          **kwargs)
        # overrides
        page_width = self.pagesize[0]
        self.kwargs['x'] = self.kwargs.get('x', page_width / 2.0)
        self.kwargs['y'] = self.margin_bottom / 2.0

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw footer on a given canvas page."""
        cnv = cnv if cnv else self.canvas
        if not self.kwargs.get('text'):
            self.kwargs['text'] = 'Page %s' % ID
        text = TextShape(_object=None, canvas=cnv, kwargs=self.kwargs)
        text.draw()
