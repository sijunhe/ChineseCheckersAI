'''
This code is used to test and compare two strategies in playing Chinese Checkers.
'''
import time, sys, os
from boardState import *
import numpy as np 
from strategies import *


totalGames = 1
gameCount = [0, 0, 0]	# The 0-th element denotes the number of games played so far, i-th denotes the number of games player i wins, i = 1, 2.
cantGo1 = []			# The set of moves player 1 can't make
cantGo2 = []			# The set of moves player 2 can't make
playerOneExtraTurn = []	# Number of moves player 1 loses in each game, negative means player 2 loses

'''
Player One's weights: 
'''
aaaaa = [10, 1, 1]
weights1 = np.array(aaaaa)
weights1 = weights1 / np.linalg.norm(weights1)
'''
Player Two's weights: 
'''
aaaaa = [10, 1, 1]
weights2 = np.array(aaaaa)
weights2 = weights2 / np.linalg.norm(weights2)



while gameCount[0] < totalGames:
	print "################################################################################"
	gameCount[0] += 1
	boardNow = boardState(options = 'midGame') # options can be fullGame, midGame, smallGame
	turn = 0
	player = 1
	timeGameStart = time.time()
	while ((not boardNow.isEnd()) and turn < 250) :
		turn = turn + 1
		timeTurnStart = time.time()
		print('\nGame No. ' + str(gameCount[0]) + ', turn No. ' + str(turn))
		if (player == 1) :
			# move = findMove_GreedyRandom(boardNow, player, 1)
			# move = findMove_GreedyRandom(boardNow, player, 2)
			# move = findMove_MiniMax(boardNow, player, weights1, 2, cantGo1)	## Minimax strategy throughout
			move = findMove_Advanced(boardNow, player, weights1, 2, cantGo2)		## Most advanced strategy
			cantGo1.append(move)
			if (len(cantGo1) >= 5) :
				cantGo1.pop(0)
		else :
			# move = findMove_GreedyRandom(boardNow, player, 1)
			# move = findMove_GreedyRandom(boardNow, player, 2)
			move = findMove_MiniMax(boardNow, player, weights2, 2, cantGo1)	## Minimax strategy throughout
			# move = findMove_Advanced(boardNow, player, weights2, 2, cantGo2)		## Most advanced strategy
			cantGo2.append(move)
			if (len(cantGo2) >= 5) :
				cantGo2.pop(0)
		
		timeTurnEnd = time.time()
		print 'Time used = ' + str(timeTurnEnd - timeTurnStart) + " seconds."
		print('move = {}'.format(move))
		sys.stdout.flush()
		
		boardNow = boardNow.takeMove(move)
		player = 3 - player

	timeGameEnd = time.time()
	print "\n\nGame " + str(gameCount[0]) + " took " + str(timeGameEnd - timeGameStart) + " seconds."
	if (turn == 250) :
		print 'Game Stuck!!!'
	else :
		winner = boardNow.isEnd()
		loser = 3 - winner
		print 'Player ' + str(winner) + ' won!! ' + "Player " + str(loser) + " starts endGame counting:"
		gameCount[winner] += 1
		sys.stdout.flush()

		extraTurn = 0
		while (boardNow.isEnd() == 0 or boardNow.isEnd() == winner):
			if (extraTurn >= 250) :
				print 'EndGame Stuck!!!!'
				break
			extraTurn += 1
			print('\nextra turn = {}'.format(extraTurn))
			boardNow.printBoard()
			move = findMove_EndGame(boardNow, loser)
			sys.stdout.flush()
			boardNow = boardNow.takeMove(move)
		playerOneExtraTurn.append((-1)**winner * extraTurn)

	
print "player one won " + str(gameCount[1]) + " games"
print "player two won " + str(gameCount[2]) + " games"
print "Extra turns of Player 1 is:"
print playerOneExtraTurn

