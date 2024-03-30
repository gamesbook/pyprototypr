#!/usr/bin/env bash
# updated: 2024-03-29
# input: PDF from examples/simple/default_shapes.py
# requires: https://imagemagick.org/
# uses: .png files created by https://cloudconvert.com/pdf-to-png
#  * 296 pixels high by 420 pixels wide
#  * 600 dpi
magick default_shapes-1.png -crop 200x200+0+220 +repage autogrid.png
magick default_shapes-2.png -crop 200x200+0+220 +repage autogrid-sub.png
magick default_shapes-3.png -crop 200x200+0+220 +repage text.png
magick default_shapes-4.png -crop 200x200+0+220 +repage line.png
magick default_shapes-5.png -crop 200x200+0+220 +repage rectangle.png
magick default_shapes-6.png -crop 200x200+0+220 +repage circle.png
magick default_shapes-7.png -crop 200x200+0+220 +repage circle-centre.png
magick default_shapes-8.png -crop 200x200+0+220 +repage octagon.png
magick default_shapes-9.png -crop 200x200+0+220 +repage octagon-centre.png
magick default_shapes-10.png -crop 200x200+0+220 +repage hexagon.png
magick default_shapes-11.png -crop 200x200+0+220 +repage hexagon-centre.png
magick default_shapes-12.png -crop 200x200+0+220 +repage rhombus.png
magick default_shapes-13.png -crop 200x200+0+220 +repage rhombus-centre.png
magick default_shapes-14.png -crop 200x200+0+220 +repage star.png
magick default_shapes-15.png -crop 200x200+0+220 +repage ellipse.png
magick default_shapes-16.png -crop 200x200+0+220 +repage ellipse-centre.png
magick default_shapes-17.png -crop 200x200+0+220 +repage polygon.png
magick default_shapes-18.png -crop 200x200+0+220 +repage arrow.png
magick default_shapes-19.png -crop 200x200+0+220 +repage rightangle.png
magick default_shapes-20.png -crop 200x200+0+220 +repage compass.png
magick default_shapes-21.png -crop 200x200+0+220 +repage hexagons-2x2.png
# magick default_shapes-22.png -crop 200x200+0+220 +repage hexagons-coords.png
# magick default_shapes-23.png -crop 200x200+0+220 +repage hexagons-caltrops.png
# magick default_shapes-?.png -crop 200x200+0+220 +repage ?.png
magick default_shapes-22.png -crop 200x200+0+220 +repage grid.png
magick default_shapes-23.png -crop 200x200+0+220 +repage arc.png
magick default_shapes-24.png -crop 200x200+0+220 +repage bezier.png
magick default_shapes-25.png -crop 200x200+0+220 +repage polyline.png
magick default_shapes-26.png -crop 200x200+0+220 +repage shape.png
