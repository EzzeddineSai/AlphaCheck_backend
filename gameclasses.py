import copy

#0 empty. 1 black, 2 black king, -1 white, -2 white king, -3 DNE
#black starts
main_board = [[-3, 1,-3, 1,-3, 1,-3, 1],
              [ 1,-3, 1,-3, 1,-3, 1,-3],
              [-3, 1,-3, 1,-3, 1,-3, 1],
              [ 0,-3, 0,-3, 0,-3, 0,-3], 
              [-3, 0,-3, 0,-3, 0,-3, 0],
              [-1,-3,-1,-3,-1,-3,-1,-3],
              [-3,-1,-3,-1,-3,-1,-3,-1],
              [-1,-3,-1,-3,-1,-3,-1,-3]]

moves_per_piece = [(2,2),(1,1),(-2,-2),(-1,-1),(2,-2),(1,-1),(-2,2),(-1,1)]
 #for a jump, this is the move between the jump and current move
in_between = {(2,2):(1,1),(-2,-2):(-1,-1),(2,-2):(1,-1),(-2,2):(-1,1)}

index_to_move = {}
move_to_index = {}

index = 0
for i in range(8):
    for j in range(8):
        if main_board[i][j] != -3:
            for k in range(8): #loop over board pieces and each of the 8 moves per piece
                #if k < 4: #remove out of bound moves
                    
                new_i = i + moves_per_piece[k][0]
                new_j = j + moves_per_piece[k][1]
                    #if new_i <= 7 and new_i >=0 and new_j <= 7 and new_j >=0:
                index_to_move[index] = ((i,j),moves_per_piece[k])
                move_to_index[((i,j),moves_per_piece[k])] = index
                index += 1
                #else:
                #    index_to_move[index] = ((i,j),moves_per_piece[k])
                #    move_to_index[((i,j),moves_per_piece[k])] = index
                #    index += 1
                    
general_moves = list(move_to_index.keys())                                                

def sign(x):
    if x > 0:
        return 1
    else:
        return -1

def is_legal(board, player_turn, move): #legal is weaker than allowed
    
    source = (move[0][0], move[0][1])
    #print(source, board, player_turn,move)
    
   
    if sign(board[source[0]][source[1]]) != sign(player_turn):
        return False
    
    new_i, new_j = (source[0] + move[1][0],  source[1] + move[1][1]) #source+move
    
    if board[source[0]][source[1]] != 0:
        
        if new_i <= 7 and new_i >=0 and new_j <= 7 and new_j >=0:
            if abs(move[1][0]) == 1 and sign(move[1][0]) == sign(player_turn): #moving forward
                if board[new_i][new_j] == 0:
                    return True
                else:
                    return False
            
            elif  (move[1][0] == 1 and board[source[0]][source[1]] == -2) or (move[1][0] == -1 and board[source[0]][source[1]] == 2): #is king and moving 1 step back
                if board[new_i][new_j] == 0:
                    return True
                else:
                    return False
            elif abs(move[1][0]) == 2 and sign(move[1][0]) == sign(player_turn): #2 moves forward
                in_between_move = in_between[move[1]]
                in_between_piece_i, in_between_piece_j = (source[0] + in_between_move[0], source[1] + in_between_move[1])
                if board[in_between_piece_i][in_between_piece_j] != 0:
                    if board[new_i][new_j] == 0 and sign(board[in_between_piece_i][in_between_piece_j]) == -1*sign(player_turn): #in between piece is enemy
                        return True
                    else:
                        return False
                else:
                    return False
            elif  abs(move[1][0]) == 2 and sign(move[1][0]) == -1*sign(player_turn) and abs(board[source[0]][source[1]]) == 2: #(move[1][0] == 2 and board[source[0]][source[1]] == -2) or (move[1][0] == -2 and board[source[0]][source[1]] == 2): #2 moves backward and king
                in_between_move = in_between[move[1]]
                in_between_piece_i, in_between_piece_j = (source[0] + in_between_move[0], source[1] + in_between_move[1])
                if board[in_between_piece_i][in_between_piece_j] != 0:
                    if board[new_i][new_j] == 0 and sign(board[in_between_piece_i][in_between_piece_j]) == -1*sign(player_turn): #in between piece is enemy
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            
            return False
    else:
        return False

        
def find_possible_moves(board, player_turn): #board, player_turn is the state, sequence_piece
    possible_moves = []
    for i in range(len(general_moves)):
        move = index_to_move[i]
        #print("the following is legal: ", move)
        if is_legal(board, player_turn,move):
            possible_moves.append(move)
        
        #for j in range(8):
        #    all_moves = [(1,1),(-1,-1),(1,-1),(-1,1),"promote"]
            #if board[i][j] > 0 and 3: #board[i][j]
            
    return possible_moves

def find_legal_moves(board, player_turn, sequence_piece):
    """
    sequence_piece: piece which currently has the freedom to move
    """
    possible_moves = find_possible_moves(board, player_turn)
    forced_moves = []
    for move in possible_moves:
        if abs(move[1][0]) == 2:
            forced_moves.append(move)
    
    if sequence_piece == None:
        if len(forced_moves) == 0:
            return possible_moves
        else:
            return forced_moves
    else: #sequence piece is forced to move, thus only sequence piece can move
        #piece_possible_moves = []
        piece_forced_moves = []
        for move in possible_moves:
            if move[0] == sequence_piece: #filter to moves involving sequence piece
                if abs(move[1][0]) == 2: #if its a take move add it
                    piece_forced_moves.append(move)
        return piece_forced_moves
        #        piece_possible_moves.append(move)
        #if len(piece_possible_moves) == 0:
        #    return piece_possible_moves
        #else:


class GameState:
    def __init__(self,**kwargs):
        self.board = copy.deepcopy(kwargs.get('board',main_board))
        self.player_turn = kwargs.get('player_turn',1) #player_turn#####FIX HERE MAKE RANDOM
        self.sequence_piece = kwargs.get('sequence_piece',None) 
        self.human_player_color = kwargs.get('human_player_color',None)
        self.game_length = 0
        #self.starting_state = kwargs.get('starting_state',None) 

    def is_human_turn(self): #checks if its human's turn
        if self.player_turn == self.human_player_color:
            return True
        else:
            return False

    def transition(self, move): #move: (source, movement)
        #assumes legal moves (Takes sequence into account)
        #board = copy.deepcopy(brd)
        self.game_length += 1
        source_i, source_j = move[0]
        sequence_piece = None #keeps record of wether a sequence move needs to be recorded
        if abs(move[1][0]) == 1: #simple move (kings allowed)
            

            self.board[source_i+move[1][0]][source_j+move[1][1]] = self.board[source_i][source_j] 
            self.board[source_i][source_j] = 0
            if self.player_turn == -1 and source_i+move[1][0] == 0: #promote
                self.board[source_i+move[1][0]][source_j+move[1][1]] = -2
                
            elif self.player_turn == 1 and source_i+move[1][0] == 7: #promote
                self.board[source_i+move[1][0]][source_j+move[1][1]] = 2
            
        else: # 2 step move
            in_between_move = in_between[move[1]]
            in_between_piece_i, in_between_piece_j = (source_i + in_between_move[0], source_j + in_between_move[1])
            self.board[in_between_piece_i][in_between_piece_j] = 0
            self.board[source_i+move[1][0]][source_j+move[1][1]] = self.board[source_i][source_j]
            self.board[source_i][source_j] = 0
            
            if self.player_turn == -1 and source_i+move[1][0] == 0 and self.board[source_i+move[1][0]][source_j+move[1][1]] == -1: #allowed to promote if a piece is eaten
                self.board[source_i+move[1][0]][source_j+move[1][1]] = -2 #promoting ends move
            elif self.player_turn == 1 and source_i+move[1][0] == 7 and self.board[source_i+move[1][0]][source_j+move[1][1]] == 1: #promote
                self.board[source_i+move[1][0]][source_j+move[1][1]] = 2 #promoting ends move
                
            else: # did not promote
                if len(find_legal_moves(self.board,self.player_turn,(source_i+move[1][0],source_j+move[1][1]))) > 0: #forced moves avlbl
                    sequence_piece = (source_i+move[1][0],source_j+move[1][1])

        if sequence_piece == None:  # will transition player
            self.player_turn = -1*self.player_turn
            self.sequence_piece = sequence_piece
        else:
            self.sequence_piece = sequence_piece
        

    def return_game_state(self,):
        return {'board': self.board, 'sequence piece': self.sequence_piece, 'player turn': self.player_turn}

def state_compression(original_state):
    #  3 is sequence piece, 4 is sequence king
    state = copy.deepcopy(original_state)
    sequence_piece = state['sequence piece']
    board = state['board']
    if sequence_piece != None:
        sequence_piece_piece = board[sequence_piece[0]][sequence_piece[1]]
        if sequence_piece_piece == 1:
            board[sequence_piece[0]][sequence_piece[1]] = 3
        elif sequence_piece_piece == -1:
            board[sequence_piece[0]][sequence_piece[1]] = -3
        elif sequence_piece_piece == 2:
            board[sequence_piece[0]][sequence_piece[1]] = 4
        else:
            board[sequence_piece[0]][sequence_piece[1]] = -4
    
    compressed_state = []
    for i in range(8):
        for j in range(8):
            if (i+j)%2 != 0:
                compressed_state.append(board[i][j])
    compressed_state.append(state['player turn'])
    return compressed_state