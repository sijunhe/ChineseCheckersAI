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
weights[2] = 10
depth = 4
stplength = 0.1


boardStart = boardState(options = 'smallGame') # fullGame, smallGame
print "Orginal Board"
boardStart.printBoard()


boardNow = boardStart
player = 1
turn = 0
while ((not boardNow.isEnd()) and turn < 100) :
	turn = turn + 1
	(scoreMiniMax, moveList, recursions) = computeMinimax(boardNow, player, weights, depth)
	features = computeFeatures(boardNow)
	scoreRaw = np.inner(features, weights)
	# weights = weights - (scoreRaw - scoreMiniMax) * stplength / np.linalg.norm(features) * features ## weights update
	move = moveList[0]
	print('turn = {}'.format(turn))
	print('player = {}'.format(player))
	print('move = {}'.format(move))
	print('error = {}'.format(scoreMiniMax - scoreRaw))
	print('weights = {}'.format(weights))
	boardNow = boardNow.takeMove(move)
	boardNow.printBoard()
	player = 3 - player