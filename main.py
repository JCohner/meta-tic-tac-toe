import signal
import threading
import time

from server import PiecePlacer
from board import Board

class MetaTicTacToe():
  def __init__(self):

    # spawn board
    self.board_thread = threading.Thread(target=Board)

    #start server
    self.peice_place_cv = threading.Condition()
    self.server = PiecePlacer(self.peice_place_cv )

    #start workthread
    self.do_work = False
    self.work_thread = threading.Thread(target=self.work_func, args=())

  def work_func(self):
    while(self.do_work):
      print("we are wokring")
      with self.peice_place_cv:
        self.peice_place_cv.wait()

    print("exit")

  def start_work(self):
    if (self.do_work is False):
      self.do_work = True
      self.board_thread.start()
      self.work_thread.start()
    else:
      print("WARNING: already doing work")
      return

  def stop_work(self, *args):
    print("AHHH")
    if (self.do_work is True):
      self.do_work = False
      self.work_thread.join()
    else:
      print("WARNING: not doing any work, meaningless call")
      return

if __name__ == "__main__":
  m = MetaTicTacToe()
  signal.signal(signal.SIGINT, m.stop_work)
  m.start_work()
  '''
  # I really don't like that his has to be last but we'll leave it forx
  # Something with the ThreadPoolExector does not liked to be spawned within its own thread
  '''
  m.server.serve() 