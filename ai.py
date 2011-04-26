import time

class Game_ai (object):
    def __init__(self, game):
        super(Game_ai, self).__init__()
        self.game = game
        self.move = (-1,-1)
    
    def make_move(self):
        time.sleep(0.1)
        
        changes = {}
        
        for x in range(0,8):
            for y in range(0,8):
                if self.game.board[x][y] == 0:
                    c = self.game.place_piece(x, y, live_mode=False)
                    if c > 0:
                        changes[(x,y)] = c
        
        # No moves can be found
        if changes == {}:
            self.game.end_game()
            return
        
        max_key, max_val = (-1,-1), 0
        
        for k, v in changes.items():
            if v > max_val:
                max_key = k
        
        x, y = max_key
        self.game.perform_move(x, y)