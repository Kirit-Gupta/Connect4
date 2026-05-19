import pygame
class Birds:
    def __init__(self):
        self.blue_bird = []
        self.red_bird = []
        self.get_bird_surfaces()
        self.animation_speed = 0.1
        self.pos = -30

    def get_bird_surfaces(self):
        for i in range(4):
            self.blue_bird.append(pygame.image.load(f'Assets/blue-bird-{i+1}.png').convert_alpha())
        
        for i in range(7):
            self.red_bird.append(pygame.image.load(f'Assets/red-bird-{i+1}.png').convert_alpha())
    
    def next(self):
        t = pygame.time.get_ticks() / 1000
        self.pos += 2
        blue_index = int(t / self.animation_speed) % len(self.blue_bird)
        red_index = int(t / self.animation_speed) % len(self.red_bird)

        return self.blue_bird[blue_index], self.red_bird[red_index], self.pos
