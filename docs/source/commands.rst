=============
Commands List
=============

.. |dash| unicode:: U+2014 .. EM DASH SIGN

This list provides an alphabetic summary of all the
:ref:`commands <the-command-concept>` specific to
:ref:`protograf <index>`.  It is not intended to be used for learning
but is a handy cross-reference to the detailed information for that command.

.. HINT::

  :ref:`protograf <index>` is a small, specialised tool; but its part of a much
  greater Python language "ecosystem", and commands and tools from the
  :ref:`Python language <python_commands>` |dash| or other
  `Python packages <https://pypi.org>`_  |dash| can be used to further enhance
  your own script.

-  :ref:`Arc <arc-command>` * - a geometric shape that can be drawn on a page
-  :ref:`Arrow <arrow>` * - a geometric shape that can be drawn on a page
-  :ref:`Blueprint <blueprint>` - a grid of lines that can be drawn on a page
-  :ref:`Bezier <bezier>` * - a geometric shape that can be drawn on a page
-  :ref:`Card <the-card-command>`  - details for a card that is part of a
   :ref:`deck <the-deck-command>`
-  :ref:`Circle <circle>` * - a geometric shape that can be drawn on a page
-  :ref:`Compass <compass>` * - a geometric shape that can be drawn on a page
-  :ref:`Chord <chord>` * - a geometric shape that can be drawn on a page
-  :ref:`Counter <the-countersheet-command>`  - details for a counter that is part
   of a :ref:`countersheet <the-countersheet-command>`
-  :ref:`countersheet <the-countersheet-command>`  - details for a
   countersheet, containing one or more counters
-  :ref:`Create <create-command>` - start of a script; define the
   paper size, output filename, margins, units, fill color etc.
-  :ref:`Data <the-data-command>` - provides a source of information for
   a :ref:`deck <the-deck-command>` or a
   :ref:`countersheet <the-countersheet-command>` ; typically from a CSV or
   Excel file
-  :ref:`Deck <the-deck-command>`  - details for a deck, containing one or
   more :ref:`cards <the-card-command>`
-  :ref:`Dot <dot>` * - a geometric shape that can be drawn on a page
-  :ref:`DotGrid <dotgrid>` - a set, or group, of dots that can be drawn on a page
-  :ref:`Ellipse <ellipse>` * - a geometric shape that can be drawn on a page
-  :ref:`EquilateralTriangle <equilateraltriangle>` * - a geometric shape that can be drawn on a page
-  :ref:`Grid <grid>` - a set, or group, of lines that can be drawn on a page
-  :ref:`group <group-command>` - a way to  reference a stack of shapes that
   all need to be drawn together on a :ref:`card <the-card-command>`
-  :ref:`Hexagon <hexagon>` * - a geometric shape that can be drawn on a page
-  :ref:`Hexagons <hexagons>` - a set, or group, of hexagons that can be
   drawn on a page (see also :ref:`hexagonal grids <hexagonal_grids>`)
-  :ref:`Image <image>` - an external image that can be shown on a page
-  :ref:`L <l-ookup-command>` - short for *Lookup*; a way to access data
   from another :ref:`card <the-card-command>` in a
   :ref:`deck <the-deck-command>`
-  :ref:`Layout <layoutIndex>` -  used in conjuction with a location-based
   grid and specifies the shapes that are to be drawn at the grid locations
-  :ref:`Line <line>` * - a geometric shape that can be drawn on a page
-  :ref:`Lines <lines>` - a set, or group, of lines that can be drawn on a page
-  :ref:`Matrix <the-matrix-command>` - a way to create a dataset, inside a script,
   for a :ref:`deck <the-deck-command>` of cards
-  :ref:`PageBreak <pagebreak-command>` - set the start of a new page in
   the document; not required for a :ref:`Deck <the-deck-command>`
-  :ref:`Polygon <polygon>` * - a geometric shape that can be drawn on a page
-  :ref:`Polyline <polyline>` * - a geometric shape that can be drawn on a page
-  :ref:`Polyshape <polyshape>` * - a geometric shape that can be drawn on a page
-  :ref:`Repeat <layouts_repeat>` - repeat the drawing of shape across a rectangular grid pattern
-  :ref:`Rectangle <rectangle>` * - a geometric shape that can be drawn on a page
-  :ref:`Rectangles <rectangles>` - a set, or group, of rectangles that can be drawn on a page
-  :ref:`RectangularLocations <layouts_rectangular>` - defines an ordered series of
   row and column locations that create a rectangular grid of shapes - the grid itself
   is not displayed; it is used in a :ref:`Layout <layoutIndex>` command.
-  :ref:`Rhombus <rhombus>` * - a geometric shape that can be drawn on a page
-  :ref:`S <s-election-command>` - short for *Selection*; the way to draw a
   shape on a :ref:`card <the-card-command>` depending on a condition
-  :ref:`Save <save-command>` - end of a script; set the export
   image file type and filenames, as well as resolution
-  :ref:`Sector <sector>` * - a geometric shape that can be drawn on a page
-  :ref:`Sequence <layouts_sequence>` -  lay out a number of items in a straight line
-  :ref:`Square <square>` * - a geometric shape that can be drawn on a page
-  :ref:`Stadium <stadium>` * - a geometric shape that can be drawn on a page
-  :ref:`Star <star>` * - a geometric shape that can be drawn on a page
-  :ref:`Starfield <star>` - a set, or group, of dots that can be drawn on a page
-  :ref:`T <t-emplate-command>` - short for *Template*; the way to access an
   item in a column from a set of :ref:`data <the-data-command>` for a
   :ref:`card <the-card-command>`
-  :ref:`Text <text>` * - a geometric shape that can be drawn on a page
-  :ref:`Track <layouts_track>` - draw any number of shapes at the vertices of another shape
-  :ref:`Trapezoid <trapezoid>` * - a geometric shape that can be drawn on a page
-  :ref:`TriangularLocations <layouts_triangular>`- defines an ordered series of
   row and column locations that create a triangular grid of shapes - the grid itself
   is not displayed; it is used in a :ref:`Layout <layoutIndex>` command.

.. IMPORTANT::

   Commands marked with an asterisk (``*``) can be given with a uppercase or
   lowercase initial (``Commmand`` vs ``command``); meaning the shape should
   either be drawn directly at that point in the script, or that it should be
   "stored" to be drawn later.
