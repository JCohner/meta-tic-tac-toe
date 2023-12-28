import tkinter as tk
from collections import namedtuple

Point = lambda x,y : namedtuple('Point', 'x y')(x,y) 

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

    self.canvas.create_line((center.x - size / 4, center.y - size / 2), (center.x - size / 4, center.y + size / 2), width = 4, fill = 'black')
    self.canvas.create_line((center.x + size / 4, center.y - size / 2), (center.x + size / 4, center.y + size / 2), width = 4, fill = 'black')

    self.canvas.create_line((center.x - size / 2, center.y - size / 4), (center.x + size / 2, center.y - size / 4), width = 4, fill = 'black')
    self.canvas.create_line((center.x - size / 2, center.y + size / 4), (center.x + size / 2, center.y + size / 4), width = 4, fill = 'black')


if __name__ == "__main__":
  Board()