print('\n\n\n\n')


from boardState import *
from computeLegalMove import * 
from computeFeatures import *
from computeMinimax import *
from randomMove import *
import numpy as np 
import copy,time, math, sys

## initialize weights
weights = np.ones(3)
weights[0] = 10
weights = weights / np.linalg.norm(weights)
weightsSum = np.zeros(3)
gameCount = 0
# Learn the weights using linear regression
totalGames = 1
playerOneWin = 0
playerTwoWin = 0
while gameCount < totalGames:
	gameCount += 1
	print('Game = No. {}'.format(gameCount))
	boardStart = boardState(options = 'fullGame') # fullGame, smallGame
	#print "Orginal Board"
	#boardStart.printBoard()
	boardNow = boardStart
	player = 1
	turn = 0
	cantGo1 = []
	timeStart = time.time()
	#print ('weightsNow = {}'.format(weights))
	while ((not boardNow.isEnd()) and turn < 250) :
		turn = turn + 1
		timeStart = time.time()
		features = computeFeaturesFull(boardNow)
		scoreRaw = np.inner(features, weights)
		if (player == 1) :
			move = randomMove(boardNow, player)

		else :
			(scoreMiniMax, moveList, recursions) = computeMinimax(boardNow, player, weights, 2, cantGo1)
			move = moveList[0]
			cantGo1.append(move)
			if (len(cantGo1) >= 5) :
				cantGo1.pop(0)
			
		
		# if turn == 1:
		# 	if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
		# 		featureMatrix = features
		# 		scoreVector = np.array([scoreMiniMax])
		# 		predError = (scoreMiniMax - scoreRaw) ** 2
		# else:
		# 	if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
		# 		featureMatrix = np.vstack((featureMatrix,features))
		# 		score = np.array([scoreMiniMax])
		# 		scoreVector = np.vstack((scoreVector, score))
		# 		predError += (scoreMiniMax - scoreRaw) ** 2
		timeEnd = time.time()
		print('turn = {}'.format(turn))
		# print('player = {}'.format(player))
		# print('move = {}'.format(move))
		# print('recursions = {}'.format(recursions))
		# print 'time used = ' + str(timeEnd - timeStart)
		boardNow = boardNow.takeMove(move)
		#boardNow.printBoard()
		#sys.stdout.flush()
		player = 3 - player
		if (boardNow.isEndGame()):
			break
	if turn >= 250:
		print "################################################################################"
		print "################                STUCK                         ##################"
		print "################################################################################"
	
	#print('\n ##################### \n Endgame Begins!!!! \n #####################')
	while ((not boardNow.isEnd()) and turn < 300) :
		turn = turn + 1
		# print('\n\n')
		# print('turn = {}'.format(turn))
		# print('player = {}'.format(player))
		# print('\n')
		# boardNow.printBoard()
		#timeStart = time.time()
		(scoreGreedy, moveList, recursions) = findMoveGreedy(boardNow, player, 3)
		#timeEnd = time.time()
		# print('scoreGreedy = {}'.format(scoreGreedy))
		move = moveList[0]
		# print('move = {}'.format(move))
		# print('recursions = {}'.format(recursions))
		# print 'time used = ' + str(timeEnd - timeStart)
		# sys.stdout.flush()
		boardNow = boardNow.takeMove(move)
		player = 3 - player
	if boardNow.isEnd() == 1:
		playerOneWin += 1
	elif boardNow.isEnd() == -1:
		playerTwoWin += 1
	timeEnd = time.time()
print "time " + str(timeEnd - timeStart)
print "player one won " + str(playerOneWin)
print "player two won " + str(playerTwoWin)
	
