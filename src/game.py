from ball import Ball
from bullet import Bullet
from player import Player
from constantes import WHITE, BLACK, RED, GREEN, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT, FONT, FIRERATE, BALL_EQUIVALENT

import pygame
import random


class Game():
    def __init__(self, screen: pygame.Surface):
        self.screen: pygame.Surface = screen
        self.level = 0
        # Création des variables de jeu
        self.ball_level = [[BLACK, 50], [RED, 40], [GREEN, 33], [BLUE, 25]]
        self.ballEquivalents = [10,7,3,1]
        self.ballsToSpawn = BALL_EQUIVALENT
        self.perdu: bool = False
        self.shootCD: int = 0
        self.texture: pygame.Surface = pygame.transform.scale(
            pygame.image.load('./assets/bg_pxl.jpg'), (SCREEN_WIDTH*1.5, SCREEN_HEIGHT*1.5))

        # Compteurs de frames pour laisser du temps avant de passer à la suite
        self.frameNumberLoseAnim: int = 0
        self.frameNumberWinAnim : int = 0
        self.frameNumberSpawnBalls : int = 0
        self.frameNumberBeginLevel: int = 0
        
        self.shootCD: int = 0
        self.path: str = "./assets/explosion_frames/frame-"
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
    
    #Crée toutes les boules et les ajoutes dans le jeu
    def createBalls(self):
        while True:
            ballType : int = random.randint(0,len(self.ball_level)-1)
            if self.ballEquivalents[ballType] <= self.ballsToSpawn:
                newball = Ball(random.randint(100, SCREEN_WIDTH-100),
                        random.randint(-100, -40), self.ball_level[ballType][1], ballType, self.ball_level[ballType][0])
                self.balls.add(newball)
                self.all_sprites.add(newball)
                self.ballsToSpawn -= self.ballEquivalents[ballType]
                return
       
    #Passe au niveau suivant     
    def nextLevel(self):
        self.level += 1
        self.ballsToSpawn = BALL_EQUIVALENT + self.level * 5
        
        self.frameNumberWinAnim : int = 0
        self.frameNumberSpawnBalls : int = 0
        self.frameNumberBeginLevel = 0

    def showGame(self) -> tuple[bool, bool]:
        
        if self.frameNumberBeginLevel < 60:
            self.frameNumberBeginLevel += 1
            self.screen.blit(self.texture, (-150, -100))
            self.screen.blit(FONT.render('NIVEAU ' + str(self.level), True, (0, 0, 0)),(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            return True, False
            
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            if self.perdu:
                return False,False
            else:
                return False, True

        self.shootCD += 1
        
        if self.ballsToSpawn > 0:
            if self.frameNumberSpawnBalls % 20 == 0:
                self.createBalls()
            self.frameNumberSpawnBalls += 1

        # Toutes les 10 frames, on tire
        if self.shootCD == FIRERATE and not self.perdu:
            self.shootCD = 0
            bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
            self.all_sprites.add(bullet)
            self.bullets.add(bullet)

        # Update
        self.all_sprites.update()

        # Check for collisions
        hitBalls: dict[Ball, list[Bullet]] = pygame.sprite.groupcollide(
            self.balls, self.bullets, False, True)
        for hit in hitBalls:

            destroyed: bool = hit.take_damage()
            # Si la boule touchée n'est pas la plus petite
            if destroyed:
                if hit.level < len(self.ball_level)-1:

                    # On crée une boule aux mêmes co que la boule détruite
                    ball1 = Ball(
                        hit.rect.x, hit.rect.y, self.ball_level[hit.level+1][1], hit.level+1, self.ball_level[hit.level+1][0])

                    # on la décale à droite
                    ball1.decale(10)

                    # Ajout au groupe de collision des boules
                    self.balls.add(ball1)

                    # Ajout au groupe de tout les sprites
                    self.all_sprites.add(ball1)

                    # On crée une autre boule
                    ball2 = Ball(
                        hit.rect.x, hit.rect.y, self.ball_level[hit.level+1][1], hit.level+1, self.ball_level[hit.level+1][0])

                    # On la décale à gauche
                    ball2.decale(-10)

                    # Ajout au groupe de collision des boules
                    self.balls.add(ball2)

                    # Ajout au groupe de tout les sprites
                    self.all_sprites.add(ball2)
                hit.kill()

        # Draw / render

        # On render le fond en premier sinon tout est derrière
        self.screen.blit(self.texture, (-150, -100))

        self.all_sprites.draw(self.screen)

        hitPlayer = pygame.sprite.groupcollide(
            self.balls, self.playerGroup, False, False)

        # Si le perso a été touché par une balle, il perd
        if len(hitPlayer) > 0:
            self.perdu = True
            self.player.kill()

        if self.perdu:
            text_surface = FONT.render('PERDUUUUUUU', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

            if self.frameNumberLoseAnim < 17:
                self.frameNumberLoseAnim += 1
                if self.frameNumberLoseAnim <= 9:
                    deathImage = pygame.image.load(
                        self.path + "0" + str(self.frameNumberLoseAnim) + ".png")
                else:
                    deathImage = pygame.image.load(
                        self.path + str(self.frameNumberLoseAnim) + ".png")
                self.screen.blit(deathImage, (self.player.rect.left -
                                              20, self.player.rect.top-80))

        # Si il n'y a plus aucune balle, il gagne
        if len(self.balls.sprites()) == 0 and not self.perdu:
            text_surface = FONT.render('GAGNÉ', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
            if self.frameNumberWinAnim == 300 and not self.perdu:
                self.nextLevel()
            self.frameNumberWinAnim += 1

        return True, False
