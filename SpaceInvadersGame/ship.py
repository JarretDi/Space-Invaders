import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """a class for the ship and lives"""
    def __init__(self, settings, screen):
        """Initialize the ship"""
        super().__init__()
        self.screen = screen
        self.settings = settings
        
        # load ship on screen
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # start ship on bottom
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # start ship unmoving
        self.right = False
        self.left = False
        
        #set ship speed
        self.center = float(self.rect.centerx)
        
    def blitme(self):
        """Draw ship at its current location"""
        self.screen.blit(self.image, self.rect)
        
    def move(self):
        if self.right and (self.rect.right < self.screen_rect.right):
            self.rect.centerx += self.settings.ship_speed
            
        if self.left and (self.rect.left > 0):
            self.rect.centerx -= self.settings.ship_speed
    def center_ship(self):
        """center the ship on the screen"""
        self.center = self.screen_rect.centerx