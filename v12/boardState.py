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

		if options == 'midGame':
			self.fullGame = 2
			self.numPieces = 6
			self.height = 11
			self.starting = 3
			self.midElement = 5

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
		## determine the last piece position
		self.PositionOneLastElement = self.height
		for (i,j) in self.PositionOne:
			if i < self.PositionOneLastElement:
				self.PositionOneLastElement = i
		self.PositionTwoLastElement = 0
		for (i,j) in self.PositionTwo:
			if i > self.PositionTwoLastElement:
				self.PositionTwoLastElement = i
		
		## determine the first piece position
		self.PositionOneFirstElement = 0
		for (i,j) in self.PositionOne:
			if i > self.PositionOneFirstElement:
				self.PositionOneFirstElement = i
		self.PositionTwoFirstElement = self.height
		for (i,j) in self.PositionTwo:
			if i < self.PositionTwoFirstElement:
				self.PositionTwoFirstElement = i

		self.allPosition = self.PositionOne + self.PositionTwo
	
	'''
	Public
	to check whether this is already a BattleField
    '''
	def isBattleField(self, k = 2):
		if self.PositionOneFirstElement >= self.PositionTwoFirstElement - k:
			return True
		return False


	'''
	Public
	to check whether this is already an endgame
    '''
	def isEndGame(self, k = 0):
		if self.PositionTwoLastElement <= self.PositionOneLastElement - k:
			return True
		return False

	'''
	Public
	to check whether two boards are the same
    '''
	def __eq__(self, other):
		if np.array_equal(self.board, other.board):
			return True
		return False

	'''
	Public
	print the current board
    '''
	def printBoard(self):
		for i in range(self.height):
			# if i < 10: 
			# 	print str(i) + " ",
			# else:
			# 	print i,
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
		# print "  ",
		# for j in range(self.mid_width_max):
		# 	print j%10,
		print "\n"
	
	'''
	Public
	check if the game has ended
    '''
	def isEnd(self):
		if self.isEndTwo():
			return 2
		if self.isEndOne():
			return 1
		return 0

	'''
	Private
	check if player two has won
    '''
	def isEndTwo(self):
		endPieceOne = 0
		for i in range(self.starting):
			numPiece = min(self.height - i, i - (-1))
			for j in range(self.midElement - numPiece+1, self.midElement+numPiece, 2):
				if self.board[i][j] == 0:
					return 0
				if self.board[i][j] == 1:
					endPieceOne += 1
				if self.board[i][j] == 2:
					endPieceOne += 2
		if endPieceOne > self.numPieces:
			return 1
		if endPieceOne == self.numPieces:
			return 0
	
	'''
	Private
	check if player one has won
    '''
	def isEndOne(self):
		endPieceTwo = 0
		for i in range(self.height - self.starting, self.height):
			numPiece = min(self.height - i, i - (-1))
			for j in range(self.midElement - numPiece+1, self.midElement+numPiece, 2):
					if self.board[i][j] == 0:
						return 0
					if self.board[i][j] == 1:
						endPieceTwo += 2
					if self.board[i][j] == 2:
						endPieceTwo += 1
		if endPieceTwo > self.numPieces:
			return 1
		if endPieceTwo == self.numPieces:
			return 0
	'''
	Public Method
	Go! 
	Given current board, move piece from original to next position, create new board without changing the original board
    '''
	def takeMove(self, move):
		newBoard = copy.deepcopy(self.board)
		newBoard[move[2]][move[3]] = newBoard[move[0]][move[1]]
		newBoard[move[0]][move[1]] = 0
		if self.fullGame == 1:
			newBoardState = boardState(options = 'fullGame', inputBoard = newBoard)
		else:
			newBoardState = boardState(options = 'smallGame', inputBoard = newBoard)
		return newBoardState


       