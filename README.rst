===========
pyprototypr
===========

**pyprototypr** is a simple Python utility for designing and creating simple,
regular, graphical output in PDF format.

It was originally created to handle prototyping of cards, counters, tiles and
boards for board games, but can be used for creation of any document that has
regular or repeating elements; typically containing a mix of graphics and text.


Requirements
============

**pyprototypr** requires a version of Python 3.11.  If this is not your default
Python version, you may want to use **pyenv** (see `Appendix VI <https://github.com/gamesbook/pyprototypr/blob/master/docs/manual.rst#appendix-vi-working-with-pyenv>`_. of the manual)
to install that and then install and use **pyprototypr** in a `virtualenv
<https://pypi.python.org/pypi/virtualenv/>`_.


Documentation
=============

See the ``docs`` directory for the full `manual <https://github.com/gamesbook/pyprototypr/blob/master/docs/manual.rst>`_.

This is also available as a `PDF <https://github.com/gamesbook/pyprototypr/blob/master/docs/manual.pdf>`_.


Quick Start (for the impatient)
===============================

After downloading this package via git, and creating and activating a virtual
environment, you can install **pyprototypr** via::

    python setup.py install

As a quickstart test that **pyprototypr**  works, then you can use one (or
more) of the files from any of the ``examples`` sub-directories.

Make a copy of ``example1.py`` script from the ``examples/manual`` directory - open
`example1.py <https://github.com/gamesbook/pyprototypr/blob/master/examples/manual/example1.py>`_
in your browser, click on the ``Raw`` button, and then save the file into a
local directory on your machine.

Open a command-line window (aka terminal or console), activate the virtual
environment, change to the directory where you saved that file and type::

    python example1.py

This script is very simple; it contains these lines::

    # `example1` script for pyprototypr
    # Written by: Derek Hohls
    # Created on: 29 February 2016
    from pyprototypr.draw import *
    Create()
    PageBreak()
    Save()

and is designed to produce a single, blank A4-sized page. It should create an
output file called ``example1.pdf``, which will appear in the same directory as
the script. You should be able to open and view this file via any PDF viewer
program or app.

If this works, then try out other examples from any of the ``examples``
sub-directories (**note** that some examples may use additional files such
as images or spreadsheets).
