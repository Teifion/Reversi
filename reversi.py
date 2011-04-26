import ai

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
		self.victory = 0
		
		self.board = [[0 for x in range(8)] for x in range(8)]
		
		self.board[3][3] = 1
		self.board[3][4] = 2
		self.board[4][3] = 2
		self.board[4][4] = 1
		
		# Setup AI
		self.use_ai = True
		self.ai = ai.Game_ai(self)
		
		self.has_changed = True
		self.ai_is_ready = False
	
	def player_move(self, x, y):
		# If the game is over we don't need to do anything here
		if self.victory != 0:
			return
		
		# Is it the AI turn?
		if self.use_ai and self.player != 1:
			return
		
		self.perform_move(x,y)
		
		# Maybe have the AI make a move
		if self.use_ai:
			self.ai_is_ready = True
	
	def perform_move(self, x, y):
		# First check that the tile is empty
		if self.board[x][y] != 0:
			raise Illegal_move("Player {0} tried to place a tile at {1},{2} but it is already occupied by {3}".format(
				self.player,
				x, y,
				self.board[x][y]
			))
		
		# Place it and work out the flips
		self.place_piece(x, y)
		
		# Does this end the game?
		all_tiles = [item for sublist in self.board for item in sublist]
		
		empty_tiles = len([0 for tile in all_tiles if tile == 0])
		white_tiles = len([0 for tile in all_tiles if tile == 1])
		black_tiles = len([0 for tile in all_tiles if tile == 2])
		
		# No moves left to make, end the game
		if white_tiles < 1 or black_tiles < 1 or empty_tiles < 1:
			self.end_game()
			return
		
		# Are there any moves able to be made?
		move_found = self.move_can_be_made()
		
		if not move_found:
			self.end_game()
			return
		
		# Alternate between player 1 and 2
		self.player = 3 - self.player
		self.has_changed = True
	
	def move_can_be_made(self):
		move_found = False
		
		for x in range(0,8):
			for y in range(0,8):
				if move_found: continue
				if self.game.board[x][y] == 0:
					c = self.place_piece(x, y, live_mode=False)
					if c > 0:
						move_found = True
		
		return move_found
	
	def ai_move(self):
		self.ai.make_move()
		self.ai_is_ready = False
	
	def end_game(self):
		all_tiles = [item for sublist in self.board for item in sublist]
		
		white_tiles = len([0 for tile in all_tiles if tile == 1])
		black_tiles = len([0 for tile in all_tiles if tile == 2])
		
		if white_tiles > black_tiles:
			self.victory = 1
		elif white_tiles < black_tiles:
			self.victory = 2
		else:
			self.victory = -1
		
		self.has_changed = True
	
	def place_piece(self, x, y, live_mode=True):
		if live_mode:
			self.board[x][y] = self.player
		change_count = 0
		
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
			if search_complete:
				change_count += len(changes)
				if live_mode:
					for i in changes:
						self.board[x][i] = self.player
		
		# Down?
		if self.player in column[y:]:
			changes = []
			search_complete = False
			
			for i in range(y+1,8,1):
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
			if search_complete:
				change_count += len(changes)
				if live_mode:
					for i in changes:
						self.board[x][i] = self.player
		
		# Left?
		if self.player in row[:x]:
			changes = []
			search_complete = False
			
			for i in range(x-1,-1,-1):
				if search_complete: continue
				
				counter = row[i]
				
				if counter == 0:
					changes = []
					search_complete = True
				elif counter == self.player:
					search_complete = True
				else:
					changes.append(i)
			
			# Perform changes
			if search_complete:
				change_count += len(changes)
				if live_mode:
					for i in changes:
						self.board[i][y] = self.player
		
		# Right?
		if self.player in row[x:]:
			changes = []
			search_complete = False
			
			for i in range(x+1,8,1):
				if search_complete: continue
				
				counter = row[i]
				
				if counter == 0:
					changes = []
					search_complete = True
				elif counter == self.player:
					search_complete = True
				else:
					changes.append(i)
			
			# Perform changes
			if search_complete:
				change_count += len(changes)
				if live_mode:
					for i in changes:
						self.board[i][y] = self.player
		
		# Diagonals are a little harder
		xy_sum = x + y
		i, j = 0, xy_sum
		bl_tr_diagonal = []
		
		for q in range(0, xy_sum):
			if 0 <= i < 8 and 0 <= j < 8:
				bl_tr_diagonal.append(self.board[i][j])
			
			i += 1
			j -= 1
		
		i, j = x-min(x,y), y-min(x,y)
		br_tl_diagonal = []
		for q in range(0, xy_sum):
			if 0 <= i < 8 and 0 <= j < 8:
				br_tl_diagonal.append(self.board[i][j])
			
			i += 1
			j += 1
		
		# Up Right
		if self.player in bl_tr_diagonal:
			changes = []
			search_complete = False
			i = 0
			lx, ly = x, y
			
			while 0 <= lx < 8 and 0 <= ly < 8:
				lx += 1
				ly -= 1
				
				if lx > 7 or ly < 0: break
				if search_complete: continue
				
				counter = self.board[lx][ly]
				
				if counter == 0:
					changes = []
					search_complete = True
				elif counter == self.player:
					search_complete = True
				else:
					changes.append((lx, ly))
			
			# Perform changes
			if search_complete:
				change_count += len(changes)
				if live_mode:
					for i, j in changes:
						self.board[i][j] = self.player
		
		# Down Right
		if self.player in bl_tr_diagonal:
			changes = []
			search_complete = False
			i = 0
			lx, ly = x, y
			
			while 0 <= lx < 8 and 0 <= ly < 8:
				lx -= 1
				ly += 1
				
				if lx < 0 or ly > 7: break
				if search_complete: continue
				
				counter = self.board[lx][ly]
				
				if counter == 0:
					changes = []
					search_complete = True
					break
				elif counter == self.player:
					search_complete = True
					break
				else:
					changes.append((lx, ly))
			
			
			# Perform changes
			if search_complete:
				change_count += len(changes)
				if live_mode:
					for i, j in changes:
						self.board[i][j] = self.player
		
		
		# Up Left
		if self.player in br_tl_diagonal:
			changes = []
			search_complete = False
			i = 0
			lx, ly = x, y
			
			while 0 <= lx < 8 and 0 <= ly < 8:
				lx -= 1
				ly -= 1
				
				if lx < 0 or ly < 0: break
				if search_complete: continue
				
				counter = self.board[lx][ly]
				
				if counter == 0:
					changes = []
					search_complete = True
				elif counter == self.player:
					search_complete = True
				else:
					changes.append((lx, ly))
			
			# Perform changes
			if search_complete:
				change_count += len(changes)
				if live_mode:
					for i, j in changes:
						self.board[i][j] = self.player
		
		# Down Right
		if self.player in br_tl_diagonal:
			changes = []
			search_complete = False
			i = 0
			lx, ly = x, y
			
			while 0 <= lx < 8 and 0 <= ly < 8:
				lx += 1
				ly += 1
				
				if lx > 7 or ly > 7: break
				if search_complete: continue
				
				counter = self.board[lx][ly]
				
				if counter == 0:
					changes = []
					search_complete = True
				elif counter == self.player:
					search_complete = True
				else:
					changes.append((lx, ly))
			
			# Perform changes
			if search_complete:
				change_count += len(changes)
				if live_mode:
					for i, j in changes:
						self.board[i][j] = self.player
		
		if change_count == 0 and live_mode:
			self.board[x][y] = 0
			raise Illegal_move("Player {0} tried to place a tile at {1},{2} but that will result in 0 flips".format(
				self.player,
				x, y,
			))
		
		if change_count > 0:
			print("Tested at {0},{1} and found {2} changes".format(x, y, change_count))
		return change_count
	
	def ascii_board(self):
		"""
		Print board so that it can be debugged in the terminal
		"""
		for r in self.board:
			print("".join([str(t) for t in r]))
		print("")
	
