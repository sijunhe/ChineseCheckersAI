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
	def __init__(self, options = 'smallGame', inputBoard = None, player = 1):
		#number of features
		self.numFeature = 8
		self.weights = np.ones((self.numFeature,1))
		self.myPosition = []
		self.opponentPosition = []
		self.player = player
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
						self.board[i, j] = self.player
						self.myPosition.append((i,j))

					elif i >= self.height - self.starting:
						self.board[i, j] = 3 - self.player
						self.opponentPosition.append((i,j))
					else:
						self.board[i, j] = 0
			self.allPosition = self.myPosition + self.opponentPosition	
		## initialize with input board
		else:
			self.board = inputBoard
			for i in range(self.height):
				for j in range(self.mid_width_max):
					if self.board[i,j] == self.player:
						self.myPosition.append((i,j))
					if self.board[i,j] == (3-self.player):
						self.opponentPosition.append((i,j))
			self.allPosition = self.myPosition + self.opponentPosition
       
		self.features = self.computeFeatures()
		self.scoreRaw = np.dot(self.features.transpose(), self.weights)
		
				
	'''
	Public
	print the current board
    '''
	def printBoard(self):
		for i in range(self.height):
			for j in range(self.mid_width_max):
				if self.board[i,j] == 0:
					print "o",
				elif self.board[i,j] == self.player:
					print self.player,
				elif self.board[i,j] == (3-self.player):
					print 3-self.player,
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
	Public
	compute the feature values of current board
    '''
	def computeFeatures(self):
		features = np.zeros(self.weights.shape)
		### Compute every feature

		# my position - distance to the end
		for (i,j) in self.myPosition:
			features[0] += (self.height - 1 - i)**2
		# opponent positin - distance to the end
		for (i,j) in self.opponentPosition:
			features[1] += i**2

		# my position - distance to the center
		for (i,j) in self.myPosition:
			features[2] += (j-self.midElement)**2
		# opponent positin - distance to the center
		for (i,j) in self.opponentPosition:
			features[3] += (j-self.midElement)**2

		#my position - variance of pieces distribution
		for (i,j) in self.myPosition:
			for (k,l) in self.myPosition:
					features[4] += (i-k)**2 + (j-l)**2
		#opponent position - variance of pieces distribution
		for (i,j) in self.opponentPosition:
			for (k,l) in self.opponentPosition:
					features[5] += (i-k)**2 + (j-l)**2

		return features

	'''
	Public Method
	Find all legal moves, including 1 roll and repetitive hops
    '''	
	def computeLegalMove(self):
		possibleMoveBoard = []
		for (i, j) in self.myPosition:
			## current piece x and y position
			rollMoves = self.findLegalRoll(i,j)
			for (nexti, nextj) in rollMoves:
				possibleMoveBoard.append(((i,j),(nexti, nextj)))
			possibleMoveBoard += self.computeRepetitiveHop(i,j)

		return possibleMoveBoard

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
			newBoardState = boardState(options = 'fullGame', inputBoard = newBoard, player = 3 - self.player)
		else:
			newBoardState = boardState(options = 'smallGame', inputBoard = newBoard, player = 3 - self.player)
		return newBoardState

	'''
	Private Method
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
	Private Method computeRepetitiveHop
	Compute repetitive hop for a piece, given the coordinate hopi and hopj
	Calls computeRepetitiveHopRecursion
    '''	
	def computeRepetitiveHop(self, hopi, hopj):
		possibleMoveBoard = []
		pastPosition = {}
		pastPosition[(hopi, hopj)] = 1
		for (basei, basej) in self.allPosition:
			hopMove= self.findLegalHop(hopi, hopj, basei, basej)
			if hopMove is not None:
				(nexti, nextj) = hopMove
				if (nexti, nextj) not in pastPosition:
					pastPosition[(nexti, nextj)] = 1
					futureBoard = copy.deepcopy(self.board)
					futureBoard[hopi][hopj] = 0
					futureBoard[nexti][nextj] = 1	
					possibleMoveBoard.append(((hopi,hopj),(nexti, nextj)))
					if self.fullGame == 0:
						futureBoardState = boardState(options = 'smallGame', inputBoard = futureBoard, player = self.player)
					else:
						futureBoardState = boardState(options = 'fullGame', inputBoard = futureBoard, player = self.player)
					futureBoardState.computeRepetitiveHopRecursion(hopi, hopj, nexti, nextj, pastPosition, possibleMoveBoard)
		
		return possibleMoveBoard



	'''
	Private
	Compute repetitive hop for a piece, given the coordinate hopi and hopj
	Find a legal hop moves, given the cooridnate of a piece and the base
    '''	
	def computeRepetitiveHopRecursion(self, origini, originj, hopi, hopj, pastPosition, possibleMoveBoard):
		for (basei, basej) in self.allPosition:
			hopMove= self.findLegalHop(hopi, hopj, basei, basej)
			if hopMove is not None:
				(nexti, nextj) = hopMove
				if (nexti, nextj) not in pastPosition:
					#print "piece " + str(hopi) + " " + str(hopj) + " going " + str(nexti) + " " + str(nextj)
					pastPosition[(nexti, nextj)] = 1
					futureBoard = copy.deepcopy(self.board)
					futureBoard[hopi][hopj] = 0
					futureBoard[nexti][nextj] = 1
					possibleMoveBoard.append(((origini, originj),(nexti, nextj)))	
					if self.fullGame == 0:
						futureBoardState = boardState(options = 'smallGame', inputBoard = futureBoard, player = self.player)
					else:
						futureBoardState = boardState(options = 'fullGame', inputBoard = futureBoard, player = self.player)
					#futureBoardState.printBoard()
					futureBoardState.computeRepetitiveHopRecursion(origini, originj, nexti, nextj, pastPosition, possibleMoveBoard)

	'''
	Private
	Find a legal hop moves, given the cooridnate of a piece and the base
    '''	
	def findLegalHop(self, hopi, hopj, basei, basej):
		hopMove = None
		if self.isAdjacent(hopi, hopj, basei, basej):
			diffi = basei - hopi
			diffj = basej - hopj
			nexti = basei + diffi
			nextj = basej + diffj
			if nexti < self.height and nextj < self.mid_width_max:
				if self.board[nexti][nextj] == 0:
					hopMove = (nexti, nextj)
				
		return hopMove

	'''
	Private
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
		