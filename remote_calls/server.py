from concurrent import futures
import logging

import grpc

from remote_calls.game_pb2_grpc import PiecePlacerServicer, add_PiecePlacerServicer_to_server
from remote_calls.game_pb2 import Reply, PlayerChoice


class PiecePlacer(PiecePlacerServicer):
  def ChooseSquare(self, request, context):
    return Reply(message=f"Player {request.shape} requested place on square {request.square}")

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PiecePlacerServicer_to_server(PiecePlacer(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()
