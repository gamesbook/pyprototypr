# pyprototypr

__pyprototypr__ is a utility written in Python for designing and creating
simple, regular, graphical outputs in PDF (or PNG/GIF) format via a script.

__pyprototypr__  has been created to handle prototyping of cards, counters,
tiles and boards for board games, but can be also used for creation of any
simple design that has regular or repetitive elements; typically containing
a mix of graphics and text.

> You do not need to know the Python language to be able to use __pyprototypr__!

## Documentation

The online documentation for __pyprototypr__ starts with the
[Table of Contents](https://github.com/gamesbook/pyprototypr/blob/master/docs/index.rst)

If you're not familiar with any kind of programming or scripting, you should
probably read some of the introductory sections, and especially the
[installation](https://github.com/gamesbook/pyprototypr/blob/master/docs/setting_up.rst)
before proceeding...

## Requirements

__pyprototypr__ requires Python (version of 3.11 or higher) to be installed
and running on your machine.

If this is **not** your current Python version, or Python is not installed on
your machine, may want to use [uv](https://docs.astral.sh/uv/guides/install-python)
which is a cross-platform tool able to install both Python and __pyprototypr__.

## Quick Start (for the impatient)

Assuming that Python 3.11 or higher is installed on your machine, you can then
install __pyprototypr__ via:
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
link in your browser, click on the `Raw` button (near the top right), and then
save the web page as a file into a local directory on your machine.

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

If it does not work, you may want to look in more detail at the
[installation](https://github.com/gamesbook/pyprototypr/blob/master/docs/setting_up.rst)
guide.

## Contributions

Please see the [list of contributors](CONTRIBUTORS.txt).

## Work-in-Progress

These features are **not** guaranteed to be implemented, but they are
current / potential areas of work or development that have been identified.

* [x] Page numbering
* [ ] New shapes:
    * [x] Square shape
    * [x] Equilateral Triangle shape
    * [x] Sector shape (wedge of a circle)
    * [x] Trapezoid shape
    * [ ] Diamond shape
    * [ ] Parallelogram shape
    * [ ] Wave shape
    * [ ] Cross shape
    * [ ] Pod shape
* [ ] Common objects:
    * [ ] Cube (rhombus composite)
    * [ ] Domino (dots inside rectangle outline)
    * [ ] Die (6-sided with dots)
    * [ ] Picture Frame (trapezoid composite)
* [x] Arrow: basic styling; rotation
* [x] Circle, Rectangle, Hexagon: centre cross
* [x] Hexagons: "pointy" layout
* [ ] Hexagons: 18xx tile example (requires `Arcs` below!)
* [ ] Line:
    * [x] end style
    * [ ] join style
* [ ] Polyline: create arcs along path
* [ ] Arcs (pathways) inside a hexagon (**in progress**)
* [ ] Shortcut notation for styling of: area, line, text, etc.
* [ ] Track: layout shapes along a rectangle, circle or polygon (**in progress**)
* [x] Notches: different styles for a Rectangle
* [ ] Srripes: interior "lines" for a Rectangle
* [x] Interior hatching:
    * [x] rectangle
    * [x] hexagon
    * [x] equilateral triangle
    * [x] conditional for rounded rectangle
* [x] Layout: virtual grids for putting shapes into locations in different patterns
* [x] Rotation:
    * [x] text along a line
    * [x] shape labels (at centre of shape)
    * [x] Polygon
    * [x] Stadium
    * [ ] Trapezoid
    * [ ] Triangle
* [ ] Cards:
    * [ ] allow for copies of a card
    * [ ] 'wrapper' for counters (default 1" squares)
* [ ] Color:
    * [ ] add support for CMYK

## Planned/Potential Board Examples

* [ ] Abstract boards: Go, Ludo, 9 Mens Morris, Wari, Queens Guard, Backgammon
* [ ] Wargame board: Squad Leader with terrain features (vector and bitmap)
* [ ] Traveller board: showing a fully styled Star system (to demo a custom Shape?)
* [x] WarpWar board: showing a fully-styled sector
* [ ] 18xx board: show a basic map with tracks, towns, cities and off-map areas

## Acknowledgements

> *The world is full of power and energy and a person can go far by just
> skimming off a tiny bit of it.* "Snow Crash", Neal Stephenson.

As always, with Python, you are building "on the shoulders of giants".
In this case, the
[ReportLab PDF Toolkit](https://https://docs.reportlab.com/reportlab/userguide/ch1_intro/)
provides all of the core infrastructure used to do the underlying graphics
processing and PDF file creation; __pyprototypr__ is effectively a highly
customised wrapper to simplify common uses around its existing and extensive
capabilities.

Additional libraries in use include:

* `svglib` https://pypi.org/project/svglib/ - support for drawing SVG images
* `bgg-api` https://pypi.org/project/bgg-api/ - support for access to the
  [BoardGameGeek](https://boardgamegeek.com) API
* `xlrd` https://pypi.org/project/xlrd/ - support for access to Excel `.xls` files
* `openpyxl` https://pypi.org/project/openpyxl/ - support for access to Excel `.xlsx` files
* `pymupdf` https://pymupdf.io/ - support for export from PDF to PNG images
* `imageio` https://pypi.org/project/imageio/- support for compiling PNGs to a GIF
* `jinja` https://jinja.palletsprojects.com - template logic with variables (for cards)

## License

__pyprototypr__ is licensed under the GNU General Public License.
