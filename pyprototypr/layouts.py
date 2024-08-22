# -*- coding: utf-8 -*-
"""
Create layouts - grids, repeats, sequences and tracks - for pyprototypr
"""
# lib
import copy
import logging
import math
import random

# third party
# local
from pyprototypr.utils.geoms import (
    Point, Link, Location, TrackPoint)  # named tuples
from pyprototypr.utils import geoms, tools
from pyprototypr.base import BaseShape, BaseCanvas
from pyprototypr.shapes import (
    CircleShape, HexShape, ImageShape, LineShape, PolylineShape, RectangleShape, SquareShape, TextShape)

log = logging.getLogger(__name__)

DEBUG = False



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
