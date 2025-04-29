import random
import pygame
import math
from constantes import RED, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE

# Font
pygame.init()
font = pygame.font.SysFont('Arial', 24)

class Ball(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, radius: int, level: int = 0, color: tuple[int,int,int] = RED):
        super().__init__()
        # Créer une surface transparente
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        self.level: int = level
        self.life: int = 3
        self.color: tuple[int,int,int] = color
        self.radius: int = radius
        
        # Générer des points pour créer un polygone irrégulier
        self.points = self._generate_rock_shape()
        
        # Dessiner le polygone sur la surface
        pygame.draw.polygon(self.image, self.color, self.points)
        
        # Dessiner les points de vie
        self.life_points:int = random.randint(1, radius)
        self.life_points_surface = font.render(str(self.life_points), True, WHITE)
        self.life_points_surface_rect = self.life_points_surface.get_rect()
        self.life_points_surface_rect.center = (self.radius, self.radius)
        self.image.blit(self.life_points_surface, self.life_points_surface_rect)
        
        # Créer un masque de collision pour une détection plus précise
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Vitesse de déplacement
        self.speed_y: int = random.randint(1, 8)
        self.speed_x: int = random.randint(1, 2) * (-1)**random.randint(1, 2)
    
    def _generate_rock_shape(self) -> list[tuple[int, int]]:
        """Génère des points pour créer une forme de roche irrégulière"""
        points = []
        num_points = random.randint(6, 8)  # Nombre de points du polygone
        
        for i in range(num_points):
            angle = (2 * math.pi * i) / num_points
            # Ajouter une variation aléatoire au rayon
            x = self.radius + self.radius * math.cos(angle)
            y = self.radius + self.radius * math.sin(angle)
            points.append((int(x), int(y)))
            
        return points
    
    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        
        self.speed_x = -self.speed_x if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH else self.speed_x 
        self.speed_y = random.randint(-9, -7) if self.rect.bottom > SCREEN_HEIGHT else self.speed_y + 0.1
        
    def take_damage(self) -> bool:
        self.life_points -= 1
        
        self.life_points_surface = font.render(str(self.life_points), True, WHITE)
        self.life_points_surface_rect = self.life_points_surface.get_rect()
        self.life_points_surface_rect.center = (self.radius, self.radius)
        
        self.image = pygame.Surface((self.image.get_rect().width, self.image.get_rect().width), pygame.SRCALPHA)
        
        pygame.draw.polygon(self.image, self.color, self.points)
        self.image.blit(self.life_points_surface, self.life_points_surface_rect)
        
        return self.life_points == 0
        
    def decale(self, decale: int):
        self.rect.x += decale
        
    def level(self)->int:
        return self.level