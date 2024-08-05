echo "Creating PDFs for all examples (except those in examples/manual)"
echo ""
# -- examples: simple
echo "Creating simple examples..."
python examples/simple/basic.py
python examples/simple/cards.py
python examples/simple/card_design.py
python examples/simple/card_images.py
python examples/simple/diagram.py
python examples/simple/default_shapes.py
python examples/simple/customised_shapes.py
python examples/simple/grid_shapes.py
python examples/simple/track_shapes.py
python examples/simple/hexagons.py
# -- boards: abstract
echo "Creating abstract boards..."
python examples/boards/abstract/chessboard.py
python examples/boards/abstract/chessboard_brown.py
python examples/boards/abstract/hex_game.py
python examples/boards/abstract/hexhex.py
python examples/boards/abstract/hexhex_circles.py
python examples/boards/abstract/hexhex_dots.py
# python examples/boards/abstract/
# -- boards: commercial
echo "Creating commercial boards..."
python examples/boards/commercial/hex_game.py
python examples/boards/commercial/orion_game_board.py
python examples/boards/commercial/squadleader.py
python examples/boards/commercial/traveller_draft.py
python examples/boards/commercial/traveller_black.py
python examples/boards/commercial/warpwar.py
# -- counters
echo "Creating counters..."
python examples/counters/counters.py
python examples/counters/counters_excel.py
python examples/counters/counters_csv.py
# -- Board Game Geek
echo "Creating BGG game sheet..."
python examples/bgg/example01.py

echo "Done!"
