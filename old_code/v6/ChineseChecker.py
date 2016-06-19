from boardState import *
from computeLegalMove import * 
from computeFeatures import *
from computeMinimax import *
import numpy as np 
import copy

from Tkinter import Tk, Canvas, Frame, BOTH

pieceSize = 40
margin = 50
spacing = 5

class ChineseCheckerUI(Frame):
    
    def __init__(self, parent, options = 0):
        Frame.__init__(self, parent)   
        if options == 0:
            self.full = 0
            self.game = boardState(options = 'smallGame')
            self.HEIGHT = pieceSize * self.game.height + 2 * margin
            self.WIDTH = pieceSize * self.game.mid_width_max + 2 * margin
        elif options == 1:
            self.full = 1
            self.game = boardState(options = 'fullGame')
            self.HEIGHT = pieceSize * self.game.height + 2 * margin
            self.WIDTH = pieceSize * self.game.mid_width_max + 2 * margin
        self.row, self.col = -1, -1
        self.parent = parent
        self.initUI()
        
        
    def initUI(self):
        
        self.parent.title("Colours")        
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)
        for i in xrange(self.game.height):
            for j in xrange(self.game.mid_width_max):
                if self.game.board[i][j] == 1:
                    self.canvas.create_oval(margin + j * pieceSize + spacing, 
                        margin + i * pieceSize + spacing, 
                        margin + (j + 1) * pieceSize - spacing, 
                        margin + (i + 1) * pieceSize - spacing, 
                        outline="black", fill="blue", width=2)
                elif self.game.board[i][j] == 2:
                    self.canvas.create_oval(margin + j * pieceSize + spacing, 
                        margin + i * pieceSize + spacing, 
                        margin + (j + 1) * pieceSize - spacing, 
                        margin + (i + 1) * pieceSize - spacing, 
                        outline="black", fill="red", width=2)
                elif self.game.board[i][j] == 0:
                    self.canvas.create_oval(margin + j * pieceSize + spacing, 
                        margin + i * pieceSize + spacing, 
                        margin + (j + 1) * pieceSize - spacing, 
                        margin + (i + 1) * pieceSize - spacing, 
                        outline="black", fill="grey", width=2)
                
        self.canvas.pack(fill=BOTH, expand=1)

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            if self.game.board[self.row][self.col] == 1:
                self.canvas.create_oval(margin + self.col * pieceSize + spacing, 
                    margin + self.row * pieceSize + spacing, 
                    margin + (self.col + 1) * pieceSize - spacing, 
                    margin + (self.row + 1) * pieceSize - spacing, 
                    outline="green", fill="blue", width=2, tags="cursor")
            elif self.game.board[self.row][self.col] == 2:
                self.canvas.create_oval(margin + self.col * pieceSize + spacing, 
                    margin + self.row * pieceSize + spacing, 
                    margin + (self.col + 1) * pieceSize - spacing, 
                    margin + (self.row + 1) * pieceSize - spacing, 
                    outline="green", fill="red", width=2, tags="cursor")
            elif self.game.board[self.row][self.col] == 0:
                self.canvas.create_oval(margin + self.col * pieceSize + spacing, 
                    margin + self.row * pieceSize + spacing, 
                    margin + (self.col + 1) * pieceSize - spacing, 
                    margin + (self.row + 1) * pieceSize - spacing, 
                    outline="green", fill="grey", width=2, tags="cursor")

    def __cell_clicked(self, event):
        x, y = event.x, event.y
        if (margin < x < self.WIDTH - margin and margin < y < self.HEIGHT - margin):
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = (y - margin) / pieceSize, (x - margin) / pieceSize

            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
                #self.__draw_cursor(0)
            elif self.game.board[row][col] != -1:
                self.row, self.col = row, col
            
        self.__draw_cursor()

    
def main():
  
    root = Tk()
    ex = ChineseCheckerUI(root, 1)
    root.geometry("%dx%d" % (ex.WIDTH, ex.HEIGHT + 40))
    root.mainloop()  


if __name__ == '__main__':
    main()  