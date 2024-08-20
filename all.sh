echo "Creating PDFs for all examples (except those in examples/manual)"
echo ""
# -- examples: simple
echo "Creating simple examples..."
python examples/simple/cards_design.py -d /tmp
python examples/simple/cards_images.py -d /tmp
python examples/simple/customised_shapes.py -d /tmp
python examples/simple/customised_blueprint.py -d /tmp
python examples/simple/demo.py -d /tmp
python examples/simple/diagram.py -d /tmp
python examples/simple/default_shapes.py -d /tmp
python examples/simple/grid_shapes.py -d /tmp
python examples/simple/hexagons.py -d /tmp
python examples/simple/track_shapes.py -d /tmp
# -- boards: abstract
echo "Creating abstract boards..."
python examples/boards/abstract/chessboard.py -d /tmp
python examples/boards/abstract/chessboard_brown.py -d /tmp
python examples/boards/abstract/hex_game.py -d /tmp
python examples/boards/abstract/hexhex.py -d /tmp
python examples/boards/abstract/hexhex_circles.py -d /tmp
python examples/boards/abstract/hexhex_dots.py -d /tmp
# python examples/boards/abstract/
# -- boards: commercial
echo "Creating commercial boards..."
python examples/boards/commercial/ack_map.py -d /tmp
python examples/boards/commercial/orion_game_board.py -d /tmp
python examples/boards/commercial/squadleader.py -d /tmp
python examples/boards/commercial/traveller_draft.py -d /tmp
python examples/boards/commercial/traveller_black.py -d /tmp
python examples/boards/commercial/warpwar.py -d /tmp
# -- counters
echo "Creating counters..."
python examples/counters/counters.py -d /tmp
python examples/counters/counters_excel.py -d /tmp
python examples/counters/counters_csv.py -d /tmp
python examples/counters/blocks_csv.py -d /tmp
# -- cards
echo "Creating cards..."
python examples/cards/cards_matrix_one.py -d /tmp
python examples/cards/cards_matrix_two.py -d /tmp
python examples/cards/cards_standard.py -d /tmp
# -- various
echo "Creating various..."
python examples/various/chords.py -d /tmp
python examples/various/clock.py -d /tmp
python examples/various/objects.py -d /tmp
python examples/various/world_clocks.py -d /tmp
# -- Board Game Geek
echo "Creating BGG game sheet..."
python examples/bgg/example01.py -d /tmp

echo "Done!"
