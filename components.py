import pygame
from settings import *

class SoundManager:
    def __init__(self):
        self.sound_library = {} 
        self.load_sound('move', 'move.wav')
        self.load_sound('capture', 'capture.wav')
        self.load_sound('notify', 'notify.wav')

    def load_sound(self, name, filepath):
        try:
            sound = pygame.mixer.Sound(filepath)
            self.sound_library[name] = sound
        except FileNotFoundError:
            self.sound_library[name] = pygame.mixer.Sound(buffer=bytearray([0]*100))

    def play(self, name):
        if name in self.sound_library:
            self.sound_library[name].play()

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=12)
        
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Timer:
    def __init__(self, total_seconds, x, y):
        self.start_seconds = total_seconds
        self.total_seconds = total_seconds
        self.x = x
        self.y = y
        self.last_update = 0

    def reset(self):
        self.total_seconds = self.start_seconds
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= 1000:
            self.total_seconds -= 1
            self.last_update = now
        return self.total_seconds <= 0

    def draw(self, screen, active):
        minutes = self.total_seconds // 60
        seconds = self.total_seconds % 60
        time_text = f"{minutes:02}:{seconds:02}"
        
        bg_rect = pygame.Rect(self.x, self.y, 100, 40)
        text_color = BLACK
        if active: 
            pygame.draw.rect(screen, (200, 255, 200), bg_rect) 
            pygame.draw.rect(screen, (0, 200, 0), bg_rect, 3)  
        else:
            pygame.draw.rect(screen, WHITE, bg_rect)
            pygame.draw.rect(screen, BLACK, bg_rect, 2)
            
        if self.total_seconds < 30: text_color = (255, 0, 0)

        surf = timer_font.render(time_text, True, text_color)
        text_rect = surf.get_rect(center=bg_rect.center)
        screen.blit(surf, text_rect)