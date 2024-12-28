=======================
Abstract Board Examples
=======================

These examples are part of **pyprototypr** `supplied examples <index.rst>`_.

Bear in mind that the images shown in these examples are lower-resolution
screenshots; the original PDFs that can be generated from the source scripts
will demonstrate full scalability.

.. _table-of-contents:

Table of Contents
=================

- `Chess`_
- `Hex`_
- `HexHex Games`_
- `TicTacToe`_

Chess
=====
`↑ <table-of-contents_>`_

=========== ==================================================================
Title       *Chess Board*
----------- ------------------------------------------------------------------
Source Code `<https://github.com/gamesbook/pyprototypr/blob/master/examples/boards/abstract/chessboard.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a regular Chess board.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/chessboard.png
               :width: 66%
=========== ==================================================================

=========== ==================================================================
Title       *Chess Board - Brown*
----------- ------------------------------------------------------------------
Source Code `<https://github.com/gamesbook/pyprototypr/blob/master/examples/boards/abstract/chessboard_brown.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a regular Chess board with
            brown styling and grid references.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/chessboard_brown.png
               :width: 66%
=========== ==================================================================

Hex
===
`↑ <table-of-contents_>`_

"Hex" is the title of a game invented by Piet Hein.

=========== ==================================================================
Title       *Hex Board*
----------- ------------------------------------------------------------------
Source Code `<https://github.com/gamesbook/pyprototypr/blob/master/examples/boards/abstract/hex_game.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a Hex game board.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/hex_game.png
               :width: 90%
=========== ==================================================================


HexHex Games
============
`↑ <table-of-contents_>`_

There are many games that are played on "hexagonal" board i.e. a board that is
hexagonal in outline and is composed of many hexagons.  The number of hexagons
on a side is used to identify the board size, for example; *hexhex5* is a
board with 5 smaller hexagons along each side.

=========== ==================================================================
Title       *Plain HexHex Board*
----------- ------------------------------------------------------------------
Source Code `<https://github.com/gamesbook/pyprototypr/blob/master/examples/boards/abstract/hexhex.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a regular HexHex board.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/hexhex.png
               :width: 66%
=========== ==================================================================

=========== ==================================================================
Title       *HexHex Board - Circular Spaces*
----------- ------------------------------------------------------------------
Source Code `<https://github.com/gamesbook/pyprototypr/blob/master/examples/boards/abstract/hexhex_circles.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a HexHex board, but with
            circles replacing the usual hexagons in the layout; these are
            placed at the centre of where that hexagon would be drawn.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/hexhex_circles.png
               :width: 66%
=========== ==================================================================

=========== ==================================================================
Title       *HexHex Board - Hexagonal Spaces*
----------- ------------------------------------------------------------------
Source Code `<https://github.com/gamesbook/pyprototypr/blob/master/examples/boards/abstract/hexhex_hexagons.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a HexHex board, but with
            smaller hexagons replacing the usual hexagons in the layout; these
            are placed at the centre of where that hexagon would be drawn.

            In addition, the centre space is masked.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/hexhex_hexagons.png
               :width: 66%
=========== ==================================================================


TicTacToe
=========
`↑ <table-of-contents_>`_

=========== ==================================================================
Title       *TicTacToe Board and Game*
----------- ------------------------------------------------------------------
Source Code `<https://github.com/gamesbook/pyprototypr/blob/master/examples/boards/abstract/tictactoe.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a board and then show a series
            of moves played out on that board.

            This example uses ``RectangularLocations()`` to create a virutal
            grid representing the centres of each space on the board.  One
            ``Layout()`` command then places green squares representing board
            spaces on that grid ; another ``Layout()`` command then places
            a set of shapes, representing all pieces placed on the board up to
            that turn, using their grid-location as a reference.

            The example requires the use of Python lists to record the moves:

              .. code:: python

                turns = [(me,1,1), (you,2,2), (me,1,3), (you,1,2)]

            The use of a loop allows the program to process all the moves and
            create one page for the board state after each move:

              .. code:: python

                for number, turn in enumerate(turns):

            Finally, the ``Save()`` command specifies output to a GIF image,
            along with the framerate (interval between showing each new image).

              .. code:: python

                Save(output='gif',framerate=0.5)

            (*Hint:* normally, you will need to do a "refresh" of the page to
            see the GIF animation.)

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/tictactoe.gif
               :width: 50%
=========== ==================================================================
