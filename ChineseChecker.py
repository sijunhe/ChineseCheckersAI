from core.boardState import *
from core.strategies import *
import numpy as np 
import copy, time
from Tkinter import Tk, Canvas, Frame, BOTH, Entry, TOP, BOTTOM, END

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
            self.game = boardState(options = 'midGame')
            self.HEIGHT = pieceSize * self.game.height + 2 * margin
            self.WIDTH = pieceSize * self.game.mid_width_max + 2 * margin
        self.possibleMoves = []
        self.cantGo = []
        self.weights = [0.911, 0.140, 0.388]
        self.depth = 2
        self.turn = 1
        self.row, self.col = -1, -1
        self.parent = parent
        self.initUI()
        
        
    def initUI(self):
        
        self.parent.title("Chinese Checkers")
              
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
                
        self.canvas.pack(fill=BOTH, expand = 1)
        self.msgWindow = Entry(self.parent)
        self.msgWindow.insert(0, 'Your Turn')
        self.msgWindow.pack()

        self.canvas.bind("<Button-1>", self.__cell_clicked)


    def __repaint(self):
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


        

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        self.canvas.delete("possible_moves")
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

    def __draw_possible_moves(self, possibleMoves):
        for (newi, newj) in possibleMoves:
            if self.game.board[newi][newj] == 0:
                self.canvas.create_oval(margin + newj * pieceSize + spacing, 
                    margin + newi * pieceSize + spacing, 
                    margin + (newj + 1) * pieceSize - spacing, 
                    margin + (newi + 1) * pieceSize - spacing, 
                    outline="yellow", fill="grey", width=2, tags="possible_moves")

        
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
        
            if (self.row, self.col) not in self.possibleMoves:
                ## draw selected cells
                self.__draw_cursor()    
                
                ## draw possible moves
                if self.row != -1 and self.col != -1:
                    self.oldi = self.row
                    self.oldj = self.col
                    if self.turn == 1:
                        moves = computeLegalMoveSpecify(self.game, 1, self.row, self.col)
                    elif self.turn == 2:
                        moves = computeLegalMoveSpecify(self.game, 2, self.row, self.col)
                    self.possibleMoves = [(newi, newj) for (oldi, oldj, newi, newj) in moves]
                    self.__draw_possible_moves(self.possibleMoves)

            else:
                self.game = self.game.takeMove((self.oldi, self.oldj, self.row, self.col))
                self.__repaint()
                self.row, self.col = -1, -1
                self.possibleMoves = []
                self.turn = 3 - self.turn
                if self.turn == 2:
                    msg = 'Your turn'
                    self.msgWindow.delete(0, END)
                    self.msgWindow.insert(0, msg)
                    move = findMove_Advanced(self.game, self.turn, self.weights, self.depth, self.cantGo)
                    print move
                    self.cantGo.append(move)
                    if (len(self.cantGo) >= 5) :
                        self.cantGo.pop(0)
                    self.game = self.game.takeMove(move)
                    self.__repaint()
                    if self.game.isEnd() == 1:
                        msg = 'You won!'
                    elif self.game.isEnd() == 2:
                        msg = 'You lost!'
                    self.msgWindow.delete(0, END)
                    self.msgWindow.insert(0, msg)
                    self.row, self.col = -1, -1
                    self.possibleMoves = []
                    self.turn = 3 - self.turn
                    
    
def main():
  
    root = Tk()
    ex = ChineseCheckerUI(root, 1)
    root.geometry("%dx%d" % (ex.WIDTH, ex.HEIGHT + 40)) 
    root.mainloop()  


if __name__ == '__main__':
    main()  