pyprototypr: Layouts
====================

Overview 
---------

**pyprototypr** allows you to place elements that make up your design
anywhere within a page, or over a series of pages within a ``Deck``, but
it also includes commands that let you place, or “layout”, elements in a
more repetitive or regular way within a page.

To support this, **pyprototypr** includes a number of different kinds of
**layouts**.

The most basic layout is that of a simple **sequence**, with elements
placed at regular x- and y-positions in a linear direction.

In a similar way elements can be placed along a **track**. The track can
be defined as the border of a rectangle or polygon shape; or at specific
angles along the circumference of a circle. The properties needed to
construct this kind of layout differ slightly from that of a simple
linear layout but the principle is the same. The track can be visible,
or not.

The other way that elements can be laid out on a page is through a
**grid layout**. In **pyprototypr**, such a grid can be derived from
various of the built-in shapes - for example, ``Hexagons`` - or it can
be constructed using a supplied set of properties. Because these grids
do not themselves appear on the page, they are termed “virtual grids”.

A virtual grid is not itself specifically drawn; rather it contains a
set of points at which elements can be drawn. This set of points can be
accessed indirectly, by providing a sequence or list of elements, which
are then drawn in the order required, starting from a known point on the
grid; or each point can be referred to by directly using its identity
and the element then assigned to that point’s position.

The first approach is useful when the entire grid will be filled with a
single element (or a repeating set of elements), and the second is more
suitable when only some locations of the grid will be used, or a much
finer degrees of control is needed with differing elements going into
very specific - possibly irregular - places.

Command Summary 
----------------

Very briefly, the different kinds of layout commands are as follows.

Linear layouts, where elements appear in one-dimensional space:

-  **Sequence()** - allows a set of elements to be placed at regular
   spacings
-  **Track()** - the elements are positioned along the line used to
   delineate a shape; they can be placed either at the vertices of that
   line (e.g. at the corners of a square) or in the centre between two
   sequential vertices.

Grid-based layouts, where elements appear in two-dimensional space:

-  **RectangularLayout()** - allows elements to be placed at a series of
   differing x- and y-points with rectangular spacing; the x- and
   y-values will correspond to the centre of the element being placed.
-  **TriangularLayout()** - allows elements to be placed at a series of
   differing x- and y-points with triangular spacing; the x- and
   y-values will correspond to the centre of the element being placed.
-  **IrregularLayout()** - allows elements to be placed at a series of
   x- and y-points that are completely defined by the script - they
   could even be random!

Sequence Command 
-----------------
