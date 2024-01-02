import signal
import threading
from multiprocessing import Process, Queue
import time
import logging
import os

from tictac.server import PiecePlacer
from tictac.board import Board
from tictac.state import State
from tictac.worker import Worker 
from tictac.helpers import Move, Piece

class MetaTicTacToe(Worker):
  def __init__(self):
    super().__init__("main")
    self.keep_alive = True

    self.move_queue = Queue()

    # spawn board
    self.board = Board(self.move_queue)

    #start server
    self.peice_place_cv = threading.Condition()
    self.piece_place_server = PiecePlacer(self.peice_place_cv )

    self.state = State(self.move_queue)

  def work_func(self):
    while(self.do_work.value):
      with self.peice_place_cv:
        self.peice_place_cv.wait(timeout = 1)
        req = self.piece_place_server.place_request_queue.get()
        move = Move(Piece(req.piece), req.square)
        self.state.enqueue_move(move)

    print("exit")

  def begin(self):
      self.board.start_work()
      self.piece_place_server.start_work()
      self.state.start_work()
      self.start_work()


  def kill(self, *args):
    self.piece_place_server.stop_work()
    self.board.stop_work()
    self.state.stop_work()
    self.stop_work()

    self.keep_alive = False

if __name__ == "__main__":
  logging.basicConfig(filename='logs/main.log', encoding='utf-8', level=logging.INFO)
  logging.getLogger().addHandler(logging.StreamHandler())
  m = MetaTicTacToe()
  signal.signal(signal.SIGINT, m.kill)
  m.begin()
  print(f"main thread: {os.getpid()}")
  while (m.keep_alive):
    time.sleep(1)