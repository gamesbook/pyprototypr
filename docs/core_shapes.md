# pyprototypr: Core Shapes

## Overview

These descriptions of the available shapes assume you are familiar with the concepts,
terms and ideas presented in [Basic Concepts](basic_concepts.md) - especially
*units*, *properties* and *defaults*.

Where possible, basic examples show how a shape would appear on a page when only the
defaults are used.  This means for most cases, *lines* are drawn in black, with a width
of 1mm (0.1cm) and shapes are *filled* with a white color.

To make it easier to see where and how a shape has been drawn, these examples have
been created with a background grid for reference: the values of **x** appear across
the bottom of the grid; those for **y** up along the left side.

## Commonalities

There are some properties that can be set for many of the shapes; example of these
are presented at the end, rather than being repeated across shape.

## Linear Shapes

These shapes are created from a line of some sort; the most basic being a simple line.
They effectively only have 1 dimension.

### Line

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/line.png"></td>
    <td>
    <p>This example shows the shape constructed using the command with all defaults:</p>
    <pre>Line()</pre>
    <p>It has the following properties based on the defaults:
      <ul>
        <li>length of 1cm</li>,
        <li>starts at x-position 1cm and at y-position 1cm</li>,
        <li>heading/default direction is 90&deg; (clockwise from 0&deg; "north").</li>
      </ul>
    </p>
    </td>
  </tr>
</table>

### AutoGrid

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/autogrid.png"></td>
    <td>
    <p>This example shows the shape constructed using the command with all defaults:</p>
    <pre>AutoGrid()</pre>
    <p>This grid is designed to quickly construct a grid that can act as a "backround"
    reference on which other shapes can be drawn and position.  Its unlikely to be used
    for a final drawing!</p>
    <p>It has the following properties based on the defaults:
      <ul>
        <li>grid interval of 1cm</li>,
        <li>starts at x-position 1cm and at y-position 1cm</li>,
        <li>heading/default direction is 90&deg; (clockwise from 0&deg; "north").</li>
      </ul>
    </p>
    </td>
  </tr>
</table>


## Enclosed Shapes

These shapes are created by enclosing an area; the most basic being a simple rectangle.
They effectively have 2 dimensions. The difference between these and linear shapes is
that the area enclosed can be filled with a color; the default fill color is white.

### Rectangle

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/rectangle.png"></td>
    <td>
    <p>This example shows the shape constructed using the command with all defaults:</p>
    <pre>Rectangle()</pre>
    <p>It has the following properties based on the defaults:
      <ul>
        <li>length of 1cm and height of 1cm</li>,
        <li>bottom-left corner at x-position 1cm and at y-position 1cm</li>,
        <li>fill color is white.</li>
      </ul>
    </p>
    </td>
  </tr>
</table>

### Circle

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/circle.png"></td>
    <td>
    <p>This example shows the shape constructed using the command with all defaults:</p>
    <pre>Circle()</pre>
    <p>It has the following properties based on the defaults:
      <ul>
        <li>diameter of 1cm</li>,
        <li>the "bounding" square has a bottom-left corner x-position 1cm and y-position 1cm</li>,
        <li>fill color is white.</li>
      </ul>
    </p>
    </td>
  </tr>
</table>

### Octagon

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/octagon.png"></td>
    <td>
    <p>This example shows the shape constructed using the command with all defaults:</p>
    <pre>Octagon()</pre>
    <p>It has the following properties based on the defaults:
      <ul>
        <li>height and width of 1cm</li>,
        <li>bottom-left "corner" at x-position 1cm and at y-position 1cm</li>,
        <li>fill color is white.</li>
      </ul>
    </p>
    </td>
  </tr>
</table>

### Ellipse

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/ellipse.png"></td>
    <td>
    <p>This example shows the shape constructed using the command with all defaults:</p>
    <pre>Ellipse()</pre>
    <p>It has the following properties based on the defaults:
      <ul>
        <li>starts at x-position 1cm and at y-position 1cm</li>,
        <li>ends at x-position 2cm and at y-position 2cm</li>,
        <li>fill color is white.</li>
      </ul>
    </p>
    </td>
  </tr>
</table>

### Hexagon

Hexagons are a shape widely used in gaming, second only to squares, because of their
ability to create a uniform grid. There is therefore some focus in **pyprototypr** on
being able to set various properties for them that are less applicable to other shapes.

Further information about using hexagons can be found in the section on
[Hexagonal Grids](hexagonal_grids.md).

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/hexagon.png"></td>
    <td>
    <p>This example shows the shape constructed using the command with all defaults:</p>
    <pre>Hexagon()</pre>
    <p>It has the following properties based on the defaults:
      <ul>
        <li>height - from flat edge to flat edge - of 1cm</li>,
        <li>bottom-left "corner" at x-position 1cm and at y-position 1cm; so the
            left-point of the hexagon is at x-position 1cm and the bottom flat edge
            is at y-position 1cm </li>,
        <li>fill color is white.</li>
      </ul>
    </p>
    </td>
  </tr>
</table>

## Other Shapes
