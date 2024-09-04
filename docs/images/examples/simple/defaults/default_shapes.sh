#!/usr/bin/env bash
# requires: https://imagemagick.org/
# uses: default_shapes-*.png image files created by Save() command from
#       examples/simple/default_shapes.py
# These images are:
#    * 1229 pixels high by 1749 pixels wide
#    * 600 dpi
magick default_shapes-1.png -crop  800x750+50+900 +repage blueprint.png
magick default_shapes-2.png -crop  800x750+50+900 +repage blueprint-sub.png
magick default_shapes-3.png -crop  800x750+50+900 +repage text.png
magick default_shapes-4.png -crop  800x750+50+900 +repage line.png
magick default_shapes-5.png -crop  800x750+50+900 +repage rectangle.png
magick default_shapes-6.png -crop  800x750+50+900 +repage circle.png
magick default_shapes-7.png -crop  800x750+50+900 +repage circle-centre.png
magick default_shapes-8.png -crop  800x750+50+900 +repage hexagon.png
magick default_shapes-9.png -crop  800x750+50+900 +repage hexagon-pointy.png
magick default_shapes-10.png -crop  800x750+50+900 +repage hexagon-centre.png
magick default_shapes-11.png -crop  800x750+50+900 +repage rhombus.png
magick default_shapes-12.png -crop  800x750+50+900 +repage rhombus-centre.png
magick default_shapes-13.png -crop  800x750+50+900 +repage star.png
magick default_shapes-14.png -crop  800x750+50+900 +repage ellipse.png
magick default_shapes-15.png -crop  800x750+50+900 +repage ellipse-centre.png
magick default_shapes-16.png -crop  800x750+50+900 +repage polygon.png
magick default_shapes-17.png -crop  800x750+50+900 +repage arrow.png
magick default_shapes-18.png -crop  800x750+50+900 +repage rightangle.png
magick default_shapes-19.png -crop  800x750+50+900 +repage equiangle.png
magick default_shapes-20.png -crop  800x750+50+900 +repage compass.png
magick default_shapes-21.png -crop  800x750+50+900 +repage hexagons-2x2.png
magick default_shapes-22.png -crop  800x750+50+900 +repage grid.png
magick default_shapes-23.png -crop  800x750+50+900 +repage arc.png
magick default_shapes-24.png -crop  800x750+50+900 +repage bezier.png
magick default_shapes-25.png -crop  800x750+50+900 +repage polyline.png
magick default_shapes-26.png -crop  800x750+50+900 +repage shape.png
magick default_shapes-27.png -crop  800x750+50+900 +repage sector.png
magick default_shapes-28.png -crop  800x750+50+900 +repage sequence.png
magick default_shapes-29.png -crop  800x750+50+900 +repage square.png
magick default_shapes-30.png -crop  800x750+50+900 +repage stadium.png
magick default_shapes-31.png -crop  800x750+50+900 +repage starfield.png
magick default_shapes-32.png -crop  800x750+50+900 +repage dot.png
magick default_shapes-33.png -crop  800x750+50+900 +repage dotgrid.png
magick default_shapes-34.png -crop  800x750+50+900 +repage fill-stroke.png
magick default_shapes-35.png -crop  800x750+50+900 +repage transparency.png
magick default_shapes-36.png -crop  800x750+50+900 +repage track-rectangle.png
magick default_shapes-37.png -crop  800x750+50+900 +repage chord.png
magick default_shapes-38.png -crop  800x750+50+900 +repage circle-radii.png
