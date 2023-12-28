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
    self.canvas.pack(anchor=tk.CENTER, expand=True)
    self.root.mainloop()

  def generate_board(self, center, size):
    self.canvas.create_oval((center.x - 10, center.y -10 ), (center.x +10, center.y + 10))
    l1 = Line(Point(center.x - size / 4, center.y - size / 2), Point(center.x - size / 4, center.y + size / 2))
    l2 = Line(Point(center.x + size / 4, center.y - size / 2), Point(center.x + size / 4, center.y + size / 2))
    l3 = Line(Point(center.x - size / 2, center.y - size / 4), Point(center.x + size / 2, center.y - size / 4))
    l4 = Line(Point(center.x - size / 2, center.y + size / 4), Point(center.x + size / 2, center.y + size / 4))

    lines = [l1,l2,l3,l4]
    for l in lines:
      print(f"line at points: {l}")

    self.canvas.create_line(l1.p1, l1.p2, width = 4, fill = 'black')
    self.canvas.create_line(l2.p1, l2.p2, width = 4, fill = 'black')

    self.canvas.create_line(l3.p1, l3.p2, width = 4, fill = 'black')
    self.canvas.create_line(l4.p1, l4.p2, width = 4, fill = 'black')


if __name__ == "__main__":
  Board()