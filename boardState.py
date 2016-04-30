import numpy as np

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
	def __init__(self, options = 'smallGame'):
		#number of features
		self.numFeature = 7
		self.weights = np.ones((self.numFeature,1))
		self.myPosition = []
		self.opponentPosition = []
		if options == 'smallGame':
			self.height = 7
			self.starting = 2
			midElement = 3
			
		if options == 'fullGame':
			self.height = 17
			self.starting = 4
			midElement = 8

		
		self.mid_width = (self.height + 1) / 2

		## max y coorindate for center line
		## while this is now same as height, will be different if we use the hex board
		self.mid_width_max = self.mid_width * 2 - 1

		## initialize game board
	
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


	'''
	recursively compute board value according to the weights and feature value
	called by computeMiniMax for the leaves of the tree
	returns a double
    '''
	def computeFuncApprox():


	def computeLegalMove():
		returnBoard = []
		






		





