import logging
from multiprocessing import Process, Queue, Pipe, Value
import time
from collections import namedtuple, Counter
from enum import Enum

from tictac.worker import Worker
from tictac.helpers import Piece, squares, PlayState, GameState, Move, SharedEnum 

from pprint import PrettyPrinter
pp = PrettyPrinter(indent = 4)

class State(Worker):
  def __init__(self, board_update_queue=None):
    super().__init__("state")
    self.final_game_state_con_sock,self.final_game_state_recv_sock = Pipe()
    self.board_state = { x : { x: Piece.N for x in squares} for x in ['xx'] + squares }
    self.move_queue = Queue() # queue to hold state updates, elements added to this will be added to board
    self.board_update_queue = board_update_queue
    
    # need to make these pythons version of thread safe
    self.player_turn = SharedEnum(Piece.X)
    self.play_state = PlayState.IN_PLAY

  def update_state(self, square, piece):
    '''
    update self.board_state
    detect if a tic tac toe has been made (update self.board_state['xx'][square]), signal to main
    '''
    self.board_state[square[:2]][square[2:]] = piece

    # check if we need to do stuff for square
    mbs = self.board_state[square[:2]]
    logging.info(pp.pformat(mbs))
    # pp.pprint(mbs)
    cnt = Counter(mbs.values())
    # check win condition if more than 3 of same piece have been played
    is_won = False
    if (cnt[piece] >= 3):
      is_won = self.check_win(mbs)

    # if the board is one and its not the main board
    if (is_won and square[:2] != 'xx'):
      logging.info(f"Player {piece} won board {square[:2]}")
      # now check big board:
      self.update_state(f'xx{square[:2]}', piece)

    elif(is_won):
      self.play_state = PlayState.X_WON if (piece == Piece.X) else PlayState.O_WON
      print(f"GAME OVER NICE JOB: {piece}")

    # toggle player state
    print(f"play turn is {self.player_turn.get_value()}")
    self.player_turn.set_value(Piece.X if self.player_turn.get_value() == Piece.O else Piece.O)
    print(f"play turn now is {self.player_turn.get_value()}")


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
    while(self.do_work.value):
      #TODO(josh): choose first player
      while (self.move_queue.qsize() == 0 and self.do_work.value):
        time.sleep(1/120)
      if (self.do_work.value):
        move = self.move_queue.get()
        self.update_state(move.square, move.piece)
        if (self.board_update_queue != None):
          self.board_update_queue.put(move)
        
    # publish final game state
    self.final_game_state_con_sock.send(GameState(board=self.board_state, play_state=self.play_state))
    self.final_game_state_con_sock.close()
    logging.info(f"Work thread: {self.work_proc.pid} exit")

  def enqueue_move(self, move):
    self.move_queue.put(move)

  # this allows the state to automatically determine which piece needs to be placed
  def enqueue_place(self, square):
    print(f"Enqueing move of {self.player_turn.get_value()}")
    self.enqueue_move(Move(piece=self.player_turn.get_value(), square=square))

  def get_final_state(self):
    return self.final_game_state_recv_sock.recv()

if __name__ == "__main__":
  logging.basicConfig(filename='logs/state.log', encoding='utf-8', level=logging.DEBUG)
  logging.getLogger().addHandler(logging.StreamHandler())
  s = State()
  s.start_work()

  s.enqueue_move(Move(square = 'a1a1', piece = Piece.X))
  s.enqueue_move(Move(square = 'a1a2', piece = Piece.X))
  s.enqueue_move(Move(square ='a1a3', piece = Piece.X))

  time.sleep(1/60)
  s.stop_work()

  pp.pprint(s.get_final_state().board)