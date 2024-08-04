rm /home/derek/miniconda3/envs/proto/lib/python3.11/site-packages/pyprototypr*.egg
rm -rf build
rm -rf dist
python setup.py install
echo ""
python examples/simple/basic.py
python examples/simple/default_shapes.py
python examples/simple/customised_shapes.py
python examples/simple/grid_shapes.py
python examples/simple/track_shapes.py
python examples/simple/hexagons.py
