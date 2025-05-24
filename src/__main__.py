from constantes import SCREEN_WIDTH, SCREEN_HEIGHT
from menu import Menu
from game import Game

import pygame
import random
import os

# Initialize Pygame
pygame.init()

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


while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if not gameState:
        gameState, newGame = menu.showMenu(events, pause)
        if gameState and newGame:
            game = Game(screen)
            newGame = False
    else:
        gameState, pause = game.showGame()

    pygame.display.update()
    clock.tick(40)

pygame.quit()
exit(0)
