from boardState import *
from computeLegalMove import * 
from computeFeatures import *
from strategies import *
from strategiesHelpers import *
import numpy as np 
import copy,time, math, sys
#import matplotlib.pyplot as plt

'''
Initialize weights
'''
aaaaa = [10, 1, 1]
weights = np.array(aaaaa)
weights = weights / np.linalg.norm(weights)
weightsSum = np.zeros(3)
depth = 2 #Can only be even numbers: 2, 4, 6, ...
totalGames = 40


# Learn the weights using linear regression
gameCount = 0
AARVec = []
RSquareVec = []
weightsGradVec = []
predErrorVec = []
while gameCount < totalGames:
	print "################################################################################"
	gameCount += 1
	print('Game = No. {}'.format(gameCount))
	boardNow = boardState(options = 'smallGame') # fullGame, smallGame, midGame
	error = 0
	player = 1
	turn = 0
	cantGo1 = []
	cantGo2 = []
	print ('weightsNow = {}'.format(weights))

	while ((not boardNow.isEnd()) and turn < 249) :
		turn = turn + 1
		# print('\nGame No. ' + str(gameCount) + ', turn No. ' + str(turn))
		# boardNow.printBoard()
		timeStart = time.time()
		if (player == 1) :
			(scoreMaxiMax, move, recursions) = computeMaximax(boardNow, player, weights, depth / 2, cantGo1)
			cantGo1.append(move)
			if (len(cantGo1) >= 5) :
				cantGo1.pop(0)
		else :
			(scoreMaxiMax, move, recursions) = computeMaximax(boardNow, player, weights, depth / 2, cantGo2)
			cantGo2.append(move)
			if (len(cantGo2) >= 5) :
				cantGo2.pop(0)
		timeEnd = time.time()
		# print('move = {}'.format(move))
		# print('recursions = {}'.format(recursions))
		# print 'time used = ' + str(timeEnd - timeStart)
		boardNow = boardNow.takeMove(move)
		player = 3 - player
		if (boardNow.isBattleField(2)) :
			# print('\n##################################################################')
			# print('#####################  Battlefield Begins!!!!  #####################')
			# print('#####################  Let\'s fight for it!!!!  #####################')
			# boardNow.printBoard()
			# print('####################################################################')
			break

	firstBattleFieldTurn = turn + 1

	'''
	### Battlefield begins!
	'''
	while ((not boardNow.isEnd()) and turn < 250) :
		turn = turn + 1
		# print('\nGame No. ' + str(gameCount) + ', turn No. ' + str(turn))
		# boardNow.printBoard()
		timeStart = time.time()
		features = computeFeaturesFull(boardNow)
		scoreRaw = np.inner(features, weights)
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
			if scoreMiniMax <= 10 ** 3 and scoreMiniMax >= -10 ** 3:
				featureMatrix = features
				scoreVector = np.array([scoreMiniMax])
				predError = (scoreMiniMax - scoreRaw) ** 2
		else:
			if scoreMiniMax <= 10 ** 5 and scoreMiniMax >= -10 ** 5:
				featureMatrix = np.vstack((featureMatrix,features))
				score = np.array([scoreMiniMax])
				scoreVector = np.vstack((scoreVector, score))
				predError += (scoreMiniMax - scoreRaw) ** 2
		timeEnd = time.time()
		# print('scoreRaw = {}'.format(scoreRaw))
		# print('scoreMiniMax = {}'.format(scoreMiniMax))
		# print('move = {}'.format(move))
		# print('recursions = {}'.format(recursions))
		# print 'time used = ' + str(timeEnd - timeStart)
		boardNow = boardNow.takeMove(move)
		sys.stdout.flush()
		player = 3 - player
		if (boardNow.isEndGame(0)):
			# print('\n################################################################')
			# print('#####################  Endgame Begins!!!!  #####################')
			# print('#####################  Let\'s go go go!!!!  #####################')
			# boardNow.printBoard()
			# print('################################################################')
			break
	
	'''
	We don't need the following EndGame turns to tune our weights
	'''
	# while ((not boardNow.isEnd()) and turn < 250) :
	# 	turn = turn + 1
	# 	print('\n\n')
	# 	print('turn = {}'.format(turn))
	# 	print('player = {}'.format(player))
	# 	print('\n')
	# 	boardNow.printBoard()

	# 	timeStart = time.time()
	# 	move = findMove_EndGame(boardNow, player)
	# 	timeEnd = time.time()
	# 	print('move = {}'.format(move))
	# 	print 'time used = ' + str(timeEnd - timeStart)
	# 	boardNow = boardNow.takeMove(move)
	# 	player = 3 - player

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
	print ('Number of turns in training = {}'.format(turn - firstBattleFieldTurn + 1))
	print ('weightsNew = {}'.format(weightsNew))
	print ('RSquare = {}'.format(RSquare))
	print ('AAR = {}'.format(AAR))
	print ('predError = {}'.format(predError))
	print ('weightsGrad = {}'.format(weightsGrad))
	sys.stdout.flush()

	if (gameCount <= 5) :
		weights = weightsNew
	elif (gameCount <= 30) :
		weightsSum = weightsSum + weightsNew
		weights = weightsSum / np.linalg.norm(weightsSum)
	else :
		weights = 25 * weights + weightsNew
		weights = weights / np.linalg.norm(weights)



	
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