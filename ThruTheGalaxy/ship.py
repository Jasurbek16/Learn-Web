# Initialize the ship and set its starting position
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, screen, get_settings):
        # Initialize the ship and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen  # <- where to represent
        self.get_settings = get_settings
        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship2.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Start each new ship at the bottom center of the screen.
        # centering a game element
        self.rect.centerx = self.screen_rect.centerx
        # ^ the x-coordinate of the ship’s center
        # working at an edge of the screen

        self.rect.bottom = self.screen_rect.bottom
        # ^ the y-coordinate of the ship’s bottom
        # !!!rect attributes such as centerx store only integer values

        # Store a decimal value for the ship's center
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

    # Update the ship's position based on the movement flag
    def update(self):
        # Update the ship's center value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.get_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.get_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.get_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.get_settings.ship_speed_factor

        # Update rect object from self.center
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blitme(self):
        # Draw the ship at its current location.
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.centerx = self.screen_rect.centerx
        self.centery = self.screen_rect.bottom - 75
