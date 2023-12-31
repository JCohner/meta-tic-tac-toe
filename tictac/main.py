import signal
import threading
from multiprocessing import Process
import time
import logging

from server import PiecePlacer
from board import Board

class MetaTicTacToe():
  def __init__(self):

    # spawn board
    self.board = Board()

    #start server
    self.peice_place_cv = threading.Condition()
    self.piece_place_server = PiecePlacer(self.peice_place_cv )

    #start workthread
    self.do_work = False
    self.work_thread = Process(target=self.work_func, args=())

  def work_func(self):
    while(self.do_work):
      with self.peice_place_cv:
        self.peice_place_cv.wait(timeout = 1)

    print("exit")

  def start_work(self):
    if (self.do_work is False):
      self.do_work = True
      
      self.board.start_work()
      self.piece_place_server.work_thread.start() # make this start work
      self.work_thread.start()

    else:
      print("WARNING: already doing work")
      return

  def stop_work(self, *args):
    if (self.do_work is True):
      self.do_work = False
      self.piece_place_server.stop_work()
      self.board.stop_work()

    else:
      print("WARNING: not doing any work, meaningless call")
      return

if __name__ == "__main__":
  logging.basicConfig(filename='logs/main.log', encoding='utf-8', level=logging.INFO)
  logging.getLogger().addHandler(logging.StreamHandler())
  m = MetaTicTacToe()
  signal.signal(signal.SIGINT, m.stop_work)
  m.start_work()
