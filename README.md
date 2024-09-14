# pyprototypr

__pyprototypr__ is a utility written in Python for designing and creating simple,
regular, graphical output in PDF format via a script.

__pyprototypr__  has been created to handle prototyping of cards, counters, tiles
and boards for board games, but can be also used for creation of any simple
design that has regular or repetitive elements; typically containing a mix of
graphics and text.

> You do not need to know the Python to use __pyprototypr__!

## Documentation

The online documentation for __pyprototypr__ starts with the
[Table of Contents](https://github.com/gamesbook/pyprototypr/blob/master/docs/index.md)

If you're not familiar with any kind of programming or scripting, you should
probably read some of the introductory sections before proceeding ...

## Requirements

__pyprototypr__ requires a version of Python 3.11 or higher.

If this is **not** your default Python version, you may want to use **pyenv**
(or [pyenv-win](https://github.com/pyenv-win/pyenv-win) on Windows) to install
and use __pyprototypr__ in a virtual environment.

## Quick Start (for the impatient)

Install __pyprototypr__ via:
```
pip install pyprototypr
```
To check that __pyprototypr__ is working, you can use one (or more) of
the files from any of the various
[examples](https://github.com/gamesbook/pyprototypr/blob/master/examples/)
sub-directories.

As a quick test, make a copy of `example1.py` script from the `examples/manual`
directory. To do so, open the
[example1.py](https://github.com/gamesbook/pyprototypr/blob/master/examples/manual/example1.py)
link in your browser, click on the `Raw` button, and then save the web page as
a file into a local directory on your machine.

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
from pyprototypr import *
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

## Work-in-Progress

These features are not guaranteed to be addressed, but they are current / potential
areas of work or development.

* [x] Page numbering
* [ ] New shapes:
    * [x] Square shape
    * [x] Equilateral Triangle shape
    * [x] Sector shape (wedge of a circle)
    * [ ] Trapezoid shape
    * [ ] Parallelogram shape
    * [ ] Wave shape
    * [ ] Cross shape
    * [ ] Pod shape
    * [ ] Diamond shape
* [ ] Simple objects:
    * [ ] Cube (rhombus composite)
    * [ ] Domino (with outline?)
    * [ ] Picture frame (trapezoid composite)
* [ ] Arrow: styling; angled
* [x] Circle, Rectangle, Hexagon: centre cross
* [x] Rectangle: with notches
* [x] Hexagons: "pointy" layout
* [ ] Hexagons: 18xx example
* [ ] Line:
    * [x] end style
    * [ ] join style
* [ ] Polyline: add arcs
* [ ] Arcs (pathways) inside a hexagon (**in progress**)
* [ ] Shortcut notation for styling of: area, line, text, etc.
* [ ] Track: layout shapes along a rectangle, circle or polygon  (**in progress**)
* [x] Interior hatching:
    * [x] rectangle
    * [x] hexagon
    * [x] equilateral triangle
    * [x] conditional for rounded rectangle
* [x] Layout: virtual grids for putting shapes into locations in different
      patterns
* [x] Rotation:
    * [x] text along a line
    * [x] shape labels (at centre of shape)
    * [x] Polygon
    * [x] Stadium
    * [ ] Triangle
* [ ] Cards:
    * [ ] allow for copies of a card
    * [ ] 'wrapper' for counters (smaller default size)

## Planned/Potential Board Examples

* [ ] Abstract boards: Go, Ludo, 9 Mens Morris, Wari, Queens Guard, Backgammon
* [ ] Wargame board: Squad Leader with terrain features (vector and bitmap)
* [ ] Traveller board: showing a fully styled Star system (custom Shape?)
* [x] WarpWar board: showing a fully-styled sector
* [ ] 18xx board: show a basic map with tracks, towns and off-map areas

## Acknowledgements

As always, with Python, you are building "on the shoulders of giants".
In this case, the
[ReportLab PDF Toolkit](https://https://docs.reportlab.com/reportlab/userguide/ch1_intro/)
provides all of the core infrastructure used to do the underlying graphics
processing; __pyprototypr__ is really a customised wrapper to simplify common
uses and needs around its numerous and extensive capabilities.

Additional libraries in use include:

* `svglib` https://pypi.org/project/svglib/ - support for drawing SVG images
* `bgg-api` https://pypi.org/project/bgg-api/ - support for access to the BoardGameGeek API
* `xlrd` https://pypi.org/project/xlrd/ - support for access to Excel `.xls` files
* `openpyxl` https://pypi.org/project/openpyxl/ - support for access to Excel `.xlsx` files
* `pymupdf` https://pymupdf.io/ - support for export to PNG images
