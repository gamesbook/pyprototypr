# pyprototypr: Core Shapes

## Table of Contents

* [Index of Shapes](#index_shapes)
* [Overview](#overview)
* [Commonalities](#commonalties)
* [Linear Shapes](#linear_shapes)
* [Enclosed Shapes](#enclosed_shapes)
* [Compound Shapes](#compound_shapes)
* [Shapes' Common Properties](#common_properties)


## Alphabetic Index of Shapes <a name="index_shapes"></a>

* [Arc](#arc)
* [Blueprint](#blueprint)
* [Bezier](#bezier)
* [Circle](#circle)
* [Compass](#compass)
* [Chord](#chord)
* [Dot](#dot)
* [Ellipse](#ellipse)
* [Hexagon](#hexagon)
* [Hexagons](#hexagons)
* [Line](#line)
* [Polygon](#polygon)
* [Polyline](#polyline)
* [Rectangle](#rectangle)
* [Square](#square)
* [Stadium](#stadium)
* [Star](#star)
* [](#)


## Overview <a name="overview"></a>

These descriptions of the available shapes assume you are familiar with the concepts,
terms and ideas presented in [Basic Concepts](basic_concepts.md) - especially
*units*, *properties* and *defaults*.  It will also help to at least read through
the section on [Additional Concepts](additional_concepts.md).

Where possible, the basic examples first show how a shape would appear on a page
when **only** the default properties are used.  This means for most cases, that
*lines* are drawn in black, with a stroke width of 1mm (0.1cm) and shapes are
*filled* with a white color. The default length or height in most cases is 1cm.

To make it easier to see where and how a shape has been drawn, these examples have
been created with a background grid (which __pyprototypr__ refers to as a
`Blueprint`) for cross-reference: the values of **x** appear across the lower
edge of the grid (increasing from left to right); those for **y** along the
left side (increasing from bottom to top).  The grid respects the margins that
have been set, although the numbers themselves are drawn inside the margin!

> The graphics for these examples were generated from the scripts in the `examples`
> directory - look at the [default_shapes](../examples/simple/default_shapes.py) and
> [customised_shapes](../examples/simple/customised_shapes.py) files.


## Commonalities <a name="commonalties"></a>

There are some properties that can be set for many of the shapes; examples of
these are presented at the end, rather than being repeated across every shape.


## Linear Shapes <a name="linear_shapes"></a>

These shapes are created from a line of some sort; the most basic being a simple line.
A line effectively has only 1 dimension.

### Line [&#9650;](#index_shapes) <a name="line"></a>

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
        <li>length of 1cm,</li>
        <li>starts at x-position 1cm and at y-position 1cm,</li>
        <li>heading/default direction is 0&deg; (anti-clockwise from 0&deg; "east").</li>
      </ul>
    </p>
    </td>
  </tr>
</table>

### Polyline [&#9650;](#index_shapes) <a name="polyline"></a>

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/polyline.png"></td>
    <td>
    <p>This example shows an example of the shape can be constructed using a series
       of points for the line (<b>Note</b> if the points are <b>not</b> defined,
       then the script will not work and will show an error message):</p>
    <pre>Polyline(points=[(0, 0), (1, 1), (2, 0)])</pre>
    <p>As can be seen from the example; at a minimum, you need to use three points
    to draw a *Polyline*:
      <ul>
        <li>points are supplied in a list of <b>x</b> and <b>y</b> values; each point is
        wrapped with <b>( )</b> brackets, and the whole list is wrapped with
        <b>[ ]</b> brackets</li>
      </ul>
    </p>
    </td>
  </tr>
</table>

### Arc [&#9650;](#index_shapes) <a name="arc"></a>

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/arc.png"></td>
    <td>
    <p>This example shows the shape constructed using the command with all defaults:</p>
    <pre>Arc()</pre>
    <p>It has the following properties based on the defaults:
      <ul>
        <li>starts at x-position 1cm and at y-position 1cm,</li>
        <li>end at x-position 2cm and at y-position 2cm - based on a default length
            of 1cm,</li>
      </ul>
    </p>
    </td>
  </tr>
</table>

### Blueprint [&#9650;](#index_shapes) <a name="blueprint"></a>

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/blueprint.png"></td>
    <td>
    <p>This example shows the shape constructed using the command with all defaults:</p>
    <pre>Blueprint()</pre>
    <p>This command is designed to quickly construct a measured grid that can act as a
    "background" reference on which other shapes can be drawn and positioned; or as a
    "foreground" overlay to verify shape positions.  It's unlikely to be used as part
    of a final drawing!</p>
    <p>It has the following properties based on the defaults:</p>
      <ul>
        <li>grid interval of 1cm,</li>
        <li>starts at x-position 1cm and at y-position 1cm,</li>
      </ul>
    </td>
  </tr>
  <tr>
    <th width="30%">Example #2</th>
    <th>Description</th>
  </tr>
    <td><img src="images/examples/simple/defaults/blueprint-sub.png"></td>
    <td>
      <pre>Blueprint(subdivisions=5, stroke_width=0.8)</pre>
      <p>In this example, the Blueprint shows how additional lines can be added
      between the primary ones; their width is set to a fraction of the normal
      grid lines ("stroke_width").  For this example, the normal grid lines
      <i>stroke_width</i> has been made thicker than usual to help show that
      change.</p>
    </td>
  </tr>
</table>

### Chord [&#9650;](#index_shapes) <a name="chord"></a>

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/chord.png"></td>
    <td>
    <p>This example shows how the shape can be constructed:</p>
    <pre>Chord(shape=Circle(), angle=135, angle1=45)</pre>

    <p>This command will draw a line connecting two points on the circumference of a
    circle.  These points will be defined by the places intersected by two radii
    extending from the centre of the circle.  The radii themselves are not drawn but
    are defined by the angles needed to draw them.  These angles are measured by the
    degrees of clockwise rotation from the horizontal line extending "east" from the
    centre of the circle.</p>

    <p>A Chord does not have defaults that will be allow it to be drawn without any
    properties; in this example the two angle values for the "radii" have been set to
    135&deg; and 45&deg; and a default Circle has been used for the "shape".</p>
    </td>
  </tr>
</table>


## Enclosed Shapes <a name="enclosed_shapes"></a>

These shapes are created by enclosing an area; the most basic being a simple rectangle.
They effectively have 2 dimensions (height and width). The difference between these and
the linear shapes is that the area enclosed by the shape can be filled with a color;
the default fill color is white.

> **pyprototypr** comes with a predefined set of named colors, shown in the
> [colors](../examples/colorset.pdf) document.

### Rectangle [&#9650;](#index_shapes) <a name="rectangle"></a>

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
        <li>length of 1cm and height of 1cm,</li>
        <li>bottom-left corner at x-position 1cm and at y-position 1cm,</li>
        <li>fill color is white.</li>
      </ul>
    </p>
    </td>
  </tr>
</table>

### Square [&#9650;](#index_shapes) <a name="square"></a>

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/square.png"></td>
    <td>
    <p>This example shows the shape constructed using the command with all defaults:</p>
    <pre>Square()</pre>
    <p>It has the following properties based on the defaults:
      <ul>
        <li>length of 1cm and height of 1cm and side of 1cm,</li>
        <li>bottom-left corner at x-position 1cm and at y-position 1cm,</li>
        <li>fill color is white.</li>
      </ul>
    </p>
    <p>A square can be constructing by setting any one of <i>side</i>, <i>height</i>
       or <i>width</i>, as they will all be set equal to each other.
    </td>
  </tr>
</table>

### Circle [&#9650;](#index_shapes) <a name="circle"></a>

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
        <li>diameter of 1cm,</li>
        <li>the "bounding" square has a bottom-left corner at x-position 1cm and
        y-position 1cm,</li>
        <li>fill color is white.</li>
      </ul>
    </p>
    </td>
  </tr>
</table>


### Compass [&#9650;](#index_shapes) <a name="compass"></a>

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/compass.png"></td>
    <td>
    <p>This example shows the shape constructed using the command with all defaults:</p>
    <pre>Compass()</pre>
    <p>It has the following properties based on the defaults:
      <ul>
        <li>diameter of 1cm,</li>
        <li>the "bounding" square has a bottom-left corner x-position 1cm and y-position 1cm,</li>
        <li>fill color is white,</li>
        <li>all eight compass directions are displayed.</li>
      </ul>
    </p>
    </td>
  </tr>
</table>

### Dot [&#9650;](#index_shapes) <a name="dot"></a>

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/dot.png"></td>
    <td>
    <p>This example shows the shape constructed using the command with all defaults:</p>
    <pre>Dot()</pre>
    <p>It has the following properties based on the defaults:
      <ul>
        <li>centered at x-position 1cm and at y-position 1cm,</li>
        <li>is a "circle" with a diamter of 3 points; approximately 1/24th of an inch,
        or 1 millimetre</li>
        <li>stroke and fill color are both black.</li>
      </ul>
    </p>
    </td>
  </tr>
</table>

### Ellipse [&#9650;](#index_shapes) <a name="ellipse"></a>

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
        <li>starts at x-position 1cm and at y-position 1cm,</li>
        <li>ends at x-position 2cm and at y-position 2cm,</li>
        <li>fill color is white.</li>
      </ul>
    </p>
    </td>
  </tr>
</table>

### Polygon [&#9650;](#index_shapes) <a name="polygon"></a>

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/polygon.png"></td>
    <td>
    <p>This example shows the shape constructed using the command with all defaults:</p>
    <pre>Polygon()</pre>
    <p>It has the following properties based on the defaults:
      <ul>
        <li>height of 1cm,</li>
        <li>default number of sides is 6 (a hexagon),</li>
        <li>bottom-left "corner" at x-position 1cm and at y-position 1cm,</li>
        <li>fill color is white.</li>
      </ul>
    </p>
    </td>
  </tr>
</table>

### Stadium [&#9650;](#index_shapes) <a name="stadium"></a>

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/stadium.png"></td>
    <td>
    <p>This example shows the shape constructed using the command with all defaults:</p>
    <pre>Stadium()</pre>
    <p>It has the following properties based on the defaults:
      <ul>
        <li>starts at x-position 1cm and at y-position 1cm,</li>
        <li>ends at x-position 2cm and at y-position 2cm,</li>
        <li>stadium "end" are north/south direction with a radius of 0.5cm
           (half of the rectangle's default width of 1cm)</lsi>
        <li>fill color is white.</li>
      </ul>
    </p>
    </td>
  </tr>
</table>


### Hexagon [&#9650;](#index_shapes) <a name="hexagon"></a>

Hexagons are a shape widely used in gaming, second only to squares, because of
their ability to create a uniform grid with centres of each hexagon being
equidistant from others.

There is therefore some focus in **pyprototypr** on being able to set special
properties for these shapes that are not applicable to others.

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
        <li>height - from flat edge to flat edge - of 1cm,</li>
        <li>bottom-left "corner" at x-position 1cm and at y-position 1cm; so the
            left-point of the hexagon is at x-position 1cm and the bottom flat edge
            is at y-position 1cm ,</li>
        <li>fill color is white.</li>
        <li><i>orientation</i> is flat; the top of the hexagon is parallel to the bottom
            of the page.</li>
      </ul>
    </p>
    </td>
  </tr>
</table>

### Star [&#9650;](#index_shapes) <a name="star"></a>

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/star.png"></td>
    <td>
    <p>This example shows the shape constructed using the command with all defaults:</p>
    <pre>Star()</pre>
    <p>It has the following properties based on the defaults:
      <ul>
        <li>diameter of 1cm,</li>
        <li>the "bounding" square has a bottom-left corner x-position 1cm and y-position 1cm,</li>
        <li>fill color is white,</li>
        <li>there are 5 "arms" for the star.</li>
      </ul>
    </p>
    </td>
  </tr>
</table>


## Compound Shapes <a name="compound_shapes"></a>

These shapes are created by combining a single shape into a multiple, repeated
pattern.

### Hexagons [&#9650;](#index_shapes) <a name="hexagons"></a>

Hexagons are often drawn in a "honeycomb" arrangement to form a grid - for games
this is often used to delineate the spaces in which playing pieces can be placed
and their movement regulated.

> Further information about using hexagons in grids can be found in the section
> on [Hexagonal Grids](hexagonal_grids.md).

<table>
  <tr>
    <th width="30%">Example #1</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="images/examples/simple/defaults/hexagons-2x2.png"></td>
    <td>
    <p>This example shows the shape constructed using the command:</p>
    <pre>Hexagons(rows=2, cols=2)</pre>
    <p>Each hexagon has the usual default properties, but the grid itself also
       has the following defaults:
      <ul>
        <li><i>orientation</i> is flat; the top of the hexagon is parallel to
        the bottom of the page,</li>
      </ul>
    </p>
    </td>
  </tr>
</table>


## Shapes Common Properties <a name="common_properties"></a>