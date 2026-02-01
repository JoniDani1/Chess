import random
from engine import GameState
import threading
# 1. THE BRAIN: This dictionary determines the AI's personality.
# Try changing these values later! (e.g., make 'pawn' worth 10 to see it become greedy)
piece_score = {"king": 0, "queen": 9, "rook": 5, "bishop": 3, "knight": 3, "pawn": 1}
gs = GameState()
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3  # Depth 2 = AI looks at: Its Move -> Your Reply. (Fast)
           # Depth 3 = AI looks at: Its Move -> Your Reply -> Its Reply. (Slower but smarter)

def find_best_move(gs, valid_moves):
    global next_move
    next_move = None
    random.shuffle(valid_moves) # Shuffle so AI doesn't play the same game every time
    
    # Start the recursive search
    find_move_minimax(gs, valid_moves, DEPTH, gs.white_to_move)
    
    return next_move

def find_move_minimax(gs, valid_moves, depth, white_to_move):
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
            score = find_move_minimax(gs, next_moves, depth - 1, False)
            
            # 3. UNDO THE MOVE (Backtrack)
            gs.undo_move() 
            
            # 4. COMPARE
            if score > max_score:
                max_score = score
                if depth == DEPTH: # Only save the move at the top level
                    next_move = move
                    
        return max_score

    # C. MINIMIZING (Black wants NEGATIVE score)
    else: 
        min_score = CHECKMATE + 100 # Start with worst possible score (Positive is bad for Black)
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            next_moves = get_all_valid_moves(gs, 'white')
            score = find_move_minimax(gs, next_moves, depth - 1, True)
            gs.undo_move()
            
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
                    
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