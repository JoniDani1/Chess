import pygame
import sys
import ai
from settings import *
from components import *
from engine import GameState
import threading 
import queue
import copy
import asyncio

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
            #turn = 'white' if gs.white_to_move else 'black'
            if gs.is_game_over_check("white"):
                game_over = True
                audio.play("notify")
                if gs.is_check("white"):
                    winner_text = f"Checkmate! Black Wins!"
                    print("Black Wins")
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

def ai_worker(gs, return_queue):
    """
    Runs the AI logic in a separate thread to prevent UI freezing.
    """
    # Generate moves and find the best one
    valid_moves = ai.get_all_valid_moves(gs, 'black')
    if valid_moves:
        best_move = ai.find_best_move(gs, valid_moves)
        return_queue.put(best_move) 
    else:
        return_queue.put(None)


async def main():
    global game_over, winner_text

   
    ai_thinking = False
    ai_queue = queue.Queue() 
    ai_thread = None

    while True:
    
        if not game_over and not gs.white_to_move:
            
            # A. If AI is NOT thinking yet, start the thread
            if not ai_thinking:
                print("Starting AI Thread...") 
                ai_thinking = True
                
                
                # We send a "Deep Copy" (clone) of the game state to the worker.
                # Now the AI can mess up this clone without affecting the screen.
                gs_clone = copy.deepcopy(gs) 
                
                ai_thread = threading.Thread(target=ai_worker, args=(gs_clone, ai_queue))
                
                ai_thread.daemon = True 
                ai_thread.start()
            
           
            if not ai_queue.empty():
                best_move = ai_queue.get() # Grab the move from the queue
                
                # Apply the move
                if best_move:
                    gs.make_move(best_move[0], best_move[1])
                    
                    
                    end_r, end_c = best_move[1]
                    piece = gs.board[end_r][end_c]
                    # ... (Auto-Queen Logic) ...
                    if piece.type == 'pawn' and (end_r == 0 or end_r == 7):
                        piece.type = 'queen' 
                        
                    audio.play('move')
                    
                    # --- NEW CODE START ---
                    # After Black moves, check if White (Human) is checkmated!
                    if gs.is_game_over_check('white'):
                        game_over = True
                        audio.play("notify")
                        if gs.is_check('white'):
                            winner_text = "Checkmate! Black Wins!"
                        else:
                            winner_text = "Stalemate!"
                   
                    
                else:
                    game_over = True
                    audio.play("notify")
                    
                    if gs.is_check('black'):
                        winner_text = "Checkmate! White Wins!"
                    else:
                        winner_text = "Stalemate!"
                
                ai_thinking = False

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            
            if not ai_thinking:
                if event.type == pygame.MOUSEBUTTONDOWN and gs.white_to_move:
                    handle_click(pygame.mouse.get_pos())
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        gs.undo_move()
                    if event.key == pygame.K_SPACE:
                        if game_over:
                            reset_game()

        
        draw_board()

       
        if ai_thinking:
            # Draw a small text box so user knows AI is working
            font_small = pygame.font.SysFont('Arial', 30, True)
            txt = font_small.render("AI Thinking...", True, (255, 0, 0))
            screen.blit(txt, (10, 10)) # Top left corner

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)



if __name__ == "__main__":
    asyncio.run(main())