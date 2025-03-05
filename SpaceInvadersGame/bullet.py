import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """bullets"""
    
    def __init__(self, settings, screen, ship):
        """Create a bullet"""
        super().__init__()
        self.screen = screen
        
        # Create bullet at (0,0) then move items
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_length)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        # store bullet position
        self.y = float(self.rect.y)
        
        self.color = settings.bullet_color
        self.speed = settings.bullet_speed
        
    
    def update(self):
        """Move the bullet upscreen"""
        
        #update decimal position
        self.y -= self.speed
        
        #update actual position
        self.rect.y = self.y
        
    def draw(self):
        """Draw the moved bullet"""
        pygame.draw.rect(self.screen, self.color, self.rect)