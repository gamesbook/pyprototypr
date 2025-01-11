================
The Deck Command
================

This section assumes you are very familiar with the concepts, terms and
ideas for `protograf <index.rst>`_ as presented in the
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

  - `Primary Properties`_
  - `Secondary Properties`_
- `Property Examples`_


Overview
========
`↑ <table-of-contents_>`_

This command provides the overall "framework" for the cards that are defined
in the script.  It's primary purpose is to set the card size, and then
calculate how many cards appear on a page.  It manages the "flow" of cards as
they get drawn.

Primary Properties
------------------
`↑ <table-of-contents_>`_

The following are key properties that will usually need to be set for a
``Deck``:

- **cards** - this is the number of cards appearing in the deck; it defaults
  to 9; note that other commands such as ``Data()`` and ``Matrix()`` can alter
  this value
- **height** - this is the card height for a rectangular card;
  it defaults to 8.8 cm
- **width** - this is the card width for a rectangular card;
  it defaults to 6.3 cm

Secondary Properties
--------------------
`↑ <table-of-contents_>`_

The following are other properties that can also be set for a ``Deck``:

- **cols** - the maximum number of card columns that should appear on a
  page
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
  then any matching cards will be masked i.e. ignored and not drawn
- **radius** - the radius for a frame of type *hexagon* or *circle*;
  it defaults to 2.54 cm (1")
- **rounding** - sets the size of rounding on each corner of a rectangular
  frame card
- **rows** - the maximum number of card rows that should appear on a page
- **stroke** - sets the color of the card's border; defaults to black

.. _property-examples:

Property Examples
=================
`↑ <table-of-contents_>`_

- `Example 1. Defaults`_
- `Example 2. Card bleed`_
- `Example 3. Full bleed`_
- `Example 4. Offset`_
- `Example 5. Grid Marks`_
- `Example 6. Card Spacing`_
- `Example 7. Clean Layout`_
- `Example 8. Column Limit`_
- `Example 9. Row Limit`_
- `Example 10. Circular Frame`_

These examples are shown on a small A8-sized page, as the purpose is to
illustrate how the Deck properties are used; normally cards would be
set out on an A4- or Letter-sized page, but the principle will be the
same.

In all cases, for rectangular cards, a basic ``Rectangle``, with a thick
border, is used as the shape that is drawn on each card.  This purely for
illustration purposes - your cards would have their own set of shapes
that would you want to display.

The ``Rectangle`` also has its *label* set to show the Card's *sequence*
number i.e. the order in  which it is drawn (usually bottom-to-top and
left-to-right), followed by its *column* and *row* number.
The script for all this is:

  .. code:: python

    Card(
        '*',
        rectangle(
            x=0.2, y=0.2,
            width=1.7, height=2.8,
            stroke_width=1, rounding=0.2,
            label='{{sequence}}\n{{id}}')
    )

In your script, the ``Deck()`` command should appear first, followed
by one or more ``Card()`` commands.

.. HINT::

  Remember that **any number** of ``Card()`` commands, each drawing one or
  more shapes on one or more cards, can be used in a script!

Example 1. Defaults
-------------------
`^ <property-examples_>`_

.. |d01| image:: images/decks/cards_deck_01.png
   :width: 330

===== ======
|d01| This example shows the definition of a deck for a set of small
      cards.

      The card size means that there will be 4 rectangular cards on each
      A8 page:

      .. code:: python

        Deck(
            cards=4,
            height=3.2,
            width=2.1)

      The frame for the card is shown by default as a thin black line.
      The shape, or shapes drawn on a card are located within that frame,
      relative to its boundaries.

===== ======


Example 2. Card bleed
---------------------
`^ <property-examples_>`_

.. |d02| image:: images/decks/cards_deck_02.png
   :width: 330

===== ======
|d02| This example shows the definition of a deck for a set of small
      cards. The card size means that there will be 4 rectangular cards
      on each A8 page:

      .. code:: python

        Deck(
            cards=4,
            height=3.2,
            width=2.1,
            fill=silver)

      Every card can be assigned a background color via the *fill* property
      of the Deck. This is also known as a "bleed" area, and is useful in case
      the cutting is misaligned; allowing the main area of the card to still
      be visible.

===== ======


Example 3. Full bleed
---------------------
`^ <property-examples_>`_

.. |d03| image:: images/decks/cards_deck_03.png
   :width: 330

===== ======
|d03| This example shows the definition of a deck for a set of small
      cards. The card size means that there will be 4 rectangular cards
      on each A8 page:

      .. code:: python

        Deck(
            cards=4,
            height=3.2,
            width=2.1,
            fill=silver,
            bleed_fill=grey)

      The bleed area for the card can also be extended to the whole page
      (up to the margins) by using the *bleed_fill* color. In this example
      it's shown as a different color from the Cards' bleed, so that it's
      clear what its coverage is, but usually these colors would match - see
      also `Example 5. Grid Marks`_ below.

===== ======


Example 4. Offset
-----------------
`^ <property-examples_>`_

.. |d04| image:: images/decks/cards_deck_04.png
   :width: 330

===== ======
|d04| This example shows the definition of a deck for a set of small
      cards. The card size means that there will be 4 rectangular cards
      on each A8 page:

      .. code:: python

        Deck(
            cards=4,
            height=3.2,
            width=2.1,
            stroke=red,
            fill=silver,
            bleed_fill=grey,
            offset=0.25)

      To allow for the possibility that a page may not printed all the way
      to the margin, the printing area for the card frames can be offset
      from the margin by any amount (in this example, by ``0.25`` cm).

      Its also possible to offset only from the left by using **offset_x**
      or only from the bottom by using **offset_y**.

      Note that in this example, the color of the Cards frame line has been
      changed to *red*; depending on the *bleed_fill* color it can be helpful
      to set this.

===== ======


Example 5. Grid Marks
---------------------
`^ <property-examples_>`_

.. |d05| image:: images/decks/cards_deck_05.png
   :width: 330

===== ======
|d05| This example shows the definition of a deck for a set of small
      cards. The card size means that there will be 4 rectangular cards
      on each A8 page:

      .. code:: python

        Deck(
            cards=4,
            height=3.2,
            width=2.1,
            stroke=red,
            bleed_fill=silver,
            offset=0.25,
            grid_marks=True,
            grid_length=0.18)

      In this example, there are two changes from previous ones.

      There is now a consistent bleed color across both page background and
      within in the cards themselves; if no separate *fill* property is used,
      then the fill color within the card frame will be set to match that of
      the *bleed_fill*.

      The edge of the page has small marks that are designed to help with
      card cutting; ``grid_marks=True`` enables these marks, and the optional
      *grid_length* allows the length of these lines to be set; the default
      length is ``1`` cm.

===== ======


Example 6. Card Spacing
-----------------------
`^ <property-examples_>`_

.. |d06| image:: images/decks/cards_deck_06.png
   :width: 330

===== ======
|d06| This example shows the definition of a deck for a set of small
      cards. The card size means that there will be 4 rectangular cards
      on each A8 page:

      .. code:: python

        Deck(
            cards=4,
            height=3.2,
            width=2.1,
            stroke=red,
            bleed_fill=silver,
            offset=0.15,
            grid_marks=True,
            grid_length=0.18,
            spacing=0.1,
            spacing_y=0.15)

      Depending on the priniting and cutting requirements, it can be useful
      to add spacing (unused area) between the cards.  The *spacing* property
      sets spacing distance in both x- and y-directions; but it can also be
      set for each individually (using **spacing_x** for horizontal spacing
      and **spacing_y** for vertical spacing).

      Using spacing also adds extra grid marks.

      .. HINT::

        For simple "print, cut and use" cards, spacing is usually *not* needed
        as it just adds more work to the cutting step without much more value!

===== ======


Example 7. Clean Layout
-----------------------
`^ <property-examples_>`_

.. |d07| image:: images/decks/cards_deck_07.png
   :width: 330

===== ======
|d07| This example shows the definition of a deck for a set of small
      cards. The card size means that there will be 4 rectangular cards
      on each A8 page:

      .. code:: python

        Deck(
            cards=4,
            height=3.2,
            width=2.1,
            stroke=None,
            bleed_fill=silver,
            offset=0.15,
            grid_marks=True,
            grid_length=0.18,
            spacing=0.15)

      By keeping all the other adjustments to the Deck layout - *bleed_fill*,
      *offset*, *grid_marks* and (possibly) *spacing* - but disabling the
      drawing of the Card frames by setting ``stroke=None``, the result is a
      "clean" layout where small mistakes in cutting will mean cards are
      still retain a fair visual appearance.

===== ======


Example 8. Column Limit
-----------------------
`^ <property-examples_>`_

.. |d08| image:: images/decks/cards_deck_08.png
   :width: 330

===== ======
|d08| This example shows the definition of a deck for a set of small
      cards. The card size means that there will be 4 rectangular cards
      on each A8 page:

      .. code:: python

        Deck(
            cards=4,
            height=3.2,
            width=2.1,
            stroke=None,
            bleed_fill=silver,
            offset=0.15,
            grid_marks=True,
            grid_length=0.18,
            cols=1)

      By default, **protograf** will fit as many cards as possible into the
      available page area.  If for any reason, there need to be less cards on
      a page, then setting the *cols* property will limit the creation of the
      number of columns on each one.

===== ======


Example 9. Row Limit
--------------------
`^ <property-examples_>`_

.. |d09| image:: images/decks/cards_deck_09.png
   :width: 330

===== ======
|d09| This example shows the definition of a deck for a set of small
      cards. The card size means that there will be 4 rectangular cards
      on each A8 page:

      .. code:: python

        Deck(
            cards=4,
            height=3.2,
            width=2.1,
            stroke=None,
            bleed_fill=silver,
            offset=0.15,
            grid_marks=True,
            grid_length=0.18,
            rows=1)

      By default, **protograf** will fit as many cards as possible into the
      available page area.  If for any reason, there need to be less cards on
      a page, then setting the *rows* property will limit the creation of the
      number of rows on each one.

===== ======


Example 10. Circular Frame
--------------------------
`^ <property-examples_>`_

.. |d10| image:: images/decks/cards_deck_10.png
   :width: 330

===== ======
|d10| This example shows the definition of a deck for a set of small
      cards. The card size means that there will be 6 circular cards
      on each A8 page:

      .. code:: python

        Deck(
            cards=6,
            radius=1,
            bleed_fill=silver,
            offset=0.15,
            grid_marks=True,
            grid_length=0.18,
            spacing=0.15,
            frame='circle')

      The default frame for a Card is a rectangle, but this can be changed
      by setting the **frame** property to either **circle** or **hexagon**.

      In this example, because the cards are circular, the *radius* property
      needs to be set.

      The **frame** property also can be seen "in action" in various
      examples; see a `hexagonal example <examples/cards.rst#hexagon-cards>`_
      and another `circular example <examples/cards.rst#circle-cards>`_.

===== ======
