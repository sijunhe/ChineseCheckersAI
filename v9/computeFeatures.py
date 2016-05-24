from boardState import *
from computeLegalMove import *
import numpy as np

def computeFeatures(board):
	numFeature = 3
	features = np.zeros((numFeature))
	### Compute every feature
	'''distance to the end - position_1'''
	for (i,j) in board.PositionOne:
		features[0] -= (board.height - 1 - i)**2
	'''distance to the end - position_2'''
	for (i,j) in board.PositionTwo:
		features[0] += i**2
	features[0] = features[0]/board.numPieces


	'''distance to the center - position_1'''
	for (i,j) in board.PositionOne:
		features[1] -= (j-board.midElement)**2
	'''distance to the center - position_2'''
	for (i,j) in board.PositionTwo:
		features[1] += (j-board.midElement)**2
	features[1] = features[1]/board.numPieces

	# '''variance of pieces distribution - position_1'''
	# for (i,j) in board.PositionOne:
	# 	for (k,l) in board.PositionOne:
	# 			features[2] -= (j-l)**2
	# '''variance of pieces distribution - position_2'''
	# for (i,j) in board.PositionTwo:
	# 	for (k,l) in board.PositionTwo:
	# 			features[2] += (j-l)**2
	# features[2] = features[2]/(board.numPieces)**2

	return features



def computeFeaturesFull(board):
	numFeature = 3
	features = np.zeros((numFeature))
	### Compute every feature
	'''distance to the end - position_1'''
	for (i,j) in board.PositionOne:
		features[0] -= (board.height - 1 - i)**2
	'''distance to the end - position_2'''
	for (i,j) in board.PositionTwo:
		features[0] += i**2
	features[0] = features[0]/board.numPieces

	'''distance to the center - position_1'''
	for (i,j) in board.PositionOne:
		features[1] -= (j-board.midElement)**2
	'''distance to the center - position_2'''
	for (i,j) in board.PositionTwo:
		features[1] += (j-board.midElement)**2
	features[1] = features[1]/board.numPieces

	# '''variance of pieces distribution - position_1'''
	# for (i,j) in board.PositionOne:
	# 	for (k,l) in board.PositionOne:
	# 			features[2] -= (j-l)**2
	# '''variance of pieces distribution - position_2'''
	# for (i,j) in board.PositionTwo:
	# 	for (k,l) in board.PositionTwo:
	# 			features[2] += (j-l)**2
	# features[2] = features[2]/(board.numPieces)**2

	'''total squared furthest moves for each pieces - position_1'''
	moves = np.zeros((board.numPieces))
	#print 'possible moves for player 1:'
	k = 0
	for (i,j) in board.PositionOne:
		# print (i,j)
		# print 'k = {}'.format(k)
		for (i1,j1, i2,j2) in computeLegalMove(board,1):
			# print (i1,j1, i2,j2)
			if (i,j) == (i1,j1):
				# print (i1,j1)
				if i2 - i1 > moves[k]:
					moves[k] = i2 - i1
					# print (moves)
		k = k + 1
	features[2] += np.sum(np.square(moves))

	'''total squared furthest moves for each pieces - position_2'''
	moves = np.zeros((board.numPieces))
	#print 'possible moves for player 1:'
	k = 0
	for (i,j) in board.PositionTwo:
		# print (i,j)
		# print 'k = {}'.format(k)
		for (i1,j1, i2,j2) in computeLegalMove(board,2):
			# print (i1,j1, i2,j2)
			if (i,j) == (i1,j1):
				# print (i1,j1)
				if i1 - i2 > moves[k]:
					moves[k] = i1 - i2
					# print (moves)
		k = k + 1
	features[2] -= np.sum(np.square(moves))


	return features