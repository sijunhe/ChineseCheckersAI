print('\n\n\n\n')


from boardState import *
from computeLegalMove import * 
from computeFeatures import *
from computeMinimax import *
import numpy as np 
import copy
import time
import matplotlib.pyplot as plt

## initialize weights
weights = np.ones(4)
# weights[0] = 10
weights = weights / np.linalg.norm(weights)
weightsSum = np.zeros(4)

# Learn the weights using linear regression
gameCount = 0
SSRVec = []
RSquareVec = []
totalGames = 30
while gameCount < totalGames:
	print "################################################################################"
	gameCount += 1
	print('Game = No. {}'.format(gameCount))
	boardStart = boardState(options = 'smallGame') # fullGame, smallGame
	#print "Orginal Board"
	#boardStart.printBoard()
	error = 0
	boardNow = boardStart
	player = 1
	turn = 0
	cantGo1 = []
	cantGo2 = []
	print ('weightsNow = {}'.format(weights))
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
		
		# print('game = {}'.format(gameCount))
		# print('turn = {}'.format(turn))
		# print('player = {}'.format(player))
		# print('move = {}'.format(move))
		# print('recursions = {}'.format(recursions))
		# #print('error = {}'.format(error))
		# print 'time used = ' + str(timeEnd - timeStart)
		boardNow = boardNow.takeMove(move)
		#boardNow.printBoard()
		player = 3 - player
	result = np.linalg.lstsq(featureMatrix, scoreVector)
	weightsNew = result[0]
	residuals = np.dot(featureMatrix, weightsNew) - scoreVector
	SSR = result[1][0]
	SST = np.linalg.norm(scoreVector - np.average(scoreVector)) ** 2
	RSquare = 1 - SSR / SST
	SSRVec.append(SSR)
	RSquareVec.append(RSquare)
	weightsNew = weightsNew.reshape((4,))
	weightsNew = weightsNew / np.linalg.norm(weightsNew)

	print ('Number of turns = {}'.format(turn))
	print ('weightsNew = {}'.format(weightsNew))
	print ('SSR = {}'.format(SSR))
	print ('RSquare = {}'.format(RSquare))
	if (gameCount <= 6) :
		weights = weightsNew
	else :
		weightsSum = weightsSum + weightsNew
		weights = weightsSum / (gameCount - 6)
		weights = weights / np.linalg.norm(weights)
	

print('\n')
print('The SSR of all games are\n {}'.format(SSRVec))
print('\n')
print('The RSquare of all games are\n {}'.format(RSquareVec)) 

plt.plot(range(1, totalGames+1), RSquareVec, 'bo-')
plt.ylabel('R^2 of each linear regression')
plt.xlabel('Game')
plt.savefig('RSquare.eps')
plt.show()


### Play A new game with weights learned before!
# print('\n\n')
# print "################################################################################"
# boardStart = boardState(options = 'smallGame') # fullGame, smallGame
# print "Orginal Board"
# boardStart.printBoard()
# boardNow = boardStart
# player = 1
# turn = 0
# cantGo1 = []
# cantGo2 = []
# while ((not boardNow.isEnd()) and turn < 100) :
# 	turn = turn + 1
# 	timeStart = time.time()
# 	features = computeFeaturesFull(boardNow)
# 	scoreRaw = np.inner(features, weights)
# 	print('\n\n')
# 	print('turn = {}'.format(turn))
# 	print('player = {}'.format(player))
# 	print('\n')
# 	boardNow.printBoard()
# 	print('features = {}'.format(features))
# 	print('weights = {}'.format(weights))

# 	if (player == 1) :
# 		(scoreMiniMax, moveList, recursions) = computeMinimax(boardNow, player, weights, 4, cantGo1)
# 		move = moveList[0]
# 		cantGo1.append(move)
# 		if (len(cantGo1) >= 5) :
# 			cantGo1.pop(0)
# 	else :
# 		(scoreMiniMax, moveList, recursions) = computeMinimax(boardNow, player, weights, 4, cantGo2)
# 		move = moveList[0]
# 		cantGo2.append(move)
# 		if (len(cantGo2) >= 5) :
# 			cantGo2.pop(0)
	
# 	# if turn == 1:
# 	# 	if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
# 	# 		featureMatrix = features
# 	# 		scoreVector = np.array([scoreMiniMax])
# 	# else:
# 	# 	if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
# 	# 		featureMatrix = np.vstack((featureMatrix,features))
# 	# 		score = np.array([scoreMiniMax])
# 	# 		scoreVector = np.vstack((scoreVector, score))

# 	timeEnd = time.time()	
# 	print('scoreRaw = {}'.format(scoreRaw))
# 	print('scoreMiniMax = {}'.format(scoreMiniMax))
# 	print('move = {}'.format(move))
# 	print('recursions = {}'.format(recursions))
# 	print 'time used = ' + str(timeEnd - timeStart)
# 	boardNow = boardNow.takeMove(move)
# 	player = 3 - player

# print('\n\n')
# boardNow.printBoard()