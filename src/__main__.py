from ball import Ball
from bullet import Bullet
from player import Player
from constantes import RED,WHITE,BLACK,BLUE, SCREEN_WIDTH, SCREEN_HEIGHT

import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball Blast")


# Initialize player, balls, and bullets
player = Player()
balls = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

for _ in range(8):
    newball = Ball(WHITE,random.randint(0, SCREEN_WIDTH - 30),random.randint(-100, -40),30)
    balls.add(newball)
    all_sprites.add(newball)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Update
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.groupcollide(bullets, balls, True, True)
    for hit in hits:
        ball1 = Ball(BLUE,hit.rect.x,-40,30)
        ball1.decale(50)
        balls.add(ball1)
        all_sprites.add(ball1)
        
        ball2 = Ball(BLUE,hit.rect.x,-40,30)
        ball2.decale(-50)
        balls.add(ball2)
        
        balls.remove(hit)
        all_sprites.remove(hit)
        all_sprites.add(ball2)

    # Draw / render
    
    texture = pygame.image.load('./assets/bg.jpg')
    
    screen.blit(texture, (0, 0))
    all_sprites.draw(screen)

    # Flip the display
    pygame.display.flip()

pygame.quit()