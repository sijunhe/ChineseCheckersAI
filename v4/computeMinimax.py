from boardState import *
from computeLegalMove import *
from computeFeatures import *
import numpy as np
import Queue



'''
Public Method
Find Minimax score without using alpha-beta pruning;
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
# def computeMinimax_Helper1(board, player, weights, depth, bound):
# 	recursions = 0;
# 	if (depth <= 1) :
# 		if (player == 1) :
# 			score = - 10 ** 10
# 			allPossibleMoves = computeLegalMove(board, player)
# 			for move in allPossibleMoves :
# 				recursions = recursions + 1
# 				boardNext = board.takeMove(move)
# 				features = computeFeaturesFull(boardNext)
# 				scoreNext = np.inner(features, weights)
# 				if (scoreNext >= bound) :
# 					score = scoreNext
# 					moveList = [move]
# 					return (score, moveList, recursions)
# 				if (scoreNext > score) :
# 					score = scoreNext
# 					moveList = [move]
		
# 		else:
# 			score = 10 ** 10
# 			allPossibleMoves = computeLegalMove(board, player)
# 			for move in allPossibleMoves :
# 				recursions = recursions + 1
# 				boardNext = board.takeMove(move)
# 				features = computeFeaturesFull(boardNext)
# 				scoreNext = np.inner(features, weights)
# 				if (scoreNext <= bound) :
# 					score = scoreNext
# 					moveList = [move]
# 					return (score, moveList, recursions)
# 				if (scoreNext < score) :
# 					score = scoreNext
# 					moveList = [move]
		
# 	else :
# 		if (player == 1) :
# 			score = - 10 ** 10
# 			allPossibleMoves = computeLegalMove(board, player)
# 			PQofMoves = Queue.PriorityQueue()
# 			for move in allPossibleMoves :
# 				boardNext = board.takeMove(move)
# 				features = computeFeatures(boardNext)
# 				scoreRaw = np.inner(features, weights)
# 				PQofMoves.put((-scoreRaw, move))
# 			while (not PQofMoves.empty()) :
# 				(scoreRaw, move) = PQofMoves.get()
# 				boardNext = board.takeMove(move)
# 				(scoreNext, MLNext, recursionsNext) = computeMinimax_Helper(boardNext, 3 - player, weights, depth - 1, score)
# 				recursions = recursions + recursionsNext
# 				if (scoreNext >= bound) :
# 					score = scoreNext
# 					moveList = [move]
# 					moveList.extend(MLNext)
# 					return (score, moveList, recursions)
# 				if (scoreNext > score) :
# 					score = scoreNext
# 					moveList = [move]
# 					moveList.extend(MLNext)
# 		else :
# 			score = 10 ** 10
# 			allPossibleMoves = computeLegalMove(board, player)
# 			PQofMoves = Queue.PriorityQueue()
# 			for move in allPossibleMoves :
# 				boardNext = board.takeMove(move)
# 				features = computeFeatures(boardNext)
# 				scoreRaw = np.inner(features, weights)
# 				PQofMoves.put((scoreRaw, move))
# 			while (not PQofMoves.empty()) :
# 				(scoreRaw, move) = PQofMoves.get()
# 				boardNext = board.takeMove(move)
# 				(scoreNext, MLNext, recursionsNext) = computeMinimax_Helper(boardNext, 3 - player, weights, depth - 1, score)
# 				recursions = recursions + recursionsNext
# 				if (scoreNext <= bound) :
# 					score = scoreNext
# 					moveList = [move]
# 					moveList.extend(MLNext)
# 					return (score, moveList, recursions)
# 				if (scoreNext < score) :
# 					score = scoreNext
# 					moveList = [move]
# 					moveList.extend(MLNext)

# 	return (score, moveList, recursions)



def computeMinimax_Helper(board, player, weights, depth, bound, cantGo):
	recursions = 0;
	if (depth == 0) :
		features = computeFeaturesFull(board, player)
		score = np.inner(weights, features)
		moveList = []
		recursions = 1
	else :
		if (player == 1) :
			score = - 10 ** 10
			allPossibleMoves = computeLegalMove(board, player)
			PQofMoves = Queue.PriorityQueue()
			for move in allPossibleMoves :
				boardNext = board.takeMove(move)
				if (boardNext.isEnd() == 1) :
					score = 10 ** 5
					moveList = [move]
					recursions = 1
					return (score, moveList, recursions)
				if ((move not in cantGo) and (boardNext.isEnd() == 0)) :
					features = computeFeatures(board, player)
					scoreRaw = np.inner(weights, features)
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
			allPossibleMoves = computeLegalMove(board, player)
			PQofMoves = Queue.PriorityQueue()
			for move in allPossibleMoves :
				boardNext = board.takeMove(move)
				if (boardNext.isEnd() == -1) :
					score = - 10 ** 5
					moveList = [move]
					recursions = 1
					return (score, moveList, recursions)
				if ((move not in cantGo) and (boardNext.isEnd() == 0)) :
					features = computeFeatures(board, player)
					scoreRaw = np.inner(weights, features)
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
# def computeMinimax_wo(board, player, weights, depth):
# 	# recursions = recursions + 1
# 	recursions = 0;
# 	if (depth == 0) :
# 		features = computeFeaturesFull(board)
# 		score = np.inner(features, weights)
# 		moveList = []
# 		recursions = 1
# 	else :
# 		if (player == 1) :
# 			score = - 10 ** 10
# 			allPossibleMoves = computeLegalMove(board, player)
# 			for move in allPossibleMoves :
# 				boardNext = board.takeMove(move)
# 				(scoreNext, MLNext, recursionsNext) = computeMinimax_wo(boardNext, 3 - player, weights, depth - 1)
# 				recursions = recursions + recursionsNext
# 				if (scoreNext > score) :
# 					score = scoreNext
# 					moveList = [move]
# 					moveList.extend(MLNext)
# 		else :
# 			score = 10 ** 10
# 			allPossibleMoves = computeLegalMove(board, player)
# 			for move in allPossibleMoves :
# 				boardNext = board.takeMove(move)
# 				(scoreNext, MLNext, recursionsNext) = computeMinimax_wo(boardNext, 3 - player, weights, depth - 1)
# 				recursions = recursions + recursionsNext
# 				if (scoreNext < score) :
# 					score = scoreNext
# 					moveList = [move]
# 					moveList.extend(MLNext)

# 	return (score, moveList, recursions)



# def computeScoreRaw(board, weights, player) :
# 	features = computeFeatures(board)
# 	features1 = features[1:5]
# 	features2 = features[5:9]
# 	weightsSelf = weights[1:5]
# 	weightsOppo = weights[5:9]
# 	if (player == 1) :
# 		scoreRaw = features[0] * weights[0] + np.inner(weightsSelf, features1) + np.inner(weightsOppo, features2)
# 	else :
# 		scoreRaw = features[0] * weights[0] + np.inner(weightsSelf, features2) + np.inner(weightsOppo, features1)
# 	return scoreRaw

# def computeScoreRawFull(board, weights, player) :
# 	features = computeFeaturesFull(board)
# 	features1 = features[1:5]
# 	features2 = features[5:9]
# 	weightsSelf = weights[1:5]
# 	weightsOppo = weights[5:9]
# 	if (player == 1) :
# 		scoreRaw = features[0] * weights[0] + np.inner(weightsSelf, features1) + np.inner(weightsOppo, features2)
# 	else :
# 		scoreRaw = features[0] * weights[0] + np.inner(weightsSelf, features2) + np.inner(weightsOppo, features1)
# 	return scoreRaw


