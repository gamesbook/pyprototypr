=============
Commands List
=============

This list provides an alphabetic summary of all the
`commands <basic_concepts.rst#the-command-concept>`_ specific to
`pyprototypr <index.rst>`_.  It is not intended to be used for learning
but is a handy cross-reference to the detailed information for that command.

.. HINT::

  `pyprototypr <index.rst>`_ is a small, specialised tool; but its part of a much
  greater Python language "ecosystem", and commands and tools from the
  `Python language <python_commands.rst>`_ (or other
  `Python packages <https://pypi.org>`_  ) can be used to further enhance your
  own script.

-  `Arc <core_shapes.rst#arc>`_ * - a geometric shape that can be drawn on a page
-  `Arrow <core_shapes.rst#arrow>`_ * - a geometric shape that can be drawn on a page
-  `Blueprint <core_shapes.rst#blueprint>`_ - a grid of lines that can be drawn on a page
-  `Bezier <core_shapes.rst#bezier>`_ * - a geometric shape that can be drawn on a page
-  `Card <card_decks.rst#the-card-command>`_  - details for a card that is part of a
   `deck <card_decks.rst#the-deck-command>`_
-  `Circle <core_shapes.rst#circle>`_ * - a geometric shape that can be drawn on a page
-  `Compass <core_shapes.rst#compass>`_ * - a geometric shape that can be drawn on a page
-  `Chord <core_shapes.rst#chord>`_ * - a geometric shape that can be drawn on a page
-  `Counter <card_decks.rst#the-counter-command>`_  - details for a counter that is part
   of a `countersheet <card_decks.rst#the-countersheet-command>`_
-  `countersheet <card_decks.rst#the-countersheet-command>`_  - details for a
   countersheet, containing one or more `counters <card_decks.rst#the-counter-command>`_
-  `Data <card_decks.rst#the-data-command>`_ - provides a source of information for
   a `deck <card_decks.rst#the-deck-command>`_ or a
   `countersheet <card_decks.rst#the-countersheet-command>`_ ; typically from a CSV or
   Excel file
-  `Deck <card_decks.rst#the-deck-command>`_  - details for a deck, containing one or
   more `cards <card_decks.rst#the-card-command>`_
-  `Dot <core_shapes.rst#dot>`_ * - a geometric shape that can be drawn on a page
-  `DotGrid <core_shapes.rst#dotgrid>`_ - a set, or group, of dots that can be drawn on a page
-  `Ellipse <core_shapes.rst#ellipse>`_ * - a geometric shape that can be drawn on a page
-  `EquilateralTriangle <core_shapes.rst#equilateraltriangle>`_ * - a geometric shape that can be drawn on a page
-  `Grid <core_shapes.rst#grid>`_ - a set, or group, of lines that can be drawn on a page
-  `group <card_decks.rst#group-command>`_ - a way to  reference a stack of shapes that
   all need to be drawn together on a `card <card_decks.rst#the-card-command>`_
-  `Hexagon <core_shapes.rst#hexagon>`_ * - a geometric shape that can be drawn on a page
-  `Hexagons <core_shapes.rst#hexagons>`_ - a set, or group, of hexagons that can be
   drawn on a page (see also `hexagonal grids <hexagonal_grids.rst>`_)
-  `Image <core_shapes.rst#image>`_ - an external image that can be shown on a page
-  `L <card_decks.rst#l-ookup-command>`_ - short for *Lookup*; a way to access data
   from another `card <card_decks.rst#the-card-command>`_ in a
   `deck <card_decks.rst#the-deck-command>`_
-  `Layout  <layouts_rectangular.rst#layout>`_ -  used in conjuction with a location-based
   grid and specifies the shapes that are to be drawn at the grid locations
-  `Line <core_shapes.rst#line>`_ * - a geometric shape that can be drawn on a page
-  `Lines <core_shapes.rst#lines>`_ - a set, or group, of lines that can be drawn on a page
-  `Polygon <core_shapes.rst#polygon>`_ * - a geometric shape that can be drawn on a page
-  `Polyline <core_shapes.rst#polyline>`_ * - a geometric shape that can be drawn on a page
-  `Polyshape <core_shapes.rst#polyshape>`_ * - a geometric shape that can be drawn on a page
-  `Repeat <layouts_repeat.rst>`_ - repeat the drawing of shape across a rectangular grid pattern
-  `Rectangle <core_shapes.rst#rectangle>`_ * - a geometric shape that can be drawn on a page
-  `Rectangles <core_shapes.rst#rectangles>`_ - a set, or group, of rectangles that can be drawn on a page
-  `RectangularLocations <layouts_rectangular.rst>`_ - defines an ordered series of
   row and column locations that create a rectangular grid of shapes (the grid itself
   is not displayed; it is used for a `layout <layouts_rectangular.rst#layout>`_)
-  `Rhombus <core_shapes.rst#rhombus>`_ * - a geometric shape that can be drawn on a page
-  `S <card_decks.rst#s-election-command>`_ - short for *Selection*; the way to draw a
   shape on a `card <card_decks.rst#the-card-command>`_ depending on a condition
-  `Sector <core_shapes.rst#sector>`_ * - a geometric shape that can be drawn on a page
-  `Sequence <layouts_sequence.rst>`_ -  lay out a number of items in a straight line
-  `Square <core_shapes.rst#square>`_ * - a geometric shape that can be drawn on a page
-  `Stadium <core_shapes.rst#stadium>`_ * - a geometric shape that can be drawn on a page
-  `Star <core_shapes.rst#star>`_ * - a geometric shape that can be drawn on a page
-  `Starfield <core_shapes.rst#star>`_ - a set, or group, of dots that can be drawn on a page
-  `T <card_decks.rst#t-emplate-command>`_ - short for *Template*; the way to access an
   item in a column from a set of `data <card_decks.rst#the-data-command>`_ for a
   `card <card_decks.rst#the-card-command>`_
-  `Text <core_shapes.rst#text>`_ * - a geometric shape that can be drawn on a page
-  `Track <layouts_track.rst>`_ - draw any number of shapes at the vertices of another shape
-  `Trapezoid <core_shapes.rst#trapezoid>`_ * - a geometric shape that can be drawn on a page
-  `TriangularLocations <layouts_triangular.rst>`_- defines an ordered series of
   row and column locations that create a triangular grid of shapes (the grid itself
   is not displayed; it is used for a `layout <layouts_rectangular.rst#layout>`_)

.. NOTE::

   Commands marked with an asterisk (``*``) can be given with a uppercase or
   lowercase initial (``Commmand`` vs ``command``); meaning the shape should
   either be drawn directly at that point in the script, or that it should be
   "stored" to be drawn later.
