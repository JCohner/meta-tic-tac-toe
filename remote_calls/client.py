from __future__ import print_function

import logging

import grpc
from game_pb2_grpc import PiecePlayerStub
from game_pb2 import PlayerChoice

def run():
  with grpc.insecure_channel('localhost:50051') as channel:
    stub = PiecePlayerStub(channel)
    response = stub.ChooseSquare(PlayerChoice(shape='X', square="b2b2"))
    print("Client received: " + response.message)

if __name__ == "__main__":
  logging.basicConfig()
  run()