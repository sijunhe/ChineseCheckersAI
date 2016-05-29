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
	move = computeMinimax(board, player, weights, depth, cantGo)[1]
	return move


def findMove_Advanced(board, player, weights, depth, cantGo) :
	if (board.isBattleField(2)) :
		move = computeMinimax(board, player, weights, depth, cantGo)[1]
	elif (board.isEndGame(0)) :
		move = findMove_EndGame(board, player)
	else :
		move = computeMaximax(board, player, weights, depth / 2 + 1, cantGo)[1]
	return move







