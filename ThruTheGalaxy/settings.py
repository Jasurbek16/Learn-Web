# A class to store all settings for Thru the Galaxy
class Settings():

    def __init__(self):
        """Initialize the game's static settings."""
        # dimensions
        self.width = 1200
        self.height = 800
        # background color
        self.b_ground_color = (34, 46, 80)

        # Ship settings
        self.ship_limit = 3

        # values we’ll need for a new Bullet class
        self.bullet_width = 700
        self.bullet_height = 15
        self.bullet_color = 255, 179, 26
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 5

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the scores would increase for each alien in an upper lvl
        self.alien_pts_lvl_up = 1.4

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 0.5
        self.bullet_speed_factor = 2
        # control the speed of each alien
        self.alien_speed_factor = 0.5
        self.fleet_direction = 1
        # ^ 1(right) -1(left)

        # Scoring
        self.alien_pts = 40

    def increase_speed(self):
        # increase the game speed
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_pts = int(self.alien_pts * self.alien_pts_lvl_up)
