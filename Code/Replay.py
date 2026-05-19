import pygame
from .constants import *
import math

class Replay:
    def __init__(self):
        self.co_or = ((WIDTH//2) - 80, HEIGHT - 70)
        self.i = 0
        self.replay_btn = pygame.image.load('Assets/Replay_button.png').convert_alpha()
        self.base_width = self.replay_btn.get_width()
        self.base_height = self.replay_btn.get_height()
        self.mask = None
        self.x = 0
        self.y = 0

    def pulsate(self, screen):
        t = pygame.time.get_ticks() / 1000
        scale = 1 + (math.sin(t * 5) * 0.08)

        width = int(self.base_width * scale)
        height = int(self.base_height * scale)

        scaled_btn = pygame.transform.smoothscale(self.replay_btn,(width, height))
        self.x = self.co_or[0] - (width - self.base_width) // 2
        self.y = self.co_or[1] - (height - self.base_height) // 2

        self.mask = pygame.mask.from_surface(scaled_btn)
        screen.blit(scaled_btn, (self.x, self.y))
    
    def clicked(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x = mouse_x - self.x
        rel_y = mouse_y - self.y
        if rel_x < 0 or rel_y < 0:
            return False
        elif rel_x >= self.mask.get_size()[0]:
            return False
        elif rel_y >= self.mask.get_size()[1]:
            return False
        
        return self.mask.get_at((rel_x, rel_y))
