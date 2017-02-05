===========
pyprototypr
===========

About
=====

**pyprototypr** is a simple Python utility for fast creation of elements needed for prototype board or card games or other creative endevours requiring regular, simple output.

**pyprototypr** is *not* a graphic design program, nor even at the level of a tool such as nanDeck (see http://www.nand.it/nandeck/), which allows for fairly complex designs.


Concept
=======

The program should be reasonably simple, quick and useful.

* **Simple** in that name and shortcuts make sense; defaults are sensible; common things are easy
* **Quick** in that commands should be simple and easy things should take a few lines
* **Useful** for common prototypes but not at the level of complex graphic design

The assumption is that a user of this tool wants to rapidly develop a prototype in digital form, and is expecting to iterate over numerous versions in the course of a design process.  For that purpose, a clean and simple layout is better than getting bogged down in the intricacies of, for example, graduated shading or intricate interdependant layouts.

The underlying availability of Python means that more complex scenarios can, if needs be, be catered for by a programmer.


Elements
========

Primitives          Shapes             Elements
-----------------------------------------------
color               line               card
position            hex                grid
place               circle             image
size                rectangle          deck
                    oval               tile
                    polygon            text

All elements have defaults; sizes are based on 1cm (one centimeter) as a default; the default foreground color is black and the default background color is white.


Sizes
=====

Some sizes are predefined for convenience:

* iles - catan, bluemooncity
* Cards - poker, tarot
* Hexes - AH, SPI, Catan
* Paper - A4, Letter
* Labels_Avery


Keywords
========

* type []
* offset []
* x []
* y []
* width []
* height []
* size []
*  []
*  []
*  []

