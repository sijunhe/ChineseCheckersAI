import numpy as np
import copy

board = np.ndarray((17, 25), dtype = np.int32)
board.fill(0)

for i in range(4):
	for j in range(25):
		if j in range(13-i-1,13+i,2):
			board[i,j] = 1
		else: 
			board[i,j] = -1

for i in range(13,17):
	for j in range(25):
		if j in range(13-(16-i)-1,13+(16-i),2):
			board[i,j] = 2
		else:
			board[i,j] = -1

for i in range(4,9):
	for j in range(25):
		if j in range(i-4) or j in range(25-(i-4),25):
			board[i,j] = -1

for i in range(9,13):
	for j in range(25):
		if j in range(12-i) or j in range(25-(12-i),25):
			board[i,j] = -1

for i in range(4,13,2):
	for j in range(1,25,2):
		board[i,j] = -1

for i in range(5,12,2):
	for j in range(0,25,2):
		board[i,j] = -1


for i in range(17):
	for j in range(25):
		if board[i,j] == 0:
			print "o",
		elif board[i,j] == 1:
			print "1",
		elif board[i,j] == 2:
			print "2",
		# elif board[i,j] == -1:
		# 	print"-1"
		else:
			print " ",
	print "\n"