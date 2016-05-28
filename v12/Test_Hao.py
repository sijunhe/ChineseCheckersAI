# used by Hao to test his code 


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
from randomMove import * 

weights = np.ones(3)
# weights[0] = 10
depth = 4
stplength = 0.1
boardStart = boardState(options = 'midGame') # fullGame, smallGame, midGame

boardboard = boardStart.board
boardboard[0][5] = 2
boardboard[1][4] = 2
boardboard[1][6] = 2
boardboard[2][3] = 2
boardboard[2][5] = 2
boardboard[2][7] = 2
boardboard[8][3] = 1
boardboard[8][5] = 1
boardboard[8][7] = 0
boardboard[9][4] = 1
boardboard[9][6] = 1
boardboard[10][5] = 1
boardboard[5][2] = 1
boardStart = boardState(options = 'midGame', inputBoard = boardboard)

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
# print('\n\n')
# timeStart = time.time()
# (scoreMiniMax, moveList, recursions) = computeMinimax(boardStart, 1, weights, depth, [])
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


''' 
To test the code findMoveGreedy(), which is the Endgame strategy
'''
print('\n\n')
timeStart = time.time()
boardNow = boardStart
numPossibleMoves = len(computeLegalMoveForward(boardNow, 1, 0))
print 'numPossibleMoves = ' + str(numPossibleMoves)
if (numPossibleMoves > 20) :
	greedyDepth = 2
elif (numPossibleMoves > 12) :
	greedyDepth = 3
else :
	greedyDepth = 4
(scoreGreedy, moveList, recursions) = findMoveGreedy(boardStart, 1, 4)
timeEnd = time.time()
timeUsed = timeEnd - timeStart
print('moveList = {}'.format(moveList))
print('recursions = {}'.format(recursions))
print('time used = {}'.format(timeUsed))

# board2 = copy.deepcopy(boardStart)
# for move in moveList :
# 	board2 = board2.takeMove(move)
# 	board2.printBoard()
# 	print str(computeScoreEndgame(board2, 2))



''' 
To test the code computeMinimax_wo()
'''
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




'''
To test the code relating features, legamMove, takeMove
'''
# features = computeFeatures(boardStart)
# print('features = {}'.format(features))
# scoreRaw = np.inner(weights, features)
# print('scoreRaw = {}'.format(scoreRaw))

# possibleMoveBoard = computeLegalMoveForward(boardStart, 2, -2)
# for move in possibleMoveBoard:
# 	print('\n\n')
# 	print move
# 	boardNew = boardStart.takeMove(move)
# 	boardNew.printBoard()
# 	features = computeFeatures(boardNew)
# 	print('features = {}'.format(features))
# 	scoreRaw = np.inner(weights, features)
# 	print('scoreRaw = {}'.format(scoreRaw))


'''
Test the code randomMove.py
'''
# numGame = 0
# DifferentBoards = []
# while (numGame < 30) :
# 	numGame = numGame + 1
# 	print 'Game No. ' + str(numGame)
# 	(advance, move) = randomMoveMultistepSquare(boardStart, 1, 2)
# 	boardNew = boardStart.takeMove(move)
# 	step = 1
# 	while (step < 10) :
# 		step = step + 1
# 		(advance, move) = randomMoveMultistepSquare(boardNew, 1, 2)
# 		boardNew = boardNew.takeMove(move)

# 	if boardNew not in DifferentBoards :
# 		DifferentBoards.append(boardNew)
# 		boardNew.printBoard()
# print (len(DifferentBoards))