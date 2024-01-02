from collections import namedtuple
from enum import Enum
from math import sqrt


'''
'Operator Overloads'
'''
Point = lambda x,y : namedtuple('Point', 'x y')(int(x),int(y))
Line = lambda p1, p2 : namedtuple('Line', 'p1, p2')(p1, p2)
Len = lambda L : int(sqrt((L.p1.x - L.p2.x)**2 + (L.p1.y - L.p2.y)**2))


#WARNING: keep these enums aligned with the enum Piece as degined in remote_call/game.proto
Piece = Enum('Piece', ['N', 'X', 'O'])

squares = [c+r for c in ['a', 'b', 'c'] for r in ['1', '2', '3']]
Square = Enum('Squares', 
  [bs + ss for bs in squares + ['xx'] for ss in squares]
)

Move = namedtuple('Move', 'piece square')
PlayState = Enum('PlayState', ['IN_PLAY', 'X_WON', 'O_WON', 'TIE'])
GameState = namedtuple('GameState', 'board play_state')