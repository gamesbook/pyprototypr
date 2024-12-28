================
Various Examples
================

The examples are part of the **pyprototypr** `supplied examples <index.rst>`_.

Bear in mind that the images shown in these examples are lower-resolution
screenshots; the original PDFs that can be generated from the source scripts
will demonstrate full scalability.

.. _table-of-contents:

Table of Contents
=================

- `A Clock`_
- `Chords`_
- `Miscellaneous Objects 1`_
- `Miscellaneous Objects 2`_
- `World Clocks`_

A Clock
=======
`↑ <table-of-contents_>`_

=========== ==================================================================
Title       *A Wall Clock*
----------- ------------------------------------------------------------------
Source Code `<https://github.com/gamesbook/pyprototypr/blob/master/examples/various/clock.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to create a complex element - a clock - by
            combining multiple
            `customised Circles <../customised_shapes.rst#circle>`_, each with
            different properties.

            Only the first circle - the clock's outline border and its title -
            has a ``fill`` color set but the rest do not:

              .. code:: python

                Circle(cx=3, cy=4.5, radius=2.5, stroke_width=6,
                       label_size=6, label_my=1, label="PROTO")

            The other circles - which each have a `fill`` color of *None* so
            as to be transparent - make use of the ``radiii`` property to draw
            some aspect of the clock, for example the hour marks:

              .. code:: python

                Circle(
                   cx=3, cy=4.5, stroke=white, fill=None, radius=2.3,
                   radii=steps(0,360,30), radii_stroke_width=1.5,
                   radii_length=0.3, radii_offset=2.2)

            Here the setting of various ``radii_`` properties allows the marks
            to be generated.  Of interest is the use of the ``steps()`` command
            to create the list of angles needed to specify where the radii are
            to be drawn.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/various/clock.png
               :width: 50%
=========== ==================================================================

Miscellaneous Objects 1
=======================
`↑ <table-of-contents_>`_

=========== ==================================================================
Title       *Miscellaneous Objects #1*
----------- ------------------------------------------------------------------
Source Code `<../../examples/various/objects.py>`_
----------- ------------------------------------------------------------------
Discussion  The first page of this set of examples shows how to construct
            various "compound" shapes by making use of various properties of
            different shapes.
----------- ------------------------------------------------------------------
Screenshot  .. image:: images/various/objects_1.png
               :width: 80%
=========== ==================================================================


Miscellaneous Objects 2
=======================
`↑ <table-of-contents_>`_

=========== ==================================================================
Title       *Miscellaneous Objects #2*
----------- ------------------------------------------------------------------
Source Code `<../../examples/various/objects.py>`_
----------- ------------------------------------------------------------------
Discussion  The second page of this set of examples shows how to construct
            various "compound" shapes by making use of various properties of
            different shapes.
----------- ------------------------------------------------------------------
Screenshot  .. image:: images/various/objects_2.png
               :width: 80%
=========== ==================================================================


Chords
======
`↑ <table-of-contents_>`_

=========== ==================================================================
Title       *Chords (in a circle)*
----------- ------------------------------------------------------------------
Source Code `<../../examples/various/chords.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a simple effect by combining
            a basic shape - a `chord <../core_shapes.rst#chord>`_ - with a
            Python loop:

              .. code:: python

               for i in range(0, 200):
                   Chord(shape=Circle(cx=2, cy=2, radius=2, fill=None),
                         angle=Random(360), angle1=Random(360))

            Here the ``for`` loop runs for 200 times; each time it does so, a
            the ``Random()`` command pick a random value between 1 and 360 (to
            get a value, in units of degrees) to assign to the Chord's start
            and end points.
----------- ------------------------------------------------------------------
Screenshot  .. image:: images/various/chords.png
               :width: 50%
=========== ==================================================================


World Clocks
============
`↑ <table-of-contents_>`_

=========== ==================================================================
Title       *World Clocks*
----------- ------------------------------------------------------------------
Source Code `<../../examples/various/world_clocks.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to reuse a complex element - a clock - by
            means of a set of Python functions.

            This is a fairly complex script - a mini program really - which
            is likely only to be legible to a Python programmer! Its probably
            beyond the scope of this library's intended use.

            The script essentially "wraps" the clock creation approach
            described above into a function and then uses other functions to
            calculate the position of the clock hands based on the current
            time of the day.  The clock face and hand colors are changed
            depending on the day/night (and light/dark) cycle.

            Further ideas:

            -  Wrap a call to this script via a command that gets runs each
               minute e.g. via ``cron`` on Linux; this will produce an updated
               set of times which could be displayed automatically on screen
               by a suitable viewer
            -  Add a link to an API that generates quotes; use this quote for
               the header text so that a new quote appears each time the script
               is run
----------- ------------------------------------------------------------------
Screenshot  .. image:: images/various/world_clocks.png
               :width: 80%
=========== ==================================================================
