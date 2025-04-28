import pygame

from constantes import WHITE,BLACK,RED,GREEN,BLUE, SCREEN_WIDTH, SCREEN_HEIGHT, FONT

texture : pygame.Surface = pygame.transform.scale(pygame.image.load('./assets/bg.jpg'),(SCREEN_WIDTH*1.5,SCREEN_HEIGHT*1.5))

selectedOption = 0

def showMenu(screen : pygame.Surface) -> pygame.Surface:
    
    for event in pygame.event.get():
        if event.type == pygame.K_DOWN:
            if selectedOption == 0:
                selectedOption = 2
            else:
                selectedOption -= 1
        if event.type == pygame.K_UP:
            if selectedOption == 2:
                selectedOption = 0
            else:
                selectedOption += 1
            
    screen.blit(texture, (-150,-100))
    
    text_surface = FONT.render('COMMENCER', False, (0, 0, 0))
    screen.blit(text_surface,(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    text_surface = FONT.render('CRéDITS', False, (0, 0, 0)) #Justin c'est pour toi
    screen.blit(text_surface,(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 100))
    
    text_surface = FONT.render('QUITTER', False, (0, 0, 0))
    screen.blit(text_surface,(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 200))
    
    pygame.draw.circle(screen,WHITE,((SCREEN_WIDTH // 2)- 50, (SCREEN_HEIGHT // 2) + 100 * selectedOption))
    
    return screen