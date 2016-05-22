print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

from boardState import *
from computeLegalMove import * 
from computeFeatures import *
from computeMinimax import *
import numpy as np 
import copy
import time

weights = np.ones(9)
weights[1] = 10
weights[5] = -10
weights[6] = -1
weights[7] = -1
weights[8] = -1
weights = weights / np.linalg.norm(weights)
depth = 2
stplength = 1


boardStart = boardState(options = 'smallGame') # fullGame, smallGame
print "Orginal Board"
boardStart.printBoard()

errors = []
boardNow = boardStart
player = 1
turn = 0
cantGo1 = []
cantGo2 = []
while ((not boardNow.isEnd()) and turn < 100) :
	turn = turn + 1
	timeStart = time.time()
	features = computeFeaturesFull(boardNow, player)
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
		cantGo1.append(move)
		if (len(cantGo2) >= 5) :
			cantGo2.pop(0)

	timeEnd = time.time()	
	error = (scoreRaw - scoreMiniMax) / scoreMiniMax
	weights = weights - error * stplength / np.linalg.norm(features) * features ## weights update
	weights = weights / np.linalg.norm(weights)
	

	error = abs(error)
	errors.append(error)
	print '\n\n'
	print('turn = {}'.format(turn))
	print('player = {}'.format(player))
	print('move = {}'.format(move))
	print('recursions = {}'.format(recursions))
	print('error = {}'.format(error))
	print 'time used = ' + str(timeEnd - timeStart)
	print('weights = {}'.format(weights))
	boardNow = boardNow.takeMove(move)
	boardNow.printBoard()
	player = 3 - player

print errors