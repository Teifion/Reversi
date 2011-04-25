class Game_error(Exception):
	"""Errors related to the game in general"""
	pass

class Illegal_move(Game_error):
	"""Errors from illegal moves"""
	pass

class Game_rule_error(Game_error):
	"""Errors that arise from rule issues"""
	pass


class Reversi (object):
	"""
	0 = Empty
	1 = White (player 1)
	2 = Black (player 2)
	"""
	
	def __init__(self):
		super(Reversi, self).__init__()
		
		self.turn = 1
		self.player = 1
		
		self.board = [[0 for x in range(8)] for x in range(8)]
		
		self.board[3][3] = 1
		self.board[3][4] = 2
		self.board[4][3] = 2
		self.board[4][4] = 1
		
		self.has_changed = True
	
	def perform_move(self, x, y):
		# First check that the tile is empty
		if self.board[x][y] != 0:
			raise Illegal_move("Player {0} tried to place a tile at {1},{2} but it is already occupied by {3}".format(
				self.player,
				x, y,
				self.board[x][y]
			))
		
		# Is it next to an existing piece?
		next_to = False
		# Left
		if x > 0:
			if self.board[x-1][y] > 0: next_to = True
		
		# Right
		if x < 7:
			if self.board[x+1][y] > 0: next_to = True
		
		# Up
		if y > 0:
			if self.board[x][y-1] > 0: next_to = True
		
		# Down
		if y < 7:
			if self.board[x][y+1] > 0: next_to = True
		
		if not next_to:
			raise Illegal_move("Player {0} tried to place a tile at {1},{2} but it is not next to any other tiles".format(
				self.player,
				x, y,
			))
		
		# Place it and work out the flips
		self.place_piece(x, y)
		
		# Does this end the game?
		empty_found = False
		for i in range(0, 8):
			if len([0 for tile in self.board[i] if tile == 0]) > 0:
				empty_found = True
		
		if not empty_found:
			self.end_game()
		
		# Alternate between player 1 and 2
		self.player = 3 - self.player
		self.has_changed = True
	
	def end_game(self):
		raise Exception("END GAME")
	
	def place_piece(self, x, y):
		self.board[x][y] = self.player
		
		# Get a reference to the row and column that we just placed a piece on
		column = self.board[x]
		row = [self.board[i][y] for i in range(0,8)]
		
		# First can we travel up?
		if self.player in column[:y]:
			changes = []
			search_complete = False
			
			for i in range(y-1,-1,-1):
				if search_complete: continue
				
				counter = column[i]
				
				if counter == 0:
					changes = []
					search_complete = True
				elif counter == self.player:
					search_complete = True
				else:
					changes.append(i)
			
			# Perform changes
			for i in changes:
				self.board[x][i] = self.player
		
		# Down?
		if self.player in column[y:]:
			pass
		
		# Left?
		if self.player in row[:x]:
			pass
		
		# Right?
		if self.player in row[x:]:
			pass
	
	def ascii_board(self):
		for r in self.board:
			print("".join([str(t) for t in r]))
		print("")
	