print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

from boardState import *
from computeLegalMove import * 
from computeFeatures import *
from computeMinimax import *
import numpy as np 
import copy
import time

weights = np.ones(10)
weights[1] = 10
weights[2] = 10
weights[9] = 100000
weights[:9] = weights[:9] / np.linalg.norm(weights[:9])
depth = 2
stplength = 1


boardStart = boardState(options = 'smallGame') # fullGame, smallGame
print "Orginal Board"
boardStart.printBoard()

errors = []
boardNow = boardStart
player = 1
turn = 0
weights1 = weights
weights2 = weights
while ((not boardNow.isEnd()) and turn < 100) :
	turn = turn + 1
	timeStart = time.time()
	features = computeFeatures(boardNow)
	
	if (player == 1) :
		scoreRaw = np.inner(features, weights1)
		(scoreMiniMax, moveList, recursions) = computeMinimax(boardNow, player, weights1, 4)
		error = (scoreRaw - scoreMiniMax) / scoreMiniMax
		weights1 = weights1 - error * stplength / np.linalg.norm(features) * features ## weights update
		weights1[:9] = weights1[:9] / np.linalg.norm(weights1[:9])
	else :
		scoreRaw = np.inner(features, weights2)
		(scoreMiniMax, moveList, recursions) = computeMinimax(boardNow, player, weights2, 4)
		error = (scoreRaw - scoreMiniMax) / scoreMiniMax
		weights2 = weights2 - error * stplength / np.linalg.norm(features) * features ## weights update
		weights2 = weights2 / np.linalg.norm(weights2)
		weights2[:9] = weights2[:9] / np.linalg.norm(weights2[:9])
	timeEnd = time.time()	
	move = moveList[0]
	error = abs(error)
	errors.append(error)
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