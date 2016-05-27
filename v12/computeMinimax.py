from boardState import *
from computeLegalMove import *
from computeFeatures import *
import numpy as np
import Queue


def computeMaximax(board, player, weights, depth, cantGo):
	recursions = 0;
	if (depth == 0) :
		features = computeFeaturesFull(board)
		score = np.inner(features, weights)
		moveList = []
		recursions = 1
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
	# recursions = recursions + 1
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


def findMoveGreedy(board, player, depth) :
	# print 'findMoveGreedy'
	# board.printBoard()
	# print 'player = ' + str(player)
	# print 'depth = ' + str(depth)
	recursions = 1
	moveList = []
	if (depth == 0) :
		score = computeScoreEndgame(board, player)
	else :
		allPossibleMoves = computeLegalMoveForward(board, player, 0)
		score = -10 ** 5
		for move in allPossibleMoves :
			boardNext = board.takeMove(move)
			if (boardNext.isEnd() == player) :
				score = 100 ** depth
				moveList = [move]
				return (score, moveList, recursions)
			(scoreNext, MLNext, recursionsNext) = findMoveGreedy(boardNext, player, depth - 1)
			recursions += recursionsNext
			if (scoreNext > score) :
				score = scoreNext
				moveList = [move]
				moveList.extend(MLNext)
	return (score, moveList, recursions)


def computeScoreEndgame(board, player) :
	score = 0
	if (player == 1) :
		for (i, j) in board.PositionOne :
			score -= (board.height - i - 1) ** 2
			if (i == board.height - 1) :
				score += 9
			elif (i == board.height - 2) :
				score += 7
			elif (i == board.height - 3) :
				score += 5
			elif (i == board.height - 4) :
				score += 2
	else :
		for (i, j) in board.PositionTwo :
			score -= i ** 2
			if (i == 0) :
				score += 9
			elif (i == 1) :
				score += 7
			elif (i == 2) :
				score += 5
			elif (i == 3) :
				score += 2
	return score

