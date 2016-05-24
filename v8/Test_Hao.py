## used by Hao to test his code 


######################################################################################################################
## You can run the file, but do NOT change if you are not Hao  
######################################################################################################################

print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

from boardState import *
from computeLegalMove import * 
from computeFeatures import *
from computeMinimax import *
import numpy as np 
import copy
import time

weights = np.ones(4)
weights[0] = 10
depth = 4
stplength = 0.1
boardStart = boardState(options = 'fullGame') # fullGame, smallGame
print "Orginal Board"
boardStart.printBoard()


#### The whole game
# boardNow = boardStart
# player = 1
# turn = 0
# while ((not boardNow.isEnd()) and turn < 100) :
# 	turn = turn + 1
# 	(scoreMiniMax, moveList, recursions) = computeMinimax(boardNow, player, weights, depth)
# 	features = computeFeaturesFull(boardNow)
# 	scoreRaw = np.inner(features, weights)
# 	weights = weights - (scoreRaw - scoreMiniMax) * stplength * features
# 	weights = weights / np.linalg.norm(weights)
# 	move = moveList[0]
# 	print('turn = {}'.format(turn))
# 	print('player = {}'.format(player))
# 	print('move = {}'.format(move))
# 	print('error = {}'.format(scoreMiniMax - scoreRaw))
# 	print('weights = {}'.format(weights))
# 	boardNow = boardNow.takeMove(move)
# 	boardNow.printBoard()
# 	player = 3 - player



#### To test the code computeMinimax()
print('\n\n')
timeStart = time.time()
(scoreMiniMax, moveList, recursions) = computeMinimax_wo(boardStart, 1, weights, depth, [])
timeEnd = time.time()
timeUsed = timeEnd - timeStart
print('scoreMiniMax = {}'.format(scoreMiniMax))
print('moveList = {}'.format(moveList))
print('recursions = {}'.format(recursions))
print('time used = {}'.format(timeUsed))

board2 = copy.deepcopy(boardStart)
for move in moveList :
	board2 = board2.takeMove(move)
board2.printBoard()




#### To test the code computeMinimax_wo()
# print('\n\n')
# timeStart = time.time()
# (scoreMiniMax, moveList, recursions) = computeMinimax_wo(boardStart, 1, weights, depth)
# timeEnd = time.time()
# timeUsed = timeEnd - timeStart
# print('scoreMiniMax = {}'.format(scoreMiniMax))
# print('moveList = {}'.format(moveList))
# print('recursions = {}'.format(recursions))
# print('time used = {}'.format(timeUsed))
# board2 = copy.deepcopy(boardStart)
# for move in moveList :
# 	board2 = board2.takeMove(move)
# board2.printBoard()




#### To test the code relating features, legamMove, takeMove
# features = computeFeatures(boardStart)
# print('features = {}'.format(features))
# scoreRaw = np.inner(weights, features)
# print('scoreRaw = {}'.format(scoreRaw))

# possibleMoveBoard = computeLegalMove(board2, 2)
# for move in possibleMoveBoard:
# 	print('\n\n')
# 	print move
# 	boardNew = board2.takeMove(move)
# 	boardNew.printBoard()
# 	features = computeFeatures(boardNew)
# 	print('features = {}'.format(features))
# 	scoreRaw = np.inner(weights, features)
# 	print('scoreRaw = {}'.format(scoreRaw))
