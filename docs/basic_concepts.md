# pyprototypr: Basic Concepts

Like many other specialised tools, **pyprototypr** has its own set of terms
and concepts that act as "short-cuts" to help in discussions. Some of these are
likely to be common to other graphics editing or programming tools.


## How you'll use **pyprototypr**

You will be using **pyprototypr** to write what is termed a *script*
i.e. a recipe or list of instructions that are stored in a file. These
instructions are used to define a game board, a set of cards or tiles, or any
other, similar, regular graphical design of your choice.

You will then use Python to "run" the script. Python will take the file you have
written, and step through it, line by line, from top to bottom, to finally create
an output PDF file that will show the outcome of this process - hopefully with
your desired design!

If you want to make changes to the design, then you add to, delete, or change the
instructions in your script and then use Python to process it again to create an
updated PDF file.


## The "script" concept

Creating a *script* is similar to the process of building a house; in the sense
that the instructions which come first create underlying parts that are "deeper
down"; in the same way that a foundation is below a floor, which in turn is below
the walls, which are below the ceiling, which is below the roof. The lower
layers are often not "visible", even if they are there and just as important!

So, for example, a page may contain rectangles representing cards.  Each card may
then have additional rectangles placed on it, representing some aspect that is
part of your card design.  Those rectangles, in turn, could have various images
or icons placed on them. So, each item can "obscure" some part - or even all -
of the item it is placed on.

Its also possible to define things earlier in a script that are used later on.

In summary - the *order* of instructions in a script is important!

> For more on how scripts are constructed see [Script Anatomy](script_anatomy.md).


## The "page" concept

When using **pyprototypr** what you are doing is defining where and how various
things appear on a *page*.  A script can create multiple

The position of something is *where* it will be drawn on the page.  To do this,
you provide both an **x** - the horizontal position - and a **y** - the vertical
position - for each thing that you want to on appear the page.

So, if you look at an A4 page - which is 21cm wide and just less than 30cm high -
then a point in the middle of the page would have an **x position** of 10.5cm -
its distance from the left edge of the page; and a **y position** of 14.8cm -
its distance from the bottom edge of the page.  Similarly, for a letter-sized
page of 8.5" by 11", a point in the middle of the page would have an **x position**
of 4.25" and a **y position** of 5.5".

As the use of margins is common for most documents and drawings, *all* distances in
**pyprototypr** are considered to be relative to the margin settings i.e. if the
default page margin, for all edges of the the page in the previous example, was
2.5cm (1") then to locate a point at those same distances would mean using an
**x position** of 8cm and a **y position** of 12.3cm, as the position values will
effectively be increased by the margin size.


## The "element" concept

Rather than use the slightly clumsy term "thing", **pyprototypr**  uses the term
*element*.

Almost everything in **pyprototypr** that appears in the output is considered
to be an *element* of some sort.  Elements are often geometrical **shapes**, such
lines, circles or rectangles, but can also be text or images.

Examples of available geometrical **shapes** are:

* Circle
* Ellipse
* Hexagon
* Polygon
* Rectangle
* Rhombuse
* Stadium

Descriptions of all of these elements, and how to create and use them, are provided
in the section on [Core Shapes](core_shapes.md).


## Defining elements' properties

Elements can have other settings apart from their position.

For example, the rectangle which represents the outline of a card has a *size*.
The rectangle's size is measured in terms of its *height* and *width*.  The line
used to draw the rectangle also has a *stroke width* and a *color* (see below for
more about the concepts of stroke and color).  A circle will have its size defined
by a *radius* or a *diameter* which define how big it is, and so on.

> NOTE: Because the word "size" is such a general one, its not used in **pyprototypr**;
> more specific terms are used instead.

Many elements also have a *fill* that is the color with which they will be "filled".

All of these kinds of settings are called **properties**.


## Working with color

Everything we see has color.

Color in **pyprototypr**, is defined in the same way as it is in pages that appear
on the web i.e. in RGB (red-green-blue) *hexadecimal* format - for example,
*#A0522D* represents a shade of the color that we would term "brown".

> For more details on hexadecimal colors, refer to http://www.w3.org/TR/css3-color.

Colors in **pyprototypr** can also make use of names from a pre-defined list - for
example *#A0522D* is defined as the color *sienna*.  A PDF file is supplied here -
[colorset.pdf](../examples/colorset.pdf) - that shows all the names and colors available.

Properties in **pyprototypr** are typically set using a "fill" to set the color of an
area, and "stroke" to set the color of a line.


## Working with units

All positions, heights, widths, distances, line thicknesses and other kinds of
lengths or sizes all need to be measured in a particular set of **units**.

In the USA, people tend to use the so-called Imperial System. In
**pyprototypr** this means that distances might be measured in units of inches
(inches are often shown with an *"* symbol in documents, but in **pyprototypr** inches
are referred to using the term *inch*).

In almost all of the rest of the world, the Metric System is in use. In **pyprototypr**
this means that distances will be measured in units of centimetres (abbreviated in
**pyprototypr** as *cm*). Alternatively, you can choose to use millimetres
(abbreviated in **pyprototypr** as *mm*).

> For conversion purposes, 1 inch equals 25.4 centimetres or 25.4 millimetres.

**pyprototypr** also allows units of *points*, which are the measurement units
traditionally used in the printing industry.  There are 72 points in 1 inch. Internal
calculations in **pyprototypr** are all done in units i.e. all inputs, regardless of
being inches or centimetres are converted to points.


## The concept of "stroke"

While the majority of size-based properties in **pyprototypr** work with the "normal"
units you have chosen - inches or centimetres - some use points. These include font
height, that you're likely familiar with, and line thickness - termed "stroke width".


## The ""default" concept

A "default", in terms of **pyprototypr**, is a value or setting for something
(usually a *property*) which is used unless you specify otherwise.  This is helpful
in quickly drawing or testing something until you're ready to make decisions about
your own setting or value.

Some examples of defaults are:

* the default *margin* for pages in the output PDF is 1.25cm (or half of 1 inch)
* the default *units* are centimetres (*cm*)
* the default *x* and *y* positions are each 1 (one) - with default units that is 1cm
* the default line *length* is 1 (one) - with default units that is 1cm
* the default line *thickness* is 0.1 - with default units that is 1mm
* the default *line *color* is black  - which is a hexadecimal value of **#000000**
* the default *fill color* is white - which is a hexadecimal value of **#FFFFFF**
* the default *font* is Arial, with a size (height) of 12 points and the color black
