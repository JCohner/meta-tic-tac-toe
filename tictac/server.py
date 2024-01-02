from concurrent import futures
import logging
import signal
import time

from multiprocessing import Process, Queue

import grpc

from remote_calls.game_pb2_grpc import PiecePlacerServicer, add_PiecePlacerServicer_to_server
from remote_calls.game_pb2 import Reply, PlayerChoice

from tictac.worker import Worker
from tictac.helpers import Piece, Move

class PiecePlacer(PiecePlacerServicer, Worker):
  def __init__(self):
    self.thread_pool = futures.ThreadPoolExecutor(max_workers=10)
    self.server = grpc.server(self.thread_pool)
    super().__init__("server", lambda: self.server.stop(1))

    self.place_request_queue = Queue(maxsize = 81) # queue of player choices


  def ChooseSquare(self, request, context):
    self.place_request_queue.put(request)
    return Reply(message=f"Player {Piece(request.piece).name} requested place on square {request.square}")

  def work_func(self):
      port = "50051"
      add_PiecePlacerServicer_to_server(self, self.server)
      self.server.add_insecure_port("[::]:" + port)
      self.server.start()
      print("Server started, listening on " + port)
      while(self.do_work.value):
        time.sleep(1)
      print("exitted")

if __name__ == "__main__":
    logging.basicConfig()
    p = PiecePlacer()
    p.start_work()

    time.sleep(5)
    p.stop_work()
