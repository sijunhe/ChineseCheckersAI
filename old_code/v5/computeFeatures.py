from boardState import *
from computeLegalMove import *
import numpy as np

def computeFeatures(board):
	numFeature = 5
	features = np.zeros((numFeature))
	### Compute every feature
	features[0] = 1
	'''distance to the end - position_1'''
	for (i,j) in board.PositionOne:
		features[1] -= (board.height - 1 - i)**2
	'''distance to the end - position_2'''
	for (i,j) in board.PositionTwo:
		features[1] += i**2

	'''distance to the center - position_1'''
	for (i,j) in board.PositionOne:
		features[2] -= (j-board.midElement)**2
	'''distance to the center - position_2'''
	for (i,j) in board.PositionTwo:
		features[2] += (j-board.midElement)**2

	'''variance of pieces distribution - position_1'''
	for (i,j) in board.PositionOne:
		for (k,l) in board.PositionOne:
				features[3] -= (i-k)**2 + (j-l)**2
	'''variance of pieces distribution - position_2'''
	for (i,j) in board.PositionTwo:
		for (k,l) in board.PositionTwo:
				features[3] += (i-k)**2 + (j-l)**2

	return features



def computeFeaturesFull(board):
	numFeature = 5
	features = np.zeros((numFeature))
	### Compute every feature
	features[0] = 1
	'''distance to the end - position_1'''
	for (i,j) in board.PositionOne:
		features[1] -= (board.height - 1 - i)**2
	'''distance to the end - position_2'''
	for (i,j) in board.PositionTwo:
		features[1] += i**2

	'''distance to the center - position_1'''
	for (i,j) in board.PositionOne:
		features[2] -= (j-board.midElement)**2
	'''distance to the center - position_2'''
	for (i,j) in board.PositionTwo:
		features[2] += (j-board.midElement)**2

	'''variance of pieces distribution - position_1'''
	for (i,j) in board.PositionOne:
		for (k,l) in board.PositionOne:
				features[3] -= (i-k)**2 + (j-l)**2
	'''variance of pieces distribution - position_2'''
	for (i,j) in board.PositionTwo:
		for (k,l) in board.PositionTwo:
				features[3] += (i-k)**2 + (j-l)**2

	'''total furthest moves - position_1'''
	best_move = 0
	#print 'possible moves for player 1:'
	for (i1,j1, i2,j2) in computeLegalMove(board,1):
		#print (i1,j1), (i2,j2)
		if i2 - i1 > best_move:
			best_move = i2 - i1
	features[4] += best_move

	'''total furthest moves - position_2'''
	best_move = 0
	#print 'possible moves for player 2:'
	for (i1,j1, i2,j2) in computeLegalMove(board,2):
		#print (i1,j1), (i2,j2)
		if i1 - i2 > best_move:
			best_move = i1 - i2
	features[4] -= best_move


	return features