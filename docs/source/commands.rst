=============
Commands List
=============

.. |dash| unicode:: U+2014 .. EM DASH SIGN

This list provides an alphabetic summary of all the
:doc:`commands <basic_concepts#the-command-concept>` specific to
:doc:`protograf <index>`.  It is not intended to be used for learning
but is a handy cross-reference to the detailed information for that command.

.. HINT::

  :doc:`protograf <index>` is a small, specialised tool; but its part of a much
  greater Python language "ecosystem", and commands and tools from the
  :doc:`Python language <python_commands>` |dash| or other
  `Python packages <https://pypi.org>`_  |dash| can be used to further enhance
  your own script.

-  :doc:`Arc <core_shapes#arc>` * - a geometric shape that can be drawn on a page
-  :doc:`Arrow <core_shapes#arrow>` * - a geometric shape that can be drawn on a page
-  :doc:`Blueprint <core_shapes#blueprint>` - a grid of lines that can be drawn on a page
-  :doc:`Bezier <core_shapes#bezier>` * - a geometric shape that can be drawn on a page
-  :doc:`Card <card_decks#the-card-command>`  - details for a card that is part of a
   :doc:`deck <card_decks#the-deck-command>`
-  :doc:`Circle <core_shapes#circle>` * - a geometric shape that can be drawn on a page
-  :doc:`Compass <core_shapes#compass>` * - a geometric shape that can be drawn on a page
-  :doc:`Chord <core_shapes#chord>` * - a geometric shape that can be drawn on a page
-  :doc:`Counter <card_decks#the-counter-command>`  - details for a counter that is part
   of a :doc:`countersheet <card_decks#the-countersheet-command>`
-  :doc:`countersheet <card_decks#the-countersheet-command>`  - details for a
   countersheet, containing one or more
   :doc:`counters <card_decks#the-counter-command>`
-  :doc:`Create <script_anatomy#create-command>` - start of a script; define the
   paper size, output filename, margins, units, fill color etc.
-  :doc:`Data <card_decks#the-data-command>` - provides a source of information for
   a :doc:`deck <card_decks#the-deck-command>` or a
   :doc:`countersheet <card_decks#the-countersheet-command>` ; typically from a CSV or
   Excel file
-  :doc:`Deck <card_decks#the-deck-command>`  - details for a deck, containing one or
   more :doc:`cards <card_decks#the-card-command>`
-  :doc:`Dot <core_shapes#dot>` * - a geometric shape that can be drawn on a page
-  :doc:`DotGrid <core_shapes#dotgrid>` - a set, or group, of dots that can be drawn on a page
-  :doc:`Ellipse <core_shapes#ellipse>` * - a geometric shape that can be drawn on a page
-  :doc:`EquilateralTriangle <core_shapes#equilateraltriangle>` * - a geometric shape that can be drawn on a page
-  :doc:`Grid <core_shapes#grid>` - a set, or group, of lines that can be drawn on a page
-  :doc:`group <card_decks#group-command>` - a way to  reference a stack of shapes that
   all need to be drawn together on a :doc:`card <card_decks#the-card-command>`
-  :doc:`Hexagon <core_shapes#hexagon>` * - a geometric shape that can be drawn on a page
-  :doc:`Hexagons <core_shapes#hexagons>` - a set, or group, of hexagons that can be
   drawn on a page (see also :doc:`hexagonal grids <hexagonal_grids>`)
-  :doc:`Image <core_shapes#image>` - an external image that can be shown on a page
-  :doc:`L <card_decks#l-ookup-command>` - short for *Lookup*; a way to access data
   from another :doc:`card <card_decks#the-card-command>` in a
   :doc:`deck <card_decks#the-deck-command>`
-  :doc:`Layout  <layouts_rectangular#layout>` -  used in conjuction with a location-based
   grid and specifies the shapes that are to be drawn at the grid locations
-  :doc:`Line <core_shapes#line>` * - a geometric shape that can be drawn on a page
-  :doc:`Lines <core_shapes#lines>` - a set, or group, of lines that can be drawn on a page
-  :doc:`PageBreak <script_anatomy#pagebreak-command>` - set the start of a new page in
   the document; not required for a :doc:`Deck <card_decks#the-deck-command>`
-  :doc:`Polygon <core_shapes#polygon>` * - a geometric shape that can be drawn on a page
-  :doc:`Polyline <core_shapes#polyline>` * - a geometric shape that can be drawn on a page
-  :doc:`Polyshape <core_shapes#polyshape>` * - a geometric shape that can be drawn on a page
-  :doc:`Repeat <layouts_repeat>` - repeat the drawing of shape across a rectangular grid pattern
-  :doc:`Rectangle <core_shapes#rectangle>` * - a geometric shape that can be drawn on a page
-  :doc:`Rectangles <core_shapes#rectangles>` - a set, or group, of rectangles that can be drawn on a page
-  :doc:`RectangularLocations <layouts_rectangular>` - defines an ordered series of
   row and column locations that create a rectangular grid of shapes - the grid itself
   is not displayed; it is used for a :doc:`layout <layouts_rectangular#layout>`
-  :doc:`Rhombus <core_shapes#rhombus>` * - a geometric shape that can be drawn on a page
-  :doc:`S <card_decks#s-election-command>` - short for *Selection*; the way to draw a
   shape on a :doc:`card <card_decks#the-card-command>` depending on a condition
-  :doc:`Save <script_anatomy#save-command>` - end of a script; set the export
   image file type and filenames, as well as resolution
-  :doc:`Sector <core_shapes#sector>` * - a geometric shape that can be drawn on a page
-  :doc:`Sequence <layouts_sequence>` -  lay out a number of items in a straight line
-  :doc:`Square <core_shapes#square>` * - a geometric shape that can be drawn on a page
-  :doc:`Stadium <core_shapes#stadium>` * - a geometric shape that can be drawn on a page
-  :doc:`Star <core_shapes#star>` * - a geometric shape that can be drawn on a page
-  :doc:`Starfield <core_shapes#star>` - a set, or group, of dots that can be drawn on a page
-  :doc:`T <card_decks#t-emplate-command>` - short for *Template*; the way to access an
   item in a column from a set of :doc:`data <card_decks#the-data-command>` for a
   :doc:`card <card_decks#the-card-command>`
-  :doc:`Text <core_shapes#text>` * - a geometric shape that can be drawn on a page
-  :doc:`Track <layouts_track>` - draw any number of shapes at the vertices of another shape
-  :doc:`Trapezoid <core_shapes#trapezoid>` * - a geometric shape that can be drawn on a page
-  :doc:`TriangularLocations <layouts_triangular>`- defines an ordered series of
   row and column locations that create a triangular grid of shapes - the grid itself
   is not displayed; it is used for a :doc:`layout <layouts_rectangular#layout>`

.. IMPORTANT::

   Commands marked with an asterisk (``*``) can be given with a uppercase or
   lowercase initial (``Commmand`` vs ``command``); meaning the shape should
   either be drawn directly at that point in the script, or that it should be
   "stored" to be drawn later.
