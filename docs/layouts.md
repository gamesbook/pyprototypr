# pyprototypr: Layouts

## Overview

__pyprototypr__ allows you to place elements that make up your design anywhere within
a page, or over a series of pages within a Deck, but it also includes commands that
let you place, or "layout", elements in a more repetitive or regular way within a page.

To support this, __pyprototypr__ includes a number of different kinds of **layouts**.

The most basic layout is that of a simple **sequence**, with elements placed at regular
x- and y-positions in a linear direction.

In a similar way elements can be placed along a **track**. The track can be defined as
the border of a rectangle or polygon shape; or at regular interval along the
circumference of a circle. The properties needed to construct this kind of layout
differ slightly from that of a linear layout but the principle is the same.

The other way that elements can be laid out on a page is through a **grid layout**.
In __pyprototypr__, such a grid can be derived from various of the built-in shapes -
for example, Hexagons - or it can be constructed using a supplied set of properties.
Because these grids do not themselves appear on the page, they are termed "virtual grids".

A virtual grid is not itself specifically drawn; rather it contains a set of
points at which elements can be drawn. This set of points can be accessed indirectly
by providing a sequence or list of elements which are then drawn in the order required,
starting from a known point on the grid; or each point can be referred to by directly
using its identity and the element then assigned to that point's position.

The first approach is useful when the entire grid will be filled with a single element
(or a repeating set of elements), and the second is more suitable when only some
locations of the grid will be used, or a much finer degrees of control is needed with
differing elements going into very specific - possibly irregular - places.

## Commands

Very briefly, the different kinds of layout commands are as follows.

Linear layout:

* **Sequence()** - allows a set of elements to be placed at regular spacings

Track-based layout, where the elements are positioned on the line used to
delineate a shape:

* **RectangularTrack()** - allows elements to be placed along the border of a rectangle
* **PolygonTrack()** - allows elements to be placed along the border of a polygon
* **CircularTrack()** - allows elements to be placed along the circumference of a circle

Grid-based layouts, where elements appear in two-dimensonal space:

* **RectangularLayout()** - allows elements to be placed at a series of differing x-
  and y-points with rectangular spacing; the x- and y-values will correspond to the
  centre of the element being placed.
* **TriangularLayout()** - allows elements to be placed at a series of differing x-
  and y-points with triangular spacing; the x- and y-values will correspond to the
  centre of the element being placed.
* **IrregularLayout()** - allows elements to be placed at a series of x-
  and y-points that are completely defined by the script- they could even be random!
