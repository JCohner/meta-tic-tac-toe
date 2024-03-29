from collections import namedtuple
from enum import Enum
from math import sqrt

from multiprocessing import Value

'''
'Operator Overloads'
'''
Point = lambda x,y : namedtuple('Point', 'x y')(int(x),int(y))
Line = lambda p1, p2 : namedtuple('Line', 'p1, p2')(p1, p2)
Len = lambda L : int(sqrt((L.p1.x - L.p2.x)**2 + (L.p1.y - L.p2.y)**2))

'''
Enums
'''
#WARNING: keep these enums aligned with the enum Piece as degined in remote_call/game.proto
Piece = Enum('Piece', ['N', 'X', 'O'])

squares = [c+r for c in ['a', 'b', 'c'] for r in ['1', '2', '3']]
MiniBoard = Enum("MiniBoard", 
  [b for b in squares + ['N']]
)

Square = Enum('Squares', 
  [bs + ss for bs in squares + ['xx'] for ss in squares]
)
valid_squares = [s.name for s in Square]

Move = namedtuple('Move', 'piece square')
PlayState = Enum('PlayState', ['IN_PLAY', 
                               'X_MINIBOARD_SELECT',
                               'O_MINIBOARD_SELECT',
                               'X_WON',
                               'O_WON',
                               'TIE'])

# TODO: determine if superfolous
GameState = namedtuple('GameState', 'board play_state')

StateUpdate = namedtuple('StateUpdate', 'move play_state player_turn active_mini_board')

'''
Thread (process) safe helpers 
'''
class SharedEnum():
  def __init__(self, enum):
    self.enum_val = enum
    self.enum_type = type(enum)
    self.__safe_val__ = Value('i', enum.value)

  # return value as its enum type
  def get_value(self):
    with self.__safe_val__.get_lock():
      return self.enum_type(self.__safe_val__.value)

  def set_value(self, enum):
    with self.__safe_val__.get_lock():
      self.__safe_val__.value = enum.value

  def set_value_by_name(self, enum_name):
    with self.__safe_val__.get_lock():
      self.__safe_val__.value = self.enum_type[enum_name].value