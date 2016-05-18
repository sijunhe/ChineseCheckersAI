from boardState import *
import copy 

'''
Public Method
Find all legal moves, including 1 roll and repetitive hops
'''	
def computeLegalMove(board, player):
	possibleMoveBoard = []
	if player == 1:
		myPosition = board.PositionOne
	elif player == 2:
		myPosition = board.PositionTwo
	for (i, j) in myPosition:
		## current piece x and y position
		rollMoves = findLegalRoll(board, i,j)
		for (nexti, nextj) in rollMoves:
			possibleMoveBoard.append(((i,j),(nexti, nextj)))
		possibleMoveBoard += computeRepetitiveHop(board, i,j)

	allPossibleMove = []
	for ((oldi, oldj),(newi, newj)) in possibleMoveBoard:
		move = (oldi, oldj, newi, newj)
		allPossibleMove.append(move)
	return allPossibleMove

'''
Private Method
Find a legal roll moves, given the coordinate of a piece
'''	
def findLegalRoll(board, i, j):
	rollMoves = []
	if i + 1 < board.height:
		if j + 1 < board.mid_width_max:
		## can go down right? 
			if board.board[i+1][j+1] == 0:
				rollMoves.append((i+1, j+1))

		if j - 1 >= 0:
			if board.board[i+1][j-1] == 0:
		## can go down left?
				rollMoves.append((i+1, j-1))

	if i - 1 >= 0:
		if j + 1 < board.mid_width_max:
		## can go up right? 
			if board.board[i-1][j+1] == 0:
				rollMoves.append((i-1, j+1))
		if j - 1 >= 0:
			if board.board[i-1][j-1] == 0:
		## can go up left?
				rollMoves.append((i-1, j-1))

	return rollMoves
	
'''
Public Method computeRepetitiveHop
Compute repetitive hop for a piece, given the coordinate hopi and hopj
Calls computeRepetitiveHopRecursion
'''	
def computeRepetitiveHop(board, hopi, hopj):
	possibleMoveBoard = []
	pastPosition = {}
	pastPosition[(hopi, hopj)] = 1
	for (basei, basej) in board.allPosition:
		hopMove= findLegalHop(board, hopi, hopj, basei, basej)
		if hopMove is not None:
			(nexti, nextj) = hopMove
			if (nexti, nextj) not in pastPosition:
				pastPosition[(nexti, nextj)] = 1
				futureBoard = copy.deepcopy(board.board)
				futureBoard[hopi][hopj] = 0
				futureBoard[nexti][nextj] = 1	
				possibleMoveBoard.append(((hopi,hopj),(nexti, nextj)))
				if board.fullGame == 0:
					futureboard = boardState(options = 'smallGame', inputBoard = futureBoard)
				else:
					futureboard = boardState(options = 'fullGame', inputBoard = futureBoard)
				computeRepetitiveHopRecursion(board, hopi, hopj, nexti, nextj, pastPosition, possibleMoveBoard)
	
	return possibleMoveBoard



'''
Private
Compute repetitive hop for a piece, given the coordinate hopi and hopj
Find a legal hop moves, given the cooridnate of a piece and the base
'''	
def computeRepetitiveHopRecursion(board, origini, originj, hopi, hopj, pastPosition, possibleMoveBoard):
	for (basei, basej) in board.allPosition:
		hopMove= findLegalHop(board, hopi, hopj, basei, basej)
		if hopMove is not None:
			(nexti, nextj) = hopMove
			if (nexti, nextj) not in pastPosition:
				#print "piece " + str(hopi) + " " + str(hopj) + " going " + str(nexti) + " " + str(nextj)
				pastPosition[(nexti, nextj)] = 1
				futureBoard = copy.deepcopy(board.board)
				futureBoard[hopi][hopj] = 0
				futureBoard[nexti][nextj] = 1
				possibleMoveBoard.append(((origini, originj),(nexti, nextj)))	
				if board.fullGame == 0:
					futureboard = boardState(options = 'smallGame', inputBoard = futureBoard)
				else:
					futureboard = boardState(options = 'fullGame', inputBoard = futureBoard)
				#futureboard.printBoard()
				computeRepetitiveHopRecursion(board, origini, originj, nexti, nextj, pastPosition, possibleMoveBoard)

'''
Private
Find a legal hop moves, given the cooridnate of a piece and the base
'''	
def findLegalHop(board, hopi, hopj, basei, basej):
	hopMove = None
	if isAdjacent(hopi, hopj, basei, basej):
		diffi = basei - hopi
		diffj = basej - hopj
		nexti = basei + diffi
		nextj = basej + diffj
		if nexti < board.height and nextj < board.mid_width_max:
			if board.board[nexti][nextj] == 0:
				hopMove = (nexti, nextj)
			
	return hopMove

'''
Private
Return if two pieces are next to each other
'''	
def isAdjacent(Ai, Aj, Bi, Bj):
	if abs(Ai - Bi) == 1:
		if abs(Aj - Bj) == 1:
			return True

	elif abs(Ai - Bi) == 0:
		if abs(Aj - Bj) == 2:
			return True
	else:
		return False