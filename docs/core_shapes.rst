pyprototypr: Core Shapes
========================

.. |copy| unicode:: U+000A9 .. COPYRIGHT SIGN
   :trim:
.. |deg|  unicode:: U+00B0 .. DEGREE SIGN
   :ltrim:

Table of Contents
-----------------

-  `Index of Shapes`_
-  `Overview`_
-  `Commonalities`_
-  `Linear Shapes`_
-  `Enclosed Shapes`_
-  `Compound Shapes`_
-  `Shapes' Common Properties`_

Index of Shapes 
---------------

-  `Arc`_
-  `Blueprint`_
-  `Bezier`_
-  `Circle`_
-  `Compass`_
-  `Chord`_
-  `Dot`_
-  `Ellipse`_
-  `Hexagon`_
-  `Hexagons`_
-  `Line`_
-  `Polygon`_
-  `Polyline`_
-  `Rectangle`_
-  `Square`_
-  `Stadium`_
-  `Star`_


Overview 
---------

These descriptions of the available shapes assume you are familiar with
the concepts, terms and ideas presented in `Basic
Concepts <basic_concepts.md>`_ - especially *units*, *properties* and
*defaults*. It will also help to at least read through the section on
`Additional Concepts <additional_concepts.rst>`_.

Where possible, the basic examples first show how a shape would appear
on a page when **only** the default properties are used. This means for
most cases, that *lines* are drawn in black, with a stroke width of 1mm
(0.1cm) and shapes are *filled* with a white color. The default length
or height in most cases is 1cm.

To make it easier to see where and how a shape has been drawn, these
examples have been created with a background grid (which **pyprototypr**
refers to as a ``Blueprint``) for cross-reference: the values of **x**
appear across the lower edge of the grid (increasing from left to
right); those for **y** along the left side (increasing from bottom to
top). The grid respects the margins that have been set, although the
numbers themselves are drawn inside the margin!

   The graphics for these examples were generated from the scripts in
   the ``examples`` directory - look at the
   `default_shapes <../examples/simple/default_shapes.py>`_ and
   `customised_shapes <../examples/simple/customised_shapes.py>`_
   files.

Commonalities 
--------------

There are some properties that can be set for many of the shapes;
examples of these are presented at the end, rather than being repeated
across every shape.

Linear Shapes 
--------------

Arc
~~~


Bezier
~~~~~~

Chord
~~~~~


Dot
~~~~~


Line 
~~~~

Example #1
++++++++++

.. |pic1| image:: images/examples/simple/defaults/line.png
   :width: 300
   :align: top

|pic1| This example shows the shape constructed using the command with only defaults::
    Line()

It has the following properties based on the defaults:

- length of 1cm,
- starts at x-position 1cm and at y-position 1cm,
- heading/default direction is 0 |deg| (anti-clockwise from 0 |deg| "east").

Polyline
~~~~~~~~


Enclosed Shapes
---------------

These shapes are created by enclosing an area; the most basic being a simple rectangle.
They effectively have 2 dimensions (*height* and *width*). 

The difference between enclosed and linear shapes is that the area enclosed by 
the shape can be filled with a color; the default fill color is *white*.

    **pyprototypr** comes with a predefined set of named colors, shown in the
    `colors <../examples/colorset.pdf>`_ document.



Circle
~~~~~~

Compass
~~~~~~~

Ellipse
~~~~~~~

Hexagon
~~~~~~~

Polygon
~~~~~~~

Rectangle
~~~~~~~~~

Square
~~~~~~

Stadium
~~~~~~~

Star
~~~~




Compound Shapes
---------------


Blueprint
~~~~~~~~~

Hexagons
~~~~~~~~

Hexagons are often drawn in a "honeycomb" arrangement to form a grid - for games
this is often used to delineate the spaces in which playing pieces can be placed
and their movement regulated.

> Further information about using hexagons in grids can be found in the section
> on `Hexagonal Grids <hexagonal_grids.rst>`_.




Shapes' Common Properties 
-------------------------
