import tkinter as tk
from collections import namedtuple

Point = lambda x,y : namedtuple('Point', 'x y')(x,y)
Line = lambda p1, p2 : namedtuple('Line', 'p1, p2')(p1, p2)

class Board():
  def __init__(self):
    self.root = tk.Tk()
    self.SIZE = 800
    self.CENTER = Point(self.SIZE/2, self.SIZE/2)

    self.canvas = tk.Canvas(self.root, width = self.SIZE, height = self.SIZE, bg='white')
    self.generate_board(self.CENTER, 700)
    self.generate_inner_boards(700)
    self.canvas.pack(anchor=tk.CENTER, expand=True)
    self.root.mainloop()

  def generate_inner_boards(self, size):
    # accounts for padding away from wall
    offset = (self.SIZE - size) / 2 + size/6

    self.generate_board(Point(offset, offset), 200)
    self.generate_board(Point(self.CENTER.x, offset), 200)
    self.generate_board(Point(self.SIZE - offset, offset), 200)


    self.generate_board(Point(offset, self.CENTER.y ), 200)
    self.generate_board(Point(self.CENTER.x, self.CENTER.y), 200)
    self.generate_board(Point(self.SIZE - offset, self.CENTER.y), 200)

    self.generate_board(Point(offset, self.SIZE - offset), 200)
    self.generate_board(Point(self.CENTER.x, self.SIZE - offset), 200)
    self.generate_board(Point(self.SIZE - offset, self.SIZE - offset), 200)



  def generate_board(self, center, size):
    l_mod = 6
    s_mod = 2
    c_mod = 70
    w_mod = 175

    self.canvas.create_oval((center.x - size / c_mod, center.y -size / c_mod ), (center.x +size / c_mod, center.y + size / c_mod))
    l1 = Line(Point(center.x - size / l_mod, center.y - size / s_mod), Point(center.x - size / l_mod, center.y + size / s_mod))
    l2 = Line(Point(center.x + size / l_mod, center.y - size / s_mod), Point(center.x + size / l_mod, center.y + size / s_mod))
    l3 = Line(Point(center.x - size / s_mod, center.y - size / l_mod), Point(center.x + size / s_mod, center.y - size / l_mod))
    l4 = Line(Point(center.x - size / s_mod, center.y + size / l_mod), Point(center.x + size / s_mod, center.y + size / l_mod))

    lines = [l1,l2,l3,l4]
    # for l in self.lines:
    #   print(f"line at points: {l}")

    self.canvas.create_line(l1.p1, l1.p2, width = size / w_mod, fill = 'black')
    self.canvas.create_line(l2.p1, l2.p2, width = size / w_mod, fill = 'black')

    self.canvas.create_line(l3.p1, l3.p2, width = size / w_mod, fill = 'black')
    self.canvas.create_line(l4.p1, l4.p2, width = size / w_mod, fill = 'black')


if __name__ == "__main__":
  Board()