import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard():

    """A class to report scoring information."""

    def __init__(self, get_settings, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.get_settings = get_settings
        self.stats = stats

        # Font settings for scoring information.
        self.txt_color = (255, 209, 26)
        self.font = pygame.font.SysFont(None, 35)

        # Prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_lvl()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_scr = int(round(self.stats.score, -1))
        # round to the nearest 10
        score_str = "Score: {:,}".format(rounded_scr)
        # put commas after 3 places from right
        self.score_img = self.font.render(
            score_str, True, self.txt_color, self.get_settings.b_ground_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high_score into a rendered image."""
        high_scr = int(round(self.stats.high_score, -1))
        # round to the nearest 10
        high_score_str = "Score to beat: {:,}".format(high_scr)
        # put commas after 3 places from right
        self.high_score_img = self.font.render(
            high_score_str, True, self.txt_color, self.get_settings.b_ground_color)

        # Display the score at the top center
        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_lvl(self):
        """Turn the level into a rendered image."""
        self.lvl_img = self.font.render(
            str(self.stats.game_lvl), True, self.txt_color, self.get_settings.b_ground_color)

        # Position the level below the score_text
        self.lvl_rect = self.lvl_img.get_rect()
        self.lvl_rect.right = self.score_rect.right
        self.lvl_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.screen, self.get_settings)
            ship.image = pygame.image.load('images\ship3.bmp')
            ship.rect.x = 10 + ship_number * ship.rect.width
            # ships appear next to each other with a 10-pixel margin
            # on the top of the group of ships
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.screen.blit(self.lvl_img, self.lvl_rect)
        # Draw ships
        self.ships.draw(self.screen)
        # Pygame draws each ship
