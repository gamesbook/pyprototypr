=======
Layouts
=======

This section assumes you are very familiar with the concepts, terms and ideas
for `pyprototypr <index.rst>`_  as presented in the
`Basic Concepts <basic_concepts.rst>`_ , that you understand all of the
`Additional Concepts <additional_concepts.rst>`_ and that you've created some
basic scripts of your own using the `Core Shapes <core_shapes.rst>`_.

.. _table-of-contents:

Table of Contents
=================

-  `Overview`_
-  `Command Summary`_
-  `Command Details`_

Overview
========
`↑ <table-of-contents_>`_

**pyprototypr** allows you to directly define where elements, that make up
your design, should be placed within a page, or over a series of pages
within a ``Deck``, but it also includes commands that let you place, or
"layout", elements in a more repetitive or regular way within a page.

To support this, **pyprototypr** includes a number of different kinds of
**layouts**.

Sequences and Tracks
--------------------

The most basic layout is that of a simple **sequence**, with elements
placed at regular x- and y-positions in a linear direction.

In a similar way elements can be placed along a **track**. The track can
be defined as the border of a rectangle or polygon shape; or at specific
angles along the circumference of a circle. The properties needed to
construct this kind of layout differ slightly from that of a simple
linear layout but the principle is the same. The track can be visible,
or not.

Grid-based Locations
--------------------

The other way that elements can be laid out on a page is through a
grid **locations**. In **pyprototypr**, such a grid can be derived from
various of the built-in shapes - for example, ``Hexagons`` - or it can
be constructed using a supplied set of properties. Because these grids
do not themselves appear on the page, they are termed "virtual grids".

A virtual grid is **not** specifically drawn on the page; rather it creates
a set of point locations at which elements can be drawn. This set of points
can be used for creating a layout by:

1. providing a sequence or list of elements, which are then drawn in the
   order specified by the "virtual grid" points, starting from a known point
   on the grid; *or*
2. refering to each point directly, by using the identity of its locations,
   and then drawing the element using that point’s position.

.. NOTE::

    The *first approach* is useful when the entire grid will be filled with a
    single element (or a repeating set of elements), and the *second approach*
    is more suitable when only some locations of the grid will be used, or if a
    much finer degree of control is needed with differing elements going into
    very specific - and possibly irregular - places that the script specifies.


Command Summary
===============
`↑ <table-of-contents_>`_

Very briefly, the different kinds of layout commands are as follows.

Linear layouts, where elements appear in one-dimensional space:

-  **Sequence()** - allows a set of elements to be placed at regular
   intervals in a straight line
-  **Track()** - the elements are positioned along the line used to
   delineate a shape; they can be placed either at the vertices of that
   line (e.g. at the corners of a square) or in the centre between two
   sequential vertices.

Grid-based layouts, where elements appear in two-dimensional space:

-  **Repeat()** - allows an element to be placed multiple times onto
   a grid
-  **RectangularLocations()** - defines a series of differing x- and y-points
   in a rectangular pattern; these x- and y-values will set the
   centre of any element being placed on the grid
-  **TriangularLocations()** - defines a series of differing x- and y-points
   in a triangular pattern; these x- and y-values will set the
   centre of any element being placed on the grid

These Location-types are paired with the **Layout()** command, which
links them with the shapes that are to be drawn at their locations.


Command Details
===============
`↑ <table-of-contents_>`_

The commands are described in detail, with examples, in these sections:

- `Repeat <layouts_repeat.rst>`_
- `Sequence <layouts_sequence.rst>`_
- `Track <layouts_track.rst>`_
- `RectangularLocations <layouts_rectangular.rst>`_
- `TriangularLocations <layouts_triangular.rst>`_
