# pyprototypr: Terminology

__pyprototypr__ uses many terms; most of which should - hopefully - be
reasonably obvious by the context in which they are used.

However, in order to help with clarity, below is a reasonably comprehensive
list of terms used in various places, grouped by what they affect.

## Table of Contents for Terms

* [Location-orientated](#location)
* [Size- and length-orientated](#size)
* [Amount- and count-orientated](#count)
* [Direction-orientated](#direction)
* [](#)


## Location-orientated terms <a name="location"></a>


## Size- and length-orientated terms <a name="size"></a>

The majority of size and length properties will be numeric values, corresponding
to the **unit** in use.  Default is usually 1.

* **|** - the
* **|** - the
* **|** - the
* **|** - the

* **dot_point** - the diameter of a small `Dot` in **points** (there are
  72 points in an inch)
* **height** - the vertical size of a shape e.g. a `Rectangle` or a bitmap
  `Image`
* **margin** - used in `Create` command to set all margins for a page; the
  default for any margin is 1.25cm / 12.5mm (1/2 of an inch)
* **margin_top** - used in `Create` command to set top margin for a page
* **margin_bottom** - used in `Create` command to set bottom margin for a page
* **margin_left** - used in `Create` command to set left margin for a page
* **margin_right** - used in `Create` command to set right margin for a page
* **pagesize** - used in `Create` command to set the size of the pages in the
  documents; either ISO series (A0 down to A8; or B6 down to B0) or a USA type
  (_NOTE:_ the pagesize is not wrapped in quotes!)
* **scaling** - the amount by which an SVG image should be shrunk or
  expanded e.g. 0.5 makes it half-size and 2.0 doubles its size; because
  SVG is a vector-format, there will be no loss of resolution by scaling
* **side** - the length of a side of some shapes (e.g. `Square`, `Polygon`) as
  well as the distance between each adjacent point in a `TriangularLayout`
* **width** - the horizontal size of a shape e.g. a `Rectangle` or a bitmap
  `Image`
* **x** - the location of a point in the horizontal direction; its often the
  case that the distance is not absolute, but relative to some other value
  e.g. distance from a margin; or the edge of a `Card`
* **y** - the location of a point in the vertical direction; its often the
  case that the distance is not absolute, but relative to some other value
  e.g. distance from a margin; or the edge of a `Card`

## Amount- and count-orientated terms <a name="count"></a>


## Direction-orientated terms <a name="direction"></a>

In general, there are two primary ways of determining direction of something;
either by compass direction or angle.

The _angle_ is the amount of rotation, in degrees, starting from a value of
0 (zero) which is assumed to be the line parallel to the bottom of the page
(as you would normally look at it). Ninety (90) degrees is the angle of a
line to the side of the page, and so on.  The maximum rotation is 360 degrees.

A _compass direction_ is one of the following:

Primary compass directions:

* North (n) - normally corresponds to an angle of 90 degrees
* South (s) - normally corresponds to an angle of 270 degrees
* East (e) - normally corresponds to an angle of 0 degrees
* West (e) - normally corresponds to an angle of 180 degrees

Secondary compass directions:

* NorthEast (ne) - normally corresponds to an angle of 45 degrees
* SouthEast (se) - normally corresponds to an angle of 315 degrees
* NorthWest (nw) - normally corresponds to an angle of 135 degrees
* SouthWest (sw) - normally corresponds to an angle of 225 degrees

> NOTE - if a compass direction is used in the context of a **hexagon**, the
> angle is "reinterprated" to match its context e.g. the angle for NorthEast
> for a 'pointy' hexagon is 60, not 45, degrees.

Properties that use direction include:

* **direction** - can be any primary compass direction; used to show the travel
  route when moving through various kinds of  of layouts
* **facing** - can be any primary compass direction; used to show orientation
  of some types of layouts e.g. `DiamondLayout`
* **start** - can be any secondary compass direction; used to show in which
  corner of a `RectangularLayout` that shapes are first placed.
