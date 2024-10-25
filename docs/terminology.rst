===========
Terminology
===========

**pyprototypr** uses many terms; most of which should - hopefully - be
reasonably obvious by their name, or by the context in which they are
used.

However, in order to help with clarity, below is a reasonably
comprehensive list of terms used in different places, grouped by what
they affect.

Note that some shapes, such as the ``Hexagon``, have extensive
customisation properties available; rather refer to their specific
descriptions to understand exactly how these can used.

Table of Contents
-----------------

-  `Color-orientated Terms`_
-  `Location- and position-orientated Terms`_
-  `Size- and length-orientated Terms`_
-  `Amount- and count-orientated Terms`_
-  `Direction-orientated Terms`_
-  `Styling-orientated Terms`_
-  `Display-orientated Terms`_
-  `Miscellaneous Terms`_

Color-orientated terms 
-----------------------

Color is defined in the same way as it is in pages that appear on the
web i.e. in RGB (red-green-blue) *hexadecimal* format - for example,
``#A0522D`` represents a shade of the color that we would likely term
“brown”.

Colors can also be chosen from a pre-defined list of names - for example
``#A0522D`` is pre-defined as the color *sienna*. A PDF file is supplied
at `colorset.pdf <../examples/colorset.pdf>`_ - that shows all the
names and colors that are available.

In general, color can be set for the lines (**stroke**) and areas
(**fill**) that are being drawn on a page.

   **NOTE:** It is possible to use the term *None* in place of a
   specific color; this effectively means that nothing will be drawn
   there - so, an “invisible” line or area!

-  **dot_fill** - the color in which a circle is to be drawn at the
   centre of a shape
-  **fill** - the color in which an area is filled
-  **outline** - sets the line color, and at the same time sets the fill
   to be ``None``
-  **stroke** - the color in which a line or text is drawn; there are
   many strokes for particular types of lines that are set by prefixing
   this term with the name of the item in question; for example:
   **cross_stroke**; **grid_stroke**; **radii_stroke**;
   **label_stroke**; **petals_stroke** etc.
-  **stroke_fill** - sets both the line (“stroke”) and area (“fill”) to
   be the same color

Location- and position-orientated Terms 
----------------------------------------

Everything in **pyprototypr** that needs to be displayed or drawn or
positioned must be placed somewhere on the page; each thing must have
both a horizontal position - its **x** value - and a vertical position -
its **x** value. These respectively represent the distances from the
left- and bottom-edge of a page.

-  **align** - used to position text relative to its starting location;
   can be one of: *justify*, *left*, *right*, or *centre*
-  **cx** - the centre location of a shape, going in the horizontal
   direction; its often the case that the distance is not absolute, but
   relative to some other value e.g. distance from a margin; or the edge
   of a ``Card``
-  **cy** - the centre location of a shape, going in the vertical
   direction; its often the case that the distance is not absolute, but
   relative to some other value e.g. distance from a margin; or the edge
   of a ``Card``
-  **position** - the relative location with a shape; can be one of:
   *top*, *middle*, *center*, or *bottom*
-  **x** - the location of a point in the horizontal direction; its
   often the case that the distance is not absolute, but relative to
   some other value e.g. distance from a margin; or the edge of a
   ``Card``
-  **y** - the location of a point in the vertical direction; its often
   the case that the distance is not absolute, but relative to some
   other value e.g. distance from a margin; or the edge of a ``Card``

Size- and length-orientated terms 
----------------------------------

The majority of length - and width, height, diameter etc. - properties
will be numeric values, corresponding to the **unit** in use (unless
otherwise noted). The default is usually 1 e.g. 1cm.

Some sizes set in **points** - there are 72 points in an inch - so as to
align with existing conventions, or simply because these items are
typically very tiny. As far as possible, the term **size** is reserved
for these settings; for example, **font_size**, **dot_size**,

A few sizes are given descriptive names; this makes them a little easier
to set.

-  **caltrops** - a descriptive term for the relative dimensions of a
   “caltrop” - the small three-pointed shape drawn at the vertex of a
   hexagon - which can be set one of: *small*, *medium* or *large*

-  **diameter** - the diameter of a ``Circle``

-  **dot_size** - the diameter of a small ``Dot`` in **points**

-  **cross** - the height and width of the intersecting lines drawn at
   the centre of a shape

-  **height** - the vertical dimension of a shape e.g. a ``Rectangle``
   or a bitmap ``Image``

-  **margin** - used in ``Create`` command to set all margins for a
   page; the default for any margin is 1.25cm / 12.5mm (1/2 of an inch)

-  **margin_top** - used in ``Create`` command to set top margin for a
   page

-  **margin_bottom** - used in ``Create`` command to set bottom margin
   for a page

-  **margin_left** - used in ``Create`` command to set left margin for a
   page

-  **margin_right** - used in ``Create`` command to set right margin for
   a page

-  **paper** - used in ``Create`` command to set the paper format in the
   document; either ISO series (A0 down to A8; or B6 down to B0) or a
   USA type; the default is A4. (*NOTE:* the value for paper is **not**
   wrapped in quotes!)

-  **radius** - the radius of a ``Circle``

-  **scaling** - the amount by which an SVG image should be shrunk or
   expanded e.g. 0.5 makes it half-size and 2.0 doubles its size; but
   because SVG is a vector-format, there will be no loss of resolution
   through scaling

-  **side** - the length of a side of some shapes (e.g. ``Square``,
   ``Polygon``, ``Grid``) as well as the distance between each adjacent
   point in a ``TriangularLayout``

-  **stroke_width** - the thickness of a line in **points**; many
   specific widths are set by prefixing this term with the name of the
   item in question; examples: **cross_stroke_width**;
   **grid_stroke_width**; **radii_stroke_width**

-  **width** - the horizontal dimension of a shape e.g. a ``Rectangle``
   or a bitmap ``Image``

Amount- and count-orientated Terms 
-----------------------------------

-  **sides** - the number of sides of a ``Polygon`` shape

Direction-orientated Terms 
---------------------------

In general, there are two primary ways of determining direction of
something; either by compass direction or angle. Other descriptive
directions are also used.

The *angle* is the amount of rotation, in degrees, starting from a value
of 0 (zero) which is assumed to be the line parallel to the bottom of
the page (as you would normally look at it). Ninety (90) degrees is the
angle of a line to the side of the page, and so on. The maximum rotation
is 360 degrees.

A *compass direction* is one of the following:

Primary compass directions (with abbreviations shown in brackets):

-  north (n) - normally corresponds to an angle of 90 degrees
-  south (s) - normally corresponds to an angle of 270 degrees
-  east (e) - normally corresponds to an angle of 0 degrees
-  west (e) - normally corresponds to an angle of 180 degrees

Secondary compass directions (with abbreviations shown in brackets):

-  north-east (ne) - normally corresponds to an angle of 45 degrees
-  south-east (se) - normally corresponds to an angle of 315 degrees
-  north-west (nw) - normally corresponds to an angle of 135 degrees
-  south-west (sw) - normally corresponds to an angle of 225 degrees

   *NOTE* - if a compass direction is used in the context of a
   **hexagon**, the angle is “reinterpreted” to match its context
   e.g. the angle for NorthEast for a ‘pointy’ hexagon is 60, not 45,
   degrees.

Properties that use direction include:

-  **clockwise** - a ``True`` or ``False`` setting used to determine
   direction of travel around a circle
-  **direction** - can be any primary compass direction; used to show
   the travel route when moving through various types of layouts
   e.g. ``RectangularLayout``
-  **edges** - can be any primary compass direction; used to indicate
   the sides of a ``Square`` or ``Rectangle``
-  **facing** - can be any primary compass direction; used to show
   orientation of some types of layouts e.g. ``DiamondLayout``
-  **flip** - the relative vertical direction in which a triangle or rhombus 
   must be drawn; can be either: *north* or *south*
-  **hand** - the relative horizontal direction in which a triangle must
   be drawn; can be either: *east* or *west*
-  **orientation** - used for drawing hexagons; can be either: *flat* or
   *pointy*
-  **start** - can be any secondary compass direction; for example, it is
   used to show in which corner of a ``RectangularLayout`` that shapes 
   should first placed when creating a track.

Styling-orientated Terms 
-------------------------

-  **dotted** - allows a line to be broken into a series of dots of
   fixed size (3 points in length; with a gap of 3 points between each)
-  **dashed** - allows a line to be broken into a series of short lines
   of specific lengths, separated by spaces of specific lengths; there
   can any number of these length/space pairs in a list.

Display-orientated Terms
------------------------

-  **hidden** - a list of locations, indicated either by their sequence
   number (i.e. their position in the drawing order) or their row and
   column identifier which should **not** be used for display - the rest
   are displayed as normal
-  **shown** - a list of locations, indicated either by their sequence
   number (i.e. their position in the drawing order) or their row and
   column identifier which are the only ones that **must** be used for
   display - the rest are ignored

Miscellaneous Terms
-------------------

-  **debug** - a value can be set for this that will cause underlying
   values or locations to be displayed e.g. using ``debug="n"`` for a
   layout will show small dots where each point in that layout exists
-  **perimeter** - used to demarcate the boundary of a ``StarField``;
   one of *circle*, *rectangle* or *polygon*
-  **peaks** - a series of sets, each containing a primary compass
   direction and a value, that designate that the edge of a rectangle
   should be drawn as a triangular “peak”; e.g. a set of ``('n', 2)``
   would draw a 2cm high triangle on the upper (north) edge.
