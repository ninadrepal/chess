
'''
Created on Feb 26, 2018

@author: NREPAL
'''
from _operator import pos

"""
move() : in the definition of this function, consider the following checks:
    i)check if there is any piece in the position specified
    ii) check if the piece(if opposite color) can be killed with the active piece 
    by moving to the desired position
    iii)check if the active piece can move to the desired position
"""
import itertools
import sys
import pprint

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
        self.symbol = '\u265F' if self.color == BLACK else '\u2659'
        
        
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
        self.symbol = '\u265C' if self.color == BLACK else '\u2656'
        
    def move(self, x, y):
        if self.color == 'black':
            if (x, y) in white_position_list:
                pass
                
            
                
class Knight(Piece):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.symbol = '\u265E' if self.color == BLACK else '\u2658'
        
    def move(self, x, y):
        if self.color == 'black':
            if (x, y) in white_position_list:
                pass

class Bishop(Piece):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.symbol = '\u265D' if self.color == BLACK else '\u2657'
        
    def move(self, x, y):
        if self.color == 'black':
            if (x, y) in white_position_list:
                pass
        
class Queen(Piece):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.symbol = '\u265B' if self.color == BLACK else '\u2655'
        
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
        self.symbol = '\u265A' if self.color == BLACK else '\u2654'
    
    

def create_pieces():
    
    global white_pieces, black_pieces, all_pieces
    global black_pawn, white_pawn, black_rook, white_rook, black_knight
    global white_knight, black_bishop, white_bishop, black_queen, white_queen

    black_pawn = {'bp'+ str(x): Pawn(x, 7, BLACK) for x in range(1, 9)}
    white_pawn = {'wp'+ str(x): Pawn(x, 2, WHITE) for x in range(1, 9)}

    black_rook = {'br' + str(num + 1): Rook(x, 8, BLACK) for num, x in enumerate([1,8])}
    white_rook = {'wr' + str(num + 1): Rook(x, 1, WHITE) for num, x in enumerate([1,8])}

    black_knight = {'bkn' + str(num + 1): Knight(x, 8, BLACK) for num, x in enumerate([2,7])}
    white_knight = {'wkn' + str(num + 1): Knight(x, 1, WHITE) for num, x in enumerate([2,7])}

    black_bishop = {'bb' + str(num + 1): Bishop(x, 8, BLACK) for num, x in enumerate([3,6])}
    white_bishop = {'wb' + str(num + 1): Bishop(x, 1, WHITE) for num, x in enumerate([3,6])}

    black_queen = {'bq' + str(num + 1): Queen(x, 8, BLACK) for num, x in enumerate([4])}
    white_queen = {'wq' + str(num + 1): Queen(x, 1, WHITE) for num, x in enumerate([4])}

    black_king = {'bk' + str(num + 1): King(x, 8, BLACK) for num, x in enumerate([5])}
    white_king = {'wk' + str(num + 1): King(x, 1, WHITE) for num, x in enumerate([5])}
    
    white_pieces = {**white_pawn, **white_king, **white_queen, **white_rook,
                    **white_knight, **white_bishop}
    black_pieces = {**black_pawn, **black_king, **black_queen, **black_rook,
                    **black_knight, **black_bishop}
    all_pieces = {**white_pieces, **black_pieces}
    
create_pieces()

class Board(object):
    def __init__(self,x, y):
        self.x = x
        self.y = y
    
    def print_board(self):
        pass
    
    def init_positions(self, piece, x, y):
        pass
    
def print_board():
    board_list = [x for x in range(1,9)]
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
xlist = [x for x in range(1,9)]

board_list = [x for x in range(1,9)]
# print(list(itertools.product(board_list,repeat =  2)))

    

# y = [y for y in range(1,9)]


board_positions = {}
for x, y in itertools.product(xlist,xlist):
    board_positions[(x,y)] = None
# print(board_positions.iterkeys())
new_board_positions = {}

for piece in all_pieces.items():
    for position in board_positions.keys():
        if piece[-1].position == position:
#             print(position)
#             print(piece)
            new_board_positions[position] = piece
            break
        else:
            board_positions[position] = None
        

board_positions.update(new_board_positions)

print(board_positions)
for z in reversed(range(1,9)):
    print([board_positions[x][-1].symbol if board_positions[x] != None else '-' for x in itertools.product(board_list,repeat =  2) if x[-1] == z])


