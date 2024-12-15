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
Discussion  This example shows how to construct a deck of cards using these
            commands (only an extract of the code is shown here):

              .. code:: python

                l1 = line(
                    x=0.8, x1=5.6, y=7.1, y1=8.4,
                    stroke=gold, stroke_width=2)
                r1 = rectangle(
                    x=0.7, y=7.0, width=5, height=1.5,
                    stroke_width=1, rounding=0.2)
                low = group(r1, l1)

                Card([1,2,3], low)
                Card("4-6", r1)
                Card("7,8,9", l1)

            This is a simple design of lines and rectangles. These are
            assigned names which can be used directly; or indirectly as part
            of a ``group``.

            The assignment as to which card (``Card``) can either be done via
            a string e.g. ``"4-6"`` or a list of numbers e.g. ``[1,2,3]``.

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
Discussion  This example shows how to construct a deck of cards using these
            commands (only an extract of the code is shown here):

              .. code:: python

                combos = Matrix(
                    labels=['SUIT', 'VALUE', 'IMAGE'],
                    data=[
                        # tomato, lime, aqua, gold, hotpink
                        ['#FF6347', '#00FF00','#00FFFF', '#FFD700', '#FF69B4'],
                        ['5', '3', '1'],
                        # tapedrive, heart, snowflake
                        ['\u2707', '\u2766', '\u2745']
                    ])
                Data(matrix=combos)

            The use of the ``Matrix`` command is helpful for a design that is
            a combination/permutation scenario.

            In this example each card will display a unique combination of a
            *SUIT* - these are hexadecimals colors in the first list appearing
            in ``data`` - plus a *VALUE* - these are the items in the second
            list appearing in ``data`` - and an *IMAGE* - these are the
            Unicode symbols in the third list of ``data``. As can be seen, a
            Unicode symbol is shown by 4-characters prefixed by the ``\u``
            (For more, see
            `Unicode <../useful_resources.rst#unicode-characters>`_
            character resources.)

            Once defined in the ``Matrix``, the results will be generated and
            stored via the ``Data`` command's **matrix** property.
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
Discussion  This example shows how to construct a deck of cards using these
            commands (only an extract of the code is shown here).

            The bulk of the cards are generated via a ``Matrix`` (see the
            **Matrix** example above), also using Unicode symbols for the
            **SUIT** and a list of the standard card **VALUE** letters and
            numbers:

              .. code:: python

                combos = Matrix(
                    labels=['SUIT', 'VALUE'],
                    data=[
                        # spade, club, heart, diamond
                        ['\u2660', '\u2663', '\u2665', '\u2666'],
                        ['K','Q','J','10','9','8','7','6','5','4','3','2','A'],
                    ])
                Data(matrix=combos, extra=2)

            The **extra** property for the ``Data`` command allows the deck to
            consist of more more cards than those generated by the ``Matrix``;
            so, in this case, 4 suits multiplied by 13 values is 52 cards.

            The Royalty cards require an image, whose settings are created via
            a ``Common`` command:

              .. code:: python

                royals = Common(x=1.5, y=2, width=3.5, height=5)
                Card("14", image("images/king_c.png", common=royals))
                Card("15", image("images/queen_c.png", common=royals))

            The Ace of Spades is often specially demarcated in a deck via a
            more elaborate design. In this case, the design is simply two
            large spades symbols, of different colors, superimposed:

              .. code:: python

                Card("13",
                     text(
                         x=3.15, y=2.5,
                         font_size=180, stroke=black, text='\u2660'),
                     text(x=3.15, y=3.8,
                         font_size=60, stroke=white, text='\u2660'))

            The Jokers (not shown in the screenshot) are the extra 2 cards
            needed for a standard deck. In this case they also require an
            image, as well as text whose settings are created via a
            ``Common`` command:

              .. code:: python

                Card("53",
                     text(common=value_top, stroke=black, text='J'),
                     text(common=value_low, stroke=black, text='J'),
                     image("images/joker_black.png", x=1, y=2, width=5, height=5))


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
Discussion  This example shows how to construct a deck of cards using these
            commands (only an extract of the code is shown here):

              .. code:: python

                Data(images="pictures", images_filter=".png,.jpg")
                # add an image from Data to each card
                Card("*", image("*", x=0, y=0, width=6.3, height=8.8))

            The commands for generating cards that just consist of an image
            are simple.  the ``Data`` command's **images** property points to
            a directory containing all the images. It can be helpful to ensure
            that any non-image files stored in that  directory are ignored;
            for this purpose the **images_filter** property can be set to
            contain a list of allowable file extensions.

            The ``Card`` command sets all cards in the deck (via ``*``) to
            each use an image; but in thise case no ``Image`` name is set
            as this will be "filled in" with the names from the ``Data``.

            *Credits:* the original image that was "chopped up" to form the
            set of images used for these example cards was sourced from:
            https://picjumbo.com/mysterious-fantasy-forest-with-old-bridges/

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/cards/cards_images.png
               :width: 90%
=========== ==================================================================
