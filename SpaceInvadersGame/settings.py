class Settings():
    """Stores settings for game"""
    
    def __init__(self):
        """initialize static settings"""
        #screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        #ship
        self.ship_limit = 3
        
        #aliens
        self.fleet_drop_speed = 10
        
        #bullet
        self.bullet_width = 3
        self.bullet_length = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_max = 3
        
        #on new level
        self.speed_up = 1.1
        self.points_multiplier = 1.5
        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """initialize variable settings"""
        #ship
        self.ship_speed = 1
        
        #bullets
        self.bullet_speed = 2
        
        #aliens
        self.alien_speed = 0.5 
        self.fleet_direction = 1
        #interp. 1 = right, -1 = left
        self.alien_points = 50
    
    def increase_speed(self):
        """increase speed on new level"""
        #ship
        self.ship_speed *= self.speed_up
        
        #bullets
        self.bullet_speed *= self.speed_up
        
        #aliens
        self.alien_speed *= self.speed_up
        self.alien_points = int(self.alien_points * self.points_multiplier)