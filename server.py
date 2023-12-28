from concurrent import futures
import logging

import grpc

from remote_calls.game_pb2_grpc import PiecePlacerServicer, add_PiecePlacerServicer_to_server
from remote_calls.game_pb2 import Reply, PlayerChoice

class PiecePlacer(PiecePlacerServicer):
  def ChooseSquare(self, request, context):
    return Reply(message=f"Player {str(request.piece)} requested place on square {request.square}")

  def serve(self):
      port = "50051"
      self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
      add_PiecePlacerServicer_to_server(PiecePlacer(), self.server)
      self.server.add_insecure_port("[::]:" + port)
      self.server.start()
      print("Server started, listening on " + port)
      self.server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    PiecePlacer().serve()
