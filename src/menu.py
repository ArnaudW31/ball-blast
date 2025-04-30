import pygame

from constantes import WHITE,BLACK,RED,GREEN,BLUE, SCREEN_WIDTH, SCREEN_HEIGHT, FONT

class Menu():
    def __init__(self):
        self.selectedOption : int = 0
        self.texture : pygame.Surface = pygame.transform.scale(pygame.image.load('./assets/bg.jpg'),(SCREEN_WIDTH*1.5,SCREEN_HEIGHT*1.5))
    
    def showMenu(self,screen : pygame.Surface, keyEvent) -> pygame.Surface:
        
        goTogame : bool = False
        for event in keyEvent:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.selectedOption == 2:
                        self.selectedOption = 0
                    else:
                        self.selectedOption += 1
                if event.key == pygame.K_UP:
                    if self.selectedOption == 0:
                        self.selectedOption = 2
                    else:
                        self.selectedOption -= 1
                        
                if event.key == pygame.K_a:
                    if self.selectedOption == 0:
                        goTogame = True
                    elif self.selectedOption == 2:
                        pygame.quit()
                        exit(0)
                
        screen.blit(self.texture, (-150,-100))
        
        text_surface = FONT.render('COMMENCER', False, (0, 0, 0))
        screen.blit(text_surface,(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        text_surface = FONT.render('CRéDITS', False, (0, 0, 0)) #Justin c'est pour toi
        screen.blit(text_surface,(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 100))
        
        text_surface = FONT.render('QUITTER', False, (0, 0, 0))
        screen.blit(text_surface,(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 200))
        
        pygame.draw.circle(screen,WHITE,((SCREEN_WIDTH // 2)- 50, (SCREEN_HEIGHT // 2) + 100 * self.selectedOption + 25),5)
        
        return screen, goTogame