class BoardModel:

    def __init__(self):
        self.board = []
        self.board.append([Piece("Rook",1), Piece("Knight",1), Piece("Bishop",1), Piece("Queen",1), Piece("King",1), Piece("Bishop",1), Piece("Knight",1), Piece("Rook",1)])
        self.board.append([Piece("Pawn",1), Piece("Pawn",1), Piece("Pawn",1), Piece("Pawn",1), Piece("Pawn",1), Piece("Pawn",1), Piece("Pawn",1), Piece("Pawn",1)],)
        self.board.append([None, None, None, None, None, None, None, None,])
        self.board.append([None, None, None, None, None, None, None, None,])
        self.board.append([None, None, None, None, None, None, None, None,])
        self.board.append([None, None, None, None, None, None, None, None,])
        self.board.append([Piece("Pawn",2), Piece("Pawn",2), Piece("Pawn",2), Piece("Pawn",2), Piece("Pawn",2), Piece("Pawn",2), Piece("Pawn",2), Piece("Pawn",2)])
        self.board.append([Piece("Rook",2), Piece("Knight",2), Piece("Bishop",2), Piece("Queen",2), Piece("King",2), Piece("Bishop",2), Piece("Knight",2), Piece("Rook",2)])

    def __str__(self):
        out = ""
        for row in self.board:
            for piece in row:
                if piece is not None:
                    out += f"{piece} "
                else:
                    out += "[ ]"
            out += "\n"
        return out  

    def is_inbounds(self, start_row, start_col, end_row, end_col):
        return (-1 < start_row < 8) and (-1 < start_col < 8) and (-1 < end_row < 8) and (-1 < end_col < 8)

    def get(self, row, col):
        return self.board[row][col]

    def move(self, start_row, start_col, end_row, end_col):
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = None

class Piece:

    def __init__(self, piece_type, player_turn):
        self.piece_type = piece_type
        self.player_turn = player_turn

    def __str__(self):
        if self.player_turn == 1:
            if self.piece_type == "Rook": 
                return "R1"
            elif self.piece_type == "Knight": 
                return "K1"
            elif self.piece_type == "Bishop": 
                return "B1"
            elif self.piece_type == "Queen": 
                return "Q1"
            elif self.piece_type == "King": 
                return "KG1"
            elif self.piece_type == "Pawn": 
                return "P1"
        elif self.player_turn == 2:
            if self.piece_type == "Rook": 
                return "R2"
            elif self.piece_type == "Knight": 
                return "K2"
            elif self.piece_type == "Bishop": 
                return "B2"
            elif self.piece_type == "Queen": 
                return "Q2"
            elif self.piece_type == "King": 
                return "KG2"
            elif self.piece_type == "Pawn": 
                return "P2"

class ChessController:
    def __init__(self):
        self.board_model = BoardModel()

        self.player_move = "Player 1"
    def change_turn(self):

        if self.player_move == "Player 1":
            self.player_move = "Player 2"
        else:
            self.player_move = "Player 1"

    def start(self):
        # Main Game Loop
        while True:
            try:
                print(self.board_model)
                print("It is " + self.player_move + " turn to move a piece")
        
                # User Input
                start_row = int (input ("Row Number Start: "))
                start_col = int (input ("Column Number Start: "))
                end_row = int (input ("Row Number Destination: "))
                end_col = int (input ("Column Number Destination: "))
                print("\n")
                
                source_piece = self.board_model.get(start_row,start_col)
                destination_piece = self.board_model.get(end_row, end_col)
                
            except ValueError:
                print("Need to give a number for row and column")

            # Check if inbounds
            if not self.board_model.is_inbounds(start_row, start_col, end_row, end_col):
                print("That is not a coordinate on the board, please choose a row and column value beteen 0-7.")
                continue

            # Check if source piece is empty
            if source_piece == None:
                print("That starting location you picked doesnt have a piece in it, pick a different starting row and column.")
                continue

            # ensures users actually moves piece 
            if source_piece == destination_piece:
                print("You didn't move the " + source_piece + ", go again")
                continue

            #if self.board_model.king_position():
            #    print(self.king1_position)
            #    print(self.king2_position)

            # If move is legal: move piece
            if self.is_legal_move(start_row, start_col, end_row, end_col):
                self.board_model.move(start_row, start_col, end_row, end_col)
                self.change_turn()
            else:
                print("Invalid  move, try again")
    

    def is_legal_move(self, start_row, start_col, end_row, end_col):

        source_piece = self.board_model.get(start_row,start_col)
        destination_piece = self.board_model.get(end_row, end_col)

        if source_piece is not None:

        #ensures players can only move their pieces 
            if self.player_move == "Player 1" and source_piece.player_turn != 1:
                print("Please select a player 1 piece")
                return False
            if self.player_move == "Player 2" and source_piece.player_turn != 2:
                print("Please select a player 2 piece")
                return False
            #doesn't allow player to take a piece from their own team 
            if (destination_piece is not None) and ((source_piece.player_turn == 1 and destination_piece.player_turn == 1) or (source_piece.player_turn == 2 and destination_piece.player_turn == 2)):
                print("Your own piece is in the destintion spot")
                return False

            if (((source_piece.player_turn == 1 or source_piece.player_turn == 2) and destination_piece == None) or (source_piece.player_turn == 1 and destination_piece.player_turn == 2) or (source_piece.player_turn == 2 and destination_piece.player_turn == 1)):

                # Check Player 1 Pawn Moves
                if source_piece.piece_type == "Pawn":
                    if self.pawn_move(source_piece, start_row, start_col, end_row, end_col):
                        return True
                    else:
                        print("You can't make the pawn move like that")
                        return False

                elif source_piece.piece_type == "Rook" and (source_piece.player_turn == 1 or source_piece.player_turn == 2):
                    #checks that if the column and row are being changed then the code returns false before running the function rook_move
                    if not (((abs(start_row - end_row) > 0) and (abs(start_col - end_col) == 0)) or ((abs(start_row - end_row) == 0) and (abs(start_col - end_col) > 0))):
                        return False 

                    #elif (source_piece == "R1" and "2" in destination_piece) or (source_piece == "R2" and "1" in destination_piece) or (destination_piece == None):
                    elif self.rook_move(start_row, start_col, end_row, end_col):
                        return True
                
                    else:
                        print("You can't make the rook move like that")
                        return False 

                elif source_piece.piece_type == "Bishop" and (source_piece.player_turn == 1 or source_piece.player_turn == 2):
                    #checks that the bishop slope is 1
                    if not (abs((start_row - end_row)/(start_col - end_col))) == 1:
                        return False 

                    elif self.bishop_move(start_row, start_col, end_row, end_col):
                        return True

                    else:
                        print("You can't make the bishop move like that")
                        return False

                elif source_piece.piece_type == "Queen" and (source_piece.player_turn == 1 or source_piece.player_turn == 2):
                        
                    if self.queen_move(start_row, start_col, end_row, end_col):
                        return True
                    else:
                        print("You can't make the Queen move like that")
                        return False

                elif source_piece.piece_type == "Knight" and (source_piece.player_turn == 1 or source_piece.player_turn == 2):

                    if self.knight_move(start_row, start_col, end_row, end_col):
                        return True 
                    else:
                        print("You can't make the Knight move like that")
                        return False

                elif source_piece.piece_type == "King" and (source_piece.player_turn == 1 or source_piece.player_turn == 2):
                    if self.king_move(start_row, start_col, end_row, end_col): 
                        return True
                    
                    else:
                        print("You can't make the King move like that")
                        return False
        else:
            return False
    
    def pawn_move(self, source_piece, start_row, start_col, end_row, end_col):
        
        #Control movement of player 1 pawn
        if source_piece.player_turn == 1:
            #allow pawn to double jump on first move
            if start_row == 1 and end_col == start_col and self.board_model.get(start_row + 1,start_col) == None and self.board_model.get(start_row + 2,start_col) == None and (1 < end_row < 4):
                return True
            #pawn to attack an opponents piece 
            elif (start_col != end_col) and (abs(end_col - start_col) == 1) and (end_row - start_row == 1):
                return True 
            #normal pawn move of moving one spot vertically 
            elif (end_col == start_col and (end_row == start_row + 1) and self.board_model.get(end_row, end_col) == None):
                return True 

         #Control movement of player 2 
        if source_piece.player_turn == 2:
            #allow pawn to double jump on first move
            if start_row == 6 and end_col == start_col and self.board_model.get(start_row - 1 ,start_col) == None and self.board_model.get(start_row - 2,start_col) == None and (6 > end_row > 3):
                return True
            #pawn to attack an opponents piece 
            elif (start_col != end_col) and (abs(end_col - start_col) == 1) and (start_row - end_row == 1):
                return True 
            #normal pawn move of moving one spot vertically 
            elif (end_col == start_col and (end_row == start_row - 1) and self.board_model.get(end_row, end_col) == None):
                return True     
            
    def rook_move(self, start_row, start_col, end_row, end_col):

        loop = abs((end_row - start_row) + (end_col - start_col)) - 1
        if (start_row - end_row != 0):
            #move rook down or up
            if start_row < end_row:
                x = start_row
                y = end_col  
            elif start_row > end_row:
                x = end_row
                y = end_col 
            for i in range(loop):
                x = x + 1
                if not self.board_model.get(x,y) == None:
                    return False
            return True  

        elif (start_col - end_col != 0):
            #move rook right or left
            if start_col < end_col: 
                x = end_row
                y = start_col
            elif start_col > end_col: 
                x = end_row
                y = end_col
            for i in range(loop):
                y = y + 1
                if not self.board_model.get(x,y) == None:
                    return False
            return True

    def bishop_move(self, start_row, start_col, end_row, end_col):
            
        loop = abs(end_row - start_row) -1
           
        #bishop move diagonally down and right
        if ((end_row > start_row) and (end_col > start_col)):
            x = start_row
            y = start_col
            for i in range (loop):
                x = x + 1
                y = y + 1 
                if not self.board_model.get(x,y) == None:
                    return False 
            return True
        #bishop move diagonally down and left
        elif ((end_row > start_row) and (end_col < start_col)):
            x = start_row
            y = start_col
            for i in range (loop):
                x = x + 1
                y = y - 1 
                if not self.board_model.get(x,y) == None:
                    return False 
            return True
        #bishop move diagonally up and right
        elif ((end_row < start_row) and (end_col > start_col)):
            x = start_row
            y = start_col
            for i in range (loop):
                x = x - 1
                y = y + 1 
                if not self.board_model.get(x,y) == None:
                    return False 
            return True

        #bishop move diagonally up and left
        elif ((end_row < start_row) and (end_col < start_col)):
            x = start_row
            y = start_col
            for i in range (loop):
                x = x - 1
                y = y - 1 
                if not self.board_model.get(x,y) == None:
                    return False 
            return True
    
    def queen_move(self, start_row, start_col, end_row, end_col):
        #allows queen to move like the rook 
        if ((start_row - end_row != 0) and (start_col - end_col == 0)) or ((start_row - end_row == 0) and (start_col - end_col != 0)):
            return self.rook_move(start_row, start_col, end_row, end_col)

        #allows queen to move like the bishop
        elif (abs((start_row - end_row)/(start_col - end_col))) == 1:
            return self.bishop_move(start_row, start_col, end_row, end_col)

        else:
            return False
            
    def knight_move(self, start_row, start_col, end_row, end_col):
        if ((start_row - end_row != 0) and (start_col - end_col == 0)) or ((start_row - end_row == 0) and (start_col - end_col != 0)):
            return False
        elif (abs((start_row - end_row)/(start_col - end_col))) == 1:
            return False
        elif (start_row - 3) < end_row < (start_row + 3) and (start_col - 3) < end_col < (start_col + 3):
            return True
        else:
            return False
        
    def king_move(self, start_row, start_col, end_row, end_col):
        if ((start_row - 2) < end_row < (start_row + 2)) and ((start_col - 2) < end_col < (start_col + 2)):
            return True

        else:
            return False
         

if __name__ == "__main__":
    chess = ChessController()
    chess.start()