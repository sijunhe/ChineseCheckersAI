from boardState import *
from computeLegalMove import * 

board1 = boardState(options = 'smallGame')
print "Orginal Board"
board1.printBoard()
possibleMoveBoard = computeLegalMove(board1, 1)
for move in possibleMoveBoard:
	print move

print possibleMoveBoard[2]
((oldi, oldj),(newi, newj)) = possibleMoveBoard[2]
board2 = board1.takeMove(oldi, oldj, newi, newj)
board2.printBoard()
twoSteps = computeLegalMove(board2, 2)
for twoStep in twoSteps:
	print twoStep