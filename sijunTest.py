## used by Siun to test his code 


######################################################################################################################
## You can run the file, but do NOT change if you are not sijun 
######################################################################################################################


from boardState import *

x = boardState(options = 'smallGame')
print "Orginal Board"
x.printBoard()
possibleMoveBoard = x.computeLegalMove()
for move in possibleMoveBoard:
	print move

print possibleMoveBoard[2]
((oldi, oldj),(newi, newj)) = possibleMoveBoard[2]
test = x.takeMove(oldi, newi, oldj, newj)
test.printBoard()
twoSteps = test.computeLegalMove()
for twoStep in twoSteps:
	print twoStep