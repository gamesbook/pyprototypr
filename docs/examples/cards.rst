=============
Card Examples
=============

These examples are part of the set of `supplied examples <index.rst>`_
with **pyprototypr**.

Bear in mind that the images shown in these examples are lower-resolution
screenshots; the original PDFs that can be generated from the source scripts
will demonstrate full scalability.

.. _table-of-contents:

Table of Contents
=================

- `Simple`_
- `Matrix Generated`_
- `Standard Playing Cards`_
- `Image-only Cards`_

Simple
======
`↑ <table-of-contents_>`_

=========== ==================================================================
Title       *Simple set of Cards*
----------- ------------------------------------------------------------------
Source Code `<../../examples/cards/cards_design.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a deck of cards using

              .. code:: python

                Data(filename="counters.xls")

            To set changes for cards at intervals; for example, every even
            card and also every odd card:

              .. code:: python

                # element added to every odd card
                Card(steps(1,9,2), rectangle())
                # element added to every even card
                Card(steps(2,9,2), circle())

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/cards/cards_simple.png
               :width: 90%
=========== ==================================================================


Matrix Generated
================
`↑ <table-of-contents_>`_

=========== ==================================================================
Title       *Cards generated from a Matrix*
----------- ------------------------------------------------------------------
Source Code `<../../examples/cards/cards_matrix_one.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a deck of cards using

              .. code:: python

                Data(filename="counters.xls")

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/cards/cards_matrix.png
               :width: 90%
=========== ==================================================================


Standard Playing Cards
======================
`↑ <table-of-contents_>`_

=========== ==================================================================
Title       *Standard Playing Cards generated from a Matrix & Images*
----------- ------------------------------------------------------------------
Source Code `<../../examples/cards/cards_standard.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a deck of cards using

              .. code:: python

                Data(filename="counters.xls")

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/cards/cards_standard.png
               :width: 90%
=========== ==================================================================


Image-Only Cards
================
`↑ <table-of-contents_>`_

=========== ==================================================================
Title       *Cards generated from an images directory*
----------- ------------------------------------------------------------------
Source Code `<../../examples/cards/cards_images.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a deck of cards using

              .. code:: python

                Data(filename="counters.xls")

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/cards/cards_images.png
               :width: 90%
=========== ==================================================================
