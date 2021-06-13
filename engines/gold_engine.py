import chess
import random
from strategies import MinimalEngine
from engine_wrapper import EngineWrapper


class GoldEngine(MinimalEngine):
    def search(self, board, *args):
        #print(str(board.legal_moves))
        #print(str(type(board.legal_moves[0])))
        if (board == chess.Board()):
            print("here")
            Nf3 = chess.Move.from_uci("g1f3")
            return Nf3
        return random.choice(list(board.legal_moves))
