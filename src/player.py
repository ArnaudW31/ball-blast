import pygame
from constantes import RED, SCREEN_WIDTH, SCREEN_HEIGHT

# https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.canon = pygame.transform.scale(pygame.image.load("assets/canon.png"),(50,100))
        self.rect = self.canon.get_rect()
        self.image = self.canon
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        
        self.wheelL = Wheel(-20)
        self.wheelR = Wheel(20)
        
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        
        w, h = self.image.get_size()
        
        self.rect.x += self.speed_x
        self.wheelL.translate(self.speed_x)
        self.wheelR.translate(self.speed_x)
        self.wheelL.rotate(self.speed_x*1.4)
        self.wheelR.rotate(self.speed_x*1.4)
        
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    
    def getWheels(self):
        return (self.wheelL,self.wheelR)
            
class Wheel(pygame.sprite.Sprite):
    def __init__(self,xoffset):
        super().__init__()
        self.original_image = pygame.transform.scale(pygame.image.load("assets/wheel.png"),(25,25))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.xoffset = xoffset
        self.rect.centerx = SCREEN_WIDTH // 2 + xoffset
        self.rect.bottom = SCREEN_HEIGHT - 5
        self.angleRotated = 0
        
    def translate(self,x):
        self.rect.x += x
    
        
    def rotate(self,angle):
        self.angleRotated += angle
        rotated_image = pygame.transform.rotate(self.original_image,self.angleRotated)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        
        self.image = rotated_image
        self.rect = rotated_rect