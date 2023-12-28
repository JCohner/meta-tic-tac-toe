from server import PiecePlacer
from board import Board

class MetaTicTacToe():
  def __init__(self):
    # self.board = Board()
    self.server = PiecePlacer()
    self.server.serve()


if __name__ == "__main__":
  MetaTicTacToe()