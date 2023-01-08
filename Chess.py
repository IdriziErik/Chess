
class BoardModel:
    def __init__(self):
        self.board = []
        self.board.append(["R1","K1","B1","Q1","KG1","B1","K1","R1"])
        self.board.append(["[]","[]","[]","[]","[]","[]","[]","[]"])
        self.board.append(["[]","[]","[]","[]","[]","[]","[]","[]"])
        self.board.append(["[]","[]","[]","[]","[]","[]","[]","[]"])
        self.board.append(["[]","[]","[]","[]","[]","[]","[]","[]"])
        self.board.append(["[]","[]","[]","[]","P2","[]","[]","[]"])
        self.board.append(["[]","[]","[]","P2","[]","[]","[]","[]"])
        self.board.append(["R2","K2","B2","Q2","KG2","B2","K2","R2"])
        #self.board.append(["P1","P1","P1","[]","P1","P1","P1","P1"])

    def is_inbounds(self, start_row, start_col, end_row, end_col):
        return (-1 < start_row < 8) and (-1 < start_col < 8) and (-1 < end_row < 8) and (-1 < end_col < 8)

    """Doing this because the Board object is not subscriptable
    Need to provide a way to access the underlying array data structure
    From outside the board object.
    """
    def get(self, row, col):
        return self.board[row][col]

    def move(self, start_row, start_col, end_row, end_col):
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = "[]"

    def __str__(self):
        """This is a Operator Override/Magic Method/Dunder Methods
    
        Anytime a Board object is converted to a string, it calls this method:
        """
        out = ""
        for row in self.board:
            out += f"{row}\n"
        return out

class ChessController:
    def __init__(self):
        # Creation of the board
        self.board_model = BoardModel()
     
        # Probably would want a better variable name here player1_pieces, player2_pieces  
        player_1 = ["P1","R1","K1","B1","Q1","KG1"]
        player_2 = ["P2","R2","K2","B2","Q2","KG2"]

        self.player_move = "Player 1"
        #changes whos turn it is 
    def change_turn(self):

        if self.player_move == "Player 1":
            self.player_move = "Player 2"
        else:
            self.player_move = "Player 1"

    def start(self):
        # Main Game Loop
        while True:
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



            # Check if inbounds
            if not self.board_model.is_inbounds(start_row, start_col, end_row, end_col):
                print("That is not a coordinate on the board, please choose a row and column value beteen 0-7.")
                continue

            # Check if source piece is empty
            if source_piece == "[]":
                print("That starting location you picked doesnt have a piece in it, pick a different starting row and column.")
                continue

            # ensures users actually moves piece 
            if source_piece == destination_piece:
                print("You didn't move the " + source_piece + ", go again")
                continue

            # If move is legal: move piece
            if self.is_legal_move(start_row, start_col, end_row, end_col):
                self.board_model.move(start_row, start_col, end_row, end_col)
                self.change_turn()
            else:
                print("Invalid  move, try again")
    
    def is_legal_move(self, start_row, start_col, end_row, end_col):

        source_piece = self.board_model.get(start_row,start_col)
        destination_piece = self.board_model.get(end_row, end_col)

        #ensures players can only move their pieces 
        if self.player_move == "Player 1" and  "1" not in source_piece:
            print("Please select a player 1 piece")
            return False
        if self.player_move == "Player 2" and "2" not in source_piece:
            print("Please select a player 2 piece")
            return False
        #doesn't allow player to take a piece from their own team 
        if ("1" in source_piece and "1" in destination_piece) or ("2" in source_piece and "2" in destination_piece):
            print("Your own piece is in the destintion spot")
            return False

        if (("1" in source_piece and "2" in destination_piece) or ("2" in source_piece and "1" in destination_piece) or ("1" or "2" in source_piece and destination_piece == "[]")):

            # Check Player 1 Pawn Moves
            if source_piece == "P1":

                #P1 to be able to make a double jump if in row 1
                if start_row == 1 and end_col == start_col and self.board_model.get(start_row + 1,start_col) == "[]" and self.board_model.get(start_row + 2,start_col) == "[]" and (1 < end_row < 4):
                    return True
                    
                # Check Pawn attack
                elif (start_col != end_col):
                    # Check if piece diagonal right of P1 is opposite team
                    if ("2" in self.board_model.get(start_row + 1, start_col + 1) and (start_col < end_col < start_col + 2)):
                        return True
                    # Check if piece diagonal left of P1 is opposite team
                    elif ("2" in self.board_model.get(start_row + 1, start_col - 1) and (start_col > end_col > start_col - 2)):
                        return True

                elif (self.board_model.get(start_row + 1,start_col) == "[]") and (end_row == start_row + 1) and (start_col == end_col):
                    return True
                

            # Check Player 2 Pawn Moves
            if source_piece == "P2":
                #P2 to be able to make a double jump if in row 6
                if start_row == 6 and end_col == start_col and self.board_model.get(start_row -1,start_col) == "[]" and self.board_model.get(start_row -2,start_col) == "[]" and (3 < end_row < 6):
                    return True
                #P2 take a piece 
                elif (start_col != end_col):
                    #to take a piece that is diagonal left of P2
                    if ("1" in self.board_model.get(start_row - 1,start_col - 1)) and (start_col > end_col > start_col - 2):
                        return True
                    #to take a piece that is diagonal right of P2
                    elif ("1" in self.board_model.get(start_row - 1,start_col + 1)) and (start_col < end_col < start_col + 2):
                        return True

                elif (self.board_model.get(start_row -1,start_col) == "[]") and (end_row == start_row - 1) and (start_col == end_col):
                    return True

            if source_piece == "R1" or source_piece == "R2":
                #checks that if the column and row are being changed then the code returns false before running the function rook_move
                if not (((abs(start_row - end_row) > 0) and (abs(start_col - end_col) == 0)) or ((abs(start_row - end_row) == 0) and (abs(start_col - end_col) > 0))):
                    return False 

                #elif (source_piece == "R1" and "2" in destination_piece) or (source_piece == "R2" and "1" in destination_piece) or (destination_piece == "[]"):
                elif self.rook_move(start_row, start_col, end_row, end_col):
                    return True
            
                else:
                    print("You can't make the rook move like that")

            if source_piece == "B1" or source_piece == "B2":
                #checks that the bishop slope is 1
                if not (abs((start_row - end_row)/(start_col - end_col))) == 1:
                    print("Wrong")
                    return False 

                elif self.bishop_move(start_row, start_col, end_row, end_col):
                    return True

                else:
                    print("You can't make the bishop move like that")
            
            if source_piece == "Q1" or source_piece == "Q2":
                    
                if self.queen_move(start_row, start_col, end_row, end_col):
                    return True
                else:
                    print("You can't make the Queen move like that")

            if source_piece == "K1" or source_piece == "K2":

                if self.knight_move(start_row, start_col, end_row, end_col):
                    return True 
                else:
                    print("You can't make the Knight move like that")

            if source_piece == "KG1" or source_piece == "KG2":
                if self.king_move(start_row, start_col, end_row, end_col):
                    return True
                
            else:
                print("You can't make the King move like that")
                
  
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
                if not self.board_model.get(x,y) == "[]":
                    return False
            return True
        if (start_col - end_col != 0):
            #move rook right or left
            if start_col < end_col: 
                x = end_row
                y = start_col
            elif start_col > end_col: 
                x = end_row
                y = end_col
            for i in range(loop):
                y = y + 1
                if not self.board_model.get(x,y) == "[]":
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
                    if not self.board_model.get(x,y) == "[]":
                        return False 
            #bishop move diagonally down and left
            elif ((end_row > start_row) and (end_col < start_col)):
                x = start_row
                y = start_col
                for i in range (loop):
                    x = x + 1
                    y = y - 1 
                    if not self.board_model.get(x,y) == "[]":
                        return False 
            #bishop move diagonally up and right
            elif ((end_row < start_row) and (end_col > start_col)):
                x = start_row
                y = start_col
                for i in range (loop):
                    x = x - 1
                    y = y + 1 
                    if not self.board_model.get(x,y) == "[]":
                        return False 
            #bishop move diagonally up and left
            elif ((end_row < start_row) and (end_col < start_col)):
                x = start_row
                y = start_col
                for i in range (loop):
                    x = x - 1
                    y = y - 1 
                    if not self.board_model.get(x,y) == "[]":
                        return False 
            return True
    
    def queen_move(self, start_row, start_col, end_row, end_col):
        #allows queen to move like the rook 
        if ((start_row - end_row != 0) and (start_col - end_col == 0)) or ((start_row - end_row == 0) and (start_col - end_col != 0)):
            return self.rook_move(start_row, start_col, end_row, end_col)
        #allows queen to move like the bishop
        elif (abs((start_row - end_row)/(start_col - end_col))) == 1:
            return self.bishop_move(start_row, start_col, end_row, end_col)

        return False
            
    def knight_move(self, start_row, start_col, end_row, end_col):
        if ((start_row - end_row != 0) and (start_col - end_col == 0)) or ((start_row - end_row == 0) and (start_col - end_col != 0)):
            return False
        elif (abs((start_row - end_row)/(start_col - end_col))) == 1:
            return False
        elif (start_row - 3) < end_row < (start_row + 3) and (start_col - 3) < end_col < (start_col + 3):
            return True
        
        
    def king_move(self, start_row, start_col, end_row, end_col):
        if ((start_row - 2) < end_row < (start_row + 2)) and ((start_col - 2) < end_col < (start_col + 2)):
            return True
         

if __name__ == "__main__":
    chess = ChessController()
    chess.start()