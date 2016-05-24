print range(4)

	def isEnd(self):
		my_endPiece = 0
		opponent_endPiece = 0
		for i in range(self.height):
			numPiece = min(self.height - i, i - (-1))	
			for j in range(self.midElement - numPiece+1, self.midElement+numPiece, 2):
				if i < self.starting:
					if self.board[i,j] == 2:
						opponent_endPiece += 1
				elif i >= self.height - self.starting:
					if self.board[i,j] == 1:
						my_endPiece += 1
		if 	(opponent_endPiece == self.numPieces) or (my_endPiece == self.numPieces):
			return True
		else:



		#my position - total furthest moves
		possibleMoveBoard = self.computeLegalMove()
		best_move = 0
		for ((i1,j1), (i2,j2)) in possibleMoveBoard:
			if i2 - i1 > best_move:
				best_move = i2 - i1
		self.features[6] = best_move