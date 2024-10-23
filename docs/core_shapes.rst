pyprototypr: Core Shapes
========================

Table of Contents
-----------------

-  `Index of Shapes <#index_shapes>`__
-  `Overview <#overview>`__
-  `Commonalities <#commonalties>`__
-  `Linear Shapes <#linear_shapes>`__
-  `Enclosed Shapes <#enclosed_shapes>`__
-  `Compound Shapes <#compound_shapes>`__
-  `Shapes’ Common Properties <#common_properties>`__

Alphabetic Index of Shapes 
---------------------------

-  `Arc <#arc>`__
-  `Blueprint <#blueprint>`__
-  `Bezier <#bezier>`__
-  `Circle <#circle>`__
-  `Compass <#compass>`__
-  `Chord <#chord>`__
-  `Dot <#dot>`__
-  `Ellipse <#ellipse>`__
-  `Hexagon <#hexagon>`__
-  `Hexagons <#hexagons>`__
-  `Line <#line>`__
-  `Polygon <#polygon>`__
-  `Polyline <#polyline>`__
-  `Rectangle <#rectangle>`__
-  `Square <#square>`__
-  `Stadium <#stadium>`__
-  `Star <#star>`__


Overview 
---------

These descriptions of the available shapes assume you are familiar with
the concepts, terms and ideas presented in `Basic
Concepts <basic_concepts.md>`__ - especially *units*, *properties* and
*defaults*. It will also help to at least read through the section on
`Additional Concepts <additional_concepts.md>`__.

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
   `default_shapes <../examples/simple/default_shapes.py>`__ and
   `customised_shapes <../examples/simple/customised_shapes.py>`__
   files.

Commonalities 
--------------

There are some properties that can be set for many of the shapes;
examples of these are presented at the end, rather than being repeated
across every shape.

Linear Shapes 
--------------

Line 
~~~~

Example #1
++++++++++

.. container:: twocol

   .. container:: leftside

      .. image:: images/examples/simple/defaults/line.png
        :width: 80
        :align: left

   .. container:: rightside

      This example shows the shape constructed using the command with all defaults::

          Line()

      It has the following properties based on the defaults:

      - length of 1cm,</li>
      - starts at x-position 1cm and at y-position 1cm,
      - heading/default direction is 0 (anti-clockwise from 0 "east").


Shapes Common Properties 
-------------------------
