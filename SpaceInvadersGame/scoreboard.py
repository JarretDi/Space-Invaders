import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    def __init__(self, settings, screen, stats):
        """a class to store score"""
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        
        #font settings
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        
        #prepare scoreboard
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
    
    def prep_score(self):
        """turn score into image"""
        rounded_score = int(round(self.stats.score, -1))
        score = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score, True, self.text_color, self.settings.bg_color)
        
        #display at top right
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """turn high score into image"""
        high_score = int(round(self.stats.high_score, -1))
        score = "{:,}".format(high_score)
        self.high_score_image = self.font.render(score, True, self.text_color, self.settings.bg_color)
        
        #display at top of screen
        self.high_score_rect = self.score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
    
    def prep_level(self):
        """turn level into image"""
        level = str(self.stats.level)
        self.level_image = self.font.render(level, True, self.text_color, self.settings.bg_color)
        
        #display below score
        self.level_rect = self.score_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
    
    def prep_ships(self):
        """turn ship lives into image"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
    
    def show_stats(self):
        """draw stats"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
    
    
    
    