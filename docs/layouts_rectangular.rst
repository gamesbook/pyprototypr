=========================
RectangularLocations Command
=========================

**pyprototypr** allows you to directly define where elements, that make up
your design, should be placed within a page, or over a series of pages
within a ``Deck``, but it also includes commands that let you place, or
"layout", elements in a more repetitive or regular way within a page.

Overview
========

The ``RectangularLocations()`` command defines an ordered series
of row and column locations that create a rectangular spacing.  The x- and
y-values of these rows and columns are then used to set the centres of
the elements that can be placed there using the ``Layout()`` command.

Apart from the ``RectangularLocations()`` command described here, there are
also other ways to place elements on a page:

- `Sequences <layouts_sequence.rst>`_
- `Tracks <layouts_track.rst>`_
- `TriangularLocationss <layouts_triangular.rst>`_


Usage
=====

The ``RectangularLocations()`` command accepts the following properties:

- **cols** - this is
- **rows** - this is
- **direction** - this is
- **start** - this is
- **shape** -

The ``Layout()`` command accepts the following properties:

- **grid** - this *must* be the first property used for the command; it will
  refer to
- **shapes** - this is a list of one or more of the core shapes available,
  for example, a circle or rectangle


Basic Examples
--------------

NOTE that all examples below make use of common ```Circle`` shape of:

  .. code:: python

    circles = Common(
        x=0, y=0, diameter=1.0,
        label="{count}/{col}-{row}", label_size=6)
    a_circle = circle(common=circles)

Example 1.
~~~~~~~~~~

.. |rl0| image:: images/layouts/rect_basic_east.png
   :width: 330

===== ======
|rl0| This example shows the element constructed using differing values for the
      its properties.

      .. code:: python

          rect = RectangularLocations(
              cols=3, rows=4,
              start="NW", direction="east")
          Layout(rect, shapes=[a_circle,])
===== ======
