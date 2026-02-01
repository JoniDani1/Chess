from settings import *
import pygame
import sys

class ChessPiece:
    def __init__(self, color, type):
        self.color = color
        self.type = type
        self.has_moved = False

class GameState:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.white_to_move = True
        self.move_log = []
        self.init_board()

    def init_board(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        # Pawns
        for col in range(8):
           # self.board[1][col] = ChessPiece('black', 'pawn')
            self.board[6][col] = ChessPiece('white', 'pawn')
        # # Rooks
        # self.board[0][0] = self.board[0][7] = ChessPiece('black', 'rook')
        # self.board[7][0] = self.board[7][7] = ChessPiece('white', 'rook')
        # # Knights
        # self.board[0][1] = self.board[0][6] = ChessPiece('black', 'knight')
        # self.board[7][1] = self.board[7][6] = ChessPiece('white', 'knight')
        # # Bishops
        # self.board[0][2] = self.board[0][5] = ChessPiece('black', 'bishop')
        # self.board[7][2] = self.board[7][5] = ChessPiece('white', 'bishop')
        # Queens
        #self.board[0][3] = ChessPiece('black', 'queen')
        self.board[7][3] = ChessPiece('white', 'queen')
        # Kings
        self.board[0][4] = ChessPiece('black', 'king')
        self.board[7][4] = ChessPiece('white', 'king')

    def make_move(self, start_pos, end_pos):
        r_start, c_start = start_pos
        r_end, c_end = end_pos
        
        piece = self.board[r_start][c_start]
        target = self.board[r_end][c_end]
        
        # Save for Undo
        self.move_log.append({
            'piece': piece, 
            'start': start_pos, 
            'end': end_pos, 
            'captured': target,
            'has_moved_before': piece.has_moved
        })
        
        # Execute Move
        self.board[r_end][c_end] = piece
        self.board[r_start][c_start] = None
        piece.has_moved = True
        self.white_to_move = not self.white_to_move

        if piece.type == 'king' and abs(c_start - c_end) == 2:
            # Kingside Castle (Moves Right)
            if c_end > c_start: 
                rook = self.board[r_start][7]
                self.board[r_start][5] = rook # Move Rook to F-file
                self.board[r_start][7] = None
                rook.has_moved = True
            # Queenside Castle (Moves Left)
            else: 
                rook = self.board[r_start][0]
                self.board[r_start][3] = rook # Move Rook to D-file
                self.board[r_start][0] = None
                rook.has_moved = True

    def undo_move(self):
        if not self.move_log: return
        
        move = self.move_log.pop()
        piece = move['piece']
        start_r, start_c = move['start']
        end_r, end_c = move['end']
        
        self.board[start_r][start_c] = piece
        self.board[end_r][end_c] = move['captured']
        piece.has_moved = move['has_moved_before']
        self.white_to_move = not self.white_to_move

        if piece.type == 'king' and abs(start_c - end_c) == 2:
            # Kingside Undo (Rook was at 5, needs to go back to 7)
            if end_c > start_c: 
                rook = self.board[start_r][5]
                self.board[start_r][7] = rook
                self.board[start_r][5] = None
                rook.has_moved = False 
            # Queenside Undo (Rook was at 3, needs to go back to 0)
            else:
                rook = self.board[start_r][3]
                self.board[start_r][0] = rook
                self.board[start_r][3] = None
                rook.has_moved = False

    def reset(self):
        self.init_board()
        self.white_to_move = True
        self.move_log = []

    def get_valid_moves(self, piece, row, col):
        moves = []
        if piece.type == 'pawn':
            direction = -1 if piece.color == 'white' else 1
            if 0 <= row+direction < 8 and self.board[row+direction][col] is None:
                moves.append((row+direction, col))
                if (piece.color == 'white' and row == 6) or (piece.color == 'black' and row == 1):
                    if self.board[row+2*direction][col] is None:
                        moves.append((row+2*direction, col))
            for dc in [-1, 1]:
                if 0 <= row+direction < 8 and 0 <= col+dc < 8:
                    target = self.board[row+direction][col+dc]
                    if target and target.color != piece.color:
                        moves.append((row+direction, col+dc))
        
        elif piece.type == 'rook':
            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                for i in range(1, 8):
                    r, c = row+dr*i, col+dc*i
                    if 0<=r<8 and 0<=c<8:
                        if self.board[r][c] is None: moves.append((r,c))
                        elif self.board[r][c].color != piece.color: moves.append((r,c)); break
                        else: break
                    else: break
                    
        elif piece.type == 'bishop':
            for dr, dc in [(1,1),(1,-1),(-1,1),(-1,-1)]:
                for i in range(1, 8):
                    r, c = row+dr*i, col+dc*i
                    if 0<=r<8 and 0<=c<8:
                        if self.board[r][c] is None: moves.append((r,c))
                        elif self.board[r][c].color != piece.color: moves.append((r,c)); break
                        else: break
                    else: break
                    
        elif piece.type == 'knight':
            for dr, dc in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
                r, c = row+dr, col+dc
                if 0<=r<8 and 0<=c<8:
                    if self.board[r][c] is None or self.board[r][c].color != piece.color:
                        moves.append((r,c))
                        
        elif piece.type == 'queen':
            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
                for i in range(1, 8):
                    r, c = row+dr*i, col+dc*i
                    if 0<=r<8 and 0<=c<8:
                        if self.board[r][c] is None: moves.append((r,c))
                        elif self.board[r][c].color != piece.color: moves.append((r,c)); break
                        else: break
                    else: break
                    
        elif piece.type == 'king':
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    if dr==0 and dc==0: continue
                    r, c = row+dr, col+dc
                    if 0<=r<8 and 0<=c<8:
                        if self.board[r][c] is None or self.board[r][c].color != piece.color:
                            moves.append((r,c))
            # Castling
            if not piece.has_moved:
                if self.board[row][5] is None and self.board[row][6] is None:
                    rook = self.board[row][7]
                    if rook and rook.type=='rook' and not rook.has_moved: 
                        moves.append((row, 6))
                # Queenside
                if self.board[row][1] is None and self.board[row][2] is None and self.board[row][3] is None:
                    rook = self.board[row][0]
                    if rook and rook.type=='rook' and not rook.has_moved: 
                        moves.append((row, 2))
        return moves

    def is_square_attacked(self, r, c, defense_color):
        enemy_color = 'black' if defense_color == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == enemy_color:
                    if piece.type == 'king': 
                        if abs(row-r)<=1 and abs(col-c)<=1: return True
                    elif piece.type == 'pawn':
                        d = -1 if piece.color=='white' else 1
                        if row+d==r and abs(col-c)==1: return True
                    else:
                        if (r,c) in self.get_valid_moves(piece, row, col): return True
        return False

    def is_check(self, color):
        king_pos = None
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p.type=='king' and p.color==color:
                    king_pos = (r,c); break
            if king_pos: break
        if not king_pos: return False
        return self.is_square_attacked(king_pos[0], king_pos[1], color)

    def get_safe_moves(self, piece, row, col):
        moves = self.get_valid_moves(piece, row, col)
        safe = []
        for m in moves:
            tr, tc = m
            if piece.type=='king' and abs(tc-col)==2:
                if self.is_check(piece.color): continue
                d = 1 if tc>col else -1
                if self.is_square_attacked(row, col+d, piece.color): continue
            
            orig = self.board[tr][tc]
            self.board[tr][tc] = piece
            self.board[row][col] = None
            
            if not self.is_check(piece.color): safe.append(m)
            
            self.board[row][col] = piece
            self.board[tr][tc] = orig
        return safe

    def is_game_over_check(self, color):
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p.color==color:
                    if self.get_safe_moves(p, r, c): return False
        return True

    def get_promotion_choice(self, screen, color):
        dialog_width, dialog_height = 440, 160
        x = (WIDTH - dialog_width) // 2
        y = (HEIGHT - dialog_height) // 2
        
        options = ["queen", "rook", "bishop", "knight"]
        icon_size = 80 
        spacing = 20
        buttons = [] 

        total_width = (icon_size * 4) + (spacing * 3)
        start_x = x + (dialog_width - total_width) // 2
        start_y = y + 60 

        for i, piece_type in enumerate(options):
            path = f"images/{color}_{piece_type}.png"
            try:
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (icon_size, icon_size))
            except FileNotFoundError:
                img = pygame.Surface((icon_size, icon_size))
                img.fill((255, 255, 255))
                txt = font.render(piece_type[0].upper(), True, (0,0,0))
                img.blit(txt, (30, 20))

            btn_x = start_x + i * (icon_size + spacing)
            rect = pygame.Rect(btn_x, start_y, icon_size, icon_size)
            buttons.append({'type': piece_type, 'image': img, 'rect': rect})

        waiting = True
        choice = "queen" 
        
        while waiting:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in buttons:
                        if btn['rect'].collidepoint(mouse_pos):
                            choice = btn['type']
                            waiting = False

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            pygame.draw.rect(screen, (50, 50, 50), (x, y, dialog_width, dialog_height), border_radius=15)
            pygame.draw.rect(screen, (255, 255, 255), (x, y, dialog_width, dialog_height), 4, border_radius=15)
            
            text = font.render(f"Promote {color.capitalize()} Pawn:", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH//2, y + 30))
            screen.blit(text, text_rect)
            
            for btn in buttons:
                if btn['rect'].collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (100, 255, 100), btn['rect'], border_radius=8) 
                else:
                    pygame.draw.rect(screen, (80, 80, 80), btn['rect'], border_radius=8) 

                screen.blit(btn['image'], btn['rect'])
                
            pygame.display.flip()
            pygame.time.wait(15)
            
        return choice