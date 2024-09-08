# pyprototypr: Layouts

## Overview

**pyprototypr* *allows you to place elements that make up your design anywhere within
a page, or over a series of pages within a deck, but it also includes commands that
you to place, or "layout", elements in a more repetitive or regular way within a page.

To support this, **pyprototypr* *includes a number of different kinds of layouts.

The most basic layout is that of a simple sequence, with elements placed at regular
x- and y-poisitions.

The next most straightforward layout is that of a linear feature; so placing elements
along a line or a polyline. Elements are placed at regular distances along the line
or at a percentage of the total distance along the line.

In a similar way elements can be placed along the border of a polygon shape; for
example, at regular interval along the border of a square or rectangle, or along the
circumference of a circle. The properties needed to construct this kind of layout
differ slightly from that of a line but the principle is the same.

The other way that elements can be laid out on a page is through a grid.
In *pyprototypr*, such a grid can be derived from various of the built-in shapes -
for example, Hexagons - or it can be constructed using a supplied set of properties.
Because these grids do not themselves appear on the page, they are termed "virtual grids".

A virtual grid is not specifically drawn on the page; rather it contains a set of
points at which elements can be drawn. This set of points can be accessed indirectly
by providing a sequence or list of elements which are then drawn in the order required,
starting from a known point on the grid; or each point can be referred to by directly
using its identity and the element then assigned to that point's position.
The first approach is useful when the entire grid will be filled with a single element
(or a repeating set of elements), and the second is more suitable when only some parts
of the grid will be filled or a much finer degrees of control is needed with differing
elements going into very specific - possibly irregular - places.

Very briefly, the different kinds of layout commands are:

* **Sequence()** - allows a set of elements to be placed at regular spacings
* **LineLayout()** - allows elements to be placed along a line; either at fixed distances
  or percentage of the total line length
* **PolygonLayout()** - allows elements to be placed along the border of a polygon
* **CircleLayout()** - allows elements to be placed along the circumference of a circle
* **GridLayout()** - allows elements to be placed at a series of differing x-
  and y-points; the x- and y-values will correspond to the centre of the element
  being placed.
