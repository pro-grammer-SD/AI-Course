import os
import chess
import chess.svg
import cairosvg
from PIL import Image
from modules.sf import gbm
print(gbm())

board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

svg = chess.svg.board(
    board,
     arrows=[chess.svg.Arrow(chess.E4, chess.F6, color="#0000cccc")],
    size=350
)

output_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(output_dir, "board.png")
cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=output_path)

img = Image.open(output_path)
img.show()
