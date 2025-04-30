from ball import Ball
from bullet import Bullet
from player import Player
from constantes import WHITE,BLACK,RED,GREEN,BLUE, SCREEN_WIDTH, SCREEN_HEIGHT, FONT

import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen : pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball Blast")

# Création des variables de jeu
ball_level = [[BLACK,40],[RED,30],[GREEN,25],[BLUE,20]]
perdu : bool = False
shootCD : int = 0
texture : pygame.Surface = pygame.transform.scale(pygame.image.load('./assets/bg.jpg'),(SCREEN_WIDTH*1.5,SCREEN_HEIGHT*1.5))

frameNumber : int = 0
path : str = "./assets/explosion_frames/frame-"

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

# Création des boules
for _ in range(2):
    newball = Ball(random.randint(100, SCREEN_WIDTH-100),random.randint(-100, -40),ball_level[0][1],0,ball_level[0][0])
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
            if event.key == pygame.K_ESCAPE:
                running = False
    
    
    shootCD += 1
    
    #Toutes les 10 frames, on tire
    if shootCD == 10 and not perdu:
        shootCD = 0
        bullet = Bullet(player.rect.centerx, player.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

    # Update
    all_sprites.update()

    # Check for collisions
    hitBalls = pygame.sprite.groupcollide(balls, bullets, False, True)
    for hit in hitBalls:
        
        destroyed : bool = hit.take_damage()
        #Si la boule touchée n'est pas la plus petite
        if destroyed:
            player.score += hit.base_life_points
            if hit.level < len(ball_level)-1:
                
                #On crée une boule aux mêmes co que la boule détruite
                ball1 = Ball(hit.rect.x,hit.rect.y,ball_level[hit.level+1][1],hit.level+1,ball_level[hit.level+1][0])
                
                #on la décale à droite
                ball1.decale(10)
                
                #Ajout au groupe de collision des boules
                balls.add(ball1)
                
                #Ajout au groupe de tout les sprites
                all_sprites.add(ball1)
                
                
                #On crée une autre boule
                ball2 = Ball(hit.rect.x,hit.rect.y,ball_level[hit.level+1][1],hit.level+1,ball_level[hit.level+1][0])
                
                #On la décale à gauche
                ball2.decale(-10)
                
                #Ajout au groupe de collision des boules
                balls.add(ball2)
                
                #Ajout au groupe de tout les sprites
                all_sprites.add(ball2)
            hit.kill()

    # Draw / render
    
    # On render le fond en premier sinon tout est derrière
    screen.blit(texture, (-150,-100))
    
    all_sprites.draw(screen)
    
    hitPlayer = pygame.sprite.groupcollide(balls, playerGroup, False, False)
    
    #Si le perso a été touché par une balle, il perd
    if len(hitPlayer) > 0:
        perdu = True
        player.kill()
        
    if perdu:
        text_surface = FONT.render('PERDUUUUUUU', False, (0, 0, 0))
        screen.blit(text_surface,(SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - text_surface.get_height() // 2))
        
        if frameNumber < 17:
            frameNumber += 1
            deathImage = pygame.image.load(path + str(frameNumber).zfill(2) + ".png")
            screen.blit(deathImage,(player.rect.left-20,player.rect.top-80))
    
    #Si il n'y a plus aucune balle, il gagne
    if len(balls.sprites()) == 0 and not perdu:
        text_surface = FONT.render('GAGNÉ', False, (0, 0, 0))
        screen.blit(text_surface,(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    #Affiche le score
    score_surface = FONT.render(f'Score: {player.score}', False, (0, 0, 0))
    screen.blit(score_surface, (10, 10))
    
    # Flip the display
    pygame.display.flip()

pygame.quit()
exit(0)