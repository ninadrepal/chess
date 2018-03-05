'''
Created on Feb 26, 2018

@author: NREPAL
'''



MOVE_FLAG = False
KILL_FLAG = False
WHITE = 'white'
BLACK = 'black'
black_position_list = []
white_position_list = []

def check_position(x, y):
    pass

def check_square_color(x, y):
    if x + y & 1:
        return BLACK # odd: 6 & 1 = 0
    else:
        return WHITE
    
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

class King(Piece):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, color)


class Black(Pawn, Rook, Bishop, Knight, Queen, King):
    def __init__(self, x, y, color):
        super().__init__(x, y, 'black')
        
        


# when you kill the piece remove the piece from the position list and the 
# piece object dictionaries that are created herewith

black_pawns = {x: Pawn(x, 7, WHITE) for x in range(1, 9)}
white_pawns = {x: Pawn(x, 2, BLACK) for x in range(1, 9)}

