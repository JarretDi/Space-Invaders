import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class for creating an alien"""
    
    def __init__(self, settings, screen):
        """initialize alien"""
        super().__init__()
        self.settings = settings
        self.screen = screen
        
        # load alien image and rect
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()
        
        # start alien at top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # store aliens position
        self.x = float(self.rect.x)
        
    def check_edges(self):
        #return true if alien is at edge of screen
        screen_rect = self.screen.get_rect()
        if (self.rect.right >= screen_rect.right) or (self.rect.left <= 0):
            return True
        
    def update(self):
        # moves alien right
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
        
    def blitme(self):
        """draw alien at its current position"""
        self.screen.blit(self.image, self.rect)
        
        