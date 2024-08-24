===========
pyprototypr
===========

About
=====

**pyprototypr** is a simple Python utility for fast creation of elements needed for
prototype board or card games or other creative endevours requiring regular, simple
output.

**pyprototypr** is *not* a graphic design program, nor even at the level of tools such
as nanDeck (see http://www.nand.it/nandeck/), or MultiDeck
(https://www.semicolon.com/multideck/multideck.html),  both of which have support for
fairly complex designs.


Concept
=======

The program should be reasonably simple, quick and useful.

* **Simple** in that name and shortcuts make sense; defaults are sensible; common things are easy
* **Quick** in that commands should be simple and easy things should take a few lines
* **Useful** for common prototypes but not at the level of complex graphic design
* **Readable** in that commands use common names rather than quirky abbreviations or special characters.

The assumption is that a user of this tool wants to rapidly develop a prototype in
digital form, and is expecting to iterate over numerous versions in the course of a
design process.  For that purpose, a clean and simple layout is better than getting
bogged down in the complexities of, for example, graduated shading or intricate
interdependant layouts.

The underlying availability of Python means that more complex scenarios can,
if needs be, be catered for by a programmer.


Elements
========

========== ========== ========
Properties Shapes     Layouts
========== ========== ========
stroke     line       card
x,y        hexagon    deck
location   circle     grid
size       rectangle  tile
height     ellipse    sequence
width      polygon    track
cx,cy      image
angle      text
========== ========== ========

All elements have default properties; sizes are based on 1cm (centimeter) as a default;
the default foreground color, used for drawing lines, is black and the default
background color, used for filling in areas, is white.


Default Sizes
=============

Some sizes are predefined with names for convenience:

* Tiles - catan, bluemooncity
* Cards - poker, tarot
* Hexagons - AH, SPI, Catan
* Paper - A4, Letter
* Labels_Avery
