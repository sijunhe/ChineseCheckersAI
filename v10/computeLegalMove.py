from boardState import *
import copy 


'''
Public Method
Find all legal moves of a specific  (i, j), including 1 roll and repetitive hops
'''	
def computeLegalMoveSpecify(board, player, i, j):
	possibleMoveBoard = []
	if player == 1:
		myPosition = board.PositionOne
	elif player == 2:
		myPosition = board.PositionTwo
	if (i, j) not in myPosition :
		return possibleMoveBoard

	rollMoves = findLegalRoll(board, i,j)
	for (nexti, nextj) in rollMoves:
		possibleMoveBoard.append((i,j, nexti, nextj))
	possibleMoveBoard += computeRepetitiveHop(board, i,j)

	return possibleMoveBoard

'''
Public Method
Find all legal moves forward that only allows for backing n in height
'''	
def computeLegalMoveForward(board, player, maxBackwardDistance = 1):
	possibleMoveBoard = []
	AllPossibleMoves = computeLegalMove(board, player)
	if player == 1:
	# 	myPosition = board.PositionOne
	# 	for (i, j) in myPosition:
	# 	## current piece x and y position
	# 		rollMoves = findLegalRoll(board, i,j)
	# 		for (nexti, nextj) in rollMoves:
	# 			if (nexti - i >= -maxBackwardDistance):
	# 				possibleMoveBoard.append((i,j,nexti, nextj))
	# 	possibleHops = computeRepetitiveHop(board, i,j)
	# 	for (i, j,nexti, nextj) in possibleHops:
	# 		if (nexti - i >= -maxBackwardDistance):
	# 			possibleMoveBoard.append((i,j,nexti, nextj))
		for (i, j,nexti, nextj) in AllPossibleMoves :
			if (nexti - i >= -maxBackwardDistance):
				possibleMoveBoard.append((i,j,nexti, nextj))

	elif player == 2:
		# myPosition = board.PositionTwo
		# for (i, j) in myPosition:
		# ## current piece x and y position
		# 	rollMoves = findLegalRoll(board, i,j)
		# 	for (nexti, nextj) in rollMoves:
		# 		if (nexti - i <= maxBackwardDistance):
		# 			possibleMoveBoard.append((i,j,nexti, nextj))
		# possibleHops = computeRepetitiveHop(board, i,j)
		# for (i, j,nexti, nextj) in possibleHops:
		# 	if (nexti - i <= maxBackwardDistance):
		# 		possibleMoveBoard.append((i,j,nexti, nextj))
		for (i, j,nexti, nextj) in AllPossibleMoves :
			if (nexti - i <= maxBackwardDistance):
				possibleMoveBoard.append((i,j,nexti, nextj))
	return possibleMoveBoard

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
			possibleMoveBoard.append((i,j,nexti, nextj))
		possibleMoveBoard += computeRepetitiveHop(board, i,j)
	return possibleMoveBoard

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

	if j + 2 < board.mid_width_max:
		if board.board[i][j+2] == 0:
			rollMoves.append((i, j+2))

	if j - 2 >= 0:
		if board.board[i][j-2] == 0:
			rollMoves.append((i, j-2))



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
	hopMoves= findLegalHop(board, hopi, hopj)
	if hopMoves is not None:
		for hopMove in hopMoves:
			(nexti, nextj) = hopMove
			if (nexti, nextj) not in pastPosition:
				#print "piece " + str(hopi) + " " + str(hopj) + " going " + str(nexti) + " " + str(nextj)
				pastPosition[(nexti, nextj)] = 1
				futureBoard = copy.deepcopy(board.board)
				futureBoard[hopi][hopj] = 0
				futureBoard[nexti][nextj] = 1
				possibleMoveBoard.append((hopi, hopj,nexti, nextj))	
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
	hopMoves= findLegalHop(board, hopi, hopj)
	if hopMoves is not None:
		for hopMove in hopMoves:
			(nexti, nextj) = hopMove
			if (nexti, nextj) not in pastPosition:
				#print "piece " + str(hopi) + " " + str(hopj) + " going " + str(nexti) + " " + str(nextj)
				pastPosition[(nexti, nextj)] = 1
				futureBoard = copy.deepcopy(board.board)
				futureBoard[hopi][hopj] = 0
				futureBoard[nexti][nextj] = 1
				possibleMoveBoard.append((origini, originj,nexti, nextj))	
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
def findLegalHop(board, hopi, hopj):
	hopMove = []
	for i in range(1,7):
		move = isMoveable(board, hopi, hopj, i, maxDistance = 10)
		if move is not None:
			hopMove.append(move)
	return hopMove

'''
Private
Return the possible move of going 1 direction
'''	
def isMoveable(board, Ai, Aj, direction, maxDistance = 10000):
	if direction == 1:
		## move down right
		distance = 1
		nexti = Ai - 1
		nextj = Aj + 1
		while isInBound(board, nexti, nextj) and board.board[nexti][nextj] == 0 and distance < maxDistance:
			distance += 1
			nexti -= 1
			nextj += 1
		if not isInBound(board, nexti, nextj):
			return None
		if board.board[nexti][nextj] == 1 or board.board[nexti][nextj] == 2:
			targeti = nexti - distance
			targetj = nextj + distance
			if isInBound(board, targeti, targetj):
				if board.board[targeti][targetj] == 0:
					while nexti != targeti and nextj != targetj:
						nexti -= 1
						nextj += 1
						if board.board[nexti][nextj] != 0:
							return None
					return (targeti, targetj)
	if direction == 2:
		## move right
		distance = 1
		nexti = Ai
		nextj = Aj + 2
		while isInBound(board, nexti, nextj) and board.board[nexti][nextj] == 0 and distance < maxDistance:
			distance += 1
			nextj += 2
		if not isInBound(board, nexti, nextj):
			return None
		if board.board[nexti][nextj] == 1 or board.board[nexti][nextj] == 2:
			targeti = nexti
			targetj = nextj + 2 * distance
			if isInBound(board, targeti, targetj):
				if board.board[targeti][targetj] == 0:
					while nexti != targeti and nextj != targetj:
						nextj += 2
						if board.board[nexti][nextj] != 0:
							return None
					return (targeti, targetj)
	if direction == 3:
		## move down right
		distance = 1
		nexti = Ai + 1
		nextj = Aj + 1
		while isInBound(board, nexti, nextj) and board.board[nexti][nextj] == 0 and distance < maxDistance:
			distance += 1
			nexti += 1
			nextj += 1
		if not isInBound(board, nexti, nextj):
			return None
		if board.board[nexti][nextj] == 1 or board.board[nexti][nextj] == 2:
			targeti = nexti + distance
			targetj = nextj + distance
			if isInBound(board, targeti, targetj):
				if board.board[targeti][targetj] == 0:
					while nexti != targeti and nextj != targetj:
						nexti += 1
						nextj += 1
						if board.board[nexti][nextj] != 0:
							return None
					return (targeti, targetj)
	if direction == 4:
		## move down right
		distance = 1
		nexti = Ai + 1
		nextj = Aj - 1
		while isInBound(board, nexti, nextj) and board.board[nexti][nextj] == 0 and distance < maxDistance:
			distance += 1
			nexti += 1
			nextj -= 1
		if not isInBound(board, nexti, nextj):
			return None
		if board.board[nexti][nextj] == 1 or board.board[nexti][nextj] == 2:
			targeti = nexti + distance
			targetj = nextj - distance
			if isInBound(board, targeti, targetj):
				if board.board[targeti][targetj] == 0:
					while nexti != targeti and nextj != targetj:
						nexti += 1
						nextj -= 1
						if board.board[nexti][nextj] != 0:
							return None
					return (targeti, targetj)
	if direction == 5:
		## move left
		distance = 1
		nexti = Ai
		nextj = Aj - 2
		while isInBound(board, nexti, nextj) and board.board[nexti][nextj] == 0 and distance < maxDistance:
			distance += 1
			nextj -= 2
		if not isInBound(board, nexti, nextj):
			return None
		if board.board[nexti][nextj] == 1 or board.board[nexti][nextj] == 2:
			targeti = nexti
			targetj = nextj - 2 * distance
			if isInBound(board, targeti, targetj):
				if board.board[targeti][targetj] == 0:
					while nexti != targeti and nextj != targetj:
						nextj -= 2
						if board.board[nexti][nextj] != 0:
							return None
					return (targeti, targetj)
	if direction == 6:
		## move top left
		distance = 1
		nexti = Ai - 1
		nextj = Aj - 1
		while isInBound(board, nexti, nextj) and board.board[nexti][nextj] == 0 and distance < maxDistance:
			distance += 1
			nexti -= 1
			nextj -= 1
		if not isInBound(board, nexti, nextj):
			return None
		if board.board[nexti][nextj] == 1 or board.board[nexti][nextj] == 2:
			targeti = nexti - distance
			targetj = nextj - distance
			if isInBound(board, targeti, targetj):
				if board.board[targeti][targetj] == 0:
					while nexti != targeti and nextj != targetj:
						nexti -= 1
						nextj -= 1
						if board.board[nexti][nextj] != 0:
							return None
					return (targeti, targetj)

'''
Private
Return the possible move of going 1 direction
'''	
def isInBound(board, Ai, Aj):
	if Ai < board.height and Ai >= 0 and Aj < board.mid_width_max and Aj >= 0:
		return True
	return False



	