==============
Script Anatomy
==============

**To Be Done**

Start, Middle and End
=====================

Basic Shapes
============

Layout, Repeats and Tracks
==========================

Commands
========

Create Command
~~~~~~~~~~~~~~

PageBreak Command
~~~~~~~~~~~~~~~~~

Save Command
~~~~~~~~~~~~

Comments
========

Drawing vs Creating
===================

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
keyboard). In this case, the script will “fail silently” because
properties that don’t exist are simply ignored. This kind of mistake is
must harder to spot, often because the default value will then be used
instead and it will seem as though the script is drawing something
incorrectly.

Supplying the script with a **duplicate property**, for example::

       display = hexagon(stroke=black, fill=white, height=2, stroke=2)
                                                             ^^^^^^^^
   SyntaxError: keyword argument repeated: stroke

This kind of mistake is usually easier to see as both keywords, in this
case, are part of the same commmand and error you see highlights the
repetition.

Errors are discussed further in the `Additional Concepts <additional_concepts.rst>`_.

