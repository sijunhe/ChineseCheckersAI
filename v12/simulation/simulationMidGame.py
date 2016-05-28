# This file is used to test a weight. To be specific, both players play the game with this weights, and this file will keep track of each step

#print('\n\n\n\n\n\n\n\n')
print "################################################################################"
import copy, time, sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from boardState import *
from computeLegalMove import * 
from computeFeatures import *
from computeMinimax import *
from randomMove import *
import numpy as np 

aaaaa = [10, 1, 1]
weights = np.array(aaaaa)
weights = weights / np.linalg.norm(weights)
cantGo1 = []
cantGo2 = []
# featureMatrix = np.array([[]])
# scoreVector = np.array([])
gameCount = 0
playerOneGameWon = 0
playerTwoGameWon = 0
totalGames = 1
while gameCount < totalGames:
	gameCount += 1
## Startgame begins!
	turn = 0
	boardStart = boardState(options = 'smallGame') # fullGame, smallGame
	#print "Orginal Board"
	#boardStart.printBoard()
	boardNow = boardStart
	player = 1

	while (turn < 249) :
		turn = turn + 1
		timeGameStart = time.time()

		# print('\n\n')
		print('turn = {}'.format(turn))
		# print('player = {}'.format(player))
		# print('\n')
		# boardNow.printBoard()
		timeStart = time.time()
		if (player == 1) :
			# (scoreMaxiMax, moveList, recursions) = computeMaximax(boardNow, player, weights, 2, cantGo1)
			# move = moveList[0]
			# cantGo1.append(move)
			# if (len(cantGo1) >= 5) :
			# 	cantGo1.pop(0)
			move = randomMove(boardNow, player)
		else :
			(scoreMaxiMax, moveList, recursions) = computeMinimax(boardNow, player, weights, 2, cantGo2)
			move = moveList[0]
			cantGo2.append(move)
			if (len(cantGo2) >= 5) :
				cantGo2.pop(0)
		timeEnd = time.time()
		# print('move = {}'.format(move))
		# print('recursions = {}'.format(recursions))
		print 'time used = ' + str(timeEnd - timeStart)
		sys.stdout.flush()
		boardNow = boardNow.takeMove(move)
		player = 3 - player
		if (boardNow.isBattleField(2)) :
			print('\n##################################################################')
			print('#####################  Battlefield Begins!!!!  #####################')
			print('#####################  Let\'s fight for it!!!!  #####################')
			print('####################################################################')
			break

	turnAtBattleField = turn + 1

	### Battlefield begins!
	while ((not boardNow.isEnd()) and turn < 250) :
		turn = turn + 1
		timeStart = time.time()
		features = computeFeaturesFull(boardNow)
		#scoreRaw = np.inner(features, weights)

		# print('\n\n')
		print('turn = {}'.format(turn))
		# print('player = {}'.format(player))
		# print('\n')
		# boardNow.printBoard()
		# print('features = {}'.format(features))
		# print('weights = {}'.format(weights))

		if (player == 1) :
			move = randomMove(boardNow, player)
			# (scoreMiniMax, moveList, recursions) = computeMinimax(boardNow, player, weights, 4, cantGo1)
			# move = moveList[0]
			# cantGo1.append(move)
			# if (len(cantGo1) >= 5) :
			# 	cantGo1.pop(0)
		else :
			(scoreMiniMax, moveList, recursions) = computeMinimax(boardNow, player, weights, 2, cantGo2)
			move = moveList[0]
			cantGo2.append(move)
			if (len(cantGo2) >= 5) :
				cantGo2.pop(0)
		
		# if turn == turnAtBattleField:
		# 	if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
		# 		featureMatrix = features
		# 		scoreVector = np.array([scoreMiniMax])
		# else:
		# 	if scoreMiniMax != 10 ** 5 and scoreMiniMax != -10 ** 5:
		# 		featureMatrix = np.vstack((featureMatrix,features))
		# 		score = np.array([scoreMiniMax])
		# 		scoreVector = np.vstack((scoreVector, score))


		timeEnd = time.time()	
		# print('scoreRaw = {}'.format(scoreRaw))
		# print('scoreMiniMax = {}'.format(scoreMiniMax))
		# print('move = {}'.format(move))
		# print('recursions = {}'.format(recursions))
		print 'time used = ' + str(timeEnd - timeStart)
		sys.stdout.flush()
		boardNow = boardNow.takeMove(move)
		player = 3 - player
		if (boardNow.isEndGame(1)) :
			print('\n################################################################')
			print('#####################  Endgame Begins!!!!  #####################')
			print('#####################  Let\'s go go go!!!!  #####################')
			break

	### Endgame playing
	while ((not boardNow.isEnd()) and turn < 250) :
		turn = turn + 1
		#print('\n\n')
		print('turn = {}'.format(turn))
		#print('player = {}'.format(player))
		#print('\n')
		#boardNow.printBoard()

		timeStart = time.time()
		#print ('All possible moves = {}'.format(computeLegalMove(boardNow, player)))
		#print ('All forward moves = {}'.format(computeLegalMoveForward(boardNow, player, -1)))
		if (player == 2) :
			numPossibleMoves = len(computeLegalMoveForward(boardNow, player, -1))
			if (numPossibleMoves > 20) :
				greedyDepth = 2
			elif (numPossibleMoves > 12) :
				greedyDepth = 3
			else :
				greedyDepth = 4
			#print ('greedyDepth = {}'.format(greedyDepth))
			(scoreGreedy, moveList, recursions) = findMoveGreedy(boardNow, player, greedyDepth)
			#timeEnd = time.time()
			#print('scoreGreedy = {}'.format(scoreGreedy))
			move = moveList[0]
			#print('move = {}'.format(move))
			#print('recursions = {}'.format(recursions))
		else:
			move = randomMove(boardNow, player)
		timeEnd = time.time()
		print 'time used = ' + str(timeEnd - timeStart)
		sys.stdout.flush()
		boardNow = boardNow.takeMove(move)
		player = 3 - player


	if turn >= 250:
		print "################################################################################"
		print "################                STUCK                         ##################"
		print "################################################################################"

	print('\n\n')
	timeGameEnd = time.time()
	print "game took" + str(timeGameEnd - timeGameStart)
	print boardNow.isEnd()
	if boardNow.isEnd() == 1:
		print "player 1 won"
		playerOneGameWon += 1
	elif boardNow.isEnd() == -1:
		print "player 2 won"
		playerTwoGameWon += 1

	sys.stdout.flush()
	# boardNow.printBoard()
	# result = np.linalg.lstsq(featureMatrix, scoreVector)
	# weightsNew = result[0]
	# residuals = np.dot(featureMatrix, weightsNew) - scoreVector
	# SSR = result[1][0]
	# SST = np.linalg.norm(scoreVector - np.average(scoreVector)) ** 2
	# RSquare = 1 - SSR / SST
	# weightsNew = weightsNew.reshape((3,))
	# weightsNew = weightsNew / np.linalg.norm(weightsNew)

	# print ('Number of turns = {}'.format(turn))
	# print ('weightsNew = {}'.format(weightsNew))
	# print ('SSR = {}'.format(SSR))
	# print ('RSquare = {}'.format(RSquare))
