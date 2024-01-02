from __future__ import print_function

import logging

import argparse

import grpc
from remote_calls.game_pb2_grpc import PiecePlacerStub
from remote_calls.game_pb2 import PlayerChoice

from tictac.helpers import Piece, Square

def run():
  # arg parse and validation
  parser = argparse.ArgumentParser(
                    prog='tictactoe client',
                    description='allows users to specify the piece and square to place',
                    epilog="I hope you're having as much fun as me")


  parser.add_argument("-s", "--square", help="square to place piece", type=str)
  parser.add_argument("-p", "--piece", help="X or O", type=str)

  args = parser.parse_args()
  piece = args.piece 
  if ((piece.lower() != 'x') and (piece.lower() != 'o')):
    logging.error(f"Cmon bozo you need to specify the piece as X or O. Your answer: {piece} doesnt cut it")
    return
  valid_piece = Piece.X if piece.lower() == 'x' else Piece.O

  valid_squares = [s.name for s in Square]
  square = args.square
  if (square not in valid_squares):
    logging.error(f"Bozo! you gotta input a valid square.")
    return
  valid_square = square.lower()

  with grpc.insecure_channel('localhost:50051') as channel:
    stub = PiecePlacerStub(channel)
    # using ints to keep enums aligned... maybe not great
    response = stub.ChooseSquare(PlayerChoice(piece=valid_piece.value, square=valid_square))
    print("Client received: " + response.message)

if __name__ == "__main__":
  logging.basicConfig()
  run()