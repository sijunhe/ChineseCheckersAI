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
	print('\n\n')
	print('turn = {}'.format(turn))
	print('player = {}'.format(player))
	boardNow.printBoard()
	print('features = {}'.format(features))
	print('weights = {}'.format(weights))

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
	
	# if turn == 1:
	# 	if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
	# 		featureMatrix = features
	# 		scoreVector = np.array([scoreMiniMax])
	# else:
	# 	if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
	# 		featureMatrix = np.vstack((featureMatrix,features))
	# 		score = np.array([scoreMiniMax])
	# 		scoreVector = np.vstack((scoreVector, score))

	timeEnd = time.time()	
	print('scoreRaw = {}'.format(scoreRaw))
	print('scoreMiniMax = {}'.format(scoreMiniMax))
	print('move = {}'.format(move))
	print('recursions = {}'.format(recursions))
	print 'time used = ' + str(timeEnd - timeStart)
	boardNow = boardNow.takeMove(move)
	player = 3 - player

print('\n\n')
boardNow.printBoard()