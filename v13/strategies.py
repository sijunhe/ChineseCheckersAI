import copy, time, sys, os
from boardState import *
from computeLegalMove import * 
from computeFeatures import *
from strategiesHelpers import *
import numpy as np 

def findMove_GreedyRandom(board, player, depth) :
	move = randomMoveMultistepSquare(board, player, depth)[1]
	return move

def findMove_EndGame(board, player) :
	numPossibleMoves = len(computeLegalMoveForward(board, player, 0))
	if (numPossibleMoves > 20) :
		greedyDepth = 2
	elif (numPossibleMoves > 10) :
		greedyDepth = 3
	else :
		greedyDepth = 4
	move = findMove_EndGame_Helper(board, player, greedyDepth)[1]
	return move

def findMove_MiniMax(board, player, weights, depth, cantGo) :
	(scoreMiniMax, moveList, recursions) = computeMinimax(board, player, weights, depth, cantGo)
	move = moveList[0]
	return move










