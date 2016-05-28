# This file is used to test a weight. To be specific, both players play the game with this weights, and this file will keep track of each step

#print('\n\n\n\n\n\n\n\n')
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
playerOneGameWon = playerTwoGameWon = 0
playerOneExtraTurn = playerTwoExtraTurn = 0
totalGames = 1
while gameCount < totalGames:
	print "################################################################################"
	gameCount += 1
## Startgame begins!
	turn = 0
	boardStart = boardState(options = 'midGame') # fullGame, smallGame
	#print "Orginal Board"
	#boardStart.printBoard()
	boardNow = boardStart
	player = 1
	timeGameStart = time.time()
	### Battlefield begins!
	while ((not boardNow.isEnd()) and turn < 250) :
		turn = turn + 1
		timeStart = time.time()
		features = computeFeaturesFull(boardNow)

		print('turn = {}'.format(turn))
		
		if (player == 1) :
			move = randomMoveMultistep(boardNow, player, 2)[1]
		
		else :
			(scoreMiniMax, moveList, recursions) = computeMinimax(boardNow, player, weights, 2, cantGo2)
			move = moveList[0]
			cantGo2.append(move)
			if (len(cantGo2) >= 5) :
				cantGo2.pop(0)
		
		timeEnd = time.time()	
		print 'time used = ' + str(timeEnd - timeStart)
		sys.stdout.flush()
		boardNow = boardNow.takeMove(move)
		player = 3 - player

	timeGameEnd = time.time()
	print "game " + str(gameCount) + " took " + str(timeGameEnd - timeGameStart) + " seconds"
	if boardNow.isEnd() == 1:
		print "player 1 won"
		playerOneGameWon += 1
	elif boardNow.isEnd() == 2:
		print "player 2 won"
		playerTwoGameWon += 1

	sys.stdout.flush()
	if boardNow.isEnd() == 1:
		## player 1 won, player 2 finish the game with endGame moves
		print "Player 1 finishes, player 2 starts endGame counting"
		extraTurn = 0
		player = 2
		while (boardNow.isEnd() != 2):
			extraTurn += 1
			print('extra turn = {}'.format(extraTurn))
			numPossibleMoves = len(computeLegalMoveForward(boardNow, player, -1))
			if (numPossibleMoves > 20) :
				greedyDepth = 2
			elif (numPossibleMoves > 12) :
				greedyDepth = 3
			else :
				greedyDepth = 4
			(scoreGreedy, moveList, recursions) = findMoveGreedy(boardNow, player, greedyDepth)
			move = moveList[0]
			sys.stdout.flush()
			boardNow = boardNow.takeMove(move)
			boardNow.printBoard()
		playerTwoExtraTurn.append(extraTurn)

	elif boardNow.isEnd() == 2:
		## player 2 won, player 1 finish the game with endGame moves
		print "Player 2 finishes, player 1 starts endGame counting"
		extraTurn = 0
		player = 1
		while (boardNow.isEnd() != 1):
			extraTurn += 1
			print('extra turn = {}'.format(extraTurn))
			boardNow.printBoard()
			numPossibleMoves = len(computeLegalMoveForward(boardNow, player, -1))
			if (numPossibleMoves > 20) :
				greedyDepth = 2
			elif (numPossibleMoves > 12) :
				greedyDepth = 3
			else :
				greedyDepth = 4
			(scoreGreedy, moveList, recursions) = findMoveGreedy(boardNow, player, greedyDepth)
			move = moveList[0]
			print scoreGreedy
			print moveList
			sys.stdout.flush()
			boardNow = boardNow.takeMove(move)
		playerOneExtraTurn.append(extraTurn)
	
print "player one won " + str(playerOneGameWon) + " games"
print "player two won " + str(playerTwoGameWon) + " games"

