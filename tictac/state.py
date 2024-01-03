import logging
from multiprocessing import Process, Queue, Pipe, Value
import time
from collections import namedtuple, Counter
from enum import Enum

from tictac.worker import Worker
from tictac.helpers import *

from pprint import PrettyPrinter
pp = PrettyPrinter(indent = 4)

class State(Worker):
  def __init__(self, board_update_queue=None):
    super().__init__("state")
    self.final_game_state_con_sock,self.final_game_state_recv_sock = Pipe()
    self.board_state = { x : { x: Piece.N for x in squares} for x in ['xx'] + squares }
    self.move_queue = Queue() # queue to hold state updates, elements added to this will be added to board
    self.board_update_queue = board_update_queue

    '''
    Game state variables
    '''
    self.player_turn = SharedEnum(Piece.X)
    self.play_state = SharedEnum(PlayState.IN_PLAY)
    self.active_mini_board = SharedEnum(MiniBoard.N)

  def update_state(self, square, piece):
    # Meta Tic Tac Toe Mechanics
    pass_through_if_main_board = True if (square[:2] == 'xx') else False
    if (not pass_through_if_main_board):
      allowed_miniboard = self.active_mini_board.get_value()
      play_state = self.play_state.get_value()

      # Handle case in which next user click represents mini board selection
      if ((play_state == PlayState.O_MINIBOARD_SELECT) or (play_state == PlayState.X_MINIBOARD_SELECT)):
        logging.info(f"Player {piece} is setting allowed mini board to: {square[:2]}")
        self.active_mini_board.set_value_by_name(square[:2])
        self.play_state.set_value(PlayState.IN_PLAY)
        if (self.board_update_queue != None):
          self.board_update_queue.put(StateUpdate(move = None, 
                                                  play_state = self.play_state.get_value(),
                                                  player_turn = self.player_turn.get_value(),
                                                  active_mini_board = self.active_mini_board.get_value()))
        return False

      # nominal is allowed to play in given miniboard check
      else:
        is_allowed_miniboard = True if (MiniBoard[square[:2]] ==  allowed_miniboard) else False
        is_first_place = True if (self.active_mini_board.get_value() == MiniBoard.N) else False
        if (not is_allowed_miniboard and not is_first_place):
          logging.info(f"Player {piece.name} attempted to play in an invalid square: {square} must play in miniboard: {allowed_miniboard}")
          return False
        is_not_already_played = True if self.board_state[square[:2]][square[2:]] == Piece.N else False
        if (not is_not_already_played):
          logging.error("Cannot play where a piece is already played!")
          return False


    '''
    update self.board_state
    detect if a tic tac toe has been made (update self.board_state['xx'][square]), signal to main
    '''
    self.board_state[square[:2]][square[2:]] = piece

    # check if we need to do stuff for square
    mbs = self.board_state[square[:2]]
    # logging.info(pp.pformat(mbs))
    # pp.pprint(mbs)
    cnt = Counter(mbs.values())
    # check win condition if more than 3 of same piece have been played
    is_won = False
    if (cnt[piece] >= 3):
      is_won = self.check_win(mbs, piece)

    # if the board is one and its not the main board
    if (is_won and square[:2] != 'xx'):
      logging.info(f"Player {piece} won board {square[:2]}")
      # mark on board
      if (self.board_update_queue != None):
        self.board_update_queue.put(StateUpdate(move = Move(piece=piece, square=f"xx{square[:2]}"), 
                                                play_state = None,
                                                player_turn = None,
                                                active_mini_board = None))

      # now check big board:
      self.update_state(f'xx{square[:2]}', piece)

    elif(is_won):
      self.play_state.set_value(PlayState.X_WON if (piece == Piece.X) else PlayState.O_WON)
      print(f"GAME OVER NICE JOB: {piece}")

    # toggle player state # TODO (i think we may want to nest this in if not passthrough)
    
    # increment logic not to be done by main board state update
    if (not pass_through_if_main_board):
      self.player_turn.set_value(Piece.X if self.player_turn.get_value() == Piece.O else Piece.O)
      self.increment_next_mini_board(piece, square)
      print(f"PlayState is: {self.play_state.get_value()}\nNext playable board is: {self.active_mini_board.get_value()}")

    return True

  def increment_next_mini_board(self, piece, square):
    current_inner_square = square[2:]
    # check if destination board is not won
    if self.board_state['xx'][current_inner_square] == Piece.N:
      self.active_mini_board.set_value_by_name(current_inner_square)
    else:
      print("Sending opponent to already won board waiting for mini board selection")
      self.play_state.set_value(PlayState.X_MINIBOARD_SELECT if (piece == Piece.X) else PlayState.O_MINIBOARD_SELECT)
      self.active_mini_board.set_value(MiniBoard.N)

  def check_win(self, mbs, piece):
    win_cons = [
      (mbs['a2'] == mbs['b2'] == mbs['c2'] == piece), # win_con_2
      (mbs['b1'] == mbs['b2'] == mbs['b3'] == piece), # win_con_5
      (mbs['a1'] == mbs['b2'] == mbs['c3'] == piece), # win_con_7
      (mbs['a3'] == mbs['b2'] == mbs['c1'] == piece), # win_con_8
      (mbs['a1'] == mbs['a2'] == mbs['a3'] == piece), # win_con_4
      (mbs['c1'] == mbs['c2'] == mbs['c3'] == piece), # win_con_6
      (mbs['a1'] == mbs['b1'] == mbs['c1'] == piece), # win_con_1
      (mbs['a3'] == mbs['b3'] == mbs['c3'] == piece), # win_con_5
    ]
    return any(win_cons)

  def work_func(self):
    while(self.do_work.value):
      #TODO(josh): choose first player
      while (self.move_queue.qsize() == 0 and self.do_work.value):
        time.sleep(1/120)
      if (self.do_work.value):
        move = self.move_queue.get()
        valid_update = self.update_state(move.square, move.piece)
        if (self.board_update_queue != None and valid_update):
          update = StateUpdate(move = move, 
                               play_state = self.play_state.get_value(),
                               player_turn = self.player_turn.get_value(),
                               active_mini_board = self.active_mini_board.get_value())
          self.board_update_queue.put(update)
        
    # publish final game state
    self.final_game_state_con_sock.send(GameState(board=self.board_state, play_state=self.play_state.get_value()))
    self.final_game_state_con_sock.close()
    logging.info(f"Work thread: {self.work_proc.pid} exit")

  def enqueue_move(self, move):
    if move.square not in valid_squares:
      raise ValueError(f"Must be a valid square")
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