===========================
TriangularLocations Command
===========================

**pyprototypr** allows you to directly define where elements, that make up
your design, should be placed within a page, or over a series of pages
within a ``Deck``, but it also includes commands that let you place, or
"`layout <layouts.rst>`_", elements in a more repetitive or regular way
within a page.

Overview
========

The ``TriangularLocations()`` command defines an ordered series
of row and column locations that create a triangular spacing.  The x- and
y-values of these rows and columns are then used to set the centres of
the elements that can be placed there using the ``Layout()`` command.

Apart from the ``TriangularLocations()`` command described here, there are
also other ways to place elements on a page:

- `Sequences <layouts_sequence.rst>`_
- `Tracks <layouts_track.rst>`_
- `RectangularLocations <layouts_rectangular.rst>`_


Usage
=====

The ``TriangularLocations()`` command accepts the following properties:

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

All examples below make use of common ```Circle`` shape (called *a_circle*)
defined as:

  .. code:: python

    circles = Common(
        x=0, y=0, diameter=1.0,
        label="{{sequence}}//{{col}}-{{row}}", label_size=6)
    a_circle = circle(common=circles)

In these examples, the placeholder names ``{{sequence}}``, ``{{col}}``
and ``{{row}}`` will be replaced, in the label for the Circle, by the
values for the row and column in which that circle is placed, as well as
by the sequence number (order) in which that Circle is drawn.

Example 1.
~~~~~~~~~~

.. |tl0| image:: images/layouts/rect_basic_east.png
   :width: 330

===== ======
|tl0| This example shows the element constructed using differing values for the
      its properties.

      .. code:: python

          TriangularLocations()

===== ======
