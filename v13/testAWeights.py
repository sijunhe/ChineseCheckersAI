# This file is used to test a weight. To be specific, both players play the game with this weights, and this file will keep track of each step

print "################################################################################"

from boardState import *
from computeLegalMove import * 
from computeFeatures import *
from strategies import *
from strategiesHelpers import *
import numpy as np 
import copy
import time

boardNow = boardState(options = 'smallGame') # fullGame, smallGame, midGame
player = 1
turn = 0
aaaaa = [10, 1, 1]
weights = np.array(aaaaa)
weights = weights / np.linalg.norm(weights)
cantGo1 = []
cantGo2 = []
depth = 2 #Can only be even numbers: 2, 4, 6, ...


## Startgame begins!
while (turn < 249) :
	turn = turn + 1
	timeStart = time.time()

	print('\n\n')
	print('turn = {}'.format(turn))
	print('player = {}'.format(player))
	print('\n')
	boardNow.printBoard()

	timeStart = time.time()
	if (player == 1) :
		(scoreMaxiMax, move, recursions) = computeMaximax(boardNow, player, weights, depth/2, cantGo1)
		cantGo1.append(move)
		if (len(cantGo1) >= 5) :
			cantGo1.pop(0)
	else :
		(scoreMaxiMax, move, recursions) = computeMaximax(boardNow, player, weights, depth/2, cantGo2)
		cantGo2.append(move)
		if (len(cantGo2) >= 5) :
			cantGo2.pop(0)
	timeEnd = time.time()
	print('move = {}'.format(move))
	print('recursions = {}'.format(recursions))
	print 'time used = ' + str(timeEnd - timeStart)
	boardNow = boardNow.takeMove(move)
	player = 3 - player
	if (boardNow.isBattleField(2)) :
		print('\n##################################################################')
		print('#####################  Battlefield Begins!!!!  #####################')
		print('#####################  Let\'s fight for it!!!!  #####################')
		print('####################################################################')
		break

firstBattleFieldTurn = turn + 1

'''
### Battlefield begins!
'''
while ((not boardNow.isEnd()) and turn < 250) :
	turn = turn + 1
	timeStart = time.time()
	features = computeFeaturesFull(boardNow)
	scoreRaw = np.inner(features, weights)

	print('\n\n')
	print('turn = {}'.format(turn))
	print('player = {}'.format(player))
	print('\n')
	boardNow.printBoard()
	print('features = {}'.format(features))
	print('weights = {}'.format(weights))

	if (player == 1) :
		(scoreMiniMax, move, recursions) = computeMinimax(boardNow, player, weights, depth, cantGo1)
		cantGo1.append(move)
		if (len(cantGo1) >= 5) :
			cantGo1.pop(0)
	else :
		(scoreMiniMax, move, recursions) = computeMinimax(boardNow, player, weights, depth, cantGo2)
		cantGo2.append(move)
		if (len(cantGo2) >= 5) :
			cantGo2.pop(0)
	
	if turn == firstBattleFieldTurn:
		if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
			featureMatrix = features
			scoreVector = np.array([scoreMiniMax])
	else:
		if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
			featureMatrix = np.vstack((featureMatrix,features))
			score = np.array([scoreMiniMax])
			scoreVector = np.vstack((scoreVector, score))


	timeEnd = time.time()	
	print('scoreRaw = {}'.format(scoreRaw))
	print('scoreMiniMax = {}'.format(scoreMiniMax))
	print('move = {}'.format(move))
	print('recursions = {}'.format(recursions))
	print 'time used = ' + str(timeEnd - timeStart)
	boardNow = boardNow.takeMove(move)
	player = 3 - player
	if (boardNow.isEndGame(0)) :
		print('\n################################################################')
		print('#####################  Endgame Begins!!!!  #####################')
		print('#####################  Let\'s go go go!!!!  #####################')
		print('################################################################')
		break

'''
### Endgame begins!
'''
while ((not boardNow.isEnd()) and turn < 250) :
	turn = turn + 1
	print('\n\n')
	print('turn = {}'.format(turn))
	print('player = {}'.format(player))
	print('\n')
	boardNow.printBoard()

	timeStart = time.time()
	move = findMove_EndGame(boardNow, player)
	timeEnd = time.time()
	print('move = {}'.format(move))
	print 'time used = ' + str(timeEnd - timeStart)
	boardNow = boardNow.takeMove(move)
	player = 3 - player


if turn >= 250:
	print "################################################################################"
	print "################                STUCK                         ##################"
	print "################################################################################"

print('\n\n')
boardNow.printBoard()
result = np.linalg.lstsq(featureMatrix, scoreVector)
weightsNew = result[0]
residuals = np.dot(featureMatrix, weightsNew) - scoreVector
SSR = result[1][0]
SST = np.linalg.norm(scoreVector - np.average(scoreVector)) ** 2
RSquare = 1 - SSR / SST
weightsNew = weightsNew.reshape((3,))
weightsNew = weightsNew / np.linalg.norm(weightsNew)

print ('Number of turns = {}'.format(turn))
print ('weightsNew = {}'.format(weightsNew))
print ('SSR = {}'.format(SSR))
print ('RSquare = {}'.format(RSquare))
