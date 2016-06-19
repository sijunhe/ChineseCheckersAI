from boardState import *
from computeLegalMove import *
from computeFeatures import * 
from computeMinimax import *
from randomMove import * 

board1 = boardState(options = 'fullGame')
board1.printBoard()

# print randomMove(board1, 2)

print randomMoveMultistep(board1, 1, 2)
print randomMoveMultistep(board1, 1, 2)
print randomMoveMultistep(board1, 1, 2)
print randomMoveMultistep(board1, 1, 2)