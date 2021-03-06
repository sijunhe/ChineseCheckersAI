print('\n\n\n\n')


from boardState import *
from computeLegalMove import * 
from computeFeatures import *
from computeMinimax import *
import numpy as np 
import copy,time, math, sys
import matplotlib.pyplot as plt

## initialize weights
weights = np.ones(3)
weights[0] = 10
weights = weights / np.linalg.norm(weights)
weightsSum = np.zeros(3)

# Learn the weights using linear regression
gameCount = 0
AARVec = []
RSquareVec = []
weightsGradVec = []
predErrorVec = []
totalGames = 100
while gameCount < totalGames:
	print "################################################################################"
	gameCount += 1
	print('Game = No. {}'.format(gameCount))
	boardStart = boardState(options = 'midGame') # fullGame, smallGame
	print "Orginal Board"
	boardStart.printBoard()
	error = 0
	boardNow = boardStart
	player = 1
	turn = 0
	cantGo1 = []
	cantGo2 = []
	print ('weightsNow = {}'.format(weights))
	while ((not boardNow.isEnd()) and turn < 250) :
		turn = turn + 1
		timeStart = time.time()
		features = computeFeaturesFull(boardNow)
		scoreRaw = np.inner(features, weights)
		if (player == 1) :
			(scoreMiniMax, moveList, recursions) = computeMinimax(boardNow, player, weights, 2, cantGo1)
			move = moveList[0]
			cantGo1.append(move)
			if (len(cantGo1) >= 5) :
				cantGo1.pop(0)
		else :
			(scoreMiniMax, moveList, recursions) = computeMinimax(boardNow, player, weights, 2, cantGo2)
			move = moveList[0]
			cantGo2.append(move)
			if (len(cantGo2) >= 5) :
				cantGo2.pop(0)
		
		if turn == 1:
			if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
				featureMatrix = features
				scoreVector = np.array([scoreMiniMax])
				predError = (scoreMiniMax - scoreRaw) ** 2
		else:
			if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
				featureMatrix = np.vstack((featureMatrix,features))
				score = np.array([scoreMiniMax])
				scoreVector = np.vstack((scoreVector, score))
				predError += (scoreMiniMax - scoreRaw) ** 2
		timeEnd = time.time()
		print('scoreRaw = {}'.format(scoreRaw))
		print('scoreMiniMax = {}'.format(scoreMiniMax))
		print('move = {}'.format(move))
		print('recursions = {}'.format(recursions))
		print 'time used = ' + str(timeEnd - timeStart)
		boardNow = boardNow.takeMove(move)
		boardNow.printBoard()
		sys.stdout.flush()
		player = 3 - player
		if (boardNow.isEndGame()):
			break
	if turn >= 250:
		print "################################################################################"
		print "################                STUCK                         ##################"
		print "################################################################################"
	timeEnd = time.time()
	result = np.linalg.lstsq(featureMatrix, scoreVector)
	weightsNew = result[0]
	weightsNew = weightsNew.reshape((3,))
	weightsNew = weightsNew / np.linalg.norm(weightsNew)
	SSR = result[1][0]
	SST = np.linalg.norm(scoreVector - np.average(scoreVector)) ** 2
	RSquare = 1 - SSR / SST
	AARVec.append(SSR / turn)
	RSquareVec.append(RSquare)
	weightsGrad = np.linalg.norm(weights - weightsNew)
	weightsGradVec.append(weightsGrad)
	predError = math.sqrt(predError / turn)
	predErrorVec.append(predError)
	AAR = math.sqrt(SSR / turn)

	print ('Number of turns = {}'.format(turn))
	print ('weightsNew = {}'.format(weightsNew))
	print ('RSquare = {}'.format(RSquare))
	print ('AAR = {}'.format(AAR))
	print ('predError = {}'.format(predError))
	print ('weightsGrad = {}'.format(weightsGrad))
	sys.stdout.flush()

	if (gameCount <= 5) :
		weights = weightsNew
	else :
		weightsSum = weightsSum + weightsNew
		weights = weightsSum / (gameCount - 5)
		weights = weights / np.linalg.norm(weights)

	print('\n ##################### \n Endgame Begins!!!! \n #####################')
	while ((not boardNow.isEnd()) and turn < 300) :
		turn = turn + 1
		print('\n\n')
		print('turn = {}'.format(turn))
		print('player = {}'.format(player))
		print('\n')
		boardNow.printBoard()
		timeStart = time.time()
		(scoreGreedy, moveList, recursions) = findMoveGreedy(boardNow, player, 3)
		timeEnd = time.time()
		print('scoreGreedy = {}'.format(scoreGreedy))
		move = moveList[0]
		print('move = {}'.format(move))
		print('recursions = {}'.format(recursions))
		print 'time used = ' + str(timeEnd - timeStart)
		sys.stdout.flush()
		boardNow = boardNow.takeMove(move)
		player = 3 - player
	
print('\n')
print('The RSquare of all games are\n {}'.format(RSquareVec)) 
print('\n')
print('The AAR of all games are\n {}'.format(AARVec))
print('\n')
print('The average prediction error of all games are\n {}'.format(predErrorVec)) 
print('\n')
print('The gradient of weights of all games are\n {}'.format(weightsGradVec))

# plt.plot(range(1, totalGames+1), RSquareVec, 'bo-')
# plt.ylabel('R^2 of each linear regression')
# plt.xlabel('Game')
# plt.savefig('RSquare.pdf')
# plt.show()

# plt.plot(range(1, totalGames+1), AARVec, 'bo-')
# plt.ylabel('AAR of each linear regression')
# plt.xlabel('Game')
# plt.savefig('AAR.pdf')
# plt.show()

# plt.plot(range(1, totalGames+1), predErrorVec, 'bo-')
# plt.ylabel('The average prediction error of the weights of each game')
# plt.xlabel('Game')
# plt.savefig('predError.pdf')
# plt.show()

# plt.plot(range(1, totalGames+1), weightsGradVec, 'bo-')
# plt.ylabel('Norm of gradient of the weights')
# plt.xlabel('Game')
# plt.savefig('weightsGrad.pdf')
# plt.show()

### To test a weights from training, run the code testAWeights.py