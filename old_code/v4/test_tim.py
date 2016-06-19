from boardState import *
from computeFeatures import *
from computeLegalMove import *
x = boardState(options = 'smallGame')
x.printBoard()

# x.board[2,3] = 2; x.board[1,2] = 0;
# x.board[3,2] = 1; x.board[5,2] = 0;
# x.board[4,6] = 2; x.board[3,7] = 0;
# x.board[12,6] = 1; x.board[13,7] = 0;

''' isEnd testing'''
# x.printBoard()
# print 'game ends? {}'.format(x.isEnd())

''' feature testing '''
print 'position One {}'.format(x.PositionOne)
print 'position Two {}'.format(x.PositionTwo)
x.board[2,3] = 1; x.board[1,2] = 0;
x.board[3,2] = 2; x.board[5,2] = 0;
x.printBoard()
x.PositionOne = []; x.PositionTwo = []
for i in range(x.height):
	for j in range(x.mid_width_max):
		if x.board[i,j] == 1:
			x.PositionOne.append((i,j))
		if x.board[i,j] == 2:
			x.PositionTwo.append((i,j))
x.allPosition = x.PositionOne + x.PositionTwo
# x.PositionOne[1] = (2,3); 
# x.PositionTwo[0] = (3,2); 
print 'position One {}'.format(x.PositionOne)
print 'position Two {}'.format(x.PositionTwo)
print computeFeatures(x)
