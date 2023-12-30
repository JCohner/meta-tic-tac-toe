import logging
from multiprocessing import Process, Queue
import time
from collections import namedtuple, Counter
from enum import Enum

from worker import Worker
from board import Piece, squares 

from pprint import PrettyPrinter
pp = PrettyPrinter(indent = 4)

Move = namedtuple('Move', 'piece square')

class State(Worker):
  def __init__(self):
    super().__init__()
    self.board_state = { x : { x: Piece.N for x in squares} for x in ['xx'] + squares }
    self.move_queue = Queue() # queue to hold state updates, elements added to this will be added to board
    self.player_turn = Piece.N # make some mechanism to decide first 


  def toggle_player_state(self):
    if (self.player_turn == Piece.X):
      self.player_turn = Piece.O
    elif (self.player_turn == Piece.O):
      self.player_turn = Piece.X

  def update_state(self, square, piece):
    '''
    update self.board_state
    detect if a tic tac toe has been made (update self.board_state['xx'][square]), signal to main
    '''
    self.board_state[square[:2]][square[2:]] = piece

    # check if we need to do stuff for square
    mbs = self.board_state[square[:2]]
    pp.pprint(mbs)
    cnt = Counter(mbs.values())
    # check win condition if more than 3 of same piece have been played
    is_won = False
    if (cnt[piece] >= 3):
      is_won = self.check_win(mbs)
      print(f"Win result: {is_won}")

    # if the board is one and its not the main board
    if (is_won and square[:2] != 'xx'):
      self.board_state['xx'][square[:2]] = piece
    elif(is_won):
      print(f"GAME OVER NICE JOB: {piece}")


  def check_win(self, mbs):
    win_cons = [
      (mbs['a2'] == mbs['b2'] == mbs['c2']), # win_con_2
      (mbs['b1'] == mbs['b2'] == mbs['b3']), # win_con_5
      (mbs['a1'] == mbs['b2'] == mbs['c3']), # win_con_7
      (mbs['a3'] == mbs['b2'] == mbs['c1']), # win_con_8
      (mbs['a1'] == mbs['a2'] == mbs['a3']), # win_con_4
      (mbs['c1'] == mbs['c2'] == mbs['c3']), # win_con_6
      (mbs['a1'] == mbs['b1'] == mbs['c1']), # win_con_1
      (mbs['a3'] == mbs['b3'] == mbs['c3']), # win_con_5
    ]
    return any(win_cons)

  def work_func(self):
    while(True):
      #TODO(josh): choose first player
      while (self.move_queue.qsize() == 0):
        time.sleep(0.5)
      move = self.move_queue.get() 
      self.update_state(*move)
      self.toggle_player_state()

    logging.info(f"Work thread: {self.work_proc.pid} exit")

  def enqueue_move(self, move):
    self.move_queue.put(move)

if __name__ == "__main__":
  logging.basicConfig(filename='logs/state.log', encoding='utf-8', level=logging.DEBUG)
  logging.getLogger().addHandler(logging.StreamHandler())
  s = State()
  s.start_work()

  s.enqueue_move(Move('a1a1', Piece.X))
  s.enqueue_move(Move('a1a2', Piece.X))
  s.enqueue_move(Move('a1a3', Piece.X))

  s.stop_work()