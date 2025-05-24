import pygame

from constantes import WHITE, BLACK, RED, GREEN, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT, FONT


class Menu():
    def __init__(self, screen: pygame.Surface):
        self.screen: pygame.Surface = screen
        self.selectedOption: int = 0
        self.texture: pygame.Surface = pygame.transform.scale(
            pygame.image.load('./assets/bg_pxl.jpg').convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

    def showMenu(self, keyEvent, pause: bool = False) -> bool:
        newGame: bool = False
        if pause:
            numberOfOptions = 3
        else:
            numberOfOptions = 2

        goTogame: bool = False
        for event in keyEvent:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.selectedOption == numberOfOptions:
                        self.selectedOption = 0
                    else:
                        self.selectedOption += 1
                if event.key == pygame.K_UP:
                    if self.selectedOption == 0:
                        self.selectedOption = numberOfOptions
                    else:
                        self.selectedOption -= 1

                if event.key == pygame.K_a:
                    if pause:
                        if self.selectedOption == 0:
                            goTogame = True
                        elif self.selectedOption == 1:
                            newGame = True
                            goTogame = True
                        elif self.selectedOption == 3:
                            pygame.quit()
                            exit(0)
                    else:
                        if self.selectedOption == 0:
                            goTogame = True
                            newGame = True
                        elif self.selectedOption == 2:
                            pygame.quit()
                            exit(0)

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit(0)

        self.screen.blit(self.texture, (0, 0))

        delta = 100 if pause else 0

        if pause:
            text_surface = FONT.render('REPRENDRE', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

            text_surface = FONT.render('NOUVELLE PARTIE', False, (0, 0, 0))
            self.screen.blit(text_surface, (SCREEN_WIDTH //
                                            2, SCREEN_HEIGHT // 2 + 100))
        else:
            text_surface = FONT.render('COMMENCER', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        text_surface = FONT.render(
            'CRÉDITS', False, (0, 0, 0))  # Merci
        self.screen.blit(text_surface, (SCREEN_WIDTH //
                                        2, (SCREEN_HEIGHT // 2) + 100 + delta))

        text_surface = FONT.render('QUITTER', False, (0, 0, 0))
        self.screen.blit(text_surface, (SCREEN_WIDTH //
                                        2, (SCREEN_HEIGHT // 2) + 200 + delta))

        pygame.draw.circle(self.screen, WHITE, ((SCREEN_WIDTH // 2) - 50,
                           (SCREEN_HEIGHT // 2) + 100 * self.selectedOption + 25), 5)

        return goTogame, newGame
