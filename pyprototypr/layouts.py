# -*- coding: utf-8 -*-
"""
Create grids, repeats, sequences, layouts and connections - for pyprototypr
"""
# lib
import copy
import logging
import math
# third party
# local
from pyprototypr.utils.geoms import Point, Locale, Place  # named tuples
from pyprototypr.utils import geoms, tools, support
from pyprototypr.base import BaseShape, BaseCanvas
from pyprototypr.shapes import (
    CircleShape, LineShape, PolygonShape, PolylineShape, RectangleShape, TextShape)

log = logging.getLogger(__name__)

DEBUG = False


# ---- grids

class GridShape(BaseShape):
    """
    Grid on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(GridShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        self.use_side = False
        if 'side' in kwargs:
            self.use_side = True
            if 'width' in kwargs or 'height' in kwargs:
                self.use_side = False

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a grid on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- convert to using units
        x = self._u.x + self._o.delta_x
        y = self._u.y + self._o.delta_y
        height = self._u.height  # of each grid item
        width = self._u.width  # of each grid item
        if self.side and self.use_side:  # square grid
            side = self.unit(self.side)
            height, width = side, side
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
        self.set_canvas_props(index=ID)  # this causes Image to disappear ???
        # ---- draw grid
        cnv.grid(x_cols, y_cols)  # , stroke=1, fill=1)


class DotGridShape(BaseShape):
    """
    Dot Grid on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(DotGridShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a dot grid on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- convert to using units
        x = 0 + self.unit(self.offset_x)
        y = 0 + self.unit(self.offset_y)
        height = self._u.height  # of each grid item
        width = self._u.width  # of each grid item
        if self.side:  # square grid
            side = self.unit(self.side)
            height, width = side, side
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
        self.kwargs = kwargs
        self._object = _object or TextShape(_object=None, canvas=canvas, **kwargs)
        self.setting = kwargs.get('setting', (1, 1, 1, 'number'))
        if isinstance(self.setting, list):
            self.setting_list = self.setting
        else:
            self.calculate_setting_list()

        self.gap_x = self.gap_x or self.gap
        self.gap_y = self.gap_y or self.gap

    def calculate_setting_list(self):
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
        # ---- store sequence values in setting_list
        self.setting_list = []
        try:
            if self.set_type.lower() in ['n', 'number']:
                self.set_stop = self.setting[1] + 1 if self.set_inc > 0 else self.setting[1] - 1
                self.setting_iterator = range(self.set_start, self.set_stop, self.set_inc)
                self.setting_list = list(self.setting_iterator)
            elif self.set_type.lower() in ['l', 'letter']:
                self.setting_list = []
                start, stop = ord(self.set_start), ord(self.set_stop)
                curr = start
                while True:
                    if self.set_inc > 0 and curr > stop:
                        break
                    if self.set_inc < 0 and curr < stop:
                        break
                    self.setting_list.append(chr(curr))
                    curr += self.set_inc
            elif self.set_type.lower() in ['r', 'roman']:
                self.set_stop = self.setting[1] + 1 if self.set_inc > 0 else self.setting[1] - 1
                self.setting_iterator = range(self.set_start, self.set_stop, self.set_inc)
                _setting_list = list(self.setting_iterator)
                self.setting_list = [
                    support.roman(int(value)) for value in _setting_list]
            elif self.set_type.lower() in ['e', 'excel']:
                self.set_stop = self.setting[1] + 1 if self.set_inc > 0 else self.setting[1] - 1
                self.setting_iterator = range(self.set_start, self.set_stop, self.set_inc)
                _setting_list = list(self.setting_iterator)
                self.setting_list = [
                    support.excel_column(int(value)) for value in _setting_list]
            else:
                tools.feedback(
                    f"The settings type '{self.set_type}' must rather be one of:"
                    " number, roman, excel or letter!", True)
            # tools.feedback(f'{self.setting_list=}')
        except Exception as err:
            log.warning(err)
            tools.feedback(
                f"Unable to evaluate Sequence setting '{self.setting}';"
                " - please check and try again!", True)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        _off_x, _off_y = off_x, off_y

        for key, item in enumerate(self.setting_list):
            _ID = ID if ID is not None else self.shape_id
            _locale = Locale(sequence=item)
            kwargs['locale'] = _locale._asdict()
            # tools.feedback(f'*   @Seqnc@ {self.gap_x=}, {self.gap_y=}')
            off_x = _off_x + key * self.gap_x
            off_y = _off_y + key * self.gap_y
            flat_elements = tools.flatten(self._object)
            log.debug("flat_eles:%s", flat_elements)
            for each_flat_ele in flat_elements:
                flat_ele = copy.copy(each_flat_ele)  # allow props to be reset
                try:  # normal element
                    if self.deck_data:
                        new_ele = self.handle_custom_values(flat_ele, _ID)
                    else:
                        new_ele = flat_ele
                    new_ele.draw(off_x=off_x, off_y=off_y, ID=_ID, **kwargs)
                except AttributeError:
                    new_ele = flat_ele(cid=_ID) if flat_ele else None
                    if new_ele:
                        flat_new_eles = tools.flatten(new_ele)
                        log.debug("%s", flat_new_eles)
                        for flat_new_ele in flat_new_eles:
                            log.debug("%s", flat_new_ele)
                            if self.deck_data:
                                new_flat_new_ele = self.handle_custom_values(flat_new_ele, _ID)
                            else:
                                new_flat_new_ele = flat_new_ele
                            new_flat_new_ele.draw(
                                off_x=off_x, off_y=off_y, ID=_ID, **kwargs
                            )

# ---- repeats


class RepeatShape(BaseShape):
    """
    Shape is drawn multiple times.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(RepeatShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
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
        self.offset_x = self.offset_x or self.offset
        self.offset_y = self.offset_y or self.offset
        self.gap_x = self.gap_x or self.gap
        self.gap_y = self.gap_y or self.gap
        if self.repeat:
            (
                self.repeat_across,
                self.repeat_down,
                self.gap_y,
                self.gap_x,
                self.offset_x,
                self.offset_y,
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

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props

        for col in range(self.cols):
            for row in range(self.rows):
                if ((col + 1) in self.across) and ((row + 1) in self.down):
                    off_x = col * self.width + self.offset_x + col * (
                        self.gap_x - (self.margin_left or self.margin))
                    off_y = row * self.height + self.offset_y + row * (
                        self.gap_y - (self.margin_bottom or self.margin))
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


class VirtualShape():
    """
    Common properties and methods for all virtual shapes (layout and track)
    """

    def to_int(self, value, label='', maximum=None, minimum=None) -> int:
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

    def to_float(self, value, label='') -> int:
        """Set a value to a float; or stop if an invalid value."""
        try:
            float_value = float(value)
            return float_value
        except Exception:
            _label = f" for {label}" if label else ''
            tools.feedback(f'"{value}"{_label} is not a valid floating number!', True)

# ---- virtual Locations


class VirtualLocations(VirtualShape):
    """
    Common properties and methods to define virtual Locations.

    Virtual Locations are not drawn on the canvas; they provide the
    locations/points where user-defined shapes will be drawn.
    """

    def __init__(self, rows, cols, **kwargs):
        kwargs = kwargs
        self.x = self.to_float(kwargs.get('x', 1.0), 'x')  # left(lower) corner
        self.y = self.to_float(kwargs.get('y', 1.0), 'y')  # left(lower) corner
        self.rows = self.to_int(rows, 'rows')
        self.cols = self.to_int(cols, 'cols')
        self.side = self.to_float(kwargs.get('side', 0), 'side')
        self.layout_size = self.rows * self.cols
        self.spacing = kwargs.get('interval', 1)
        self.row_spacing = kwargs.get('y_interval', self.spacing)
        self.col_spacing = kwargs.get('x_interval', self.spacing)
        # offset
        self.col_even = kwargs.get('col_even', 0)
        self.col_odd = kwargs.get('col_odd', 0)
        self.row_even = kwargs.get('row_even', 0)
        self.row_odd = kwargs.get('row_odd', 0)
        # layout
        self.pattern = kwargs.get('pattern', 'default')
        self.direction = kwargs.get('direction', 'east')
        self.facing = kwargs.get('facing', 'east')  # for diamond, triangle
        self.flow = None  # used for snake; see validate() for setting
        # start / end
        self.start = kwargs.get('start', None)
        self.stop = kwargs.get('stop', 0)
        self.label_style = kwargs.get('label_style', None)
        self.validate()

    def validate(self):
        """Check for valid settings and combos."""
        self.stop = self.to_int(self.stop, 'stop')
        self.rows = self.to_int(self.rows, 'rows')
        self.cols = self.to_int(self.cols, 'cols')
        self.start = str(self.start)
        self.pattern = str(self.pattern)
        self.direction = str(self.direction)
        if self.pattern.lower() not in [
                'default', 'd', 'snake', 's', 'outer', 'o']:
            tools.feedback(
                f"{self.pattern} is not a valid pattern - "
                "use 'default', 'outer', 'snake'", True)
        if self.direction.lower() not in ['north', 'n', 'south', 's', 'west', 'w', 'east', 'e']:
            tools.feedback(
                f"{self.direction} is not a valid direction - "
                "use 'north', south', 'west', or 'east'", True)
        if self.facing.lower() not in ['north', 'n', 'south', 's', 'west', 'w', 'east', 'e']:
            tools.feedback(
                f"{self.facing} is not a valid facing - "
                "use 'north', south', 'west', or 'east'", True)
        if 'n' in self.start.lower()[0] and 'n' in self.direction.lower()[0] \
                or 's' in self.start.lower()[0] and 's' in self.direction.lower()[0] \
                or 'w' in self.start.lower()[0] and 'w' in self.direction.lower()[0] \
                or 'e' in self.start.lower()[0] and 'e' in self.direction.lower()[0]:
            tools.feedback(f"Cannot use {self.start} with {self.direction}!", True)
        if self.direction.lower() in ['north', 'n', 'south', 's']:
            self.flow = 'vert'
        elif self.direction.lower() in ['west', 'w', 'east', 'e']:
            self.flow = 'hori'
        else:
            tools.feedback(f"{self.direction} is not a valid direction!", True)
        if self.label_style and self.label_style.lower() != 'excel':
            tools.feedback(f"{self.label_style } is not a valid label_style !", True)
        if self.col_odd and self.col_even:
            tools.feedback("Cannot use 'col_odd' and 'col_even' together!", True)
        if self.row_odd and self.row_even:
            tools.feedback("Cannot use 'row_odd' and 'row_even' together!", True)

    def set_id(self, col: int, row: int) -> str:
        """Create an ID from row and col values."""
        if self.label_style and self.label_style.lower() == 'excel':
            return '%s%s' % (tools.sheet_column(col), row)
        else:
            return '%s,%s' % (col, row)

    def set_compass(self, compass: str) -> str:
        """Return full lower-case value of primary compass direction."""
        if not compass:
            return None
        _compass = str(compass).lower()
        match _compass:
            case 'n' | 'north':
                return 'north'
            case 's' | 'south':
                return 'south'
            case 'e' | 'east':
                return 'east'
            case 'w' | 'west':
                return 'west'
            case _:
                raise ValueError(
                    f'"{compass}" is an invalid primary compass direction!')

    def next_locale(self) -> Locale:
        """Yield next Locale for each call."""
        pass


class RectangularLocations(VirtualLocations):
    """
    Common properties and methods to define a virtual rectangular layout.
    """

    def __init__(self, rows=2, cols=2, **kwargs):
        super(RectangularLocations, self).__init__(rows, cols, **kwargs)
        self.kwargs = kwargs
        _spacing = kwargs.get('spacing', 1)
        self.spacing = tools.as_float(_spacing, 'spacing')
        if kwargs.get('col_spacing'):
            self.col_spacing = tools.as_float(kwargs.get('col_spacing'), 'col_spacing')
        else:
            self.col_spacing = self.spacing
        if kwargs.get('row_spacing'):
            self.row_spacing = tools.as_float(kwargs.get('row_spacing'), 'row_spacing')
        else:
            self.row_spacing = self.spacing
        self.start = kwargs.get('start', 'sw')
        if self.cols < 2 or self.rows < 2:
            tools.feedback(
                f"Minimum layout size is 2x2 (cannot use {self.cols }x{self.rows})!",
                True)
        if self.start.lower() not in ['sw', 'se', 'nw', 'ne']:
            tools.feedback(
                f"{self.start} is not a valid start - "
                "use: 'sw', 'se', 'nw', or 'ne'", True)
        if self.side and kwargs.get('col_spacing'):
            tools.feedback(
                'Using side will override col_spacing and offset values!', False)
        if self.side and  kwargs.get('row_spacing'):
            tools.feedback(
                'Using side will override row_spacing and offset values!', False)

    def next_locale(self) -> Locale:
        """Yield next Location for each call."""
        _start = self.start.lower()
        _dir = self.direction.lower()
        current_dir = _dir
        match _start:
            case 'sw':
                row_start = 1
                col_start = 1
                clockwise = True if _dir in ['north', 'n'] else False
            case 'se':
                row_start = 1
                col_start = self.cols
                clockwise = True if _dir in ['west', 'w'] else False
            case 'nw':
                row_start = self.rows
                col_start = 1
                clockwise = True if _dir in ['east', 'e'] else False
            case 'ne':
                row_start = self.rows
                col_start = self.cols
                clockwise = True if _dir in ['south', 's'] else False
            case _:
                raise ValueError(
                    f'"{self.direction}" is an invalid secondary compass direction!')
        col, row, count = col_start, row_start, 0
        max_outer = 2 * self.rows + (self.cols - 2) * 2
        corner = None
        # print(f'\n*** {self.start=} {self.layout_size=} {max_outer=} {self.stop=} {clockwise=}')
        # ---- triangular layout
        if self.side:
            self.col_spacing = self.side
            self.row_spacing = math.sqrt(3) / 2. * self.side
            _dir = -1 if self.row_odd < 0 else 1
            self.row_odd = _dir * (self.col_spacing / 2.)
            if self.row_even:
                _dir = -1 if self.row_even < 0 else 1
                self.row_odd = 0
                self.row_even = _dir * (self.col_spacing / 2.)
        while True:  # rows <= self.rows and col <= self.cols:
            count = count + 1
            # calculate point based on row/col
            # TODO!  set actual x and y
            x = self.x + (col - 1) * self.col_spacing
            y = self.y + (row - 1) * self.row_spacing
            # offset(s)
            if self.side:
                if row & 1:
                    x = x + self.row_odd
                if not row & 1:
                    x = x + self.row_even
            else:
                if self.col_odd and col & 1:
                    y = y + self.col_odd
                if self.col_even and not col & 1:
                    y = y + self.col_even
                if self.row_odd and row & 1:
                    x = x + self.row_odd
                if self.row_even and not row & 1:
                    x = x + self.row_even
            # print(f'*** {count=} {row=},{col=} // {x=},{y=}')
            # ---- set next grid location
            match self.pattern.lower():
                # ---- * snake
                case 'snake' | 'snaking' | 's':
                    # tools.feedback(f'*** {count=} {self.layout_size=} {self.stop=}')
                    if count > self.layout_size or (self.stop and count > self.stop):
                        return
                    yield Locale(col, row, x, y, self.set_id(col, row), count, corner)
                    # next grid location
                    match self.direction.lower():
                        case 'e' | 'east':
                            col = col + 1
                            if col > self.cols:
                                col = self.cols
                                if row_start == self.rows:
                                    row = row - 1
                                else:
                                    row = row + 1
                                self.direction = 'w'

                        case 'w' | 'west':
                            col = col - 1
                            if col < 1:
                                col = 1
                                if row_start == self.rows:
                                    row = row - 1
                                else:
                                    row = row + 1
                                self.direction = 'e'

                        case 'n' | 'north':
                            row = row + 1
                            if row > self.rows:
                                row = self.rows
                                if col_start == self.cols:
                                    col = col - 1
                                else:
                                    col = col + 1
                                self.direction = 's'

                        case 's' | 'south':
                            row = row - 1
                            if row < 1:
                                row = 1
                                if col_start == self.cols:
                                    col = col - 1
                                else:
                                    col = col + 1
                                self.direction = 'n'

                    x = self.x + (col - 1) * self.col_spacing
                    y = self.y + (row - 1) * self.row_spacing

                # ---- * outer
                case 'outer' | 'o':
                    if count > max_outer:
                        return
                    corner = None
                    if row == 1 and col == 1:
                        corner = 'sw'
                    if row == self.rows and col == 1:
                        corner = 'nw'
                    if row == self.rows and col == self.cols:
                        corner = 'ne'
                    if row == 1 and col == self.cols:
                        corner = 'se'
                    yield Locale(col, row, x, y, self.set_id(col, row), count, corner)
                    # next grid location
                    # print(f'*** {count=} {current_dir=} {row=},{col=} // {row_start=},{col_start=}')

                    if row == 1 and col == 1:
                        corner = 'sw'
                        if clockwise:
                            current_dir = 'n'
                            row = row + 1
                        else:
                            current_dir = 'e'
                            col = col + 1

                    if row == self.rows and col == 1:
                        corner = 'nw'
                        if clockwise:
                            current_dir = 'e'
                            col = col + 1
                        else:
                            current_dir = 's'
                            row = row - 1

                    if row == self.rows and col == self.cols:
                        corner = 'ne'
                        if clockwise:
                            current_dir = 's'
                            row = row - 1
                        else:
                            current_dir = 'w'
                            col = col - 1

                    if row == 1 and col == self.cols:
                        corner = 'se'
                        if clockwise:
                            current_dir = 'w'
                            col = col - 1
                        else:
                            current_dir = 'n'
                            row = row + 1

                    if not corner:
                        match current_dir:
                            case 'e' | 'east':
                                col = col + 1
                            case 'w' | 'west':
                                col = col - 1
                            case 'n' | 'north':
                                row = row + 1
                            case 's' | 'south':
                                row = row - 1

                    x = self.x + (col - 1) * self.col_spacing
                    y = self.y + (row - 1) * self.row_spacing

                # ---- * regular
                case _:  # default pattern
                    yield Locale(col, row, x, y, self.set_id(col, row), count, corner)
                    # next grid location
                    match self.direction.lower():
                        case 'e' | 'east':
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
                        case 'w' | 'west':
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
                        case 'n' | 'north':
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
                        case 's' | 'south':
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

                    x = self.x + (col - 1) * self.col_spacing
                    y = self.y + (row - 1) * self.row_spacing
                    # tools.feedback(f"{x=}, {y=}, {col=}, {row=}, ")


class TriangularLocations(VirtualLocations):
    """
    Common properties and methods to define  virtual triangular locations.
    """

    def __init__(self, rows=2, cols=2, **kwargs):
        super(TriangularLocations, self).__init__(rows, cols, **kwargs)
        self.kwargs = kwargs
        self.start = kwargs.get('start', 'north')
        self.facing = kwargs.get('facing', 'north')
        if (self.cols < 2 and self.rows < 1) or (self.cols < 1 and self.rows < 2):
            tools.feedback(
                f"Minimum layout size is 2x1 or 1x2 (cannot use {self.cols }x{self.rows})!",
                True)
        if self.start.lower() not in [
                'north', 'south', 'east', 'west', 'n', 'e', 'w', 's', ]:
            tools.feedback(
                f"{self.start} is not a valid start - "
                "use: 'n', 's', 'e', or 'w'", True)

    def next_locale(self) -> Locale:
        """Yield next Location for each call."""
        _start = self.set_compass(self.start.lower())
        _dir = self.set_compass(self.direction.lower())
        _facing = self.set_compass(self.facing.lower())
        current_dir = _dir

        # TODO - create logic
        if self.pattern.lower() in ['snake', 'snaking', 's']:
            tools.feedback('Snake pattern NOT YET IMPLEMENTED', True)

        # ---- store row/col as list of lists
        array = []
        match _facing:
            case 'north' | 'south':
                for length in range(1, self.cols + 1):
                    _cols = [col for col in range(1, length + 1)]
                    if _cols:
                        array.append(_cols)
            case 'east' | 'west':
                for length in range(1, self.rows + 1):
                    _rows = [row for row in range(1, length + 1)]
                    if _rows:
                        array.append(_rows)
            case _:
                tools.feedback(f'The facing value {self.facing} is not valid!', True)
        # print(f'{_facing}', f'{self.cols=}',  f'{self.rows=}',array)

        # ---- calculate initial conditions
        col_start, row_start = 1, 1
        match (_facing, _start):
            case ('north', 'north'):
                row_start = 1
                col_start = 1
                clockwise = True if _dir == 'north' else False
            case ('north', 'west'):
                row_start = 1
                col_start = self.cols
                clockwise = True if _dir == 'west' else False
            case ('north', 'east'):
                row_start = self.rows
                col_start = 1
                clockwise = True if _dir == 'east' else False

        col, row, count = col_start, row_start, 0
        max_outer = 2 * self.rows + (self.cols - 2) * 2
        corner = None
        # print(f'\n*** {self.start=} {self.layout_size=} {max_outer=} {self.stop=} {clockwise=}')
        # ---- set row and col spacing
        match _facing:
            case 'north' | 'south':  # layout is row-oriented
                self.col_spacing = self.side
                self.row_spacing = math.sqrt(3) / 2. * self.side
            case 'east' | 'west':  # layout is col-oriented
                self.col_spacing = math.sqrt(3) / 2. * self.side
                self.row_spacing = self.side
        # ---- iterate the rows and cols
        hlf_side = self.side / 2.0
        for key, entry in enumerate(array):
            match _facing:
                case 'north':  # layout is row-oriented
                    y = self.y + (self.rows - 1) * self.row_spacing - (key + 1) * self.row_spacing
                    dx = 0.5 * (self.cols - len(entry)) * self.col_spacing - \
                        (self.cols - 1) * 0.5 * self.col_spacing
                    for val, loc in enumerate(entry):
                        count = count + 1
                        x = self.x + dx + val * self.col_spacing
                        yield Locale(
                            loc, key + 1, x, y, self.set_id(loc, key + 1), count, corner)
                case 'south':  # layout is row-oriented
                    y = self.y + key * self.row_spacing
                    dx = 0.5 * (self.cols - len(entry)) * self.col_spacing - \
                        (self.cols - 1) * 0.5 * self.col_spacing
                    for val, loc in enumerate(entry):
                        count = count + 1
                        x = self.x + dx + val * self.col_spacing
                        yield Locale(
                            loc, key + 1, x, y, self.set_id(loc, key + 1), count, corner)
                case 'east':  # layout is col-oriented
                    x = self.x + self.cols * self.col_spacing - (key + 2) * self.col_spacing
                    dy = 0.5 * (self.rows - len(entry)) * self.row_spacing - \
                        (self.rows - 1) * 0.5 * self.row_spacing
                    for val, loc in enumerate(entry):
                        count = count + 1
                        y = self.y + dy + val * self.row_spacing
                        yield Locale(
                            key + 1, loc, x, y, self.set_id(key + 1, loc), count, corner)
                case 'west':  # layout is col-oriented
                    x = self.x + key * self.col_spacing
                    dy = 0.5 * (self.rows - len(entry)) * self.row_spacing - \
                        (self.rows - 1) * 0.5 * self.row_spacing
                    for val, loc in enumerate(entry):
                        count = count + 1
                        y = self.y + dy + val * self.row_spacing
                        yield Locale(
                            key + 1, loc, x, y, self.set_id(key + 1, loc), count, corner)
        return


class DiamondLocations(VirtualLocations):
    """
    Common properties and methods to define virtual diamond locations.
    """

    def __init__(self, rows=1, cols=2, **kwargs):
        super(DiamondLocations, self).__init__(rows, cols, **kwargs)
        self.kwargs = kwargs
        if (self.cols < 2 and self.rows < 1) or (self.cols < 1 and self.rows < 2):
            tools.feedback(
                f"Minimum layout size is 2x1 or 1x2 (cannot use {self.cols }x{self.rows})!",
                True)

    def next_locale(self) -> Locale:
        """Yield next Location for each call."""

# ---- tracks

# See proto.py

# ---- other layouts


class ConnectShape(BaseShape):
    """
    Connect two shapes (Rectangle), based on a position, on a given canvas.

       Q4 | Q1
       -------
       Q3 | Q2

    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(ConnectShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # overrides
        self.shape_from = kwargs.get("shape_from", None)  # could be a GridShape
        self.shape_to = kwargs.get("shape_to", None)  # could be a GridShape

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a connection (line) between two shapes on given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- style
        style = self.style or "direct"
        # ---- shapes and positions
        try:
            shp_from, shape_from_position = self.shape_from  # tuple form
        except Exception:
            shp_from, shape_from_position = self.shape_from, "S"
        try:
            shp_to, shape_to_position = self.shape_to  # tuple form
        except Exception:
            shp_to, shape_to_position = self.shape_to, "N"
        # ---- shape props
        shape_from = self.get_shape_in_grid(shp_from)
        shape_to = self.get_shape_in_grid(shp_to)
        edge_from = shape_from.get_bounds()
        edge_to = shape_to.get_bounds()
        x_f, y_f = self.key_positions(shape_from, shape_from_position)
        x_t, y_t = self.key_positions(shape_to, shape_to_position)
        xc_f, yc_f = shape_from.get_center()
        xc_t, yc_t = shape_to.get_center()
        # x,y: use fixed/supplied; or by "name"; or by default; or by "smart"
        if style == "path":
            # ---- path points
            points = []

            if xc_f == xc_t and yc_f > yc_t:  # above
                points = [
                    self.key_positions(shape_from, "S"),
                    self.key_positions(shape_to, "N"),
                ]
            if xc_f == xc_t and yc_f < yc_t:  # below
                points = [
                    self.key_positions(shape_from, "N"),
                    self.key_positions(shape_to, "S"),
                ]
            if xc_f > xc_t and yc_f == yc_t:  # left
                points = [
                    self.key_positions(shape_from, "W"),
                    self.key_positions(shape_to, "E"),
                ]
            if xc_f < xc_t and yc_f == yc_t:  # right
                points = [
                    self.key_positions(shape_from, "E"),
                    self.key_positions(shape_to, "W"),
                ]

            if xc_f < xc_t and yc_f < yc_t:  # Q1
                if edge_from.right < edge_to.left:
                    if edge_from.top < edge_to.bottom:
                        log.debug("A t:%s b:%s", edge_from.top, edge_to.bottom)
                        delta = (edge_to.bottom - edge_from.top) / 2.0
                        points = [
                            self.key_positions(shape_from, "N"),
                            (xc_f, edge_from.top + delta),
                            (xc_t, edge_from.top + delta),
                            self.key_positions(shape_to, "S"),
                        ]
                    elif edge_from.top > edge_to.bottom:
                        log.debug("B t:%s b:%s", edge_from.top, edge_to.bottom)
                        points = [
                            self.key_positions(shape_from, "N"),
                            (xc_f, yc_t),
                            self.key_positions(shape_to, "W"),
                        ]
                    else:
                        pass
                else:
                    log.debug("C t:%s b:%s", edge_from.top, edge_to.bottom)
                    points = [
                        self.key_positions(shape_from, "N"),
                        (xc_f, yc_t),
                        self.key_positions(shape_to, "W"),
                    ]
            if xc_f < xc_t and yc_f > yc_t:  # Q2
                log.debug("Q2")

            if xc_f > xc_t and yc_f > yc_t:  # Q3
                log.debug("Q3")

            if xc_f > xc_t and yc_f < yc_t:  # Q4
                log.debug("Q4")
                if edge_from.left < edge_to.right:
                    if edge_from.top < edge_to.bottom:
                        log.debug(" A t:%s b:%s", edge_from.top, edge_to.bottom)
                        delta = (edge_to.bottom - edge_from.top) / 2.0
                        points = [
                            self.key_positions(shape_from, "N"),
                            (xc_f, edge_from.top + delta),
                            (xc_t, edge_from.top + delta),
                            self.key_positions(shape_to, "S"),
                        ]
                    elif edge_from.top > edge_to.bottom:
                        log.debug(" B t:%s b:%s", edge_from.top, edge_to.bottom)
                        points = [
                            self.key_positions(shape_from, "N"),
                            (xc_f, yc_t),
                            self.key_positions(shape_to, "E"),
                        ]
                    else:
                        pass
                else:
                    log.debug(" C t:%s b:%s", edge_from.top, edge_to.bottom)
                    points = [
                        self.key_positions(shape_from, "N"),
                        (xc_f, yc_t),
                        self.key_positions(shape_to, "E"),
                    ]

            if xc_f == xc_t and yc_f == yc_t:  # same!
                return
            self.kwargs["points"] = points
            plin = PolylineShape(None, cnv, **self.kwargs)
            plin.draw(ID=ID)
        elif style == "direct":  # straight line
            # ---- direct points
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

        N,S,E,W = North, South, East, West
        """
        top = _shape.y + _shape.height
        btm = _shape.y
        mid_horizontal = _shape.x + _shape.width / 2.0
        mid_vertical = _shape.y + _shape.height / 2.0
        left = _shape.x
        right = _shape.x + _shape.width
        _positions = {
            "NW": (left, top),
            "N": (mid_horizontal, top),
            "NE": (right, top),
            "SW": (left, btm),
            "S": (mid_horizontal, btm),
            "SE": (right, btm),
            "W": (left, mid_vertical),
            "E": (right, mid_vertical),
            # '': (),
        }
        if location:
            return _positions.get(location, ())
        else:
            return _positions
