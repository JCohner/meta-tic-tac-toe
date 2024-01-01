import logging
import time

from pprint import PrettyPrinter

from tictac.state import State, Move, Piece, GameState, PlayState

pp = PrettyPrinter(indent=4)

class TestState:
  def test_mini_board_win(self):
    # logging.getLogger().addHandler(logging.StreamHandler())
    s = State()
    s.start_work()
    s.enqueue_move(Move('a1a1', Piece.X))
    s.enqueue_move(Move('a1a2', Piece.X))
    s.enqueue_move(Move('a1a3', Piece.X))
    time.sleep(1/100)
    s.stop_work()
    assert s.get_final_state().board['xx']['a1'] == Piece.X

  def test_mini_board_win_2(self):
    s = State()
    s.start_work()
    s.enqueue_move(Move('c3a1', Piece.X))
    s.enqueue_move(Move('c3b2', Piece.X))
    s.enqueue_move(Move('c3c3', Piece.X))
    time.sleep(1/100)
    s.stop_work()
    assert s.get_final_state().board['xx']['c3'] == Piece.X

  def test_big_board_win(self):
    s = State()
    s.start_work()
    s.enqueue_move(Move('c3a1', Piece.X))
    s.enqueue_move(Move('c3b2', Piece.X))
    s.enqueue_move(Move('c3c3', Piece.X))

    s.enqueue_move(Move('c2a1', Piece.X))
    s.enqueue_move(Move('c2b2', Piece.X))
    s.enqueue_move(Move('c2c3', Piece.X))

    s.enqueue_move(Move('c1a1', Piece.X))
    s.enqueue_move(Move('c1b2', Piece.X))
    s.enqueue_move(Move('c1c3', Piece.X))

    time.sleep(1/100)
    s.stop_work()

    game_state = s.get_final_state()

    print(f"final state {game_state.play_state}")

    assert game_state.board['xx']['c3'] == Piece.X
    assert game_state.board['xx']['c2'] == Piece.X
    assert game_state.board['xx']['c1'] == Piece.X
    assert game_state.play_state == PlayState.X_WON