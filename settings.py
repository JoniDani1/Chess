import pygame

pygame.init()

WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8


WHITE_SQ = (235, 236, 208)   
BLACK_SQ = (119, 149, 86)    
HIGHLIGHT = (186, 202, 68)   
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER = (100, 255, 100)
TEXT_COLOR = (20, 20, 20)
FPS = 60

font = pygame.font.SysFont('Arial', 24, bold=True)
big_font = pygame.font.SysFont('Arial', 64, bold=True)
timer_font = pygame.font.SysFont('Consolas', 30, bold=True)


