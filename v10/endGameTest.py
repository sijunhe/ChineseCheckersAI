from boardState import *
from computeLegalMove import *
from computeFeatures import * 
from computeMinimax import *
import time

numPieces = 10
height = 17
starting = 4
midElement = 8
mid_width = (height + 1) / 2
mid_width_max = mid_width * 2 - 1
board = np.ndarray((height, mid_width_max), dtype = np.int32)
board.fill(-1)
for i in range(height):
	numPiece = min(height - i, i - (-1))
	for j in range(midElement - numPiece+1, midElement+numPiece, 2):
		if i < starting:
			board[i, j] = 2

		elif i >= height - starting:
			board[i, j] = 1
		else:
			board[i, j] = 0
board[0][8] = 0
board[2][10] = 0
board[4][10] = 2
board[7][7] = 2
board[10][8] = 2
board[16][8] = 0
board[14][10] = 0
board[13][11] = 0
board[13][9] = 0
board[13][5] = 0
board[12][10] = 1
board[12][8] = 1
board[12][6] = 1
board[11][5] = 1
board[10][6] = 1
board1 = boardState(options = 'fullGame', inputBoard = board)
board1.printBoard()
boardNow = board1
print('\n ##################### \n Endgame Begins!!!! \n #####################')
player = 2
while ((not boardNow.isEnd())) :
	print('\n\n')
	print('player = {}'.format(player))
	print('\n')

	timeStart = time.time()
	print ('All possible moves = {}'.format(computeLegalMove(boardNow, player)))
	print ('legal move forward = {}'.format(computeLegalMoveForward(boardNow, player, 0)))
	(scoreGreedy, moveList, recursions) = findMoveGreedy(boardNow, player, 3)
	timeEnd = time.time()
	print('scoreGreedy = {}'.format(scoreGreedy))
	move = moveList[0]
	print('move = {}'.format(move))
	print('recursions = {}'.format(recursions))
	print 'time used = ' + str(timeEnd - timeStart)
	boardNow = boardNow.takeMove(move)
	boardNow.printBoard()
	player = 3 - player
