class Settings():
    """Class for storaging settings for game."""
    def __init__(self):
        """Game settings initialization."""
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.bullet_width = 10
        self.bullet_height = 5
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5
        self.fleet_drop_speed = 10
        self.ship_limit = 3
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3
        self.alien_speed = 0.5
        # fleet_direction: 1 - moving right, -1 - moving left.
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
