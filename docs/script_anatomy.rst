==============
Script Anatomy
==============

A "script" is the short-cut name for a file containing list of instructions 
that will be read and processed by Python.  The script is usually given an
extension of ".py:.

    *NOTE* This document assumes that **pyprototypr** is working on your 
    computer, and that you have read the `Basic Concepts <basic_concepts.rst>`_

Table of Contents
=================

- `Start, Middle and End`_
- `Commands`_
- `Comments`_
- `Drawing vs Assigning`_
- `Basic Shapes`_
- `Card Decks`_
- `Layout, Repeats and Tracks`_
- `The FEEDBACK Message`_
- `Making Mistakes`_


Start, Middle and End
=====================

A script will normally start with a `Create command`_, then contain a series
of `other commands`_ with the instructions for your particular needs (each 
comand can run over multiple lines).  
    
    If your needs are more complex, you may be embedding "pure" Python commands,
    or even using tools provided by other Python libaries. 

If the design you are wokring on needs multiple pages, then a `PageBreak command`_
can be inserted, followed again by the specific commands you need.

The final command in the script will be the `Save command`_, which triggers the
creation of the output; by default a PDF file.


Commands
========

Create Command
--------------

The ``Create()`` command is the first, essential command that should appear
in a script. It sets up the basic document framework for the inclusion of all
the elements that will appear.

By default, it will setup an A4 page (in portait mode), with 
a margin of one-half inch (1.25cm), and units of centimetres; 
the resulting output file will have the same name as the script, 
but with a '.pdf' extension.

To customise the command, set properties as follows:

- **paper**: use a paper size from either of the ISO series - A0 down to A8; 
  or B6 down to B0 - or a USA type - letter, legal or elevenSeventeen
- **filename**: name of the output PDF file
- **units**: these can be ``cm`` (centimetres), ``in`` (inches), ``mm`` 
  (millimetres), or ``points``
- **landscape**: "wrap" the paper size with ``landscape()`` to change the page
  orientation
- **margin**: set the margin value (uses the defined `units`)
- **margin_top** - set top margin
- **margin_bottom** - set bottom margin
- **margin_left** - set left margin
- **margin_right** - set right margin

Here is an example of a ``Create`` command::

    Create(
        paper=landscape(A3),
        units=in,
        filename="testA3.pdf",
        margin_top=1,
        margin_left=1,
    )

PageBreak Command
-----------------

The ``PageBreak()`` command is only needed if you need to start a new page.

Save Command
------------

The ``Save()`` is usually the last to appear.  By default it simply results in
the outcome of all the commands used being written out to a PDF file.

To customise the command, set properties as follows:

- **?**: 
- **?**: 
- **?**: 
- **?**: 


Other Commands
--------------

There are numerous othger commands which are either used to draw shapes, or 
sets of shapes, or to control how and where shapes appear. See:

- `Core shapes <core_shapes.rst>`_ 
- `Card and Deck commands <card_decks.rst>`_
- `Repetitive and reuse commands <advanced_commands.rst>`_
- `Layout commands <layouts.rst>`_ 
- `Hexagonal grid commands <hexagonal_grids.rst>`_

Comments
========

It can be useful to "annotate" a script with other details that can remind
you, as a reader, about what and/or why apsects of the script.

Single Line Comments
--------------------

Simply insert a ``#``, followed by space, at the start of the comment line::

    # this is the rim of the clock
    Circle(stroke_width=5)

Multiple Line Comments
----------------------

Use a pair of triple-quotes to surround the lines of comments::

    """
    This is a useful script.
    It was created to remind me about grids.
    It should not be used for normal designs.
    """
    Create()


Drawing vs Assigning
====================

All of the `shape <core_shapes.rst>`_ commands can either be called with a
capital letter or a lowercase letter.

The use of a capital is the more common case, and it effectively tells 
**p** to "draw this shape now"::

    Circle(stroke_width=5)

The use of a lowercase is normally when you assign a shape to a name, so that
it can be used (or drawn) later on in the script::

    # this circle is not drawn at this point
    clock = sircle(stroke_width=5)

    # circle (aka "clock") will be drawn when the card(s) are drwan
    Card("*", clock)


Basic Shapes
============


Card Decks
==========

A common element in many games is a deck - or multiple decks - of cards.
**pyprototypr** also considers items such tiles or counters to be "cards";
they are really just "shapes containing other shapes"

There are two key commands for creating a deck of cards: the ``Card()`` and 
the ``Deck()``.  These are discussed in detail in the `card decks <card_decks.rst>`_ section.

A useful "getting started" approach is to look through the section with
`basic worked examples <worked_example.rst>`_ which show an increasingly
complex set of examples for setting up and running scripts to generate a 
deck of cards.


Layout, Repeats and Tracks
==========================


The FEEDBACK Message
====================




Making Mistakes
===============

It is, unfortunately, all too easy to make mistakes while writing
scripts.

These are some common kinds of mistakes:

Supplying the script an **incorrect value**, for example, giving the
location a value of ``3.0`` when you meant to give it ``0.3``; this kind
of mistake can usually be detected when you look at the PDF, although it
may not be immediately obvious exactly what has happened.

Supplying the script an **incorrect kind of value**, for example, giving
the ``y`` location a value of ‘a’ instead of a number. The script will
stop at this point and give you a feedback message.

Supplying the script a **property that does not exist**, for example,
using ``u=2.0`` when you meant to say ``y=2.0`` (which can happen
because those two letters are located right next to each other on a
keyboard and the letters are bit similar). In this case, the script will 
“fail silently” because properties that don’t exist are simply ignored. 
This kind of mistake is much harder to spot; often because the default value 
will then be used instead and it will seem as though the script is drawing something incorrectly.

Supplying the script with a **duplicate property**, for example::

   display = hexagon(stroke=black, fill=white, height=2, stroke=2)
                                                         ^^^^^^^^
   SyntaxError: keyword argument repeated: stroke

This kind of mistake is usually easier to see as both keywords, in this
case, are part of the same commmand and error message you see also highlights 
the repetition with the ``^^^^^^^^`` characters.

Errors are discussed further in the `Additional Concepts 
<additional_concepts.rst>`_ section.

