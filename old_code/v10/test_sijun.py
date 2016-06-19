from boardState import *
from computeLegalMove import *
from computeFeatures import * 
from computeMinimax import *
from randomMove import * 

board1 = boardState(options = 'fullGame')
print randomMove(board1, 1)