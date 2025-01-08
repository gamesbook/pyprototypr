================
The Deck Command
================

This section assumes you are very familiar with the concepts, terms and
ideas for `pyprototypr <index.rst>`_ as presented in the
`Basic Concepts <basic_concepts.rst>`_ , that you understand all of the
`Additional Concepts <additional_concepts.rst>`_
and that you've created some basic scripts of your own using the
`Core Shapes <core_shapes.rst>`_.

It also assumes you have read through the section on
`card decks <card_decks.rst>`_.

.. _table-of-contents:

Table of Contents
=================

- `Overview`_


Overview
========
`↑ <table-of-contents_>`_

This command provides the overall "framework" for the cards that are defined
in the script.  It's primary purpose is to set the card size, and then
calculate how many cards appear on a page.  It manages the "flow" of cards as
they get drawn.

Primary Properties
------------------

The following are key properties that will usually need to be set for a
``Deck``:

- **cards** - this is the number of cards appearing in the deck; it defaults
  to 9; note that other commands such as ``Data()`` and ``Matrix()`` can alter
  this value
- **height** - this is the card height; it defaults to 8.8 cm
- **width** - this is the card width; it defaults to 6.3 cm
- **radius** - this is a circular or hexagonal card's radius;
  it defaults to 2.54 cm (1")

Secondary Properties
--------------------

The following are other properties that can also be set for a ``Deck``:

- **copy** - the name of a column in the dataset defined by
  `the Data Command <card_decks.rst#the-data-command>`_) that specifies
  how many copies of a card are needed
- **fill** - sets the color of the card's area; defaults to white
- **frame** - the default card frame is a rectangle (or square, if the
  height and width match); but can be set to *hexagon* or *circle*
- **grid_marks** - if set to ``True``, will cause small marks (``1`` cm in
  length) to be drawn at the border of the page that align with the edges of
  the card frames
- **grid_length** - if set to ``True``, will cause small marks to be drawn at
  the border of the page that align with the edges of the cards
- **mask** - an expression which should evaluate to ``True` or ``False``;
  this expression uses the same kind of syntax as the
  `T(emplate) command <card_decks.rst#the-template-command>`_
  and it uses data available from the Deck's
  `Data Command <card_decks.rst#the-data-command>`_); if ``True``
  then any matching cards will be masked i.e. ignored and not drawn.
- **rounding** - sets the size of rounding on each corner of a rectangular
  frame card
- **stroke** - sets the color of the card's border; defaults to black

.. HINT::

    The **frame** property can be seen "in action" in illustrated examples;
    see a `hexagonal example <examples/cards.rst#hexagon-cards>`_ and a
    `circular example <examples/cards.rst#circle-cards>`_.


Other Resources
===============
`↑ <table-of-contents_>`_
