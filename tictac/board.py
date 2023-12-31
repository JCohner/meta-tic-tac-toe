import tkinter as tk
from collections import namedtuple
from enum import Enum
from math import sqrt
import time
from multiprocessing import Process, Lock
import threading
import logging

from pprint import PrettyPrinter, pformat
pp = PrettyPrinter(indent=4)

'''
'Operator Overloads'
'''
Point = lambda x,y : namedtuple('Point', 'x y')(int(x),int(y))
Line = lambda p1, p2 : namedtuple('Line', 'p1, p2')(p1, p2)
Len = lambda L : int(sqrt((L.p1.x - L.p2.x)**2 + (L.p1.y - L.p2.y)**2))


Piece = Enum('Piece', ['N', 'X', 'O'])
squares = [c+r for c in ['a', 'b', 'c'] for r in ['1', '2', '3']]
Square = Enum('Squares', 
  [bs + ss for bs in squares + ['xx'] for ss in squares]
)

class Board():
  def __init__(self):
    self.lock = threading.Lock()
    self.ev = threading.Event()
    self.do_work = False
    self.work_thread = Process(target=self.work_func, name="Board")

    self.root = tk.Tk()
    self.SIZE = 800
    self.CENTER = Point(self.SIZE/2, self.SIZE/2)

    self.lines = {}
    self.centers = {}

    self.canvas = tk.Canvas(self.root, width = self.SIZE, height = self.SIZE, bg='white')
    self.generate_board(self.CENTER, 700, "xx")
    self.generate_inner_boards(700)
    logging.debug(pformat(self.lines))

    self.generate_centers()
    logging.debug(pformat(self.centers))

    self.canvas.pack(anchor=tk.CENTER, expand=True)
    self.root.bind("<Button-1>", self.click_handler)

    self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

  def work_func(self):
    self.root.mainloop()

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
      self.on_closing()
    else:
      print("WARNING: not doing any work, meaningless call")
      return

  def on_closing(self):
    self.root.quit()
    self.root.destroy()

  def generate_inner_boards(self, size):
    # accounts for padding away from wall
    offset = (self.SIZE - size) / 2 + size/6

    self.generate_board(Point(offset, offset), 200, 'a1')
    self.generate_board(Point(self.CENTER.x, offset), 200, 'b1')
    self.generate_board(Point(self.SIZE - offset, offset), 200, 'c1')


    self.generate_board(Point(offset, self.CENTER.y ), 200, 'a2')
    self.generate_board(Point(self.CENTER.x, self.CENTER.y), 200, 'b2')
    self.generate_board(Point(self.SIZE - offset, self.CENTER.y), 200, 'c2')

    self.generate_board(Point(offset, self.SIZE - offset), 200, 'a3')
    self.generate_board(Point(self.CENTER.x, self.SIZE - offset), 200, 'b3')
    self.generate_board(Point(self.SIZE - offset, self.SIZE - offset), 200, 'c3')

  def generate_board(self, center, size, name):
    l_mod = 6
    s_mod = 2
    c_mod = 70
    w_mod = 175

    self.canvas.create_oval((center.x - size / c_mod, center.y -size / c_mod ), (center.x +size / c_mod, center.y + size / c_mod))
    v1 = Line(Point(center.x - size / l_mod, center.y - size / s_mod), Point(center.x - size / l_mod, center.y + size / s_mod))
    v2 = Line(Point(center.x + size / l_mod, center.y - size / s_mod), Point(center.x + size / l_mod, center.y + size / s_mod))
    h1 = Line(Point(center.x - size / s_mod, center.y - size / l_mod), Point(center.x + size / s_mod, center.y - size / l_mod))
    h2 = Line(Point(center.x - size / s_mod, center.y + size / l_mod), Point(center.x + size / s_mod, center.y + size / l_mod))

    lines = {
      'v1' : v1,
      'v2' : v2,
      'h1' : h1,
      'h2' : h2,
    }

    self.lines[name] = lines

    self.canvas.create_line(v1.p1, v1.p2, width = size / w_mod, fill = 'black')
    self.canvas.create_line(v2.p1, v2.p2, width = size / w_mod, fill = 'black')

    self.canvas.create_line(h1.p1, h1.p2, width = size / w_mod, fill = 'black')
    self.canvas.create_line(h2.p1, h2.p2, width = size / w_mod, fill = 'black')

  def get_board(self, event, board):
    # print(f"Checking: {event.x}, {event.y} for board: {board}")
    # pp.pprint(self.lines[board])

    row = None
    column = None

    # switch stuff
    if event.y < self.lines[board]["h1"].p1.y and event.y > self.lines[board]["v1"].p1.y:
      row = "1"
    elif event.y > self.lines[board]["h1"].p1.y and event.y < self.lines[board]["h2"].p1.y:
      row = "2"
    elif event.y > self.lines[board]["h2"].p1.y and event.y < self.lines[board]["v2"].p2.y:
      row = "3"
    else:
      row = "?"

    if event.x < self.lines[board]["v1"].p1.x and event.x > self.lines[board]["h1"].p1.x:
      column = "a"
    elif event.x > self.lines[board]["v1"].p1.x and event.x < self.lines[board]["v2"].p1.x:
      column = "b"
    elif event.x > self.lines[board]["v2"].p1.x and event.x < self.lines[board]["h2"].p2.x:
      column = "c"
    else:
      column = "?"

    return column + row

  def generate_centers(self):
    for key, item in self.lines.items():
      temp_d = {}
      offset_to_center = Point(x = 1/6 * Len(self.lines[key]['h1']), 
                               y = 1/6 * Len(self.lines[key]['v1']))
      for i, l in zip(['1','2','3'], [1, 3, 5]):
        for j, k in zip(['a','b','c'], [1, 3, 5]):
          p = Point(x = self.lines[key]['h1'].p1.x + k * offset_to_center.x, 
                    y = self.lines[key]['v1'].p1.y + l * offset_to_center.y)
          temp_d[j+i] = p
          # if key != "xx":
          #   self.canvas.create_text(*p, text = key+j+i)
      self.centers[key] = temp_d

  def generate_shape(self, shape, square):
    p = self.centers[square[:2]][square[2:]]
    size_mod = Len(self.lines[square[:2]]['h1']) * 1/4
    corners = (p.x - size_mod/2, p.y - size_mod/2), (p.x + size_mod/2, p.y + size_mod/2)
    other_corners = (p.x - size_mod/2, p.y + size_mod/2), (p.x + size_mod/2, p.y - size_mod/2)
    if (shape == Piece.O):
      self.canvas.create_oval(*corners, outline='red', width = 4)
    elif (shape == Piece.X):
      self.canvas.create_line(*corners, width = 4, fill = 'red')
      self.canvas.create_line(*other_corners, width = 4, fill = 'red')
    else:
      # throw err
      pass

  def click_handler(self, event):
    click_point = Point(event.x, event.y)
    mini_board = self.get_board(click_point, "xx")
    square = self.get_board(click_point, mini_board)
    print(mini_board + square)
    self.generate_shape(Piece.X, mini_board + square)

if __name__ == "__main__":
  logging.basicConfig(filename='logs/board.log', encoding='utf-8', level=logging.DEBUG)
  logging.getLogger().addHandler(logging.StreamHandler())
  b = Board()