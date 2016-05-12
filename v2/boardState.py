import numpy as np
import copy
'''
Class: boardState
Represents the current board boardState
'''
class boardState:

	## Small Game           Full Game
	## depth = 7           depth = 17
	## starting = 2        starting = 4
	## mid_length = 4      mid_length = 9

	'''
	Constructor for a small or a full game
	default is small game
	'''
	def __init__(self, options = 'smallGame', inputBoard = None):
		self.PositionOne = []
		self.PositionTwo = []
		
		if options == 'smallGame':
			self.fullGame = 0
			self.numPieces = 3
			self.height = 7
			self.starting = 2
			self.midElement = 3
			
		if options == 'fullGame':
			self.fullGame = 1
			self.numPieces = 10
			self.height = 17
			self.starting = 4
			self.midElement = 8

		
		self.mid_width = (self.height + 1) / 2

		## max y coorindate for center line
		## while this is now same as height, will be different if we use the hex board
		self.mid_width_max = self.mid_width * 2 - 1

		## initialize game board
		if inputBoard is None:
			self.board = np.ndarray((self.height, self.mid_width_max), dtype = np.int32)
			self.board.fill(-1)
			for i in range(self.height):
				numPiece = min(self.height - i, i - (-1))
				for j in range(self.midElement - numPiece+1, self.midElement+numPiece, 2):
					if i < self.starting:
						self.board[i, j] = 1
						self.PositionOne.append((i,j))

					elif i >= self.height - self.starting:
						self.board[i, j] = 2
						self.PositionTwo.append((i,j))
					else:
						self.board[i, j] = 0
		## initialize with input board
		else:
			self.board = inputBoard
			for i in range(self.height):
				for j in range(self.mid_width_max):
					if self.board[i,j] == 1:
						self.PositionOne.append((i,j))
					if self.board[i,j] == 2:
						self.PositionTwo.append((i,j))
		self.allPosition = self.PositionOne + self.PositionTwo


	'''
	Public
	print the current board
    '''
	def printBoard(self):
		for i in range(self.height):
			for j in range(self.mid_width_max):
				if self.board[i,j] == 0:
					print "o",
				elif self.board[i,j] == 1:
					print "1",
				elif self.board[i,j] == 2:
					print "2",
				else:
					print " ",
			print "\n"
	

	'''
	Public
	check if the game has ended
    '''
	def isEnd(self):
		my_endPiece = 0
		opponent_endPiece = 0
		for i in range(self.height):
			numPiece = min(self.height - i, i - (-1))	
			for j in range(self.midElement - numPiece+1, self.midElement+numPiece, 2):
				if i < self.starting:
					if self.board[i,j] == 2:
						opponent_endPiece += 1
				elif i >= self.height - self.starting:
					if self.board[i,j] == 1:
						my_endPiece += 1
		if 	(opponent_endPiece == self.numPieces) or (my_endPiece == self.numPieces):
			return True
		else:
			return False

	'''
	Public Method
	Go! 
	Given current board, move piece from original to next position, create new board
    '''
	def takeMove(self, oldi, oldj, newi, newj):
		newBoard = copy.deepcopy(self.board)
		newBoard[oldi][oldj] = 0
		newBoard[newi][newj] = 1
		if self.fullGame == 1:
			newBoardState = boardState(options = 'fullGame', inputBoard = newBoard)
		else:
			newBoardState = boardState(options = 'smallGame', inputBoard = newBoard)
		return newBoardState
       