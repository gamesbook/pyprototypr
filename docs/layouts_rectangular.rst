============================
RectangularLocations Command
============================

**pyprototypr** allows you to directly define where elements, that make up
your design, should be placed within a page, or over a series of pages
within a ``Deck``, but it also includes commands that let you place, or
"`layout <layouts.rst>`_", elements in a more repetitive or regular way
within a page.

.. _table-of-contents:

Table of Contents
=================

- `Overview`_
- `Usage`_
- `Key Properties`_


Overview
========
`↑ <table-of-contents_>`_

The ``RectangularLocations()`` command defines an ordered series
of row and column locations that create a rectangular grid.  The x- and
y-values of these rows and columns are then used to set the centres of
the elements that can be placed there using the ``Layout()`` command.

The rows and columns themselves are not drawn - if needed you can use the
*debug* property to display them (see `Example 9. Debug`_  below).

Apart from the ``RectangularLocations()`` command described here, there are
also other ways to place elements on a page:

- `Sequences <layouts_sequence.rst>`_
- `Tracks <layouts_track.rst>`_
- `TriangularLocations <layouts_triangular.rst>`_


Usage
=====
`↑ <table-of-contents_>`_

The ``RectangularLocations()`` command accepts the following properties:

- **cols** - this is the number of locations in the horizontal direction
- **rows** - this is the number of locations in the vertical direction
- **spacing** - this is horizontal distance between columns, as well as the
  vertical distance between rows, in the grid; defaults to ``1`` cm
- **col_spacing** - this is horizontal distance between columns in the grid;
  defaults to **spacing**
- **row_spacing** - this is vertical distance between rows in the grid;
  defaults to **spacing**
- **direction** - this is compass direction of the line of travel when
  creating the row and column layout
- **start** - this is initial corner, defined a ecomdary compass direction,
  from where the grid is drawn
- **pattern** - this is the way in which the grid is draw; default is to draw
  each row, and then move across all columns in a regular line; but the setting
  can also be:

  - *snaking* - which means the direction is reversed across each row
  - *outer* - which means only the locations in the outer-most edge of the grid
    are created

The ``Layout()`` command accepts the following properties:

- **grid** - this *must* be the first property used for the command; it will
  refer to, in this case, a row & column grid created by ``RectangularLocations()``
- **shapes** - this is a list of one or more of the core shapes available,
  for example, a circle or rectangle
- **masked** - a list of sequence numbers of any shapes that should **not**
  be displayed
- **visible** - a list of sequence numbers of the **only** shapes that should
  be displayed
- **debug** - this will display the centre points of the grid, along with any
  extra information specified.  Allowed settings for debug include:

  - *none* - only the locations are shown
  - *count* - shows the sequence number (i.e. the order of drawing)
  - *xy* - shows x- and y-values
  - *yx* - shows y- and x-values
  - *rowcol* - shows row and column numbers
  - *colrow* - shows column and row numbers
  - *id* - shows the internal ID number assigned to the location

.. _key-properties:

Key Properties
==============
`↑ <table-of-contents_>`_

- `Example 1. Rows and Columns`_
- `Example 2. Start and Direction`_
- `Example 3. Row and Column Spacing`_
- `Example 4. Row and Column Offset`_
- `Example 5. Snaking`_
- `Example 6. Outer Edge`_
- `Example 7. Masked`_
- `Example 8. Visible`_
- `Example 9. Debug`_

All examples below make use of a common ```Circle`` shape (called *a_circle*)
defined as:

  .. code:: python

    circles = Common(
        x=0, y=0, diameter=1.0,
        label="{count}/{col}-{row}", label_size=6)
    a_circle = circle(common=circles)

In these examples, the placeholder names ``{count}``, ``{col}`` and ``{row}``
will be replaced, in the label for the Circle, by the values for the row and
column in which that circle is placed, as well as by the sequence number
(order) in which that Circle is drawn.

Example 1. Rows and Columns
---------------------------
`^ <key-properties_>`_

.. |r00| image:: images/layouts/rect_basic_default.png
   :width: 330

===== ======
|r00| This example shows the element constructed using the following values
      for its properties.

      .. code:: python

        rect = RectangularLocations(
            cols=3, rows=4)
        Layout(rect, shapes=[a_circle,])

===== ======

Example 2. Start and Direction
------------------------------
`^ <key-properties_>`_

.. |r01| image:: images/layouts/rect_basic_east.png
   :width: 330

===== ======
|r01| This example shows the element constructed using the following values
      for its properties.

      .. code:: python

        rect = RectangularLocations(
            cols=3, rows=4,
            start="NW", direction="east")
        Layout(rect, shapes=[a_circle,])

===== ======

Example 3. Row and Column Spacing
---------------------------------
`^ <key-properties_>`_

.. |02a| image:: images/layouts/rect_basic_spacing.png
   :width: 330

===== ======
|02a| This example shows the element constructed using the following values
      for its properties.

      .. code:: python

        rect = RectangularLocations(
            cols=3, rows=4, start="NW", direction="east",
            spacing=1.25)
        Layout(rect, shapes=[a_circle,])

===== ======

.. |02b| image:: images/layouts/rect_basic_spacing_row_col.png
   :width: 330

===== ======
|02b| This example shows the element constructed using the following values
      for its properties.

      .. code:: python

        rect = RectangularLocations(
            cols=3, rows=4, start="NW", direction="east",
            x=1.5, y=1.5,
            row_spacing=1.25, col_spacing=0.75)
        Layout(rect, shapes=[a_circle,])

===== ======


Example 4. Row and Column Offset
--------------------------------
`^ <key-properties_>`_

.. |03a| image:: images/layouts/rect_basic_east_even.png
   :width: 330

===== ======
|03a| This example shows the element constructed using the following values
      for its properties.

      .. code:: python

        rect = RectangularLocations(
            cols=3, rows=4, start="NW", direction="east",
            col_even=0.5)
        Layout(rect, shapes=[a_circle,])

===== ======

.. |03b| image:: images/layouts/rect_basic_east_odd.png
   :width: 330

===== ======
|03b| This example shows the element constructed using the following values
      for its properties.

      .. code:: python

        rect = RectangularLocations(
            cols=3, rows=4, start="NW", direction="east",
            row_odd=0.5)
        Layout(rect, shapes=[a_circle,])

===== ======

Example 5. Snaking
------------------
`^ <key-properties_>`_

.. |r03| image:: images/layouts/rect_basic_snake.png
   :width: 330

===== ======
|r03| This example shows the element constructed using the following values
      for its properties.

      .. code:: python

        rect = RectangularLocations(
            cols=3, rows=4, start="NW", direction="east",
            pattern="snake")
        Layout(rect, shapes=[a_circle,])

===== ======

Example 6. Outer Edge
---------------------
`^ <key-properties_>`_

.. |r04| image:: images/layouts/rect_basic_outer.png
   :width: 330

===== ======
|r04| This example shows the element constructed using the following values
      for its properties.

      .. code:: python

        rect = RectangularLocations(
            cols=3, rows=4, start="NW", direction="east",
            pattern="outer")
        Layout(rect, shapes=[a_circle,])

===== ======

Example 7. Masked
-----------------
`^ <key-properties_>`_

.. |r05| image:: images/layouts/rect_basic_outer_mask.png
   :width: 330

===== ======
|r05| This example shows the element constructed using the following values
      for its properties.

      .. code:: python

        rect = RectangularLocations(
            cols=3, rows=4, start="NW", direction="east",
            pattern="outer")
        Layout(rect, shapes=[a_circle,], masked=[2,7])

===== ======

Example 8. Visible
------------------
`^ <key-properties_>`_

.. |r06| image:: images/layouts/rect_basic_outer_visible.png
   :width: 330

===== ======
|r06| This example shows the element constructed using the following values
      for its properties.

      .. code:: python

        rect = RectangularLocations(
            cols=3, rows=4, start="NW", direction="east",
            pattern="outer")
        Layout(rect, shapes=[a_circle,], visible=[1,3,6,8])

===== ======

Example 9. Debug
----------------
`^ <key-properties_>`_

.. |07a| image:: images/layouts/rect_basic_debug.png
   :width: 330

===== ======
|07a| This example shows the element constructed using the following values
      for its properties.

      .. code:: python

        rect = RectangularLocations(
            cols=3, rows=4, x=0.5, y=0.5)
        Layout(rect, debug='none')

===== ======

.. |07b| image:: images/layouts/rect_basic_debug_count.png
   :width: 330

===== ======
|07b| This example shows the element constructed using the following values
      for its properties.

      .. code:: python

        rect = RectangularLocations(
            cols=3, rows=4, x=0.5, y=0.5)
        Layout(rect, debug='count')

===== ======

.. |07c| image:: images/layouts/rect_basic_debug_colrow.png
   :width: 330

===== ======
|07c| This example shows the element constructed using the following values
      for its properties.

      .. code:: python

        rect = RectangularLocations(
            cols=3, rows=4, x=0.5, y=0.5)
        Layout(rect, debug='colrow')

===== ======
