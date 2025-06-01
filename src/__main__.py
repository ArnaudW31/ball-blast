from constantes import SCREEN_WIDTH, SCREEN_HEIGHT
from menu import Menu
from game import Game

import pygame
import random
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Set up the display
pygame.display.set_caption("Ball Blast")
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Game loop
running = True
clock = pygame.time.Clock()

menu: Menu = Menu(screen)
game: Game = None

# Gestion des états
gameState = False
pause = False
newGame = False

playMusic = True

pygame.mixer.music.load("assets/sound/menu.mp3")
pygame.mixer.music.play()

while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break

    if not gameState:
        gameState, newGame = menu.showMenu(events, pause)
        if gameState and newGame:
            game = Game(screen)
            newGame = False

        # Si on passe du menu au jeu
        if gameState:
            playMusic = True
    else:
        gameState, pause = game.showGame()
        if playMusic:
            pygame.mixer.music.load("./assets/sound/music" + str(random.randint(1, 3)) + ".mp3")
            pygame.mixer.music.play(loops=-1)
            playMusic = False

        # Si on passe du jeu au menu
        if not gameState:
            pygame.mixer.music.load("assets/sound/menu.mp3")
            pygame.mixer.music.play()

    pygame.display.update()
    clock.tick(40)

pygame.quit()
exit(0)
