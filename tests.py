import unittest
import reversi

def dummy_game(board):
    g = reversi.Reversi()
    
    for k, v in board.items():
        x, y = k
        g.board[x][y] = v
    
    return g

class Move_class(unittest.TestCase):
    def test_taking_to_right(self):
        g = dummy_game({
            (5,5): 2,
            (6,5): 1,
        })
        
        self.assertEqual(1, g.place_piece(4, 5, live_mode=False))
    
    def test_taking_to_left(self):
        g = dummy_game({
            (5,5): 2,
            (4,5): 1,
        })
        
        self.assertEqual(1, g.place_piece(6, 5, live_mode=False))
    
    def test_taking_to_top(self):
        g = dummy_game({
            (5,5): 2,
            (5,4): 1,
        })
        
        self.assertEqual(1, g.place_piece(5, 6, live_mode=False))
        
    def test_taking_to_bottom(self):
        g = dummy_game({
            (5,5): 2,
            (5,6): 1,
        })
        
        self.assertEqual(1, g.place_piece(5, 4, live_mode=False))
    
    
    def test_taking_to_down_right(self):
        g = dummy_game({
            (5,5): 2,
            (6,6): 1,
        })
        
        self.assertEqual(1, g.place_piece(4, 4, live_mode=False))
        
    def test_taking_to_top_right(self):
        g = dummy_game({
            (5,5): 2,
            (4,6): 1,
        })
        
        self.assertEqual(1, g.place_piece(6, 4, live_mode=False))
    
    def test_taking_to_down_left(self):
        g = dummy_game({
            (5,5): 2,
            (6,4): 1,
        })
        
        self.assertEqual(1, g.place_piece(4, 6, live_mode=False))
    
    def test_taking_to_top_left(self):
        g = dummy_game({
            (5,5): 2,
            (4,4): 1,
        })
        
        self.assertEqual(1, g.place_piece(6, 6, live_mode=False))
    
    def test_top_left_corner(self):
        # Trick test, make sure that we don't just allow it when we shouldn't
        g = dummy_game({
            (1,1): 1,
            (0,1): 1,
            (1,0): 1,
        })
        
        self.assertEqual(0, g.place_piece(0, 0, live_mode=False))
        
        
        g = dummy_game({
            (1,0): 2,
            (2,0): 1,
        })
        
        self.assertEqual(1, g.place_piece(0, 0, live_mode=False))
        
    
    def test_weird_edge_cases(self):
        g = reversi.Reversi()
        g.board = [
            [0,1,0,1,2,1,0,0],
            [0,2,2,2,2,1,0,0],
            [0,0,2,2,2,1,0,0],
            [0,1,1,1,1,1,0,0],
            [0,0,1,1,1,1,0,0],
            [0,0,1,1,1,1,2,0],
            [0,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]
        
        self.assertEqual(1, g.place_piece(0, 0, live_mode=False))

if __name__ == '__main__':
    unittest.main()