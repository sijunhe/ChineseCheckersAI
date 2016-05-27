from computeLegalMove import *
import random

'''
A greedy player that takes the move that moves up the vertical axis the most
If multiple such moves exist, take a random move among the best moves
'''	
def randomMove(board, player):
	possibleMove = computeLegalMove(board, player)
	if player == 1:
		rankedMove = sorted(possibleMove, key= lambda (i,j,nexti, nextj): nexti - i, reverse = True)
		rankedVerticalDistance = [nexti - i for (i,j,nexti, nextj) in rankedMove]
		maxMove = rankedVerticalDistance[0]
		for i in range(1, len(rankedVerticalDistance)):
			if rankedVerticalDistance[i] != maxMove:
				break
		
	if player == 2:
		rankedMove = sorted(possibleMove, key= lambda (i,j,nexti, nextj): nexti - i)
		rankedVerticalDistance = [nexti - i for (i,j,nexti, nextj) in rankedMove]
		maxMove = rankedVerticalDistance[0]
		for i in range(1, len(rankedVerticalDistance)):
			if rankedVerticalDistance[i] != maxMove:
				break

	if i == 0:
		nextMove = rankedMove[0]
	else:
		randNumber = random.randint(0, i)
		nextMove = rankedMove[randNumber]
	# print possibleMove
	# print rankedMove
	# print rankedVerticalDistance
	# print randNumber

	return nextMove



	