===========
pyprototypr
===========

**pyprototypr** is a simple Python utility for designing and creating simple,
regular, graphic output.

It was originally created to handle prototyping of cards, counters, tiles and
boards for board games, but can be used for creation of any document that has
regular or repeating elements; typically containing a mix of graphics and text.


Requirements
============

**pyprototypr** requires a version of Python 2.7.  If this is not your default
Python version, you may want to use `pyenv` (see *Appendix VI* of the manual)
to install that and then install and use `pyprototypr` in a `virtualenv
<https://pypi.python.org/pypi/virtualenv/>`_.


Documentation
=============

See the `docs` directory for the manual.


Quick Start (for the impatient)
===============================

As a quickstart test that **pyprototypr**  works, then you can use one (or
more) of the files from any of the `examples` sub-directories.

Make a copy of `example1.py` script in the `examples/manual` directory - open
http://github.com/gamesbook/pyprototypr/examples/manual/example1.py
in your browser, click on the `Raw` button, and then save the file into a
directory on your machine.

Open a command-line window (aka terminal or console), activate the virtual
environment, change to the directory where you saved that file and type::

    python example1.py

The `example1.py` script in the `examples/manual` directory contains these
lines::

    # `example1` script for pyprototypr
    # Written by: Derek Hohls
    # Created on: 29 February 2016
    from draw import *
    Create()
    PageBreak()
    Save()

and is designed to produce a single, blank A4-sized page. It should create an
output file called `test.pdf`, which will appear in the same directory as the
script. You should be able to open and view this PDF file via any PDF viewer
program or app.

If this works, then try out other examples from any of the `examples`
sub-directories (note that some examples may require additional files such
as images or spreadsheets).
