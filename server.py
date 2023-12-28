from concurrent import futures
import logging
import queue
import threading
import signal
import time

import grpc

from remote_calls.game_pb2_grpc import PiecePlacerServicer, add_PiecePlacerServicer_to_server
from remote_calls.game_pb2 import Reply, PlayerChoice

class PiecePlacer(PiecePlacerServicer):
  def __init__(self, cond_var = threading.Condition()):
    self.place_request_queue = queue.Queue(maxsize = 81) # queue of player choices
    self.cv = cond_var

    self.do_work = False
    self.thread_pool = futures.ThreadPoolExecutor(max_workers=10)
    self.work_thread = threading.Thread(target=self.serve)

  def ChooseSquare(self, request, context):
    self.place_request_queue.put(request)
    with self.cv:
      self.cv.notify()
    return Reply(message=f"Player {str(request.piece)} requested place on square {request.square}")

  def serve(self):
      port = "50051"
      self.server = grpc.server(self.thread_pool)
      add_PiecePlacerServicer_to_server(self, self.server)
      self.server.add_insecure_port("[::]:" + port)
      self.server.start()
      print("Server started, listening on " + port)
      self.server.wait_for_termination()
      print("exitted")

  def start_work(self):
    if (self.do_work is False):
      self.do_work = True
      self.work_thread.start()
    else:
      print("WARNING: already doing work")
      return
  
  def stop_work(self, *args):
    if (self.do_work is True):
      self.do_work = False
      self.work_thread.join()
    else:
      print("WARNING: not doing any work, meaningless call")
      return

if __name__ == "__main__":
    logging.basicConfig()
    p = PiecePlacer()
    p.serve()
    while(True):
      time.sleep(5)
    # p.start_work()

