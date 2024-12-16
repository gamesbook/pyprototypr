==============
Decks of Cards
==============

.. _table-of-contents:

Table of Contents
=================

- `Introduction`_
- `Basic Concepts`_
- `The Deck Command`_
- `The Card Command`_
- `The Data Command`_
- `The Matrix Command`_
- `Countersheet and Counter Commands`_
- `Supporting Commands`_

  - `group command`_
  - `T(emplate) command`_
  - `V(alue) command`_


Introduction
============
`↑ <table-of-contents_>`_

Cards are a common and widely used method of storing and transmitting
small sets of related data.

Scientists have used index cards since the 17th century and, of course,
libraries have long-used card catalogues as a way to track information
about books. Businesses in the 20th century used Rolodexes and business
cards as means to track and exchange information about individuals. Early
computers used a form of index cards called "punch" cards to store their
data. Playing cards, of course, have been popular both in China and
Europe; coming into more widespread use somewhere in the 9th and 14th
centuries respectively.

The massive rise in popularity of a game like *Magic the Gathering*, from
the 1990s, has inspired the greater use of cards in all aspects of the
modern board gaming experience, with cards taking the predominant role in
many of them.

Basic Concepts
==============
`↑ <table-of-contents_>`_

A common element in many games is a deck - or multiple decks - of cards.

    **pyprototypr** also considers items such tiles or counters to be "cards";
    they are really just "shapes containing other shapes"; see the section
    on `Countersheet and Counter Commands`_

There are two core concepts: the ``Card()`` and the ``Deck()``:

-  A ``Card()`` command is used to specify the design for a card, or range
   of cards, typically using elements that have already been defined.
   The patterns or designs can be set to appear on one or multiple cards.
-  A ``Deck()`` command is used to specify type, size and number of cards
   that  will be used to create all cards in the deck.

In many cases, the ``Data()`` command will be needed, in order to provide the
settings for the properties of the elements appearing on a card.

In some cases, the ``Matrix()`` command will be needed; this is an alternate
method of providing the settings for the properties of the elements appearing
on a card.


The Deck Command
================
`↑ <table-of-contents_>`_

This command provides the overall "framework" for the cards that are defined
in the script.  It's primary purpose is to set the card size, and then
calculate how many cards appear on a page.  It manages the "flow" of cards as
they get drawn.

Primary Properties
------------------

The following are key properties that will usually need to be set for a deck:

- **cards** - this is the number of cards appearing in the deck; it defaults
  to 9; note that other commands such as ``Data()`` and ``Matrix`` can alternate
  this value
- **height** - this is the card height; it defaults to 8.8 cm.
- **width** - this is the card width; it defaults to 6.3 cm.

Secondary Properties
--------------------

The following are other properties that can also be set for a deck:

- **margin** - the margin for the page on which cards are drawn
- **margin_left** - the left margin for the page on which cards are drawn;
  defaults to the **margin** setting
- **margin_right** - the right margin for the page on which cards are drawn;
  defaults to the **margin** setting
- **margin_top** - the top margin for the page on which cards are drawn;
  defaults to the **margin** setting
- **margin_bottom** - the bottom margin for the page on which cards are drawn;
  defaults to the **margin** setting
- **rounding** - sets the size of rounding on each corner of a card
- **fill** - sets the color of the card's area; defaults to white
- **stroke** - sets the color of the card's border; defaults to black
- **grid_marks** - if set to ``True``, will cause small marks to be drawn at
  the border of the page that align with the eddges of the cards

Deck Example #1
---------------

This example shows the definition of a simple deck for cards that are a
commonly-used size (with the default units of centimetres in place).
The card size means that  there will be 9 cards on an A4 page
(in default portrait mode):

    .. code:: python

      Deck(
        cards=18,
        height=8.8,
        width=6.3)

Deck Example #2
---------------

This example shows the definition of a deck of 27 cards that are a
default size, with rounded corner and their colors set; the grid marks
will appear along the page edges.  The default card size means that
there will be 9 cards on an A4 page (in default portrait mode):

    .. code:: python

      Deck(
        cards=27,
        grid_marks=True,
        rounding=0.3,
        fill=gold,
        border=tomato)


The Card Command
================
`↑ <table-of-contents_>`_

This command is both simple and flexible. It allows for a complex design, with
many elements, to be added to any of the cards in a deck.




The Data Command
================
`↑ <table-of-contents_>`_

This command



The Matrix Command
==================
`↑ <table-of-contents_>`_

This command



Countersheet and Counter Commands
=================================
`↑ <table-of-contents_>`_

This command


Supporting Commands
===================
`↑ <table-of-contents_>`_

The following commands are helpful in terms of increased flexibilty and
reduced repetition when designing a deck of cards.

group command
-------------

This command

T(emplate) command
------------------

This command


V(alue) command
------------------

This command
