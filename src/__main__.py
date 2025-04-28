from ball import Ball
from bullet import Bullet
from player import Player
from constantes import WHITE,BLACK,RED,GREEN,BLUE, SCREEN_WIDTH, SCREEN_HEIGHT

import pygame
import random

# Initialize Pygame
pygame.init()
pygame.font.init()

Font = pygame.font.SysFont('Comic Sans MS', 30)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball Blast")
texture = pygame.image.load('./assets/bg.jpg')

ball_level = [[BLACK,50],[RED,30],[GREEN,25],[BLUE,20]]
perdu = False

# Initialize player, balls, and bullets
player = Player()
wheels = player.getWheels()
playerGroup = pygame.sprite.Group()
playerGroup.add(player)
balls = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(playerGroup)
all_sprites.add(wheels[0])
all_sprites.add(wheels[1])

for _ in range(8):
    newball = Ball(random.randint(0, SCREEN_WIDTH),random.randint(-100, -40),ball_level[0][1],0,ball_level[0][0])
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
            elif event.key == pygame.K_ESCAPE:
                running = False

    # Update
    all_sprites.update()

    # Check for collisions
    hitBalls: dict[Ball,list[Bullet]] = pygame.sprite.groupcollide(balls, bullets, True, True)
    for hit in hitBalls:
        if hit.level < len(ball_level)-1:
            ball1 = Ball(hit.rect.x,-40,ball_level[hit.level+1][1],hit.level+1,ball_level[hit.level+1][0])
            ball1.decale(50)
            balls.add(ball1)
            all_sprites.add(ball1)
            
            ball2 = Ball(hit.rect.x,-40,ball_level[hit.level+1][1],hit.level+1,ball_level[hit.level+1][0])
            ball2.decale(-50)
            balls.add(ball2)
            all_sprites.add(ball2)
            
    hitPlayer = pygame.sprite.groupcollide(balls, playerGroup, False, False)

    # Draw / render
    
    screen.blit(texture, (0,0))
    all_sprites.draw(screen)
    
    if len(hitPlayer) > 0:
        perdu = True
        
    if perdu:
        text_surface = Font.render('PERDUUUUUUU', False, (0, 0, 0))
        screen.blit(text_surface,(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
    if len(balls.sprites()) == 0:
        text_surface = Font.render('GAGNÉ', False, (0, 0, 0))
        screen.blit(text_surface,(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Flip the display
    pygame.display.flip()

pygame.quit()
exit(0)