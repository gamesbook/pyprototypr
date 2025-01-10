# pyprototypr

__pyprototypr__ is a utility written in Python for designing and creating
simple, regular, graphical outputs in PDF (or PNG/GIF) format via a script.

__pyprototypr__  has been primarily created to handle the prototyping of cards,
counters, tiles and boards for board games, but can be also used for creating
any simple design that has regular or repetitive elements; typically a mix of
graphics and text.

> You do not need to know the Python language to be able to use __pyprototypr__
> but you do need Python installed on your machine!

## Documentation

The online documentation for __pyprototypr__ starts with the
[Table of Contents](https://github.com/gamesbook/pyprototypr/blob/master/docs/index.rst);
its highly recommended to read the sections in the order presented.

If you're not familiar with any kind of programming or scripting, you should
at least read some of the introductory sections, and especially the
[installation](https://github.com/gamesbook/pyprototypr/blob/master/docs/setting_up.rst)
before proceeding...

## Requirements

__pyprototypr__ requires Python (version of 3.11 or higher) to be installed
and running on your machine.

If this is **not** your current Python version, or Python is not installed on
your machine, may want to [install uv](https://docs.astral.sh/uv/getting-started/installation/)
which is a cross-platform tool able to [install Python](https://docs.astral.sh/uv/guides/install-python).

If using [uv](https://docs.astral.sh/uv/), it is recommended to also create and use a
[virtual environment](https://docs.astral.sh/uv/pip/environments/#creating-a-virtual-environment).

## Quick Start (for the impatient)

Assuming that Python 3.11 or higher is installed on your machine, you can then
install __pyprototypr__ via:
```
pip install pyprototypr
```
or, if using [uv](https://docs.astral.sh/uv/):
```
uv pip install pyprototypr
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
images, CSV files, or spreadsheets). You can download all the examples in a single
[ZIP file](https://github.com/gamesbook/pyprototypr/blob/master/examples.zip).

If it does not work, you may want to look in more detail at the
[installation](https://github.com/gamesbook/pyprototypr/blob/master/docs/setting_up.rst)
guide.

## Contributions

Please see the [list of contributors](CONTRIBUTORS.txt).

## Work-in-Progress

These features are **not** guaranteed to be implemented; they just represent
current / potential areas of work or development.

* [ ] New shapes:
    * [ ] Diamond shape
    * [ ] Parallelogram shape
    * [ ] Wave shape
    * [ ] Cross shape
    * [ ] Pod shape
* [ ] Common objects:
    * [ ] Cube (Rhombus composite)
    * [ ] Domino (DotGrid inside Rectangle outline)
    * [ ] Die (Rectangle with DotGrid; 3D?)
    * [ ] Picture Frame (Trapezoid composite)
* [ ] Hexagons: 18xx tile example (requires `Arcs` below!)
* [ ] Line:
    * [x] end style
    * [ ] join style
* [ ] Polyline: define arcs along the path
* [ ] Arcs (pathways) inside a hexagon (**in progress**)
* [ ] Shortcut notation for styling of: area, line, text, etc.
* [ ] Track: layout shapes along a rectangle, circle or polygon (**in progress**)
* [ ] Stripes: interior "areas" for a Rectangle
* [x] Rotation:
    * [x] text along a line
    * [x] Polygon
    * [ ] Trapezoid
    * [ ] Triangle
* [ ] Cards:
    * [ ] support card back designs
    * [ ] grid lines for hexagonal cards
    * [ ] multiple bleed areas
* [ ] Color:
    * [ ] add support for CMYK
    * [ ] investigate gradients

## Planned/Potential Board Examples

* [ ] Abstract boards: Ludo, 9 Mens Morris, Wari
* [ ] Wargame board: Squad Leader with terrain features (vector and bitmap)
* [ ] Traveller board: show a fully-styled Star system (demo a custom Shape?)
* [x] WarpWar board: show a fully-styled example
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
* `openpyxl` https://pypi.org/project/openpyxl/ - support for access to Excel files
* `pymupdf` https://pymupdf.io/ - support for exporting PDF to PNG images
* `imageio` https://pypi.org/project/imageio/- support for compiling PNGs into a GIF
* `jinja` https://jinja.palletsprojects.com - template logic with variables (for cards)

## License

__pyprototypr__ is licensed under the GNU General Public License.
