import pygame
import sys
import ai
from settings import *
from components import *
from engine import GameState

# 1. Initialize Pygame
pygame.init()
pygame.mixer.init()

# 2. Setup Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Project")
clock = pygame.time.Clock()


# 3. Load Assets
PIECE_IMAGES = {}
def load_images():
    pieces = ['pawn', 'rook', 'knight', 'bishop', 'king', 'queen']
    for color in ['white', 'black']:
        for p in pieces:
            path = f"images/{color}_{p}.png"
            try:
                img = pygame.image.load(path)
                PIECE_IMAGES[f"{color}_{p}"] = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
            except FileNotFoundError:
                surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                surf.fill((200, 200, 200) if color == 'white' else (50, 50, 50))
                PIECE_IMAGES[f"{color}_{p}"] = surf

# 4. Global State
gs = GameState()
audio = SoundManager()
load_images()
selected_piece = None
selected_pos = None

# Variables for Game Over State
game_over = False
winner_text = ""

# --- VISUALS ---
def draw_board():
    #should_flip = not gs.white_to_move 
    
    for row in range(8):
        for col in range(8):
            draw_r = row
            draw_c = col
            
            color = WHITE_SQ if (row + col) % 2 == 0 else BLACK_SQ
            pygame.draw.rect(screen, color, (draw_c * SQUARE_SIZE, draw_r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            piece = gs.board[row][col]
            if piece:
                img_key = f"{piece.color}_{piece.type}"
                screen.blit(PIECE_IMAGES[img_key], (draw_c * SQUARE_SIZE, draw_r * SQUARE_SIZE))
                
    if selected_pos:
        r, c = selected_pos
        pygame.draw.rect(screen, HIGHLIGHT, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

    # Draw Game Over Text
    if game_over:
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(150)
        s.fill((255, 255, 255))
        screen.blit(s, (0,0))
        text = big_font.render(winner_text, True, (0,0,0))
        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, rect)
        

# --- INPUT ---
def handle_click(pos):
    global selected_piece, selected_pos, game_over, winner_text
    
    if game_over: return

    col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
    
    
        
    if selected_piece:
        start_r, start_c = selected_pos

        
        safe_moves = gs.get_safe_moves(selected_piece, start_r, start_c)
    

        if (row, col) in safe_moves:
            gs.make_move((start_r, start_c), (row, col))

            piece = gs.board[row][col]
            if piece.type == 'pawn' and (row == 0 or row == 7):
                piece.type = 'queen'

            audio.play('move')
            selected_piece = None
            selected_pos = None
            
            
            # Check for Checkmate / Game Over
            turn = 'white' if gs.white_to_move else 'black'
            if gs.is_game_over_check(turn):
                game_over = True
                audio.play("notify")
                if gs.is_check(turn):
                    winner_text = f"Checkmate! {'Black' if turn=='white' else 'White'} Wins!"
                else:
                    winner_text = "Stalemate!"
        else:
            selected_piece = None
            selected_pos = None
            
    else:
        piece = gs.board[row][col]
        if piece and ((gs.white_to_move and piece.color == 'white') or (not gs.white_to_move and piece.color == 'black')):
            selected_piece = piece
            selected_pos = (row, col)
        
        

            

def reset_game():
    # 1. Access the global UI variables
    global game_over, winner_text, selected_piece, selected_pos
   
    # 2. Reset UI State
    game_over = False
    winner_text = ""
    selected_piece = None
    selected_pos = None
    
    # 3. Reset the Engine (The Brain)
    gs.reset()

# --- MAIN LOOP ---
def main():
    # --- ADD THIS LINE TO FIX THE ERROR ---
    global game_over, winner_text
    # --------------------------------------

    while True:
        # --- AI TURN LOGIC ---
        
        if not game_over and not gs.white_to_move:
            valid_moves = ai.get_all_valid_moves(gs, 'black')
            best_move = ai.find_best_move(gs, valid_moves)
            
            if best_move:
                gs.make_move(best_move[0], best_move[1])
                
                end_r, end_c = best_move[1]
                piece = gs.board[end_r][end_c]
                if piece.type == 'pawn' and (end_r == 0 or end_r == 7):
                    piece.type = 'queen' 
                audio.play('move')
                
                # Check if AI won
                if gs.is_game_over_check('white'):
                    game_over = True
                    audio.play("notify")
                    if gs.is_check('white'):
                        winner_text = "Checkmate! Black Wins!"
                    else:
                        winner_text = "Stalemate!"
                elif gs.is_game_over_check('black'):
                    game_over = True
                    audio.play("notify")
                    if gs.is_check("black"):
                        winner_text = "Checkmate! White Wins!"
                    else:
                        winner_text = "Stalemate"
            else:
                # 2. Safety Fallback: If AI returns None (panic), make a random move
                import random
                if valid_moves:
                    random_move = valid_moves[random.randint(0, len(valid_moves)-1)]
                    gs.make_move(random_move[0], random_move[1])
                    audio.play('move')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and gs.white_to_move:
                handle_click(pygame.mouse.get_pos())
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gs.undo_move()

                if event.key == pygame.K_SPACE:
                    if game_over:
                        reset_game()

        draw_board()
        pygame.display.flip()
        clock.tick(FPS)



if __name__ == "__main__":
    main()