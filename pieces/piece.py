
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
import itertools


WHITE = 'white'
BLACK = 'black'
ALIVE = 'alive'
KILLED = 'killed'
MOVE_FLAG = False
KILL_FLAG = False
black_position_list = []
white_position_list = []
black_killed_list = []
white_killed_list = []
board_positions = {}


    
# def check_square_color(x, y):
#     if x + y & 1:
#         return 'black' # odd: 6 & 1 = 0
#     else:
#         return 'white'

def check_interruptions(piece, next_position, available_moves):
    
    """ check how many of the squares between the next pos
    and the present pos are in the available pos list
    """
    """This function will NOT be applicable for Knight"""


    interruptions = [1 if board_positions[position][-1] is None else 0 for position in available_moves[0:available_moves.index(next_position)]]
# 0 if no piece on specified position. If no pieces in all positions then all zeros in the list. if all zeros that means no interruptions.
# if 1 is in the list, then there are interruptions and hence it will return True.
    kill_piece = interruptions.pop()
    if 1 not in interruptions:
        if kill_piece == 1:
            KILL_FLAG = kill_piece(piece, next_position, piece.position)
            MOVE_FLAG = KILL_FLAG
        else:
            MOVE_FLAG = True
    else:
        MOVE_FLAG = False
        
    return MOVE_FLAG, KILL_FLAG

def kill_piece(piece, next_position, present_position):
    """
    check if (x,y) in white_position_list
    check if (x,y) in black_position_list
    if yes: put in killed_pieces
    
    ALGORITHM:
    check if piece color is different
    if yes --> check if the 
    """

    try:
#         piece_positions.pop(check_piece_at_position(x, y))
        if piece.color != board_positions[(1,2)][-1].color:
            board_positions[next_position][-1].status = KILLED
            piece.position = next_position
            if check_for_check(white_king['wk1'].position if piece.color == WHITE else black_king['bk1'].position):
                board_positions[next_position][-1].status = ALIVE
                piece.position = present_position
                KILL_FLAG = False
            else:
                KILL_FLAG = True
                
        else:
            KILL_FLAG = False

    except KeyError:
        print("No piece found to be killed")
 
    
    return KILL_FLAG
   
    
def check_for_check(self, king_position):
    """
    check to see of the opposite color team gets a check after this move
    for eg: if the black color is playing a move, check to see if after the
            move, the black king gets a check
            return true if check else return false
    """
    """Algorithm:
    check the color of the piece
    check if king is in the available moves of each piece
    if yes --> check for interruptions between that pieces present position and the kings position
        if no interruptions: then return true
        if there are interruptions return false
    if no --> return false
    """
    
    check = False
    if self.color == WHITE:
        for name, piece in black_pieces.items():
            if king_position in piece.available_moves(piece, piece.position, king_position):
                if not check_interruptions(king_position, piece.available_moves(piece, piece.position, king_position)):
                    check = True
            break
    elif self.color == BLACK:
        for name, piece in white_pieces.items():
            if king_position in piece.available_moves(piece, piece.position, king_position):
                if check_interruptions(king_position, piece.available_moves(piece, piece.position, king_position)):
                    check = True
            break
    return check
                


class Piece(object):
    '''
    classdocs
    '''


    def __init__(self, x, y, color, status):        
        '''
        Constructor
        '''
        self.x = x
        self.y = y
        self.color = color
        self.position = (x, y)
        self.status = status

class Pawn(Piece):
    
    def __init__(self, x, y, color, status):
        super().__init__(x, y, color, status)
        self.symbol = '\u265F' if self.color == BLACK else '\u2659'


    def move(self, x, y):
        present_position = self.position
        next_position = (x,y)
        
        if self.color == WHITE:
            initial_move = True if present_position[-1] == 2 else False
#             possible_white_moves = [(x-1, y+1),(x, y+1), (x+1, y+1)]
            beginning_move = [(self.x, self.y+2)]
            possible_kill_moves = [(self.x-1, self.y+1), (self.x+1, self.y+1)]
            straight_move = [(self.x,self.y+1)]
            
            if board_positions[next_position] != None:
                if board_positions[next_position][-1].color == BLACK:
                    if next_position in possible_kill_moves:
                        pass
                    else:
                        MOVE_FLAG = False
                else:
                    MOVE_FLAG = False
            else:# if no piece is present at the next position to be moved:                
                if next_position in straight_move:
                    self.position = next_position
                    MOVE_FLAG = True
                elif next_position in beginning_move and initial_move == True:
                    self.position = next_position
                    MOVE_FLAG = True
                else:
                    MOVE_FLAG = False
                    
        elif self.color == BLACK:
            initial_move = True if present_position[-1] == 7 else False
#             possible_white_moves = [(x-1, y+1),(x, y+1), (x+1, y+1)]
            beginning_move = [(self.x, self.y-2)]
            possible_kill_moves = [(self.x-1, self.y-1), (self.x+1, self.y-1)]
            straight_move = [(self.x,self.y-1)]
            
            if board_positions[next_position] != None:
                if board_positions[next_position][-1].color == WHITE:
                    if next_position in possible_kill_moves:
                        pass
                    else:
                        MOVE_FLAG = False
                else:
                    MOVE_FLAG = False
            else:# if no piece is present at the next position to be moved:                
                if next_position in straight_move:
                    self.position = next_position
                    MOVE_FLAG = True
                elif next_position in beginning_move and initial_move == True:
                    self.position = next_position
                    MOVE_FLAG = True
                else:
                    MOVE_FLAG = False
        return MOVE_FLAG

class Rook(Piece):
    
    def __init__(self, x, y, color, status):
        super().__init__(x, y, color, status)
        self.symbol = '\u265C' if self.color == BLACK else '\u2656'
        
    def move(self, x, y):
        """
        ALGORITHM:
        check for check
        if no check then see available moves
        if there are no interruptions in the available moves
        """
        present_position = self.position
        next_position = (x,y)
        if check_for_check(white_king['wk1'].position if self.color == WHITE else black_king['bk1'].position):
            available_moves = self.available_moves(present_position, next_position)
            if check_interruptions(next_position, available_moves) is False:
                if kill_piece(self, next_position) is True:
                    pass
        else:
            MOVE_FLAG = False
        
#         if self.color == WHITE:
#             possible_horizontal_moves = [(self.x + incr, self.y) for incr in range((self.x - 7),(9 - self.x)) if incr !=0]
#             possiblt_vertical_moves = [(self.x, self.y + incr) for incr in range((9-self.x),(self.x - 7)) if incr !=0]
#             if self.x == x:
#                 positions_to_cover = [(self.x, y + incr) if y > self.y 
#                                      else (self.x, y - incr)
#                                      for incr in range(1, abs(self.y - y) + 1)]
#             elif self.y == y:
#                 positions_to_cover = [(self.x + incr, y) if x > self.x 
#                                      else (self.x - incr, y)
#                                      for incr in range(1, abs(self.x - x) + 1)]
#             else:
#                 MOVE_FLAG = False
# 
#             if board_positions[next_position] != None:
#                 if next_position in possible_horizontal_moves:
#                     pass


    def available_moves(self, present_position, next_position):
        """Check Available Moves"""
        (x0, y0) = present_position
        (x1, y1) = next_position
        available_rook_moves = []
        if x0 == x1:
            return [(x0, y0 + incr) if y1 > y0 else (x0, y0 - incr) for incr in range(1, abs(y0 - y1) + 1)]
        elif y0 == y1:
            return [(x0 + incr, y0) if x1 > x0 else (x0 - incr, y0) for incr in range(1, abs(x0 - x1) + 1)]
        else:
            return available_rook_moves

class Knight(Piece):
    
    def __init__(self, x, y, color, status):
        super().__init__(x, y, color, status)
        self.symbol = '\u265E' if self.color == BLACK else '\u2658'
    
    def move(self, x, y):
        if self.color == 'black':
            if (x, y) in white_position_list:
                pass
        
    
    def available_moves(self, present_position, next_position):
        (x0, y0) = present_position 
        (x1, y1) = next_position
        available_moves_list = [(x0 - 2, y0 + 1), (x0 - 1, y0 + 2), (x0 + 1, y0 + 2), (x0 + 2, y0 + 1), (x0 + 2, y0 - 1), (x0 + 1, y0 - 2), (x0 - 1, y0 - 2), (x0 - 2, y0 - 1)]
        return available_moves_list
    
class Bishop(Piece):
    
    def __init__(self, x, y, color, status):
        super().__init__(x, y, color, status)
        self.symbol = '\u265D' if self.color == BLACK else '\u2657'
        
    def move(self, x, y):
        if self.color == 'black':
            if (x, y) in white_position_list:
                pass
    
    def available_moves(self, present_position, next_position):
        (x0, y0) = present_position 
        (x1, y1) = next_position
        available_moves_list = []
        available_bishop_moves = []
        if abs(x1 - x0) == abs(y1- y0):
            if y1 > y0 and x1 > x0:
                available_bishop_moves = [(x0 + incr, y0 + incr) for incr in range(1, abs(y0 - y1) + 1)]
            elif y1> y0 and x1 < x0:
                available_bishop_moves = [(x0 - incr, y0 + incr) for incr in range(1, abs(y0 - y1) + 1)]
            elif y1 < y0 and x1> x0:
                available_bishop_moves = [(x0 + incr, y0 - incr) for incr in range(1, abs(y0 - y1) + 1)]
            elif y1 < y0 and x1 < x0:
                available_bishop_moves = [(x0 + incr, y0 + incr) for incr in range(1, abs(y0 - y1) + 1)]
                
            available_moves_list = available_bishop_moves
        else:
            available_moves_list
            
        return available_moves_list
        
class Queen(Piece):
    
    def __init__(self, x, y, color, status):
        super().__init__(x, y, color, status)
        self.symbol = '\u265B' if self.color == BLACK else '\u2655'
        
    def move(self, x, y):
        if self.color == 'black':
            if (x, y) in white_position_list:
                if not check_for_check(self, x, y):
                    pass
#                     if kill_piece(x, y):
#                         self.x = x
#                         self.y = y
#                         MOVE_FLAG = True
#                     else:
#                         MOVE_FLAG = False
        
    def available_moves(self, present_position, next_position):
        (x0, y0) = present_position 
        (x1, y1) = next_position
        available_moves = []
        if abs(x1 - x0) == abs(y1- y0):
            available_moves = available_bishop_moves(present_position, next_position)
        else:
            available_moves = available_rook_moves(present_position, next_position)
        return available_moves

class King(Piece):

    def __init__(self, x, y, color, status):
        super().__init__(x, y, color, status)
        self.symbol = '\u265A' if self.color == BLACK else '\u2654'
    
    
    def move(self):
        pass
        
    def available_moves(self, present_position, next_position):
        (x0, y0) = present_position 
        (x1, y1) = next_position
        available_moves = [(x0 - 1, y0),(x0 + 1, y0),(x0 - 1, y0 - 1), (x0 + 1, y0 + 1), (x0 - 1, y0 + 1), (x0 + 1, y0 - 1),(x0, y0 + 1),(x0, y0 - 1)]
        return available_moves



class Board(object):
    def __init__(self):
        pass
    
    def update_board(self):
        board_list = [x for x in range(1,9)]
        for x, y in itertools.product(board_list,board_list):
            board_positions[(x,y)] = None
        new_board_positions = {}
        for piece in all_pieces.items():
            for position in board_positions.keys():
                if piece[-1].position == position and piece[-1].status == ALIVE:
                    new_board_positions[position] = piece
                    break
                else:
                    board_positions[position] = None
        board_positions.update(new_board_positions)
        for z in reversed(range(1,9)):
            print([board_positions[x][-1].symbol 
                   if board_positions[x] != None else None
                   for x in itertools.product(board_list,repeat =  2) 
                   if x[-1] == z]
            )


    


# when you kill the piece remove the piece from the position list and the 
# piece object dictionaries that are created herewith


def create_pieces():
    
    global white_pieces, black_pieces, all_pieces
    global black_pawn, white_pawn, black_rook, white_rook, black_knight
    global white_knight, black_bishop, white_bishop, black_queen, white_queen
    global white_king, black_king

    black_pawn = {'bp'+ str(x): Pawn(x, 7, BLACK, ALIVE) for x in range(1, 9)}
    white_pawn = {'wp'+ str(x): Pawn(x, 2, WHITE, ALIVE) for x in range(1, 9)}

    black_rook = {'br' + str(num + 1): Rook(x, 8, BLACK, ALIVE) for num, x in enumerate([1,8])}
    white_rook = {'wr' + str(num + 1): Rook(x, 1, WHITE, ALIVE) for num, x in enumerate([1,8])}

    black_knight = {'bkn' + str(num + 1): Knight(x, 8, BLACK, ALIVE) for num, x in enumerate([2,7])}
    white_knight = {'wkn' + str(num + 1): Knight(x, 1, WHITE, ALIVE) for num, x in enumerate([2,7])}

    black_bishop = {'bb' + str(num + 1): Bishop(x, 8, BLACK, ALIVE) for num, x in enumerate([3,6])}
    white_bishop = {'wb' + str(num + 1): Bishop(x, 1, WHITE, ALIVE) for num, x in enumerate([3,6])}

    black_queen = {'bq' + str(num + 1): Queen(x, 8, BLACK, ALIVE) for num, x in enumerate([4])}
    white_queen = {'wq' + str(num + 1): Queen(x, 1, WHITE, ALIVE) for num, x in enumerate([4])}

    black_king = {'bk' + str(num + 1): King(x, 8, BLACK, ALIVE) for num, x in enumerate([5])}
    white_king = {'wk' + str(num + 1): King(x, 1, WHITE, ALIVE) for num, x in enumerate([5])}

    white_pieces = {**white_pawn, **white_king, **white_queen, **white_rook,
                    **white_knight, **white_bishop}
    black_pieces = {**black_pawn, **black_king, **black_queen, **black_rook,
                    **black_knight, **black_bishop}
    all_pieces = {**white_pieces, **black_pieces}



create_pieces()

board = Board()
board.update_board()
print('')

# print(board_positions[(1,2)][-1].color)
piece = board_positions[(1,2)][-1]
# piece.status = KILLED
print(piece.status)

piece.move(1,3)
board.update_board()
print('')
