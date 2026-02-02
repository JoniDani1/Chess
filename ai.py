import random
from engine import GameState
import math
# 1. THE BRAIN: This dictionary determines the AI's personality.
# Try changing these values later! (e.g., make 'pawn' worth 10 to see it become greedy)
piece_score = {"king": 0, "queen": 9, "rook": 5, "bishop": 3, "knight": 3, "pawn": 1}
gs = GameState()

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3  # Depth 2 = AI looks at: Its Move -> Your Reply. (Fast)
           # Depth 3 = AI looks at: Its Move -> Your Reply -> Its Reply. (Slower but smarter)



knightScore =  [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScore =  [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScore =   [[1, 1, 1, 3, 1, 1, 1, 1],
                [1, 2, 3, 3, 3, 1, 1, 1],
                [1, 3, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 3, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 3, 3, 1, 1, 1],
                [1, 1, 1, 3, 1, 1, 1, 1]]

rookScore =    [[4, 3, 4, 4, 4, 4, 3, 4],
                [4, 4, 4, 4, 4, 4, 4, 4],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [4, 4, 4, 4, 4, 4, 4, 4],
                [4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScore =   [[8, 8, 8, 8, 8, 8, 8, 8],
                    [8, 8, 8, 8, 8, 8, 8, 8],
                    [5, 6, 6, 7, 7, 6, 6, 5],
                    [2, 3, 3, 5, 5, 3, 3, 2],
                    [1, 2, 3, 4, 4, 3, 2, 1],
                    [1, 2, 3, 3, 3, 3, 2, 1],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScore =   [[0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [1, 2, 3, 3, 3, 3, 2, 1],
                    [1, 2, 3, 4, 4, 3, 2, 1],
                    [2, 3, 3, 5, 5, 3, 3, 2],
                    [5, 6, 6, 7, 7, 6, 6, 5],
                    [8, 8, 8, 8, 8, 8, 8, 8],
                    [8, 8, 8, 8, 8, 8, 8, 8]]
kingScore = [
    [ 2,  3,  1,  0,  0,  1,  3,  2],
    [ 2,  2,  0,  0,  0,  0,  2,  2],
    [-1, -2, -2, -2, -2, -2, -2, -1],
    [-2, -3, -3, -4, -4, -3, -3, -2],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3]
]

def find_best_move(gs, valid_moves):
    global next_move
    next_move = None
    global DEPTH
    alpha = -CHECKMATE
    beta = CHECKMATE

    random.shuffle(valid_moves) # Shuffle so AI doesn't play the same game every time
    
    current_turn = len(gs.move_log) // 2

    if current_turn >= 9:
        DEPTH = 4
    
    if current_turn >= 30:
        DEPTH = 5
    
    
    print(f"Turn {current_turn}: AI Strategy set to Depth {DEPTH}")
    
    # Start the recursive search
    find_move_minimax(gs, valid_moves, DEPTH, alpha, beta, gs.white_to_move)
    
    return next_move

def find_move_minimax(gs, valid_moves, depth, alpha, beta, white_to_move):
    global next_move
    
    # A. BASE CASE: If we hit max depth, just score the board and stop.
    if depth == 0:
        return score_board(gs)
    
    # B. MAXIMIZING (White wants POSITIVE score)
    if white_to_move:
        max_score = -CHECKMATE # Start with worst possible score
        for move in valid_moves:
            # 1. SIMULATE THE MOVE
            gs.make_move(move[0], move[1]) 
            
            # 2. RECURSE (Now it's Black's turn to minimize)
            next_moves = get_all_valid_moves(gs, 'black')
            score = find_move_minimax(gs, next_moves, depth - 1, alpha, beta, False)
            
            # 3. UNDO THE MOVE (Backtrack)
            gs.undo_move() 
            
            # 4. COMPARE
            if score > max_score:
                max_score = score
                if depth == DEPTH: # Only save the move at the top level
                    next_move = move
            alpha = max(alpha,score)
            if beta<=alpha:
                break
                    
        return max_score

    # C. MINIMIZING (Black wants NEGATIVE score)
    else: 
        min_score = CHECKMATE + 100 # Start with worst possible score (Positive is bad for Black)
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            next_moves = get_all_valid_moves(gs, 'white')
            score = find_move_minimax(gs, next_moves, depth - 1, alpha, beta, True)
            gs.undo_move()
            
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            beta = min(beta,score)
            if beta<=alpha:
                break
                    
        return min_score

def score_board(gs):
    # If the game is over, return extreme scores
    if gs.is_check('white') and not get_all_valid_moves(gs, 'white'):
        return -CHECKMATE # Black Wins
    if gs.is_check('black') and not get_all_valid_moves(gs, 'black'):
        return CHECKMATE # White Wins
    
    # Otherwise, sum up the material on board
    score = 0
    for row in range(8):
        for col in range(8):
            piece = gs.board[row][col]
            if piece:
                value = piece_score[piece.type]

                pos_bonus = 0
                
                if piece.type == 'pawn':
                    if piece.color == 'white':
                        pos_bonus = whitePawnScore[row][col]
                    else:
                        pos_bonus = blackPawnScore[row][col] # Already flipped in definition
                        
                elif piece.type == 'knight':
                    table = knightScore
                    if piece.color == 'white':
                        pos_bonus = table[row][col]
                    else:
                        pos_bonus = table[7-row][col] # Flip for Black
                        
                elif piece.type == 'bishop':
                    table = bishopScore
                    if piece.color == 'white':
                        pos_bonus = bishopScore[row][col]
                    else:
                        pos_bonus = table[7-row][col]
                        
                elif piece.type == 'rook':
                    table = rookScore
                    if piece.color == 'white':
                        pos_bonus = table[row][col]
                    else:
                        pos_bonus = table[7-row][col]
                        
                elif piece.type == 'queen':
                    table = queenScore
                    if piece.color == 'white':
                        pos_bonus = table[row][col]
                    else:
                        pos_bonus = table[7-row][col]
                
                elif piece.type == 'king':
                    table = kingScore
                    if piece.color == 'white':
                        pos_bonus = table[row][col]
                    else:
                        pos_bonus = table[7-row][col]
                value += pos_bonus * 0.1
                
                if piece.color == "white":
                    score += value
                else:
                    score -= value # Black pieces subtract from the score
                
    return score

def get_all_valid_moves(gs, color):
    # Helper to get every possible move for a specific color
    moves = []
    for r in range(8):
        for c in range(8):
            piece = gs.board[r][c]
            if piece and piece.color == color:
                valid_moves = gs.get_safe_moves(piece, r, c)
                for target in valid_moves:
                    moves.append(((r, c), target)) 
    return moves