==============
Basic Concepts
==============

.. |dash| unicode:: U+2014 .. EM DASH SIGN

Like many other specialised tools, :doc:`protograf <index>` has its
own set of terms and concepts that act as "short-cuts" to define
its functions and behaviour. Some of these are likely to be common to
other graphics editing or programming tools, but some are specific to it.

This is a general discussion; it may also be useful to look at the more
detailed definitions of some of the terms in the section covering
`terminology <terminology>`.

.. _table-of-contents:

Table of Contents
=================

- `How you’ll use protograf`_
- `The "script" concept`_
- `The "position" concept`_
- `The "command" concept`_
- `The "element" concept`_
- `Element properties`_
- `Working with color`_
- `Working with units`_
- `The "stroke" concept`_
- `The "default" concept`_


How you’ll use protograf
========================
`↑ <table-of-contents_>`_

You will be using **protograf** to write what is termed a **script**
i.e. a recipe or list of instructions that are stored in a file. These
instructions are used to define a game board, a set of cards or tiles,
or any other, similar, regular graphical design of your choice.

You will then use Python to "run" the script. Python will take the file
you have written, and step through it, line by line, from top to bottom,
to finally create an output PDF file or, optionally, PNG or GIF images,
that will show the outcome of this process - hopefully with your desired
design!

If you want to make changes to the design, then you add to, delete, or
change, the instructions in your script and use Python to process it
again to create the update.


The "script" concept
====================
`↑ <table-of-contents_>`_

Creating a *script* is similar to the process of building a house; in
the sense that the instructions which come first create underlying parts
that are "deeper down"; in the same way that a foundation is below a
floor, which in turn is below the walls, which are below the ceiling,
which is below the roof. The lower layers are often not "visible", even
if they are there, but they are just as important!

So, for example, a page may contain rectangles representing cards. Each
card may then have additional rectangles placed on it, representing some
aspect that is part of your card design. Those rectangles, in turn,
could have text, images or icons on/inside them. So, each item that is
created later can "obscure" some part - or even all - of the item it is placed
on which was defined previously.

Its also possible to define things earlier in a script that are reused
later on.

In summary - the *order* of instructions in a script is important as this
will affect what you see at the end!

.. HINT::

   For more detail on what goes into a script, see the section on
   :doc:`Script Anatomy <script_anatomy>`.

.. _position:

The "position" concept
======================
`↑ <table-of-contents_>`_

When using **protograf** what you are doing is defining *where* and
*how* various things should appear on a *page*. A script can create multiple
pages, but will always have at least one.

The position of something is *where* it will be drawn on the page. To do
this, you provide values for both **x** - the horizontal position - and
**y** - the vertical position - for each thing that you want to appear
on the page.

If you look at an upright A4 page - which is 21cm wide and just less
than 30cm high - then a point in the middle of the page will have an **x
position** of 10.5cm - its distance from the left edge of the page; and
a **y position** of 14.8cm - its distance from the bottom edge of the
page. Similarly, for a US letter-sized page of 8.5" by 11", a point in
the middle of the page would have an **x position** of 4.25" and a **y
position** of 5.5".

As the use of margins is common for most documents and drawings, nearly all
distances in **protograf** are considered to be relative to the margin
settings i.e. if the default page margin, for the A4 page mentioned above,
was 2.5cm (1") then to locate a point at those same distances would mean
using an **x position** of 8cm and a **y position** of 12.3cm, as the margin
size will be automtically added onto the supplied values for the position.

.. _command:

The "command" concept
=====================
`↑ <table-of-contents_>`_

Instructions in **protograf** are termed *commands*.  These usually are
written with an initial capital letter. They are effectively "imperative"
in nature, causing something to happen; for example:

- ``Save()`` - instructs the program to save the output to file
- ``Circle()`` - instructs the program to draw a circle

The :doc:`summary list of all commands <commands>` is a useful reference
for checking what is available.

.. _element:

The "element" concept
=====================
`↑ <table-of-contents_>`_

Rather than use the slightly clumsy term "thing", **protograf** uses
the term *element*.

Almost everything in **protograf** that appears in the output is
considered to be an *element* of some sort. Elements are often geometric
**shapes**, such lines, circles or rectangles, but can also be text or
images.

Examples of some of the available geometric **shapes** include:

-  Circle
-  Ellipse
-  Hexagon
-  Polygon
-  Rectangle
-  Rhombus
-  Square
-  Stadium

Descriptions of all of these shapes, and how to create and use them,
are provided in the section on :doc:`Core Shapes <core_shapes>`.

Other *elements* include things like :ref:`Hexagonal Grids <hexagonal_grids>`,
regular :ref:`layouts <layouts>` and :ref:`cards <the-card-command>`.

.. _properties:

Element properties
==================
`↑ <table-of-contents_>`_

*Elements* can have other settings apart from their `position <position_>`_

For example, the rectangle which represents the outline of a card has a
*height* |dash| its size in the vertical direction and a  *width* |dash|
its size in the horizontal direction. The line used to draw the rectangle
also has a *stroke width* and a *stroke color* (see below for more about
the concepts of stroke and width). A circle will have its size defined by a
value for its *radius* or *diameter*, and so on.

.. NOTE::

   Because the word "size" is such a general one, its not really
   used much in **protograf**; more specific terms are used instead.

Similarly, the settings for the creation of a document can be provided,
such its color, the *paper* size and so on.

All of these kinds of settings are called **properties**. Most of the
common properties are defined in the section covering
:doc:`terminology <terminology>` and their usage is covered in
the section on :doc:`core chapes <core_shapes>`.

.. _color:

Working with color
==================
`↑ <table-of-contents_>`_

Everything we see has color.

Color in **protograf**, is defined in the same way as it is in pages
that appear on the web i.e. in RGB |dash| red-green-blue |dash| *hexadecimal*
format; for example, ``#A0522D`` represents a shade of the color that we
would likely term "brown".

Colors in **protograf** can also make use of names from a pre-defined
list - for example ``#A0522D`` is defined as the color *sienna*. The
`colorset.pdf <https://github.com/gamesbook/protograf/blob/master/examples/colorset.pdf>`
file shows all the names and colors that are available.

Color properties in **protograf** are typically used via *"fill"* to
set the color of an area, and *"stroke"* to set the color of a line.

.. HINT::

   For more details on hexadecimal colors, refer to
   http://www.w3.org/TR/css3-color; the color names are listed in the
   section https://www.w3.org/TR/css-color-3/#svg-color (this list can
   also be found at https://en.wikipedia.org/wiki/X11_color_names)

.. _units:

Working with units
==================
`↑ <table-of-contents_>`_

All positions, heights, widths, distances, line thicknesses and other
kinds of lengths or sizes all need to be measured in a particular set of
**units**.

In the USA, people tend to use the so-called Imperial System. In
**protograf** this means that distances might be measured in units of
inches. Inches are often shown with an *"*, or double-quotes, symbol
in documents, but in **protograf** inches are referred to using the
term *inch*.

In almost all of the rest of the world, the Metric System is in use. In
**protograf** this means that distances will be measured in units of
centimetres; referred to in **protograf** as *cm*. Alternatively, you
can choose to use millimetres, abbreviated in **protograf** as *mm*.

.. HINT::

   For conversion purposes, 1 inch equals 2.54 centimetres or 25.4
   millimetres.

**protograf** also allows units of *points*, which are the measurement
units traditionally used in the printing industry. There are 72 points
in 1 inch. Internal calculations in **protograf** are all done in
point units i.e. all inputs, regardless of being inches or centimetres
are converted to points.

.. _stroke:

The "stroke" concept
====================
`↑ <table-of-contents_>`_

While the majority of size-based `properties <properties_>`_ in **protograf**
work with the "normal" units you have chosen - inches or centimetres - some use
points (see `working with units`_ above). These include font height, that you’re
likely familiar with from word processing programs, and line thickness - termed
"stroke width". The reason for doing this is to maintain consistency with other,
existing tools.

.. _default:

The "default" concept
=====================
`↑ <table-of-contents_>`_

A "default", in terms of **protograf**, is a value or setting for
something |dash| usually a `property <properties_>`_ |dash| which is used
unless you specify otherwise. This is helpful for quickly drawing or testing
something until you're ready to make decisions about your own specific
settings or values.

Some examples of defaults are:

-  the default *margin* for pages in the output PDF is ``1.25`` cm
   or half of 1 inch
-  the default *paper* size for pages in the output PDF is A4 |dash| similar
   to the US letter size
-  the default *units* are centimetres (*cm*)
-  the default *x* and *y* positions are each 1 (one) - with default
   units that equals 1cm
-  the default line *length* is ``1`` (one) - with default units that is 1cm
-  the default line *stroke width* is ``1`` point - that corresponds to
   1/72 inches (or 0.353 mm)
-  the default line *stroke* color is ``black`` - which has a hexadecimal
   value of ``#000000``
-  the default area *fill* color is ``white`` - which has a hexadecimal
   value of ``#FFFFFF``
-  the default *font* is Arial, with a size (height) of ``12`` points and a
   stroke color of ``black``
