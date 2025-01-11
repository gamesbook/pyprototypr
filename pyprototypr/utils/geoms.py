# -*- coding: utf-8 -*-
"""
Mathematical utility functions for protograf
"""
# lib
from collections import namedtuple
import cmath
import logging
import math
from typing import Any, List

# local
from protograf.utils.support import numbers, feedback

log = logging.getLogger(__name__)
DEBUG = False

Link = namedtuple("Link", ["a", "b", "style"])
fields = ("col", "row", "x", "y", "id", "sequence", "corner", "label")
Locale = namedtuple("Locale", fields, defaults=(None,) * len(fields))
Place = namedtuple("Place", ["shape", "rotation"])
Point = namedtuple("Point", ["x", "y"])
# ray is a mathematical term that specifies a position and direction
Ray = namedtuple("Ray", ["x", "y", "angle"])


def polygon_vertices(
    sides: int, radius: float, centre: Point, starting_angle: float = 0.0
) -> list:
    """Calculate array of Points for a polygon's vertices.

    Args:
        * sides:  number of sides
        * radius: distance from centre
        * centre: Point
        * starting_angle:  effectively the "rotation"

    Doc test:
    >>> P = polygon_vertices(6, 1.0, Point(2,2))
    >>> assert P == [Point(x=3.0, y=2.0), Point(x=2.5, y=2.8660254037844384), \
                     Point(x=1.5000000000000002, y=2.866025403784439), \
                     Point(x=1.0, y=2.0), \
                     Point(x=1.4999999999999996, y=1.1339745962155616), \
                     Point(x=2.5, y=1.1339745962155614)]
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
    #rotate = starting_angle  # this is effectively the "rotation"
    data_generator = numbers(starting_angle, 360.0 + starting_angle, _step)  # go in a full circle
    try:
        _rotate = next(data_generator)
        while True:
            points.append(degrees_to_xy(_rotate, radius, centre))
            _rotate = next(data_generator)
    except RuntimeError:
        pass  # ignore StopIteration
    finally:
        del data_generator
    return points


def degrees_to_xy(degrees: float, radius: float, origin: Point) -> Point:
    """Calculates a Point that is at an angle from the origin;
    0 is to the right.

    Args:
        * degrees: normal angle (NOT radians)

    Doc test
    >>> R = degrees_to_xy(300, 5, Point(0,0))
    >>> assert round(R.x, 2) == 2.5
    >>> assert round(R.y, 2) == -4.33
    >>> R = degrees_to_xy(210, 5, Point(0,0))
    >>> assert round(R.x, 2) == -4.33
    >>> assert round(R.y, 2) == -2.5
    >>> R = degrees_to_xy(120, 5, Point(0,0))
    >>> assert round(R.x, 2) == -2.5
    >>> assert round(R.y, 2) == 4.33
    >>> R = degrees_to_xy(30, 5, Point(0,0))
    >>> assert round(R.x, 2) == 4.33
    >>> assert round(R.y, 2) == 2.5

    >>> R = degrees_to_xy(120, 19, Point(85,113))
    >>> assert round(R.x, 2) == 75.5
    >>> assert round(R.y, 2) == 129.45
    """
    #print(f'+++ degrees_to_xy :: {degrees=}, {radius=}, {origin=}')
    radians = float(degrees) * math.pi / 180.0
    x_o = math.cos(radians) * radius + origin.x
    y_o = math.sin(radians) * radius + origin.y
    #print('+++ +++', Point(x_o, y_o))
    return Point(x_o, y_o)


def point_in_polygon(point: Point, vertices: List[Point], valid_border=False) -> bool:
    """Wrapper for is_inside_polygon() function.

    Doc Test:

    >>> point_in_polygon(Point(1,1), [ Point(1, 1), Point(2, 2), Point(3, 3)])
    False
    >>> point_in_polygon(Point(1,1), [ Point(0, 0), Point(1, 2), Point(2, 0)])
    True
    """
    _point = (point.x, point.y)
    _vertices = [(pnt.x, pnt.y) for pnt in vertices]
    return is_inside_polygon(_point, _vertices, valid_border)


def is_inside_polygon(point: tuple, vertices: list, valid_border=False) -> bool:
    """Check if point inside a polygon defined by set of vertices.

    Ref:
        https://www.linkedin.com/pulse/~
        short-formula-check-given-point-lies-inside-outside-polygon-ziemecki/

    Doc Test:

    >>> is_inside_polygon(Point(1,1), [ Point(1, 1), Point(2, 2), Point(3, 3)])
    False
    >>> is_inside_polygon(Point(1,1), [ Point(0, 0), Point(1, 2), Point(2, 0)])
    True
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
    """Calculate length of line between two Points.

    Doc Test:

    >>> length_of_line(Point(0, 0), Point(0, 1))
    1.0
    >>> length_of_line(Point(0, 0), Point(3, 4))
    5.0
    """
    # √[(x₂ - x₁)² + (y₂ - y₁)²]
    return math.sqrt((end.x - start.x) ** 2 + (end.y - start.y) ** 2)


def point_on_line(point_start: Point, point_end: Point, distance: float) -> Point:
    """Calculate new Point at a distance along a line defined by its end Points

    Doc Test:

    >>> P = Point(0,2)
    >>> Q = Point(4,4)
    >>> D = 3
    >>> R = point_on_line(P, Q, D)
    >>> assert round(R.x, 4) == 2.6833
    >>> assert round(R.y, 4) == 3.3416
    >>> P = Point(4,4)
    >>> Q = Point(0,2)
    >>> D = 3
    >>> R = point_on_line(P, Q, D)
    >>> assert round(R.x, 4) == 1.3167
    >>> assert round(R.y, 4) == 2.6584
    >>> R = point_on_line(Point(0,5), Point(0,2), 1)  # downwards
    >>> assert round(R.x, 4) == 0
    >>> assert round(R.y, 4) == 4
    >>> R = point_on_line(Point(0,2), Point(0,5), 1)  # upwards
    >>> assert round(R.x, 4) == 0
    >>> assert round(R.y, 4) == 3
    >>> R = point_on_line(Point(2,0), Point(5,0), 1)  # right
    >>> assert round(R.x, 4) == 3
    >>> assert round(R.y, 4) == 0
    >>> R = point_on_line(Point(5,0), Point(2,0), 1)  # left
    >>> assert round(R.x, 4) == 4
    >>> assert round(R.y, 4) == 0
    """
    if point_end.x == point_start.x and point_end.y == point_start.y:
        return point_start
    distance = abs(distance)
    if point_end.x != point_start.x and point_end.y != point_start.y:
        line = math.sqrt(
            (point_end.x - point_start.x) ** 2 + (point_end.y - point_start.y) ** 2
        )
        ratio = distance / line
        x = (1.0 - ratio) * point_start.x + ratio * point_end.x
        y = (1.0 - ratio) * point_start.y + ratio * point_end.y
    elif point_end.y == point_start.y:
        distance = distance * -1.0 if point_start.x > point_end.x else distance
        x = point_start.x + distance
        y = point_end.y
    elif point_end.x == point_start.x:
        distance = distance * -1.0 if point_start.y > point_end.y else distance
        y = point_start.y + distance
        x = point_end.x
    else:
        raise NotImplementedError(
            f'Cannot calculate line on point for: {point_start} and {point_end}')
    return Point(x, y)


def point_on_circle(point_centre: Point, radius: float, angle: float) -> Point:
    """Calculate Point on circumference of a circle at a specific angle in degrees

    >>> P = Point(0,0)
    >>> R = 3.0
    >>> T = 45.0
    >>> R = point_on_circle(P, R, T)
    >>> assert round(R.x, 4) == 2.1213
    >>> assert round(R.y, 4) == 2.1213
    """
    if radius == 0.0:
        return point_centre
    try:
        theta = float(angle) * math.pi / 180.0
        x = math.cos(theta) * radius + point_centre.x
        y = math.sin(theta) * radius + point_centre.y
    except:
        raise ValueError(
            f'Cannot calculate point on circle for: {point_centre}, {radius} and {angle}')
    return Point(x, y)


def fraction_along_line(point_start: Point, point_end: Point, fraction: float) -> Point:
    """Calculate new Point at a fractional distance along line defined by end Points
    """
    if fraction > 1.0 or fraction < 0.0:
        raise ValueError(
            'The fraction cannot be greater than 1 or less than 0.')
    line_length = length_of_line(start=point_start, end=point_end)
    fraction_length = fraction * line_length
    fraction_point = point_on_line(
        point_start=point_start,
        point_end=point_end,
        distance=fraction_length)
    return fraction_point


def angles_from_points(x1, y1, x2, y2, radians=False):
    """Given two points, calculate the compass and rotation angles between them

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


def separation_between_hexsides(side_a, side_b):
    """Levels of separation between two sides of a hexagon.

    Notes:
        Sides are numbered from 1 to 6 (by convention starting at furthest left).

    Doc Test:

    >>> separation_between_hexsides(1, 1)
    0
    >>> separation_between_hexsides(1, 2)
    1
    >>> separation_between_hexsides(1, 3)
    2
    >>> separation_between_hexsides(1, 4)
    3
    >>> separation_between_hexsides(1, 5)
    2
    >>> separation_between_hexsides(1, 6)
    1
    >>> separation_between_hexsides(6, 1)
    1
    >>> separation_between_hexsides('a', 1)
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
    return dist


def lines_intersect(A: Point, B: Point, C: Point, D: Point) -> bool:
    """ "Return True if line segments AB and CD intersect

    Ref:
        https://stackoverflow.com/questions/3838329

    Doc Test:

    >>> lines_intersect(Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3))
    False
    >>> lines_intersect(Point(0, 0), Point(2, 2), Point(2, 0), Point(0, 2))
    True
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


def circle_angles(radius: float, chord: float):
    """Calculate interior angles of isosceles triangle formed inside a circle.

    Source:
        https://www.quora.com/How-do-you-find-the-angles-of-an-isosceles-triangle-given-three-sides

    Doc Test:

    >>> R = circle_angles(5., 6.)
    >>> assert round(R[0], 2) == 73.74
    >>> assert round(R[1], 2) == 53.13
    """
    top = math.acos((2. * radius**2 - chord**2) / (2. * radius**2))
    base = (180. -  math.degrees(top)) / 2.
    return math.degrees(top), base, base


def equilateral_height(side: Any):
    """Calculate height of equilateral triangle from a side.

    Doc Test:

    >>> equilateral_height(5)
    4.330127018922194
    """
    _side = float(side)
    return math.sqrt(_side**2 - (0.5 * _side)**2)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
