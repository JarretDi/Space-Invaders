class GameStats():
    def __init__(self, settings):
        self.settings = settings
        
        self.reset_stats()
        self.high_score = 0
        self.level = 1
        
        self.game_active = False
        
    def reset_stats(self):
        #resets stats that can change during the game
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1