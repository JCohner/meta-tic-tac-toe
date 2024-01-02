from __future__ import print_function

import logging

import grpc
from remote_calls.game_pb2_grpc import PiecePlacerStub
from remote_calls.game_pb2 import PlayerChoice

from tictac.helpers import Piece

def run():
  with grpc.insecure_channel('localhost:50051') as channel:
    stub = PiecePlacerStub(channel)
    # using ints to keep enums aligned... maybe not great
    response = stub.ChooseSquare(PlayerChoice(piece=Piece.X.value, square="b2b2"))
    print("Client received: " + response.message)

if __name__ == "__main__":
  logging.basicConfig()
  run()