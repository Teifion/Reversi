import pygame, random, sys, time, math
from pygame.locals import *
import ai, reversi

def quit():
	pygame.quit()
	sys.exit()

COUNTER_SIZE = 40
TILE_SIZE = 50
COUNTER_PADDING = 5
FPS = 40

WINDOWWIDTH = TILE_SIZE * 8
WINDOWHEIGHT = TILE_SIZE * 8

class Engine_v1 (object):
	def __init__(self):
		super(Engine_v1, self).__init__()
		self.resources = {}
		self.keys_down = {}
		
		self.game = reversi.Reversi()
	
	# def _waitForPlayerToPressKey():
	#	while True:
	#		for event in pygame.event.get():
	#			if event.type == QUIT:
	#				quit()
	#			if event.type == KEYDOWN:
	#				if event.key == K_ESCAPE: # pressing escape quits
	#					quit()
	#				return

	def playerHasHitBaddie(self, playerRect, baddies):
		for b in baddies:
			if playerRect.colliderect(b['rect']):
				return True
		return False
	
	def add_tile(self, x, y, player):
		pass
		#	return pygame.Rect(40, 40, x * TILE_SIZE + 5, y * TILE_SIZE + 5)

	def startup(self):
		# set up pygame, the window, and the mouse cursor
		pygame.init()
		self.main_clock = pygame.time.Clock()
		self.surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
		pygame.display.set_caption('Reversi')
		# pygame.mouse.set_visible(False)

		# set up fonts
		font = pygame.font.SysFont(None, 48)

		# set up sounds
		# gameOverSound = pygame.mixer.Sound('gameover.wav')
		# pygame.mixer.music.load('background.mid')

		# set up images
		self.resources['board'] = pygame.image.load('media/board.png')
		self.resources['black'] = pygame.image.load('media/black.png')
		self.resources['white'] = pygame.image.load('media/white.png')
		
		self.draw_board()
	
	def drawText(self, text, font, surface, x, y):
		textobj = font.render(text, 1, (0,0,0))
		textrect = textobj.get_rect()
		textrect.topleft = (x, y)
		surface.blit(textobj, textrect)
	
	def draw_board(self):
		# First the board
		the_board = pygame.Rect(0, 0, WINDOWWIDTH, WINDOWHEIGHT)
		self.surface.blit(self.resources['board'], the_board)
		
		# Now the tiles
		for x in range(0, 8):
			for y in range(0, 8):
				player = self.game.board[x][y]
				counter = pygame.Rect(x * TILE_SIZE + COUNTER_PADDING, y * TILE_SIZE + COUNTER_PADDING, COUNTER_SIZE, COUNTER_SIZE)
				
				if player == 1:
					self.surface.blit(self.resources['white'], counter)
				elif player == 2:
					self.surface.blit(self.resources['black'], counter)
		
		# Has a victory occurred?
		font = pygame.font.SysFont("Helvetica", 48)
		if self.game.victory == -1:
			self.drawText("Stalemate", font, self.surface, 95, 10)
		if self.game.victory == 1:
			self.drawText("Victory to White", font, self.surface, 38, 10)
		if self.game.victory == 2:
			self.drawText("Victory to Black", font, self.surface, 39, 10)
		
		pygame.display.update()
	
	def handle_keydown(self, event):
		self.keys_down[event.key] = time.time()
		self.test_for_keyboard_commands()

	def handle_keyup(self, event):
		del(self.keys_down[event.key])

	def handle_mousedown(self, event):
		pass

	def handle_mouseup(self, event):
		x, y = event.pos
		tx = int(math.floor(x/TILE_SIZE))
		ty = int(math.floor(y/TILE_SIZE))
		
		try:
			self.game.perform_move(tx, ty)
		except reversi.Illegal_move as e:
			print("Illegal move")
		except Exception as e:
			raise

	def handle_mousemove(self, event):
		pass

	def test_for_keyboard_commands(self):
		# Cmd + Q
		if 113 in self.keys_down and 310 in self.keys_down:
			if self.keys_down[310] < self.keys_down[113]:# Cmd has to be pushed first
				quit()
	
	def start(self):
		self.startup()
		
		while True:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					self.handle_keydown(event)
				
				elif event.type == KEYUP:
					self.handle_keyup(event)
				
				elif event.type == MOUSEBUTTONUP:
					self.handle_mouseup(event)
				
				elif event.type == MOUSEBUTTONDOWN:
					self.handle_mousedown(event)
				
				elif event.type == MOUSEMOTION:
					self.handle_mousemove(event)
				
				else:
					print(event)
			
			# Turn based game so we don't need to always update
			if self.game.has_changed:
				self.draw_board()
				self.game.has_changed = False
			
			
			self.main_clock.tick(FPS)
		
		quit()
	

# topScore = 0
# while True:
#	# set up the start of the game
#	baddies = []
#	score = 0
#	playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
#	moveLeft = moveRight = moveUp = moveDown = False
#	reverseCheat = slowCheat = False
#	baddieAddCounter = 0
#	pygame.mixer.music.play(-1, 0.0)
# 
#	while True: # the game loop runs while the game part is playing
#		score += 1 # increase score
# 
#		for event in pygame.event.get():
#			if event.type == QUIT:
#				terminate()
# 
#			if event.type == KEYDOWN:
#				if event.key == ord('z'):
#					reverseCheat = True
#				if event.key == ord('x'):
#					slowCheat = True
#				if event.key == K_LEFT or event.key == ord('a'):
#					moveRight = False
#					moveLeft = True
#				if event.key == K_RIGHT or event.key == ord('d'):
#					moveLeft = False
#					moveRight = True
#				if event.key == K_UP or event.key == ord('w'):
#					moveDown = False
#					moveUp = True
#				if event.key == K_DOWN or event.key == ord('s'):
#					moveUp = False
#					moveDown = True
# 
#			if event.type == KEYUP:
#				if event.key == ord('z'):
#					reverseCheat = False
#					score = 0
#				if event.key == ord('x'):
#					slowCheat = False
#					score = 0
#				if event.key == K_ESCAPE:
#						terminate()
# 
#				if event.key == K_LEFT or event.key == ord('a'):
#					moveLeft = False
#				if event.key == K_RIGHT or event.key == ord('d'):
#					moveRight = False
#				if event.key == K_UP or event.key == ord('w'):
#					moveUp = False
#				if event.key == K_DOWN or event.key == ord('s'):
#					moveDown = False
# 
#			if event.type == MOUSEMOTION:
#				# If the mouse moves, move the player where the cursor is.
#				playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)
# 
#		# Add new baddies at the top of the screen, if needed.
#		if not reverseCheat and not slowCheat:
#			baddieAddCounter += 1
#		if baddieAddCounter == ADDNEWBADDIERATE:
#			baddieAddCounter = 0
#			baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
#			newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
#						'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
#						'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
#						}
# 
#			baddies.append(newBaddie)
# 
#		# Move the player around.
#		if moveLeft and playerRect.left > 0:
#			playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
#		if moveRight and playerRect.right < WINDOWWIDTH:
#			playerRect.move_ip(PLAYERMOVERATE, 0)
#		if moveUp and playerRect.top > 0:
#			playerRect.move_ip(0, -1 * PLAYERMOVERATE)
#		if moveDown and playerRect.bottom < WINDOWHEIGHT:
#			playerRect.move_ip(0, PLAYERMOVERATE)
# 
#		# Move the mouse cursor to match the player.
#		pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)
# 
#		# Move the baddies down.
#		for b in baddies:
#			if not reverseCheat and not slowCheat:
#				b['rect'].move_ip(0, b['speed'])
#			elif reverseCheat:
#				b['rect'].move_ip(0, -5)
#			elif slowCheat:
#				b['rect'].move_ip(0, 1)
# 
#		 # Delete baddies that have fallen past the bottom.
#		for b in baddies[:]:
#			if b['rect'].top > WINDOWHEIGHT:
#				baddies.remove(b)
# 
#		# Draw the game world on the window.
#		windowSurface.fill(BACKGROUNDCOLOR)
# 
#		# Draw the score and top score.
#		drawText('Score: %s' % (score), font, windowSurface, 10, 0)
#		drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
# 
#		# Draw the player's rectangle
#		windowSurface.blit(playerImage, playerRect)
# 
#		# Draw each baddie
#		for b in baddies:
#			windowSurface.blit(b['surface'], b['rect'])
# 
#		pygame.display.update()
# 
#		# Check if any of the baddies have hit the player.
#		if playerHasHitBaddie(playerRect, baddies):
#			if score > topScore:
#				topScore = score # set new top score
#			break
# 
#		mainClock.tick(FPS)
# 
#	# Stop the game and show the "Game Over" screen.
#	pygame.mixer.music.stop()
#	gameOverSound.play()
# 
#	drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
#	drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
#	pygame.display.update()
#	waitForPlayerToPressKey()
# 
#	gameOverSound.stop()

if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1] == 'test':
		import unittest, tests
		print("Test mode")
		# unittest.main()
	else:
		ge = Engine_v1()
		ge.start()
	
