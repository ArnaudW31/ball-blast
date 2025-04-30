from ball import Ball
from bullet import Bullet
from player import Player
from constantes import WHITE,BLACK,RED,GREEN,BLUE, SCREEN_WIDTH, SCREEN_HEIGHT, FONT, FIRERATE

import pygame
import random

class Game():
    def __init__(self):
        
        # Création des variables de jeu
        self.ball_level = [[BLACK,40],[RED,30],[GREEN,25],[BLUE,20]]
        self.perdu : bool = False
        self.shootCD : int = 0
        self.texture : pygame.Surface = pygame.transform.scale(pygame.image.load('./assets/bg.jpg'),(SCREEN_WIDTH*1.5,SCREEN_HEIGHT*1.5))

        self.frameNumber : int = 0
        self.shootCD : int = 0
        self.path : str = "./assets/explosion_frames/frame-"
        self.perdu = False

        # Initialize player, balls, and bullets
        self.player = Player()
        wheels = self.player.getWheels()
        self.playerGroup = pygame.sprite.Group()
        self.playerGroup.add(self.player)
        self.balls = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.playerGroup)
        self.all_sprites.add(wheels[0])
        self.all_sprites.add(wheels[1])

        # Création des boules
        for _ in range(2):
            newball = Ball(random.randint(100, SCREEN_WIDTH-100),random.randint(-100, -40),self.ball_level[0][1],0,self.ball_level[0][0])
            self.balls.add(newball)
            self.all_sprites.add(newball)

    def showGame(self,screen : pygame.Surface):
        
        if pygame.key.get_pressed()[pygame.K_a] and self.perdu:
            return screen, False
        self.shootCD += 1
        
        #Toutes les 10 frames, on tire
        if self.shootCD == FIRERATE and not self.perdu:
            self.shootCD = 0
            bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
            self.all_sprites.add(bullet)
            self.bullets.add(bullet)

        # Update
        self.all_sprites.update()

        # Check for collisions
        hitBalls: dict[Ball,list[Bullet]] = pygame.sprite.groupcollide(self.balls, self.bullets, False, True)
        for hit in hitBalls:
            
            destroyed : bool = hit.take_damage()
            #Si la boule touchée n'est pas la plus petite
            if destroyed:
                if hit.level < len(self.ball_level)-1:
                    
                    #On crée une boule aux mêmes co que la boule détruite
                    ball1 = Ball(hit.rect.x,hit.rect.y,self.ball_level[hit.level+1][1],hit.level+1,self.ball_level[hit.level+1][0])
                    
                    #on la décale à droite
                    ball1.decale(10)
                    
                    #Ajout au groupe de collision des boules
                    self.balls.add(ball1)
                    
                    #Ajout au groupe de tout les sprites
                    self.all_sprites.add(ball1)
                    
                    
                    #On crée une autre boule
                    ball2 = Ball(hit.rect.x,hit.rect.y,self.ball_level[hit.level+1][1],hit.level+1,self.ball_level[hit.level+1][0])
                    
                    #On la décale à gauche
                    ball2.decale(-10)
                    
                    #Ajout au groupe de collision des boules
                    self.balls.add(ball2)
                    
                    #Ajout au groupe de tout les sprites
                    self.all_sprites.add(ball2)
                hit.kill()

        # Draw / render
        
        # On render le fond en premier sinon tout est derrière
        screen.blit(self.texture, (-150,-100))
        
        self.all_sprites.draw(screen)
        
        hitPlayer = pygame.sprite.groupcollide(self.balls, self.playerGroup, False, False)
        
        #Si le perso a été touché par une balle, il perd
        if len(hitPlayer) > 0:
            self.perdu = True
            self.player.kill()
            
        if self.perdu:
            text_surface = FONT.render('PERDUUUUUUU', False, (0, 0, 0))
            screen.blit(text_surface,(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
            if self.frameNumber < 17:
                self.frameNumber += 1
                if self.frameNumber <= 9 :
                    deathImage = pygame.image.load(self.path + "0" + str(self.frameNumber) + ".png")
                else:
                    deathImage = pygame.image.load(self.path + str(self.frameNumber) + ".png")
                screen.blit(deathImage,(self.player.rect.left-20,self.player.rect.top-80))
        
        #Si il n'y a plus aucune balle, il gagne
        if len(self.balls.sprites()) == 0 and not self.perdu:
            text_surface = FONT.render('GAGNÉ', False, (0, 0, 0))
            screen.blit(text_surface,(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
        return screen, True