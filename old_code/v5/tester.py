from boardState import *
from computeLegalMove import *
from computeFeatures import * 

board1 = boardState(options = 'fullGame')
print "Orginal Board"

board1.printBoard()
print computeFeaturesFull(board1)
