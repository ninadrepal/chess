
'''
Created on Feb 26, 2018

@author: NREPAL
'''

"""
move() : in the definition of this function, consider the following checks:
    i)check if there is any piece in the position specified
    ii) check if the piece(if opposite color) can be killed with the active piece 
    by moving to the desired position
    iii)check if the active piece can move to the desired position
"""

WHITE = 'white'
BLACK = 'black'
MOVE_FLAG = False
KILL_FLAG = False
black_position_list = []
white_position_list = []
black_killed_list = []
white_killed_list = []
piece_positions = {}

def check_piece_at_position(x, y):
    position = (x, y)
    piece = list(piece_positions.keys())[list(
            piece_positions.values()).index(position)]
    return piece

def check_square_color(x, y):
    if x + y & 1:
        return 'black' # odd: 6 & 1 = 0
    else:
        return 'white'

def kill_piece(x, y):
    """
    check if (x,y) in white_position_list
    check if (x,y) in black_position_list
    if yes: put in killed_pieces
    """
    KILL_FLAG = False
    try:
        piece_positions.pop(check_piece_at_position(x, y))
        # kill the piece objects from the dictionary of objects created in the create_piece()
        KILL_FLAG = True
    except KeyError:
        print("No piece found to be killed")
        KILL_FLAG = False
    
    return KILL_FLAG
   

def update_piece_position(piece, x, y):
    piece_positions[piece] = (x, y)
    
def check_for_check(self, x, y):
    """
    check to see of the opposite color team gets a check after this move
    for eg: if the black color is playing a move, check to see if after the
            move, the black king gets a check
            return true if check else return false
    """
    pass
    
class Piece(object):
    '''
    classdocs
    '''


    def __init__(self, x, y, color):        
        '''
        Constructor
        '''
        self.x = x
        self.y = y
        self.color = color
        self.position = (x, y)


class Pawn(Piece):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        
    def move(self, x, y):
        if self.color == 'black':
            if abs(x - self.x) <= 1:
                #checks diagonal move
                if (x, y) in white_position_list:
                    if abs(y - self.y) == 1:
                        KILL_FLAG = True
                        MOVE_FLAG = True
                        self.x = x
                        self.y = y
                    else:
                        KILL_FLAG = False
                        MOVE_FLAG = False
                else:
                    if self.x == x and ((y - self.y) == 1):
                        MOVE_FLAG = True
                        self.x = x 
                        self.y = y
                    else:
                        MOVE_FLAG = False
                    
                    

class Rook(Piece):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        
    def move(self, x, y):
        if self.color == 'black':
            if (x, y) in white_position_list:
                pass
                
            
                
class Knight(Piece):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        
    def move(self, x, y):
        if self.color == 'black':
            if (x, y) in white_position_list:
                pass

class Bishop(Piece):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        
    def move(self, x, y):
        if self.color == 'black':
            if (x, y) in white_position_list:
                pass
        
class Queen(Piece):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        
    def move(self, x, y):
        if self.color == 'black':
            if (x, y) in white_position_list:
                if not check_for_check(self, x, y):
                    if kill_piece(x, y):
                        self.x = x
                        self.y = y
                        MOVE_FLAG = True
                    else:
                        MOVE_FLAG = False


class King(Piece):

    def __init__(self, x, y, color):
        super().__init__(x, y, color)


def create_pieces():
    black_pawn = {x: Pawn(x, 7, BLACK) for x in range(1, 9)}
    white_pawn = {x: Pawn(x, 2, WHITE) for x in range(1, 9)}

    black_rook = {num + 1: Rook(x, 8, BLACK) for num, x in enumerate([1,8])}
    white_rook = {num + 1: Rook(x, 1, WHITE) for num, x in enumerate([1,8])}

    black_knight = {num + 1: Knight(x, 8, BLACK) for num, x in enumerate([2,7])}
    white_knight = {num + 1: Knight(x, 1, WHITE) for num, x in enumerate([2,7])}

    black_bishop = {num + 1: Bishop(x, 8, BLACK) for num, x in enumerate([3,6])}
    white_bishop = {num + 1: Bishop(x, 1, WHITE) for num, x in enumerate([3,6])}

    black_queen = Queen(4, 8, BLACK)
    white_queen = Queen(4, 1, WHITE)

    black_king = King(5, 8, BLACK)
    white_king = King(5, 1, WHITE)
    
create_pieces()

class Board(object):
    def __init__(self,x, y):
        self.x = x
        self.y = y
    
    def print_board(self):
        pass
    
def print_board():
    print(u' \u265C    \u265E     \u265D    \u265B     \u265A    \u265D    \u265E     \u265B')
    print(u' \u265F    \u265F     \u265F    \u265F     \u265F    \u265F    \u265F     \u265F')
#     print(u'\u25FB\u25FC\u25FB\u25FC\u25FB\u25FC\u25FB\u25FC ')
    print(" -  -  -  -  -  -  -  -")
    print(" -  -  -  -  -  -  -  -")
    print(" -  -  -  -  -  -  -  -")
    print(" -  -  -  -  -  -  -  -")
    print(" -  -  -  -  -  -  -  -")
    print(u'\u2659    \u2659     \u2659    \u2659     \u2659    \u2659    \u2659     \u2659')
    print(u'\u2656    \u2658     \u2657    \u2655     \u2654    \u2657    \u2658     \u2656')
    



# when you kill the piece remove the piece from the position list and the 
# piece object dictionaries that are created herewith



