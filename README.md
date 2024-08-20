# pyprototypr

**pyprototypr** is a simple Python utility for designing and creating simple,
regular, graphical output in PDF format via a script.

**pyprototypr**  was originally created to handle prototyping of cards, counters, tiles
and boards for board games, but can be used for creation of any simple design that has
regular or repetitive elements; typically containing a mix of graphics and text.

## Documentation

The online documentation for **pyprototypr** starts with the
[Table of Contents](https://github.com/gamesbook/pyprototypr/blob/master/docs/index.md)

If you're not familiar with any kind of programming or scripting, you should probably
read some of the introductory material before proceeding ...

## Requirements

**pyprototypr** requires a version of Python 3.11 or higher.

If this is **not** your default Python version, you may want to use **pyenv**
(or [pyenv-win](https://github.com/pyenv-win/pyenv-win) on Windows) to install and
use **pyprototypr** in a virtual environment.

## Quick Start (for the impatient)

Install **pyprototypr** via:
```
pip install pyprototypr
```
As a quick check that **pyprototypr** is working, you can use one (or more) of the files
from any of the `examples` sub-directories.

Make a copy of `example1.py` script from the `examples/manual` directory. To do so, open
[example1.py](https://github.com/gamesbook/pyprototypr/blob/master/examples/manual/example1.py)
in your browser, click on the `Raw` button, and then save the file into a local
directory on your machine.

Open a command-line window (also known as a  *terminal* or a *console*), change to the
directory where you saved the above file and type:
```
python example1.py
```
and press the `Enter` key.

This script is very simple - it just contains these lines:
```
# `example1` script for pyprototypr
# Written by: Derek Hohls
# Created on: 29 February 2016
from pyprototypr.draw import *
Create()
PageBreak()
Save()
```
and is designed to produce a single, blank, A4-sized page in a PDF file.

It should create an output file called `example1.pdf`, which will appear in the
same directory as the script. You should be able to open and view this file using
any PDF-capable program or application.

If this works, then download and try out other scripts from any of the `examples`
sub-directories (**note** some examples may require additional files such as
images, CSV files, or spreadsheets).

## Planned/Potential Features

These are not guaranteed to be addressed, but they are potential areas of
work for future development.

* [x] Page numbering
* [ ] New shapes:
    * [x] Square shape
    * [x] Equilateral Triangle shape
    * [x] Sector shape (wedge of a circle)
    * [ ] Trapezoid shape
    * [ ] Wave shape
    * [ ] Domino shape (with outline?)
    * [ ] Cross shape
* [ ] Arrow: styling
* [x] Circle, Rectangle, Hexagon: centre cross
* [x] Rectangle: with notches
* [x] Hexagons: "pointy" layout
* [ ] Hexagons: 18xx example
* [ ] Line:
    * [x] end style
    * [ ] join style
* [ ] Polyline: add arcs
* [ ] Arcs (pathways): for a hexagon (**in progress**)
* [ ] Shortcut notation for styling of: area, line, text, etc.
* [ ] Track feature: layout shapes along a rectangle or circle  (**in progress**)
* [ ] Interior hatching:
    * [x] rectangle
    * [x] hexagon
    * [x] equilateral triangle
    * [ ] conditional for rounded rectangle
* [ ] Layout: a virtual grid for putting shapes into rows/cols in different patterns
* [x] Rotation:
    * [x] text along a line
    * [ ] shape labels (in the centre of shape)
    * [ ] Polygon
    * [ ] Stadium
    * [ ] Triangle
    * [ ] Octagon
* [ ] Cards:
    * [ ] allow for copies of a cards
    * [ ] 'wrapper' for tiles (default size)

## Planned/Potential Examples

* [ ] Abstract boards: Go, Ludo, 9 Mens Morris, Wari, Queens Guard, Backgammon
* [ ] Wargame board: Squad Leader with terrain features (vector/bitmap)
* [ ] Traveller board: showing a fully styled Star system (custom Shape?)
* [x] WarpWar board: showing a fully-styled sector
* [ ] 18xx board: show a basic map with tracks, towns and off-map areas
* [ ] Dartboard: using Sector shape and numbered Track

## Acknowledgements

As always, with Python, you are building "on the shoulders of giants". In this case, the
[ReportLab PDF Toolkit](https://https://docs.reportlab.com/reportlab/userguide/ch1_intro/)
provides all of the core, underlying infrastructure used to do the graphics work;
**pyprototypr** is a custom wrapper around its numerous and extensive capabilities.

Additional libraries used include:

* `svglib` https://pypi.org/project/svglib/ - support for drawing SVG images
* `bgg-api` https://pypi.org/project/bgg-api/ - support for access to the BoardGameGeek API
* `xlrd` https://pypi.org/project/xlrd/ - support for access to `.xls` files
* `openpyxl` https://pypi.org/project/openpyxl/ - support for access to `.xlsx` files
* `pymupdf` https://pymupdf.io/ - support for export to PNG images
