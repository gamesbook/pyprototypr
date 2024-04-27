# -*- coding: utf-8 -*-
"""
Utility functions for pyprototypr
"""
# lib
from collections import namedtuple
import cmath
import csv
import collections
from itertools import zip_longest
import logging
import math
import os
import pathlib
import string
import sys
import xlrd

# local
from pyprototypr.utils.support import numbers, feedback

log = logging.getLogger(__name__)
DEBUG = False

Point = namedtuple("Point", ["x", "y"])
Link = namedtuple("Link", ["a", "b", "style"])


def script_path():
    """Get the path for a script being called from command line."""
    fname = os.path.abspath(sys.argv[0])
    if fname:
        return pathlib.Path(fname).resolve().parent


def load_data(datasource=None, **kwargs):
    """
    Load data from a 'tabular' source (CSV, XLS) into a dict
    """
    dataset = {}
    log.debug("Load data from a 'tabular' source (CSV, XLS) %s", datasource)
    if datasource:
        filename, file_ext = os.path.splitext(datasource)
        if file_ext.lower() == ".csv":
            headers = kwargs.get("headers", None)
            selected = kwargs.get("selected", None)
            dataset = open_csv(datasource, headers=headers, selected=selected)
        elif file_ext.lower() == ".xls":
            headers = kwargs.get("headers", None)
            selected = kwargs.get("selected", None)
            sheet = kwargs.get("sheet", 0)
            sheetname = kwargs.get("sheetname", None)
            dataset = open_xls(
                datasource,
                sheet=sheet,
                sheetname=sheetname,
                headers=headers,
                selected=selected,
            )
        else:
            feedback('Unable to process a file %s of type "%s"' % (filename, file_ext))
    return dataset


def grouper(n, iterable, fillvalue=None):
    """group and return sets

    See:
        http://stackoverflow.com/questions/2990121/~
        how-do-i-loop-through-a-python-list-by-twos
    """
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    # grouper(3, [1,3,2,4,5,7,6,8,0], None) --> 1 3 2   4 5 7   6 8 0
    # use: for item1, item2 in grouper(3, l):
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def boolean_join(items):
    """Create a result from boolean concatenation

    >>> items = [True, '+', False]
    >>> boolean_join(items)
    False
    >>> items = [True, '|', False]
    >>> boolean_join(items)
    True
    >>> items = [True, None]
    >>> boolean_join(items)
    True
    """
    if not items or len(items) == 0:
        return None
    expr = ""
    for item in items:
        if item == "&" or item == "and" or item == "+":
            expr += " and "
        elif item == "|" or item == "or":
            expr += " or "
        elif item is not None:
            expr += "%s" % item
        else:
            pass  # ignore nones
    try:
        result = eval(expr)
    except NameError:
        return None
    return result


def query_construct(string):
    """
    Split a query string into a list of lists.

    string: str
        boolean-type expression which can be evaluated to return a True
        e.g.1 'name`=`fred' filters item for dataset['name'] == 'fred'
        e.g.2 name`fred is a shortcut for the equals expression!
        e.g.3 'name`=`fred`&`height`<`6' filters item for:
            dataset['name'] == 'fred' and dataset['height'] < 6.0
    """
    result = []
    if string:
        items = string.split("`")
        if len(items) == 2:
            items.insert(1, "=")
        for item1, item2, item3, item4 in grouper(4, items):
            result.append([item1, item2, item3, item4])
        return result
    return [(None, None, None)]


def tuple_split(string):
    """
    Split a string into a list of tuple values

    from utils.tools import tuple_split
    print(tuple_split(''))
    #[]
    print(tuple_split('3'))
    #[3]
    print(tuple_split('3,4'))
    #[(3, 4)]
    print(tuple_split('3,5 6,1 4,2'))
    #[(3, 5), (6, 1), (4, 2)]
    """
    values = []
    if string:
        try:
            _string_list = string.strip(" ").replace(";", ",").split(" ")
            for _str in _string_list:
                items = _str.split(",")
                _items = [float(itm) for itm in items]
                values.append(tuple(_items))
            return values
        except Exception:
            return values
    else:
        return values


def sequence_split(string):
    """
    Split a string into a list of individual values

    import tools
    print(tools.sequence_split(''))
    #[]
    print(tools.sequence_split('3'))
    #[3]
    print(tools.sequence_split('3,4,5'))
    #[3, 4, 5]
    print(tools.sequence_split('3-5,6,1-4'))
    #[1, 2, 3, 4, 5, 6]
    """
    values = []
    if string:
        try:
            _string = (
                string.replace(" ", "")
                .replace('"', "")
                .replace("'", "")
                .replace(";", ",")
            )
        except Exception:
            return values
    else:
        return values
    try:
        values.append(int(_string))
        return values
    except Exception:
        _strings = _string.split(",")
        # log.debug('strings:%s', _strings)
        for item in _strings:
            if "-" in item:
                _strs = item.split("-")
                seq_range = list(range(int(_strs[0]), int(_strs[1]) + 1))
                values = values + seq_range
            else:
                values.append(int(item))
    return list(set(values))  # unique


def splitq(seq, sep=None, pairs=("()", "[]", "{}"), quote="\"'"):
    """Split seq by sep but considering parts inside pairs or quoted as
       unbreakable pairs have different start and end value, quote have same
       symbol in beginning and end.

    Use itertools.islice if you want only part of splits

    Source:
        https://www.daniweb.com/programming/software-development/code/426990/\
        split-string-except-inside-brackets-or-quotes
    """
    if not seq:
        yield []
    else:
        lsep = len(sep) if sep is not None else 1
        lpair, _ = zip(*pairs)
        pairs = dict(pairs)
        start = index = 0
        while 0 <= index < len(seq):
            c = seq[index]
            if (sep and seq[index:].startswith(sep)) or (sep is None and c.isspace()):
                yield seq[start:index]
                # pass multiple separators as single one
                if sep is None:
                    index = len(seq) - len(seq[index:].lstrip())
                else:
                    while sep and seq[index:].startswith(sep):
                        index = index + lsep
                start = index
            elif c in quote:
                index += 1
                p, index = index, seq.find(c, index) + 1
                if not index:
                    raise IndexError("Unmatched quote %r\n%i:%s" % (c, p, seq[:p]))
            elif c in lpair:
                nesting = 1
                while True:
                    index += 1
                    p, index = index, seq.find(pairs[c], index)
                    if index < 0:
                        raise IndexError(
                            "Did not find end of pair for %r: %r\n%i:%s"
                            % (c, pairs[c], p, seq[:p])
                        )
                    nesting += "{lpair}({inner})".format(
                        lpair=c, inner=splitq(seq[p:index].count(c) - 2)
                    )
                    if not nesting:
                        break
            else:
                index += 1
        if seq[start:]:
            yield seq[start:]


def open_csv(filename, headers=None, selected=None):
    """Read data from CSV file into a list of dictionaries

    Supply:

      * headers is a list of strings to use instead of the first row
      * selected is a list of desired rows e.g. [2,4,7]
    """
    if not filename:
        feedback("A valid CSV filename must be supplied!")

    dict_list = []
    _file_with_path = None
    norm_filename = os.path.normpath(filename)
    if not os.path.exists(norm_filename):
        filepath = script_path()
        _file_with_path = os.path.join(filepath, norm_filename)
        if not os.path.exists(_file_with_path):
            feedback(f'Unable to find CSV "{filename}", including in {filepath}')

    try:
        csv_filename = _file_with_path or norm_filename
        if headers:
            reader = csv.DictReader(open(csv_filename), fieldnames=headers)
        else:
            reader = csv.DictReader(open(csv_filename))
        for key, item in enumerate(reader):
            if not selected:
                dict_list.append(item)
            else:
                if key + 1 in selected:
                    dict_list.append(item)
    except IOError:
        feedback('Unable to find or open CSV "%s"' % csv_filename)
    return dict_list


def open_xls(filename, sheet=0, sheetname=None, headers=None, selected=None):
    """Read data from XLS file into a list of dictionaries

    Supply:

      * sheet to select a sheet number (otherwise first is used)
      * sheetname to select a sheet by name (otherwise first is used)
      * headers is a list of strings to use instead of the first row
      * selected is a list of desired rows e.g. [2,4,7]
    """
    if not filename:
        feedback("A valid Excel filename must be supplied!")

    dict_list = []

    _file_with_path = None
    norm_filename = os.path.normpath(filename)
    if not os.path.exists(norm_filename):
        filepath = script_path()
        _file_with_path = os.path.join(filepath, norm_filename)
        if not os.path.exists(_file_with_path):
            feedback(f'Unable to find "{filename}", including in {filepath}')

    try:
        excel_filename = _file_with_path or norm_filename
        book = xlrd.open_workbook(excel_filename)
        if sheet:
            sheet = sheet - 1
            sheet = book.sheet_by_index(sheet)
        elif sheetname:
            sheet = book.sheet_by_name(sheetname)
        else:
            sheet = book.sheet_by_index(0)
        start = 1
        if not headers:
            keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]
        else:
            start = 0
            keys = headers
        if len(keys) < sheet.ncols:
            feedback(
                'Too few headers supplied for the existing columns in "%s"' % filename
            )
        else:
            dict_list = []
            for row_index in range(start, sheet.nrows):
                item = {
                    keys[col_index]: sheet.cell(row_index, col_index).value
                    for col_index in range(sheet.ncols)
                }
                if not selected:
                    dict_list.append(item)
                else:
                    if row_index + 1 in selected:
                        dict_list.append(item)
    except IOError:
        feedback('Unable to find or open Excel "%s"' % excel_filename)
    except IndexError:
        feedback('Unable to open sheet "%s"' % (sheet or sheetname))
    except xlrd.biffh.XLRDError:
        feedback('Unable to open sheet "%s"' % sheetname)
    return dict_list


def flatten(lst):
    """Flatten nested lists into a single list of lists."""
    try:
        for ele in lst:
            if isinstance(ele, collections.abc.Iterable) and not isinstance(ele, str):
                for sub in flatten(ele):
                    yield sub
            else:
                yield ele
    except TypeError:
        yield lst


def comparer(val, operator, target):
    """target could be list?? - split a string by , or ~

    assert comparer(None, None, None) == True

    assert comparer("1", '*', "1") == False

    assert comparer("1", None, "1") == True
    assert comparer("a", None, "a") == True
    assert comparer("True", None, "True") == True
    assert comparer("False", None, "False") == True

    assert comparer("1", '<', "1.1") == True
    assert comparer("a", '<', "aa") == True
    assert comparer("True", '<', "True") == False
    assert comparer("False", '<', "False") == False

    assert comparer("1", '~', "1.1") == False
    assert comparer("a", '~', "aa") == True
    assert comparer("True", '~', "True") == False
    assert comparer("False", '~', "False") == False

    assert comparer("1", '~', [1,2,3]) == True
    """

    def to_length(val, target):
        """Get length of object."""
        try:
            val = len(val)
        except Exception:
            pass
        try:
            target = len(target)
        except Exception:
            pass
        return val, target

    if target == "T" or target == "True":
        target = True
    if target == "F" or target == "False":
        target = False
    if val == "T" or val == "True":
        val = True
    if val == "F" or val == "False":
        val = False

    if not operator:
        operator = "="
    if operator in ["<", "<=", ">", ">="]:
        val, target = to_length(val, target)

    try:
        val = float(val)
    except Exception:
        pass
    try:
        target = float(target)
    except Exception:
        pass
    if operator == "=":
        if val == target:
            return True
    elif operator == "~" or operator == "in":
        try:
            if val in target:
                return True
        except TypeError:
            pass
    elif operator == "!=":
        if val != target:
            return True
    elif operator == "<":
        if val < target:
            return True
    elif operator == ">":
        if val > target:
            return True
    elif operator == ">=":
        if val >= target:
            return True
    elif operator == "<=":
        if val <= target:
            return True
    else:
        feedback("Unknown operator: %s (%s and %s)" % (operator, val, target))
    return False


def polygon_vertices(
    sides: int, radius: float, starting_angle: float, center: Point
) -> list:
    """Calculate array of Points for a polygon's vertices.

    Args:
        * sides:  number of sides
        * radius: distance from center
        * starting_angle:  effectively the "rotation"
        * center: Point
    """
    try:
        sides = int(sides)
        if sides < 3:
            sides = 3
    except ValueError:
        feedback("Polygon's sides must be an integer of 3 or more.")
        return []
    points = []
    _step = 360.0 / sides
    rotate = starting_angle  # this is effectively the "rotation"
    data_generator = numbers(starting_angle, 360, _step)  # go in a full circle
    try:
        rotate = next(data_generator)
        while True:
            points.append(degrees_to_xy(rotate, radius, center))
            rotate = next(data_generator)
    except RuntimeError:
        pass  # ignore StopIteration
    finally:
        del data_generator
    return points


def color_to_hex(name):
    """Convert a named ReportLab color (Color class) to a hexadecimal string"""
    _tuple = (int(name.red * 255), int(name.green * 255), int(name.blue * 255))
    _string = "#%02x%02x%02x" % _tuple
    return _string.upper()


def degrees_to_xy(degrees: float, radius: float, origin: Point) -> Point:
    """Calculates a Point that is at an angle from the origin;
    0 is to the right.

    Args:
        * degrees: normal angle (NOT radians)
    """
    radians = float(degrees) * math.pi / 180.0
    x_o = math.cos(radians) * radius + origin.x
    y_o = math.sin(-radians) * radius + origin.y
    return Point(x_o, y_o)


def sheet_column(num: int, lower: bool = False) -> string:
    """Convert a spreadsheet number to a column letter

    Ref:
        https://stackoverflow.com/questions/23861680/
    """

    def converter(num, lower):
        if lower:
            return (
                ""
                if num == 0
                else converter((num - 1) // 26, lower)
                + string.ascii_lowercase[(num - 1) % 26]
            )
        else:
            return (
                ""
                if num == 0
                else converter((num - 1) // 26, lower)
                + string.ascii_uppercase[(num - 1) % 26]
            )

    return converter(num, lower)


def is_inside_polygon(point: tuple, vertices: list, valid_border=False) -> bool:
    """Check if point inside a polygon defined by set of vertices.

    Ref:
        https://www.linkedin.com/pulse/~
        short-formula-check-given-point-lies-inside-outside-polygon-ziemecki/
    """

    def _is_point_in_segment(point, point_0, point_1):
        p_0 = point_0[0] - point[0], point_0[1] - point[1]
        p_1 = point_1[0] - point[0], point_1[1] - point[1]
        det = p_0[0] * p_1[1] - p_1[0] * p_0[1]
        prod = p_0[0] * p_1[0] + p_0[1] * p_1[1]
        return (
            (det == 0 and prod < 0)
            or (p_0[0] == 0 and p_0[1] == 0)
            or (p_1[0] == 0 and p_1[1] == 0)
        )

    sum_ = complex(0, 0)
    for vertex in range(1, len(vertices) + 1):
        v0, v1 = vertices[vertex - 1], vertices[vertex % len(vertices)]
        if _is_point_in_segment(point, v0, v1):
            return valid_border
        sum_ += cmath.log(
            (complex(*v1) - complex(*point)) / (complex(*v0) - complex(*point))
        )
    return abs(sum_) > 1


def length_of_line(start: Point, end: Point) -> float:
    """Calculate length of line between two Points."""
    # √[(x₂ - x₁)² + (y₂ - y₁)²]
    return math.sqrt((end.x - start.x) ** 2 + (end.y - start.y) ** 2)


def point_on_line(point_start: Point, point_end: Point, distance: float) -> Point:
    """Calculate new Point at a distance along a line defined by its Points

    >>> P = Point(0,2)
    >>> Q = Point(4,4)
    >>> D = 3
    >>> R = point_on_line(P, Q, D)
    >>> assert round(R.x, 4) == 2.6833
    >>> assert round(R.y, 4) == 3.3416
    """
    line = math.sqrt(
        (point_end.x - point_start.x) ** 2 + (point_end.y - point_start.y) ** 2
    )
    ratio = distance / line
    x = (1.0 - ratio) * point_start.x + ratio * point_end.x
    y = (1.0 - ratio) * point_start.y + ratio * point_end.y
    return Point(x, y)


def angles_from_points(x1, y1, x2, y2, radians=False):
    """Given two points, calculate the angles between them

    Returns:
        compass (float): degrees clockwise from North
        rotation (float): degrees anti-clockwise from East

    Doc Test:

    >>> # clockwise around circle from 0 degrees at North
    >>> angles_from_points(0, 0, 0, 4)
    (0.0, 90.0)
    >>> angles_from_points(0, 0, 4, 4)
    (45.0, 45.0)
    >>> angles_from_points(0, 0, 4, 0)
    (90.0, 0.0)
    >>> angles_from_points(0, 0, 4, -4)
    (135.0, 315.0)
    >>> angles_from_points(0, 0, 0, -4)
    (180.0, 270.0)
    >>> angles_from_points(0, 0, -4, -4)
    (225.0, 225.0)
    >>> angles_from_points(0, 0, -4, 0)
    (270.0, 180.0)
    >>> angles_from_points(0, 0, -4, 4)
    (315.0, 135.0)
    """
    a, b = x2 - x1, y2 - y1
    if x2 != x1:
        gradient = (y2 - y1) / (x2 - x1)
        theta = math.atan(gradient)
        angle = theta * 180.0 / math.pi
        # feedback(f'{x1-x1=} {y1-y1=} {a=} {b=} {angle=}')
        if a > 0 and b >= 0:
            compass = 90.0 - angle
        if a > 0 and b < 0:
            compass = 90 - angle
        if a < 0 and b < 0:
            compass = 270.0 - angle
        if a < 0 and b >= 0:
            compass = 270.0 - angle
    else:
        compass = 0.0
        if y2 - y1 < 0:
            compass = 180.0
    rotation = (450 - compass) % 360.0
    # feedback(f'angle fn: {compass=}, {rotation=}')
    return compass, rotation


def arc_angle_between_hexsides(side_a, side_b):
    """Arc of angle between two sides of a hexagon.

    Notes:
        Sides are numbered from 1 to 6 (by convention starting at furthest left).

    Doc Test:

    >>> arc_angle_between_hexsides(1, 1)
    0.0
    >>> arc_angle_between_hexsides(1, 2)
    60.0
    >>> arc_angle_between_hexsides(1, 3)
    120.0
    >>> arc_angle_between_hexsides(1, 4)
    180.0
    >>> arc_angle_between_hexsides(1, 5)
    120.0
    >>> arc_angle_between_hexsides(1, 6)
    60.0
    >>> arc_angle_between_hexsides(6, 1)
    60.0
    >>> arc_angle_between_hexsides('a', 1)
    """
    try:
        _side_a = 6 if (side_a % 6 == 0) else side_a % 6
        _side_b = 6 if (side_b % 6 == 0) else side_b % 6
    except TypeError:
        # tools.feedback(f'Cannot use {side_a} and/or {side_b} as side numbers.', True)
        return None
    if _side_a - _side_b > 3:
        result = (_side_b, _side_a)
    else:
        result = (_side_b, _side_a) if _side_b > _side_a else (_side_a, _side_b)
    dist = (result[0] - result[1]) % 6
    if _side_a == 2 and _side_b == 6:
        dist = 2
    if _side_a == 1 and _side_b == 5:
        dist = 2
    if _side_a == 1 and _side_b == 6:
        dist = 1
    return dist * 60.0


def lines_intersect(A: Point, B: Point, C: Point, D: Point) -> bool:
    """ "Return True if line segments AB and CD intersect

    Ref:
        https://stackoverflow.com/questions/3838329
    """

    def ccw(A: Point, B: Point, C: Point):
        return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def bezier_arc_segment(
    cx: float, cy: float, rx: float, ry: float, theta0: float, theta1: float
):
    """Compute the control points for a Bezier arc with angles theta1-theta0 <= 90.

    Points are computed for an arc with angle theta increasing in the
    counter-clockwise (CCW) direction. Zero degrees is at the "East" position.

    Returns:
        tuple: starting point and 3 control points of a cubic Bezier curve

    Source:
        https://github.com/makinacorpus/reportlab-ecomobile/blob/master/src/reportlab/graphics/renderPM.py

    Doc Test:

    >>> bezier_arc_segment(cx=1, cy=2.5, rx=0.5, ry=0.5, theta0=90, theta1=180)
    ((1.0, 3.0), (0.7238576250846034, 3.0, 0.5, 2.7761423749153966, 0.5, 2.5))
    >>> bezier_arc_segment(cx=1, cy=2.5, rx=0.5, ry=0.5, theta0=90, theta1=270)
    FEEDBACK:: Angles must have a difference less than, or equal to, 90
    """

    # Requires theta1 - theta0 <= 90 for a good approximation
    if abs(theta1 - theta0) > 90:
        feedback('Angles must have a difference less than, or equal to, 90')
        return None
    cos0 = math.cos(math.pi * theta0 / 180.0)
    sin0 = math.sin(math.pi * theta0 / 180.0)
    x0 = cx + rx * cos0
    y0 = cy + ry * sin0

    cos1 = math.cos(math.pi * theta1 / 180.0)
    sin1 = math.sin(math.pi * theta1 / 180.0)

    x3 = cx + rx * cos1
    y3 = cy + ry * sin1

    dx1 = -rx * sin0
    dy1 = ry * cos0

    half_angle = math.pi * (theta1 - theta0) / (2.0 * 180.0)
    k = abs(4.0 / 3.0 * (1.0 - math.cos(half_angle)) / (math.sin(half_angle)))
    x1 = x0 + dx1 * k
    y1 = y0 + dy1 * k

    dx2 = -rx * sin1
    dy2 = ry * cos1

    x2 = x3 - dx2 * k
    y2 = y3 - dy2 * k
    return (x0, y0), (x1, y1, x2, y2, x3, y3)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
