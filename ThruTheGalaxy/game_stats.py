# Tracking game statistics
class GameStats():

    def __init__(self, get_settings):
        """Initialize statistics."""
        self.get_settings = get_settings
        self.reset_stats()
        # Start the game in an inactive state
        self.game_active = False
        # High score (is never resetted)
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.get_settings.ship_limit
        self.score = 0
        self.game_lvl = 1
