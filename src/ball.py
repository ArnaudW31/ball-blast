import random
import pygame
from constantes import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius,color = WHITE):
        super().__init__()
        self.image = pygame.Surface((radius,radius))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = random.randint(1, 8)
    
    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 8)
            
    def decale(self, decale):
        self.rect.x += decale