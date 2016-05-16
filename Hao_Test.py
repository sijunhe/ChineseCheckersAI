## used by Hao to test his code 


######################################################################################################################
## You can run the file, but do NOT change if you are not Hao  
######################################################################################################################


from boardState import *

x = boardState(options = 'smallGame')
print "Orginal Board"
x.printBoard()
xFeatures = x.computeFeatures()
print('Features = ', xFeatures)
xScoreRaw = np.dot(xFeatures.transpose(), x.weights)
print('ScoreRaw = ', xScoreRaw)

possibleMoveBoard = x.computeLegalMove()
for move in possibleMoveBoard:
	print move
	((oldi, oldj),(newi, newj)) = move
	test = x.takeMove(oldi, oldj, newi, newj)
	test.printBoard()
	testFeatures = test.computeFeatures()
	print('Features = ', testFeatures)
	testScoreRaw = np.dot(testFeatures.transpose(), test.weights)
	print('ScoreRaw = ', testScoreRaw)
	print test.isEnd()





# print possibleMoveBoard[2]
# ((oldi, oldj),(newi, newj)) = possibleMoveBoard[2]
# test = x.takeMove(oldi, newi, oldj, newj)
# test.printBoard()
# twoSteps = test.computeLegalMove()
# for twoStep in twoSteps:
# 	print twoStep
#
# x.computeMiniMax(0)