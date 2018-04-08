"""
Created on Feb 26, 2018
@author: NREPAL
"""

import itertools

WHITE = 'White'
BLACK = 'Black'
ALIVE = 'Alive'
KILLED = 'Killed'
MOVE_FLAG = False
KILL_FLAG = False
BOARD_POSITIONS = {}


def check_interruptions(piece, next_position, available_moves):
    """
    Checks if there are any pieces on the positions between start and
    final moves. This does not hold true for Knight and King as there are
    no positions between King start and final move. And Knight has no effect
    if there are pieces in between
    """
    kill_flag = False
    if piece.__class__.__name__ not in ['Knight', 'King']:
        interruptions = [1 if BOARD_POSITIONS[position]
                         is not None else 0 for position
                         in available_moves[
                         0:available_moves.index(next_position) + 1]
                         ]
    else:
        if BOARD_POSITIONS[next_position]:
            if BOARD_POSITIONS[next_position][-1].color != piece.color:
                return True, True
        else:
            return True, False

    killed_piece = interruptions.pop()
    if 1 not in interruptions:
        if killed_piece == 1:
            kill_flag = kill_piece(piece, next_position)
            move_flag = kill_flag
        else:
            move_flag = True
    else:
        move_flag = False

    return move_flag, kill_flag


def kill_piece(piece, next_position):
    """
    Checks if the piece on the final position can be killed by the piece on
    the start position
    """
    # try to see if you can write the code in such a way that this method would
    # also be implemented if the next_position is blank. It should return false
    # if the next position is blank
    try:
        if piece.color != BOARD_POSITIONS[next_position][-1].color:
            kill_flag = True
        else:
            kill_flag = False
    except KeyError:
        print("No piece found to be killed")

    return kill_flag


def check_for_check(self, move=None):
    """
    Checks to see of the opposite color team gets a check after this move
    """

    if self.color == WHITE:
        pieces = black_pieces.items()
        king_pos = white_king['wk1'].position if move is None else move
    else:
        pieces = white_pieces.items()
        king_pos = black_king['bk1'].position if move is None else move

    check = False
    for _, piece in pieces:
        if piece.status == ALIVE:
            if king_pos in piece.available_moves(piece.position, king_pos):
#                 if not isinstance(piece, Knight):
                if check_interruptions(piece, king_pos,
                                       piece.available_moves(
                                           piece.position,
                                           king_pos)) == (True, True):
                    return True

                    

    return check


def finalize_move(piece, kill_flag, next_position, checkmate=False):
    """
    Finalizes the move of the respective pieces and updates the board position
    and the piece position
    """
    global white_king, black_king, BOARD_POSITIONS
    present_position = piece.position
    if kill_flag:
        target_kill_piece = BOARD_POSITIONS[next_position][-1]
        target_kill_piece.status = KILLED
    piece.position = next_position
    board.update_board_positions()
    if check_for_check(white_king['wk1'] if piece.color == WHITE else black_king['bk1']):
        if kill_flag:
            target_kill_piece.status = ALIVE
        piece.position = present_position
        BOARD_POSITIONS = board.update_board_positions()
        MOVE_FLAG = False
        KILL_FLAG = False
        return False
    else:
        if checkmate:
            if kill_flag:
                target_kill_piece.status = ALIVE
            piece.position = present_position
            BOARD_POSITIONS = board.update_board_positions()
            MOVE_FLAG = False
            KILL_FLAG = False
        return True



class Piece(object):
    """
    Common class for most pieces
    """
    def __init__(self, x, y, color, status):
        """
        Constructor
        """
        self.x = x
        self.y = y
        self.color = color
        self.position = (x, y)
        self.status = status

    def move(self, present_position, next_position, available_moves):
        """
        Makes the move for the piece based upon its validity
        """
        global KILL_FLAG, MOVE_FLAG
        global BOARD_POSITIONS

        if next_position in available_moves:
            MOVE_FLAG, KILL_FLAG = check_interruptions(self, next_position, available_moves)
        else:
            MOVE_FLAG = False

        if MOVE_FLAG:
            if finalize_move(self, KILL_FLAG, next_position):
                board.update_board()
            else:
                print('Play a different Move. Its a CHECK!')
                MOVE_FLAG = False  
        else:
            print("Invalid move for %s" % (self.__class__.__name__))


class Pawn(Piece):

    def __init__(self, x, y, color, status):
        super().__init__(x, y, color, status)
        self.symbol = '\u265F' if self.color == BLACK else '\u2659'

    def move(self, x, y):
        (self.x, self.y) = self.position
        present_position = self.position
        next_position = (x, y)
        global MOVE_FLAG, KILL_FLAG, BOARD_POSITIONS
        if self.color == WHITE:
            initial_move = True if present_position[-1] == 2 else False
            beginning_move = [(self.x, self.y + 2)]
            possible_kill_moves = [
                (self.x - 1, self.y + 1), (self.x + 1, self.y + 1)]
            straight_move = [(self.x, self.y + 1)]

            if BOARD_POSITIONS[next_position] is not None:
                if BOARD_POSITIONS[next_position][-1].color == BLACK:
                    if next_position in possible_kill_moves:
                        KILL_FLAG = kill_piece(self, next_position)
                        MOVE_FLAG = KILL_FLAG
                    else:
                        MOVE_FLAG = False
                else:
                    MOVE_FLAG = False
            else:  # if no piece is present at the next position to be moved:
                if next_position in straight_move:
                    MOVE_FLAG = True
                elif next_position in beginning_move and initial_move:
                    MOVE_FLAG = True
                else:
                    MOVE_FLAG = False

        elif self.color == BLACK:
            initial_move = True if present_position[-1] == 7 else False
            beginning_move = [(self.x, self.y - 2)]
            possible_kill_moves = [
                (self.x - 1, self.y - 1), (self.x + 1, self.y - 1)]
            straight_move = [(self.x, self.y - 1)]

            if BOARD_POSITIONS[next_position] is not None:
                if BOARD_POSITIONS[next_position][-1].color == WHITE:
                    if next_position in possible_kill_moves:
                        KILL_FLAG = kill_piece(self, next_position)
                    else:
                        MOVE_FLAG = False
                else:
                    MOVE_FLAG = False
            else:  # if no piece is present at the next position to be moved:
                if next_position in straight_move:
                    MOVE_FLAG = True
                elif next_position in beginning_move and initial_move:
                    MOVE_FLAG = True
                else:
                    MOVE_FLAG = False

        if MOVE_FLAG:
            if finalize_move(self, KILL_FLAG, next_position):
                board.update_board()
            else:
                print('Play a different Move. Its a CHECK!')
                MOVE_FLAG = False
        else:
            print("Invalid move for %s" %(self.__class__.__name__))


    def available_moves(self, present_position, next_position):
        """
        Check available moves based on present position and next position
        if specified
        """

        available_moves = []
        if self.color == WHITE:
            beginning_move = [(self.x, self.y + 2)]
            possible_kill_moves = [
                (self.x - 1, self.y + 1), (self.x + 1, self.y + 1)]
            straight_move = [(self.x, self.y + 1)]
            available_moves = beginning_move + possible_kill_moves + straight_move
        elif self.color == BLACK:
            beginning_move = [(self.x, self.y - 2)]
            possible_kill_moves = [
                (self.x - 1, self.y - 1), (self.x + 1, self.y - 1)]
            straight_move = [(self.x, self.y - 1)]
            available_moves = beginning_move + possible_kill_moves + straight_move

        return available_moves


class Rook(Piece):

    def __init__(self, x, y, color, status):
        super().__init__(x, y, color, status)
        self.symbol = '\u265C' if self.color == BLACK else '\u2656'

    def move(self, x, y):

        present_position = self.position
        next_position = (x, y)
        available_moves = self.available_moves(present_position, next_position)
        Piece.move(self, present_position, next_position, available_moves)

    def available_moves(self, present_position, next_position):
        """
        Check available moves based on present position and next position
        if specified
        """
        (x0, y0) = present_position
        (x1, y1) = next_position
        available_rook_moves = []
        if x0 == x1:
            return [(x0, y0 + incr) if y1 > y0 else (x0, y0 - incr)
                    for incr in range(1, abs(y0 - y1) + 1)]
        elif y0 == y1:
            return [(x0 + incr, y0) if x1 > x0 else (x0 - incr, y0)
                    for incr in range(1, abs(x0 - x1) + 1)]
        else:
            return available_rook_moves


class Knight(Piece):

    def __init__(self, x, y, color, status):
        super().__init__(x, y, color, status)
        self.symbol = '\u265E' if self.color == BLACK else '\u2658'

    def move(self, x, y):
        global KILL_FLAG, BOARD_POSITIONS
        global MOVE_FLAG
        present_position = self.position
        next_position = (x, y)
        available_moves = self.available_moves(present_position, next_position)
        if next_position in available_moves:
            if BOARD_POSITIONS[next_position] is None:
                MOVE_FLAG = True
            else:
                KILL_FLAG = kill_piece(self, next_position)
                MOVE_FLAG = KILL_FLAG
        else:
            MOVE_FLAG = False

        if MOVE_FLAG:
            if finalize_move(self, KILL_FLAG, next_position):
                board.update_board()
            else:
                print('Play a different Move. Its a CHECK!')
                MOVE_FLAG = False
        else:
            print("Invalid move for %s" %(self.__class__.__name__))



    def available_moves(self, present_position, next_position):
        """
        Check available moves based on present position and next position
        if specified
        """
        (x0, y0) = present_position
        available_moves = [(x0 - 2, y0 + 1), (x0 - 1, y0 + 2),
                           (x0 + 1, y0 + 2), (x0 + 2, y0 + 1),
                           (x0 + 2, y0 - 1), (x0 + 1, y0 - 2),
                           (x0 - 1, y0 - 2), (x0 - 2, y0 - 1)]
        
        position_range = range(1,9)
        moves = available_moves.copy()
        for move in moves:
            if move[0] and move[-1] not in position_range:
                available_moves.remove(move)


        return available_moves


class Bishop(Piece):

    def __init__(self, x, y, color, status):
        super().__init__(x, y, color, status)
        self.symbol = '\u265D' if self.color == BLACK else '\u2657'

    def move(self, x, y):

        present_position = self.position
        next_position = (x, y)
        available_moves = self.available_moves(present_position, next_position)
        Piece.move(self, present_position, next_position, available_moves)


    def available_moves(self, present_position, next_position):
        """
        Check available moves based on present position and next position
        if specified
        """
        (x0, y0) = present_position
        (x1, y1) = next_position
        available_moves_list = []
        available_bishop_moves = []
        if abs(x1 - x0) == abs(y1 - y0):
            if y1 > y0 and x1 > x0:
                available_bishop_moves = [(x0 + incr, y0 + incr)
                                          for incr in range(1, abs(y0 - y1) + 1)]
            elif y1 > y0 and x1 < x0:
                available_bishop_moves = [(x0 - incr, y0 + incr)
                                          for incr in range(1, abs(y0 - y1) + 1)]
            elif y1 < y0 and x1 > x0:
                available_bishop_moves = [(x0 + incr, y0 - incr)
                                          for incr in range(1, abs(y0 - y1) + 1)]
            elif y1 < y0 and x1 < x0:
                available_bishop_moves = [(x0 - incr, y0 - incr)
                                          for incr in range(1, abs(y0 - y1) + 1)]

            available_moves_list = available_bishop_moves
        else:
            available_moves_list

        return available_moves_list


class Queen(Piece):

    def __init__(self, x, y, color, status):
        super().__init__(x, y, color, status)
        self.symbol = '\u265B' if self.color == BLACK else '\u2655'

    def move(self, x, y):

        present_position = self.position
        next_position = (x, y)
        available_moves = self.available_moves(present_position, next_position)
        Piece.move(self, present_position, next_position, available_moves)

    def available_moves(self, present_position, next_position):
        """
        Check available moves based on present position and next position
        if specified
        """
        (x0, y0) = present_position
        (x1, y1) = next_position
        available_moves = []
        if abs(x1 - x0) == abs(y1 - y0):
            available_moves = Bishop.available_moves(
                self, present_position, next_position)
        else:
            available_moves = Rook.available_moves(
                self, present_position, next_position)
        return available_moves


class King(Piece):

    def __init__(self, x, y, color, status):
        super().__init__(x, y, color, status)
        self.symbol = '\u265A' if self.color == BLACK else '\u2654'

    def move(self, x, y):

        global KILL_FLAG, BOARD_POSITIONS
        global MOVE_FLAG
        present_position = self.position
        next_position = (x, y)
        available_moves = self.available_moves(present_position, next_position)
        if next_position in available_moves:
            if BOARD_POSITIONS[next_position] is None:
                MOVE_FLAG = True
            else:
                KILL_FLAG = kill_piece(self, next_position)
                MOVE_FLAG = KILL_FLAG

        else:
            MOVE_FLAG = False
        
        if MOVE_FLAG == True:
            if finalize_move(self, KILL_FLAG, next_position):
                board.update_board()
            else:
                print('Play a different Move. Its a CHECK!')
                MOVE_FLAG = False
        else:
            print("Invalid move for %s" %(self.__class__.__name__))


    def available_moves(self, present_position, next_position = None):
        """
        Check available moves based on present position and next position
        if specified
        """
        (x0, y0) = present_position
        available_moves = [(x0 - 1, y0), (x0 + 1, y0), (x0 - 1, y0 - 1),
                               (x0 + 1, y0 - 1), (x0, y0 - 1),(x0, y0 + 1),
                               (x0 + 1, y0 + 1), (x0 - 1, y0 + 1)]
        
        position_range = range(1,9)
        moves = available_moves.copy()
        for move in moves:
            if move[0] and move[-1] not in position_range:
                available_moves.remove(move)
     
        return available_moves

def check_mate(king, piece):

    global KILL_FLAG, BOARD_POSITIONS, checkmate, board_positions_backup
    global MOVE_FLAG
    empty_positions = []
    pieces = white_pieces.items() if king.color == WHITE else black_pieces.items()
    for move in king.available_moves(king.position):
        if BOARD_POSITIONS[move] is None:
            # the following block checks if there is an empty position and if
            # the king moves to that position, will it still be a check for the
            # king if no, that means, that there is a position where the king
            # can avoid check and hence checkmate, so return false
            if finalize_move(king, KILL_FLAG, move, checkmate=True):
                return False
            else:
                empty_positions.append(move)
        else:
            if kill_piece(king, move):
                if finalize_move(king, kill_piece(king, move), move, 
                                 checkmate = True):
                    
                    return False
                else:
                    empty_positions.append(move)

        # if the check is been given by knight or king, then ignore the below block

        # the below block will test if there are empty positions which can be
        # filled with other pieces of the same color of king.color so that the check
        # can be avoided by interruption the path through which a check is given
    if empty_positions:
        if not isinstance(piece, Knight):
            for position in empty_positions:
                for _, piece_ in pieces:
                    if not isinstance(piece_, King):
                        if piece_.status == ALIVE:
                            if position in piece_.available_moves(piece_.position, position):
                                if position in piece.available_moves(piece.position, position):
                                    MOVE_FLAG, KILL_FLAG = check_interruptions(
                                        piece_, position, piece_.available_moves(
                                            piece_.position, position))
                                    if MOVE_FLAG:
                                        if finalize_move(piece_, KILL_FLAG, position, checkmate=True):
                                            return False
    # one test case also to check if the piece giving check can be killed by
    # pieces who got check
    for _, piece_ in pieces:
        if not isinstance(piece_, King):
            if piece.position in piece_.available_moves(piece_.position, piece.position):
                if check_interruptions(
                    piece_, piece.position, piece_.available_moves(
                        piece_.position, piece.position)
                            ) == (True, True):
                    if MOVE_FLAG:
                        if finalize_move(piece_, KILL_FLAG, position, checkmate=True):
                                            return False

    return True


class Board(object):
    def __init__(self):
        self.turn = WHITE

    def update_board_positions(self):
        board_list = [x for x in range(1, 9)]
        global BOARD_POSITIONS
        for x, y in itertools.product(board_list, board_list):
            BOARD_POSITIONS[(x, y)] = None
        new_board_positions = {}
        for piece in all_pieces.items():
            for position in BOARD_POSITIONS.keys():
                if piece[-1].position == position and piece[-1].status == ALIVE:
                    new_board_positions[position] = piece
                    break
                else:
                    BOARD_POSITIONS[position] = None
        board_positions_backup = BOARD_POSITIONS
        BOARD_POSITIONS.update(new_board_positions)
        return board_positions_backup

    def update_board(self):
        Board.update_board_positions(self)
        board_list = [x for x in range(1, 9)]
        global BOARD_POSITIONS
        for z in reversed(range(1, 9)):
            print('\n')
            print(z, end='\t')
            for elem in [BOARD_POSITIONS[x][-1].symbol + '\t'
                         if BOARD_POSITIONS[x] else '.\t'
                         for x in itertools.product(board_list, repeat=2)
                         if x[-1] == z]:
                print(elem, end='')
        print('\n\n')
        print('\t1\t2\t3\t4\t5\t6\t7\t8')


def create_pieces():

    global white_pieces, black_pieces, all_pieces
    global black_pawn, white_pawn, black_rook, white_rook, black_knight
    global white_knight, black_bishop, white_bishop, black_queen, white_queen
    global white_king, black_king

    black_pawn = {'bp' + str(x): Pawn(x, 7, BLACK, ALIVE) for x in range(1, 9)}
    white_pawn = {'wp' + str(x): Pawn(x, 2, WHITE, ALIVE) for x in range(1, 9)}

    black_rook = {'br' + str(num + 1): Rook(x, 8, BLACK, ALIVE)
                  for num, x in enumerate([1, 8])}
    white_rook = {'wr' + str(num + 1): Rook(x, 1, WHITE, ALIVE)
                  for num, x in enumerate([1, 8])}

    black_knight = {'bkn' + str(num + 1): Knight(x, 8, BLACK, ALIVE)
                    for num, x in enumerate([2, 7])}
    white_knight = {'wkn' + str(num + 1): Knight(x, 1, WHITE, ALIVE)
                    for num, x in enumerate([2, 7])}

    black_bishop = {'bb' + str(num + 1): Bishop(x, 8, BLACK, ALIVE)
                    for num, x in enumerate([3, 6])}
    white_bishop = {'wb' + str(num + 1): Bishop(x, 1, WHITE, ALIVE)
                    for num, x in enumerate([3, 6])}

    black_queen = {'bq' + str(num + 1): Queen(x, 8, BLACK, ALIVE)
                   for num, x in enumerate([4])}
    white_queen = {'wq' + str(num + 1): Queen(x, 1, WHITE, ALIVE)
                   for num, x in enumerate([4])}

    black_king = {'bk' + str(num + 1): King(x, 8, BLACK, ALIVE)
                  for num, x in enumerate([5])}
    white_king = {'wk' + str(num + 1): King(x, 1, WHITE, ALIVE)
                  for num, x in enumerate([5])}

    white_pieces = {**white_pawn, **white_king, **white_queen, **white_rook,
                    **white_knight, **white_bishop}
    black_pieces = {**black_pawn, **black_king, **black_queen, **black_rook,
                    **black_knight, **black_bishop}
    all_pieces = {**white_pieces, **black_pieces}


def parse_input(user_input):
    
    init_pos, fin_pos = user_input.split(':')
    global MOVE_FLAG, checkmate
    x0, y0 = init_pos.split(',')
    x1, y1 = fin_pos.split(',')
    try:
        piece = BOARD_POSITIONS[(int(x0), int(y0))][-1]

        if board.turn == piece.color :
            piece.move(int(x1), int(y1))
            if MOVE_FLAG:
                board.turn = BLACK if piece.color == WHITE else WHITE
                if check_for_check(white_king['wk1'] if piece.color == BLACK
                                   else black_king['bk1']):
                    checkmate = check_mate(white_king['wk1'] if piece.color == BLACK
                                           else black_king['bk1'], piece)
                    if checkmate:
                        print("Checkmate !!!")
                        print(piece.color, 'wins!')
                    else:
                        print("Its Check!")
                        print(board.turn, "to play...")
                else:
                    print("\n%s to play..." %(board.turn))
            else:
                print("\n%s to play..." %(board.turn))
    
        else:
            print("Its %s\'s turn! Play again." %(board.turn))
    
    except TypeError:
        print("No piece on the specified position")


# def main():
#     """Main Function"""
#   
#     create_pieces()
#     global MOVE_FLAG, KILL_FLAG, checkmate, board
#     board = Board()
#     board.update_board()
#     global userinput_list
#     userinput_list = []
#     checkmate = False
#     print("\n\n\nGame Set.\nLets Play!\n\nWhite to begin...")
#     while True:
#         try:
#             userinput = input('\nPlease specify the start position and final position:\n\n')
#             userinput_list.append(userinput)
#             print(userinput_list)
#             MOVE_FLAG = False,
#             KILL_FLAG = False
#             parse_input(userinput)
#             if checkmate:
#                 break
#         except ValueError:
#             print("Please specify the user input correctly")
             
                
def main():
    """DEBUG MAIN FUNCTION"""
   
    create_pieces()
    global MOVE_FLAG, KILL_FLAG, checkmate, board
    board = Board()
    board.update_board()
    global userinput_list
    userinput_list = []
    checkmate = False
    print("\n\n\nGame Set.\nLets Play!\n\nWhite to begin...")
    while True:
        try:
            userinput_list = ['5,2:5,4', '1,7:1,6', '4,1:6,3', 
                    '1,6:1,5', '6,1:3,4', '1,5:1,4', '8,1:8,4','6,3:6,7']
#             userinput_list2 = ['5,2:5,4', '3,7:3,5','7,1:6,3', '5,7:5,5', '6,3:5,5', '4,8:6,6',
#                                 '5,5:4,7','5,8:4,7', '5,4:5,5', '6,6:5,5']
#             userinput_list3 =['3,2:3,4', '5,7:5,5', '4,2:4,3', '7,2:7,4', '6,7:5,6', '4,7:4,5', '3,4:4,5', '3,4:4,5']
            userinput_list4 = ['5,2:5,4', '5,7:5,5', '7,1:6,3', '6,8:5,7', '6,3:5,5', '6,7:6,6', '4,1:8,5', '5,8:6,8', '8,5:6,7']
            userinput_list5 = ['5,2:5,4', '4,7:4,5', '4,1:5,2', '4,5:5,4', '5,2:2,5', '3,8:4,7']
            userinput_list6 = ['4,2:4,4', '5,7:5', '5,7:5,5', '6,7:6,5', '4,4:5,5', '7,7:7,5', '7,1:6,3', '6,8:8,6', '5,5:5,6', '7,5:7,4', '6.4:5,5', '6,3:5,5', '8,6:3,1', '4,1:3,1', '4,8:8,4', '7,2:7,3', '8,4:5,7', '5,5:6,7', '5,7:5,6', '6,7:8,8', '8,7:8,5', '3,1:8,6', '8,6:6,6', '5,6:8,6', '5,2:5,4', '8,6:5,3', '6,2:5,3', '4,7:4,6', '6,1:2,5', '3,7:3,6', '8,8:7,6', '3,6:2,5', '7,6:6,4', '3,8:5,6', '6,4:5,6']
            userinput_list7 = ['4,2:4,4', '1,7:1,5', '5,2:5,4', '7,8:8,6', '4,1:6,3', '1,5:1,4', '6,1:3,4', '2,7:2,6', '6,3:6,7', '5,7:5,5']
            for input_ in userinput_list7:
                userinput = input_
#             userinput = input('\nPlease specify the start position and final position:\n\n')
#             userinput_list.append(userinput)
               
                print(userinput)
                MOVE_FLAG = False,
                KILL_FLAG = False
                parse_input(userinput)
                if checkmate:
                    break
            break
        except ValueError:
            print("Please specify the user input correctly")

if __name__ == main():
    main()

