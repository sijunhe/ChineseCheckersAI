from boardState import *
from computeLegalMove import * 
from computeFeatures import *
from computeMinimax import *
import numpy as np 
import copy
import time
print "################################################################################"
boardStart = boardState(options = 'smallGame') # fullGame, smallGame
print "Orginal Board"
boardStart.printBoard()
boardNow = boardStart
player = 1
turn = 0
weights = np.ones(5)
weights[0] = -1.69853196 
weights[1] =  0.06633986
weights[2] = 0.09230491 
weights[3] = -0.01052756
weights[4] = 0.23913056
cantGo1 = []
cantGo2 = []
while ((not boardNow.isEnd()) and turn < 100) :
	turn = turn + 1
	timeStart = time.time()
	features = computeFeaturesFull(boardNow)
	scoreRaw = np.inner(features, weights)
	if (player == 1) :
		(scoreMiniMax, moveList, recursions) = computeMinimax(boardNow, player, weights, 4, cantGo1)
		move = moveList[0]
		cantGo1.append(move)
		if (len(cantGo1) >= 5) :
			cantGo1.pop(0)
	else :
		(scoreMiniMax, moveList, recursions) = computeMinimax(boardNow, player, weights, 4, cantGo2)
		move = moveList[0]
		cantGo2.append(move)
		if (len(cantGo2) >= 5) :
			cantGo2.pop(0)
	
	if turn == 1:
		if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
			featureMatrix = features
			scoreVector = np.array([scoreMiniMax])
	else:
		if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
			featureMatrix = np.vstack((featureMatrix,features))
			score = np.array([scoreMiniMax])
			scoreVector = np.vstack((scoreVector, score))

	timeEnd = time.time()	
	
	print('turn = {}'.format(turn))
	print('player = {}'.format(player))
	print('move = {}'.format(move))
	print('scoreMiniMax = {}'.format(scoreMiniMax))
	print('recursions = {}'.format(recursions))
	#print('error = {}'.format(error))
	print 'time used = ' + str(timeEnd - timeStart)
	boardNow = boardNow.takeMove(move)
	boardNow.printBoard()
	player = 3 - player
result = np.linalg.lstsq(featureMatrix, scoreVector)
weights = result[0].reshape((5,))
residuals = result[1][0]
residualsVec.append(residuals)
resTurnVec.append(residuals/turn)

