==============
Basic Concepts
==============

Like many other specialised tools, **pyprototypr** has its own set of
terms and concepts that act as "short-cuts" to help it function. Some
of these are likely to be common to other graphics editing or
programming tools, but some are specific to it.

This is a general discussion; it may also be useful to look at the more
detailed definitions of some of the terms in the section covering
`terminology <terminology.rst>`_

.. _table-of-contents:

Table of Contents
=================

- `How you’ll use pyprototypr`_
- `The "script" concept`_
- `The "position" concept`_
- `The "command" concept`_
- `The "element" concept`_
- `Element properties`_
- `Working with color`_
- `Working with units`_
- `The "stroke" concept`_
- `The "default" concept`_


How you’ll use pyprototypr
==========================
`↑ <table-of-contents_>`_

You will be using **pyprototypr** to write what is termed a *script*
i.e. a recipe or list of instructions that are stored in a file. These
instructions are used to define a game board, a set of cards or tiles,
or any other, similar, regular graphical design of your choice.

You will then use Python to "run" the script. Python will take the file
you have written, and step through it, line by line, from top to bottom,
to finally create an output PDF file (or, optionally, PNG image) that
will show the outcome of this process - hopefully with your desired
design!

If you want to make changes to the design, then you add to, delete, or
change the instructions in your script and then use Python to process it
again to create an updated PDF file.

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

   For more detail on what goes into a script, see the section on `Script
   Anatomy <script_anatomy.rst>`_.

.. _position:

The "position" concept
======================
`↑ <table-of-contents_>`_

When using **pyprototypr** what you are doing is defining *where* and
*how* various things should appear on a *page*. A script can create multiple
pages, but will always have at least one.

The position of something is *where* it will be drawn on the page. To do
this, you provide values for both **x** - the horizontal position - and
**y** - the vertical position - for each thing that you want to on
appear the page.

So, if you look at an upright A4 page - which is 21cm wide and just less
than 30cm high - then a point in the middle of the page will have an **x
position** of 10.5cm - its distance from the left edge of the page; and
a **y position** of 14.8cm - its distance from the bottom edge of the
page. Similarly, for a US letter-sized page of 8.5" by 11", a point in
the middle of the page would have an **x position** of 4.25" and a **y
position** of 5.5".

As the use of margins is common for most documents and drawings, *all*
distances in **pyprototypr** are considered to be relative to the margin
settings i.e. if the default page margin, for the A4 page mentioned above,
was 2.5cm (1") then to locate a point at those same distances would mean
using an **x position** of 8cm and a **y position** of 12.3cm, as the margin
size will be automtically added onto the supplied values for the position.


The "command" concept
=====================
`↑ <table-of-contents_>`_

Instructions in **pyprototypr** are termed *commands*.  These usually are
written with an initial capital letter. They are effectively "imperative"
in nature, causing something to happen; for example:

- ``Save()`` - tells the program to save the output to file
-  ``Circle()``  - tells the program to draw a circle


The "element" concept
=====================
`↑ <table-of-contents_>`_

Rather than use the slightly clumsy term "thing", **pyprototypr** uses
the term *element*.

Almost everything in **pyprototypr** that appears in the output is
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
are provided in the section on `Core Shapes <core_shapes.rst>`_.

.. _properties:

Element properties
==================
`↑ <table-of-contents_>`_

*Elements* can have other settings apart from their `position <position_>`_

For example, the rectangle which represents the outline of a card has a
*height* (its size in the vertical direction) and a *width* (its size in
the horizontal direction). The line used to draw the rectangle also has
a *stroke width* and a *stroke color* (see below for more about the
concepts of stroke and width). A circle will have its size defined by a
value for its *radius* or *diameter*, and so on.

   *NOTE:* Because the word "size" is such a general one, its not really
   used in **pyprototypr**; more specific terms are used instead.

Similarly, the settings for the creation of a document can be provided,
such its color, *paper* size and so on.

All of these kinds of settings are called **properties**. Most of the
common properties are described in the section covering
`terminology <terminology.rst>`_.


Working with color
==================
`↑ <table-of-contents_>`_

Everything we see has color.

Color in **pyprototypr**, is defined in the same way as it is in pages
that appear on the web i.e. in RGB (red-green-blue) *hexadecimal* format
- for example, ``#A0522D`` represents a shade of the color that we would
likely term "brown".

   For more details on hexadecimal colors, refer to
   http://www.w3.org/TR/css3-color.

Colors in **pyprototypr** can also make use of names from a pre-defined
list - for example ``#A0522D`` is defined as the color *sienna*. The
`colorset.pdf <../examples/colorset.pdf>`_ file shows all the names and colors
that are available.  This is an alternate version of the list that can be
also be found at https://en.wikipedia.org/wiki/X11_color_names

Color properties in **pyprototypr** are typically used via *"fill"* to
set the color of an area, and *"stroke"* to set the color of a line.


Working with units
==================
`↑ <table-of-contents_>`_

All positions, heights, widths, distances, line thicknesses and other
kinds of lengths or sizes all need to be measured in a particular set of
**units**.

In the USA, people tend to use the so-called Imperial System. In
**pyprototypr** this means that distances might be measured in units of
inches (inches are often shown with an *"* (double quotes) symbol in
documents, but in **pyprototypr** inches are referred to using the term *inch*).

In almost all of the rest of the world, the Metric System is in use. In
**pyprototypr** this means that distances will be measured in units of
centimetres (referred to in **pyprototypr** as *cm*). Alternatively, you
can choose to use millimetres (abbreviated in **pyprototypr** as *mm*).

   For conversion purposes, 1 inch equals 2.54 centimetres or 25.4
   millimetres.

**pyprototypr** also allows units of *points*, which are the measurement
units traditionally used in the printing industry. There are 72 points
in 1 inch. Internal calculations in **pyprototypr** are all done in
point units i.e. all inputs, regardless of being inches or centimetres
are converted to points.


The "stroke" concept
====================
`↑ <table-of-contents_>`_

While the majority of size-based `properties <properties_>`_ in **pyprototypr**
work with the "normal" units you have chosen - inches or centimetres - some use
points. These include font height, that you’re likely familiar with, and
line thickness - termed "stroke width". (The reason for this is to
maintain consistency with existing tools.)


The "default" concept
=====================
`↑ <table-of-contents_>`_

A "default", in terms of **pyprototypr**, is a value or setting for
something (usually a `property <properties_>`_) which is used unless you
specify otherwise. This is helpful for quickly drawing or testing something
until you're ready to make decisions about your own setting or value.

Some examples of defaults are:

-  the default *margin* for pages in the output PDF is ``1.25`` cm
   (or half of 1 inch)
-  the default *paper* size for pages in the output PDF is A4 (similar to
   US letter size)
-  the default *units* are centimetres (*cm*)
-  the default *x* and *y* positions are each 1 (one) - with default
   units that equals 1cm
-  the default line *length* is ``1`` (one) - with default units that is 1cm
-  the default line *stroke width* is ``1`` point - that corresponds to
   1/72" (or 0.353 mm)
-  the default line *stroke* color is ``black`` - which has a hexadecimal
   value of ``#000000``
-  the default area *fill* color is ``white`` - which has a hexadecimal
   value of ``#FFFFFF``
-  the default *font* is Arial, with a size (height) of ``12`` points and a
   stroke color of ``black``
