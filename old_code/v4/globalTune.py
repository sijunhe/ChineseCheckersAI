print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

from boardState import *
from computeLegalMove import * 
from computeFeatures import *
from computeMinimax import *
import numpy as np 
import copy
import time

## initialize weights
weights = np.ones(9)
weights[1] = 10
weights[5] = -10
weights[6] = -1
weights[7] = -1
weights[8] = -1
weights = weights / np.linalg.norm(weights)
depth = 2
stplength = 1

gameCount = 0
errors = []
boardStart = boardState(options = 'smallGame') # fullGame, smallGame
print "Orginal Board"
boardStart.printBoard()

boardNow = boardStart
player = 1
turn = 0
cantGo1 = []
cantGo2 = []
while ((not boardNow.isEnd()) and turn < 100) :
	turn = turn + 1
	timeStart = time.time()
	
	if (player == 1):
		features = computeFeaturesFull(boardNow, 1)
		scoreRaw = np.inner(features, weights)
		(scoreMiniMax, moveList, recursions) = computeMinimax(boardNow, player, weights, 4, cantGo1)
		if turn == 1:
			if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
				featureMatrix = features
				scoreVector = np.array([scoreMiniMax])
		else:
			if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
				featureMatrix = np.vstack((featureMatrix,features))
				score = np.array([scoreMiniMax])
				scoreVector = np.vstack((scoreVector, score))
		error = (scoreRaw - scoreMiniMax) 
		# weights1 = weights1 - error * stplength / np.linalg.norm(features) * features ## weights update
		# weights1[:9] = weights1[:9] / np.linalg.norm(weights1[:9])
		move = moveList[0]
		cantGo1.append(move)
		if (len(cantGo1) >= 5) :
			cantGo1.pop(0)
	else :
		features = computeFeaturesFull(boardNow, 2)
		scoreRaw = np.inner(features, weights)
		(scoreMiniMax, moveList, recursions) = computeMinimax(boardNow, player, weights, 4, cantGo2)
		if turn == 1:
			if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
				featureMatrix = features
				scoreVector = np.array([scoreMiniMax])
		else:
			if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
				featureMatrix = np.vstack((featureMatrix,features))
				score = np.array([scoreMiniMax])
				scoreVector = np.vstack((scoreVector, score))
		error = (scoreRaw - scoreMiniMax) / scoreMiniMax
		# weights2 = weights2 - error * stplength / np.linalg.norm(features) * features ## weights update
		# weights2[:9] = weights2[:9] / np.linalg.norm(weights2[:9])
		move = moveList[0]
		cantGo2.append(move)
		if (len(cantGo2) >= 5) :
			cantGo2.pop(0)

	timeEnd = time.time()	
	

	error = abs(error)
	errors.append(error)
	print('turn = {}'.format(turn))
	print('player = {}'.format(player))
	print('move = {}'.format(move))
	print('recursions = {}'.format(recursions))
	#print('error = {}'.format(error))
	print 'time used = ' + str(timeEnd - timeStart)
	boardNow = boardNow.takeMove(move)
	boardNow.printBoard()
	player = 3 - player
weights = np.linalg.lstsq(featureMatrix, scoreVector)
print featureMatrix
print scoreVector
print weights