echo "Creating PDFs for all examples (except those in examples/manual)"
echo ""
mkdir -p /tmp/demo
# -- examples: simple
echo "Creating simple examples..."
python examples/simple/customised_shapes.py -d /tmp/demo
python examples/simple/customised_blueprint.py -d /tmp/demo
python examples/simple/demo.py -d /tmp/demo
python examples/simple/diagram.py -d /tmp/demo
python examples/simple/default_shapes.py -d /tmp/demo
python examples/simple/grid_shapes.py -d /tmp/demo
python examples/simple/hexagons.py -d /tmp/demo
python examples/simple/track_shapes.py -d /tmp/demo
# -- boards: abstract
echo "Creating abstract boards..."
python examples/boards/abstract/chessboard.py -d /tmp/demo
python examples/boards/abstract/chessboard_brown.py -d /tmp/demo
python examples/boards/abstract/hex_game.py -d /tmp/demo
python examples/boards/abstract/hexhex.py -d /tmp/demo
python examples/boards/abstract/hexhex_circles.py -d /tmp/demo
python examples/boards/abstract/hexhex_dots.py -d /tmp/demo
python examples/boards/abstract/hexhex_hexagons.py -d /tmp/demo
python examples/boards/abstract/hexhex_rectangles.py -d /tmp/demo
# python examples/boards/abstract/
# -- boards: commercial
echo "Creating commercial boards..."
python examples/boards/commercial/ack_map.py -d /tmp/demo
python examples/boards/commercial/orion_game_board.py -d /tmp/demo
python examples/boards/commercial/squadleader.py -d /tmp/demo
python examples/boards/commercial/traveller_draft.py -d /tmp/demo
python examples/boards/commercial/traveller_black.py -d /tmp/demo
python examples/boards/commercial/warpwar.py -d /tmp/demo
# -- counters
echo "Creating counters..."
python examples/counters/counters.py -d /tmp/demo
python examples/counters/counters_excel.py -d /tmp/demo
python examples/counters/counters_csv.py -d /tmp/demo
python examples/counters/blocks_csv.py -d /tmp/demo
# -- cards
echo "Creating cards..."
python examples/cards/cards_design.py -d /tmp/demo
python examples/cards/cards_images.py -d /tmp/demo
python examples/cards/cards_matrix_one.py -d /tmp/demo
python examples/cards/cards_matrix_two.py -d /tmp/demo
python examples/cards/cards_standard.py -d /tmp/demo
# -- various
echo "Creating various..."
python examples/various/chords.py -d /tmp/demo
python examples/various/clock.py -d /tmp/demo
python examples/various/objects.py -d /tmp/demo
python examples/various/world_clocks.py -d /tmp/demo
# -- Board Game Geek
echo "Creating BGG game sheet..."
python examples/bgg/example01.py -d /tmp/demo

echo "Done!"
