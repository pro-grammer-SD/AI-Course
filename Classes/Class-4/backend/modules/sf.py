import os
from stockfish import Stockfish

base_dir = os.path.dirname(os.path.abspath(__file__))
stockfish_path = os.path.join(base_dir, "..", "bin", "stockfish", "sf.exe")

stockfish = Stockfish(path=os.path.abspath(stockfish_path))

def gbm():
    return stockfish.get_best_move_time(1)
