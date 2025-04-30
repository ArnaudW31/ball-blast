from constantes import SCREEN_WIDTH, SCREEN_HEIGHT
from menu import Menu
from game import Game

import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
pygame.display.set_caption("Ball Blast")

# Game loop
running = True
clock = pygame.time.Clock()

menu : Menu = Menu()

gameState = False

screen : pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

while running:
    clock.tick(40)
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    if not gameState:
        screen, gameState  = menu.showMenu(screen, events)
        if gameState :
            game : Game = Game()
    else:
        screen, gameState = game.showGame(screen)
    # Flip the display
    pygame.display.flip()

pygame.quit()
exit(0)