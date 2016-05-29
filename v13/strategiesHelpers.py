from boardState import *
from computeLegalMove import *
from computeFeatures import *
import numpy as np
import Queue
import random






'''
Public Method
Find Minimax score using alpha-beta pruning;
Inputs: board, player, weights, depth;
Outputs: score(minimax score), moveList(list of moves that lead to the minimax-score note), recursions(total number of recursions).
'''	
def computeMinimax(board, player, weights, depth, cantGo):
	if (player == 1) :
		bound = 10 ** 10
	else :
		bound = - 10 ** 10

	return computeMinimax_Helper(board, player, weights, depth, bound, cantGo)



'''
Private helper function used in computeMinimax();
Inputs: board, player, weights, depth, bound(if one branch is below/above this bound, apply pruning);
Outputs: score(minimax score), moveList(list of moves that lead to the minimax-score note), recursions(total number of recursions).
'''
def computeMinimax_Helper(board, player, weights, depth, bound, cantGo):
	recursions = 0;
	if (depth == 0) :
		features = computeFeaturesFull(board)
		score = np.inner(features, weights)
		moveList = []
		recursions = 1
	else :
		if (player == 1) :
			score = - 10 ** 10
			allPossibleMoves = computeLegalMoveForward(board, player, 2)
			PQofMoves = Queue.PriorityQueue()
			for move in allPossibleMoves :
				boardNext = board.takeMove(move)
				if (boardNext.isEnd() == player) :
					score = 10 ** 5
					moveList = [move]
					recursions = 1
					return (score, moveList, recursions)
				if ((move not in cantGo) and (boardNext.isEnd() == 0)) :
					features = computeFeatures(boardNext)
					scoreRaw = np.inner(features, weights)
					PQofMoves.put((-scoreRaw, move))
			while (not PQofMoves.empty()) :
				(scoreRaw, move) = PQofMoves.get()
				boardNext = board.takeMove(move)
				(scoreNext, MLNext, recursionsNext) = computeMinimax_Helper(boardNext, 3 - player, weights, depth - 1, score, [])
				recursions = recursions + recursionsNext
				if (scoreNext >= bound) :
					score = scoreNext
					moveList = [move]
					moveList.extend(MLNext)
					return (score, moveList, recursions)
				if (scoreNext > score) :
					score = scoreNext
					moveList = [move]
					moveList.extend(MLNext)
		else :
			score = 10 ** 10
			allPossibleMoves = computeLegalMoveForward(board, player, 2)
			PQofMoves = Queue.PriorityQueue()
			for move in allPossibleMoves :
				boardNext = board.takeMove(move)
				if (boardNext.isEnd() == player) :
					score = - 10 ** 5
					moveList = [move]
					recursions = 1
					return (score, moveList, recursions)
				if ((move not in cantGo) and (boardNext.isEnd() == 0)) :
					features = computeFeatures(boardNext)
					scoreRaw = np.inner(features, weights)
					PQofMoves.put((scoreRaw, move))
			while (not PQofMoves.empty()) :
				(scoreRaw, move) = PQofMoves.get()
				boardNext = board.takeMove(move)
				(scoreNext, MLNext, recursionsNext) = computeMinimax_Helper(boardNext, 3 - player, weights, depth - 1, score, [])
				recursions = recursions + recursionsNext
				if (scoreNext <= bound) :
					score = scoreNext
					moveList = [move]
					moveList.extend(MLNext)
					return (score, moveList, recursions)
				if (scoreNext < score) :
					score = scoreNext
					moveList = [move]
					moveList.extend(MLNext)

	return (score, moveList, recursions)



'''
Public Method
Find Minimax score without using alpha-beta pruning;
Inputs: board, player, weights, depth;
Outputs: score(minimax score), moveList(list of moves that lead to the minimax-score note), recursions(total number of recursions).
'''	
def computeMinimax_wo(board, player, weights, depth, cantGo):
	recursions = 0;
	if (depth == 0) :
		features = computeFeaturesFull(board)
		score = np.inner(features, weights)
		moveList = []
		recursions = 1
	else :
		if (player == 1) :
			score = - 10 ** 10
			allPossibleMoves = computeLegalMove(board, player)
			for move in allPossibleMoves :
				if (move not in cantGo) :
					boardNext = board.takeMove(move)
					(scoreNext, MLNext, recursionsNext) = computeMinimax_wo(boardNext, 3 - player, weights, depth - 1, [])
					recursions = recursions + recursionsNext
					if (scoreNext > score) :
						score = scoreNext
						moveList = [move]
						moveList.extend(MLNext)
		else :
			score = 10 ** 10
			allPossibleMoves = computeLegalMove(board, player)
			for move in allPossibleMoves :
				if (move not in cantGo) :
					boardNext = board.takeMove(move)
					(scoreNext, MLNext, recursionsNext) = computeMinimax_wo(boardNext, 3 - player, weights, depth - 1, [])
					recursions = recursions + recursionsNext
					if (scoreNext < score) :
						score = scoreNext
						moveList = [move]
						moveList.extend(MLNext)

	return (score, moveList, recursions)



'''
One-side version of computeMinimax()
'''
def computeMaximax(board, player, weights, depth, cantGo):
	recursions = 1;
	if (depth == 0) :
		features = computeFeaturesFull(board)
		score = np.inner(features, weights)
		moveList = []
	else :
		if (player == 1) :
			score = - 10 ** 10
			allPossibleMoves = computeLegalMoveForward(board, player, 1)
			for move in allPossibleMoves :
				if (move not in cantGo) :
					boardNext = board.takeMove(move)
					(scoreNext, MLNext, recursionsNext) = computeMaximax(boardNext, player, weights, depth - 1, [])
					recursions = recursions + recursionsNext
					if (scoreNext > score) :
						score = scoreNext
						moveList = [move]
						moveList.extend(MLNext)
		else :
			score = 10 ** 10
			allPossibleMoves = computeLegalMoveForward(board, player, 1)
			for move in allPossibleMoves :
				if (move not in cantGo) :
					boardNext = board.takeMove(move)
					(scoreNext, MLNext, recursionsNext) = computeMaximax(boardNext, player, weights, depth - 1, [])
					recursions = recursions + recursionsNext
					if (scoreNext < score) :
						score = scoreNext
						moveList = [move]
						moveList.extend(MLNext)

	return (score, moveList, recursions)



'''
Function used in findMove_EndGame
'''
def findMove_EndGame_Helper(board, player, depth) :
	recursions = 1
	if (depth == 0) :
		score = computeScoreEndgame(board, player)
		move = []
	else :
		allPossibleMoves = computeLegalMoveForward(board, player, 0)
		if (len(allPossibleMoves) == 0) :
			print 'Player has no feasible moves here!!! Stuck!!!'
		else :
			score = -10 ** 5
			for moveOption in allPossibleMoves :
				boardNext = board.takeMove(moveOption)
				if (boardNext.isEnd() == player or boardNext.isEnd() == 3) :
					score = 100 ** depth
					move = moveOption
					return (score, move, recursions)
				(scoreNext, moveNext, recursionsNext) = findMove_EndGame_Helper(boardNext, player, depth - 1)
				recursions += recursionsNext
				if (scoreNext > score) :
					score = scoreNext
					move = moveOption
	return (score, move, recursions)



'''
Function used in findMove_EndGame_helper(), to evaluate an endgame board.
'''
def computeScoreEndgame(board, player) :
	score = 0
	if (player == 1) :
		for (i, j) in board.PositionOne :
			score -= (board.height - i - 1) ** 2
			if (i == board.height - 1) :
				score += 12
			elif (i == board.height - 2) :
				score += 6
			elif (i == board.height - 3) :
				score += 2
	else :
		for (i, j) in board.PositionTwo :
			score -= i ** 2
			if (i == 0) :
				score += 12
			elif (i == 1) :
				score += 6
			elif (i == 2) :
				score += 2
	return score



'''
A greedy player that takes the numSteps consecutive moves to achieve the maximal vertical advance after numSteps steps, and return the first move of this series of moves;
If multiple such moves exist, take a random move among the best moves
'''	
def randomMoveMultistepSquare(board, player, numSteps = 1):
	if (numSteps == 0) :
		maxAdvanceSq = 0
		possibleMove = []
		optimalMoves = []
		optimalMove = []
	else :
		maxAdvanceSq = -100
		optimalMoves = []
		possibleMove = computeLegalMoveForward(board, player, 0)
		if (player == 1) :
			for (i1, j1, i2, j2) in possibleMove :
				boardNext = board.takeMove((i1, j1, i2, j2))
				(maxNextSq, moveNext) = randomMoveMultistep(boardNext, player, numSteps - 1)
				advanceSq = maxNextSq + (board.height - i1)**2 - (board.height - i2)**2
				if (advanceSq > maxAdvanceSq) :
					maxAdvanceSq = advanceSq
					optimalMoves = [(i1, j1, i2, j2)]
				elif (advanceSq == maxAdvanceSq) :
					optimalMoves.append((i1, j1, i2, j2))
		else :
			for (i1, j1, i2, j2) in possibleMove :
				boardNext = board.takeMove((i1, j1, i2, j2))
				(maxNextSq, moveNext) = randomMoveMultistep(boardNext, player, numSteps - 1)
				advanceSq = maxNextSq + i1**2 - i2**2 
				if (advanceSq > maxAdvanceSq) :
					maxAdvanceSq = advanceSq
					optimalMoves = [(i1, j1, i2, j2)]
				elif (advanceSq == maxAdvanceSq) :
					optimalMoves.append((i1, j1, i2, j2))
		numMoves = len(optimalMoves)
		randNumber = random.randint(0, numMoves - 1)
		optimalMove = optimalMoves[randNumber]
		# print randNumber
		# print possibleMove
		# print optimalMoves
		# print optimalMove

	return (maxAdvanceSq, optimalMove)


	
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
		possibleMove = computeLegalMoveForward(board, player)
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

	return nextMove