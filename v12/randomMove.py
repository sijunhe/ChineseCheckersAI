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



'''
A greedy player that takes the numSteps consecutive moves to achieve the maximal vertical advance after numSteps steps, and return the first move of this series of moves;
If multiple such moves exist, take a random move among the best moves
'''	
def randomMoveMultistep(board, player, numSteps = 1):
	if (numSteps == 0) :
		maxAdvance = 0
		possibleMove = []
		optimalMoves = []
		optimalMove = []
	else :
		maxAdvance = -100
		optimalMoves = []
		possibleMove = computeLegalMove(board, player)
		if (player == 1) :
			for (i1, j1, i2, j2) in possibleMove :
				boardNext = board.takeMove((i1, j1, i2, j2))
				(maxNext, moveNext) = randomMoveMultistep(boardNext, player, numSteps - 1)
				advance = i2 - i1 + maxNext
				if (advance > maxAdvance) :
					maxAdvance = advance
					optimalMoves = [(i1, j1, i2, j2)]
				elif (advance == maxAdvance) :
					optimalMoves.append((i1, j1, i2, j2))
		else :
			for (i1, j1, i2, j2) in possibleMove :
				boardNext = board.takeMove((i1, j1, i2, j2))
				(maxNext, moveNext) = randomMoveMultistep(boardNext, player, numSteps - 1)
				advance = i1 - i2 + maxNext
				if (advance > maxAdvance) :
					maxAdvance = advance
					optimalMoves = [(i1, j1, i2, j2)]
				elif (advance == maxAdvance) :
					optimalMoves.append((i1, j1, i2, j2))
		numMoves = len(optimalMoves)
		randNumber = random.randint(0, numMoves - 1)
		optimalMove = optimalMoves[randNumber]
		# print randNumber
		# print possibleMove
		# print optimalMoves
		# print optimalMove

	return (maxAdvance, optimalMove)



	