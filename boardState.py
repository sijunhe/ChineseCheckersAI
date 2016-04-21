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
	Constructor
	'''
	def __init__(self, options = 'smallGame'):
		if options == 'smallGame':
			self.height = 7

		if options == 'fullGame':
			self.height = 17
		
		self.mid_width = (self.height + 1) / 2

		## max y coorindate for center line
		## while this is now same as height, will be different if we use the hex board
		self.mid_width_max = self.mid_width * 2 - 1

		## initialize game board
	
		self.board = np.ndarray((self.height, self.mid_width_max), dtype = np.int32)
		self.board.fill(-1)

		if options == 'smallGame':
			
			## initialize available space 
			for i in range(self.height):
				if i == 0 or i == 6:
					self.board[i, 3] = 0

				elif i == 1 or i== 5:
					for j in range(2, 5, 2):
						self.board[i, j] = 0
				
				elif i == 2 or i== 4:
					for j in range(1, 6, 2):
						self.board[i, j] = 0

				elif i == 3:
					for j in range(0, 7, 2):
						self.board[i, j] = 0

			## initialize player pieces
			## player1 = 1
			## player2 = 2
			self.board[0,3] = 1
			self.board[1,2] = self.board[1,4] = 1

			self.board[6,3] = 2
			self.board[5,2] = self.board[5,4] = 2

		if options == 'fullGame':
			## need to implement this
			pass

	
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
		
