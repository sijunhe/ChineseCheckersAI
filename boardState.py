import numpy as np
import copy

'''
Class: boardState
Represents the current board boardState
@author: Sijun He
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
		#number of features
		self.numFeature = 7
		self.weights = np.ones((self.numFeature,1))
		self.myPosition = []
		self.opponentPosition = []
		if options == 'smallGame':
			self.numPieces = 3
			self.height = 7
			self.starting = 2
			midElement = 3
			
		if options == 'fullGame':
			self.numPieces = 10
			self.height = 17
			self.starting = 4
			midElement = 8

		
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
				for j in range(midElement - numPiece+1, midElement+numPiece, 2):
					if i < self.starting:
						self.board[i, j] = 1
						self.myPosition.append((i,j))

					elif i >= self.height - self.starting:
						self.board[i, j] = 2
						self.opponentPosition.append((i,j))
					else:
						self.board[i, j] = 0	
		## initialize with input board
		else:
			self.board = inputBoard

				
	'''
	print the current board
    '''
	def printBoard(self):
		for i in range(self.height):
			for j in range(self.mid_width_max):
				if self.board[i,j] == 0:
					print "o",
				elif self.board[i,j] == 1:
					print "*",
				elif self.board[i,j] == 2:
					print "x",
				else:
					print " ",
			print "\n"
	

	'''
	check if the game has ended
    '''
	def isEnd():
		print 'TBD'


	'''
	compute the feature values of current board
    '''
	def computeFeature():
		self.features = np.zeros(self.weights.shape)
		### Compute every feature

	'''
	recursively compute the minimax tree
	returns a board
    '''
	def computeMiniMax(depth):
		print 'TBD'


	'''
	recursively compute board value according to the weights and feature value
	called by computeMiniMax for the leaves of the tree
	returns a double
    '''
	def computeFuncApprox():
		print 'TBD'


	def computeLegalMove(self):
		possibleMoveBoard = []
		for (i, j) in self.myPosition:
			## current piece x and y position
			rollMoves = self.findLegalRoll(i,j)
			for (nexti, nextj) in rollMoves:
				futureBoard = copy.deepcopy(self.board)
				futureBoard[i][j] = 0
				futureBoard[nexti][nextj] = 1	
				possibleMoveBoard.append(boardState(options = 'smallGame', inputBoard = futureBoard))

			for (basei, basej) in self.myPosition:
				hopMove= self.findLegalHop(i, j, basei, basej)
				if hopMove is not None:
					(nexti, nextj) = hopMove
					futureBoard = copy.deepcopy(self.board)
					futureBoard[i][j] = 0
					futureBoard[nexti][nextj] = 1	
					possibleMoveBoard.append(boardState(options = 'smallGame', inputBoard = futureBoard))

		return possibleMoveBoard

	'''
	Find a legal roll moves, given the cooridnate of a piece
    '''	
	def findLegalRoll(self, i, j):
		rollMoves = []
		if i + 1 < self.height:
			if j + 1 < self.mid_width_max:
			## can go down right? 
				if self.board[i+1][j+1] == 0:
					rollMoves.append((i+1, j+1))

			if j - 1 >= 0:
				if self.board[i+1][j-1] == 0:
			## can go down left?
					rollMoves.append((i+1, j-1))

		if i - 1 >= 0:
			if j + 1 < self.mid_width_max:
			## can go up right? 
				if self.board[i-1][j+1] == 0:
					rollMoves.append((i-1, j+1))
			if j - 1 >= 0:
				if self.board[i-1][j-1] == 0:
			## can go up left?
					rollMoves.append((i-1, j-1))

		return rollMoves

	'''
	Find a legal hop moves, given the cooridnate of a piece and the base
    '''	
	def findLegalHop(self, hopi, hopj, basei, basej):
		hopMove = None
		if self.isAdjacent(hopi, hopj, basei, basej):
			diffi = basei - hopi
			diffj = basej - hopj
			nexti = basei + diffi
			nextj = basej + diffj
			print nexti, nextj
			if self.board[nexti][nextj] == 0:
				hopMove = (nexti, nextj)
				

		return hopMove;

	'''
	Return if two pieces are next to each other
    '''	
	def isAdjacent(self, Ai, Aj, Bi, Bj):
		if abs(Ai - Bi) == 1:
			if abs(Aj - Bj) == 1:
				return True

		elif abs(Ai - Bi) == 0:
			if abs(Aj - Bj) == 2:
				return True
		else:
			return False
		