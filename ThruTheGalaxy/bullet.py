import pygame
from pygame.sprite import Sprite
'''using sprites, we can group related elements
in our game and act on all the grouped elements at once'''

# A class to manage bullets fired from the ship


class Bullet(Sprite):
    # Create a bullet object at the ship's current position
    def __init__(self, get_settings, screen, ship):

        super(Bullet, self).__init__()
        # ^ to inherit properly from Sprite
        # ^ allows you to call the methods of the parent class in general
        # ^ providing arguments to super() here is optional

        self.screen = screen

        # Create (from a scratch) a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, get_settings.bullet_width,
                                get_settings.bullet_height)
        # the same pos as the ship
        self.rect.centerx = ship.rect.centerx
        # looks like emerging from the ship
        self.rect.top = ship.rect.top

        # Store the bullet's position as a decimal value
        # moves only in "y" direction
        self.y = float(self.rect.y)

        self.color = get_settings.bullet_color
        self.speed_factor = get_settings.bullet_speed_factor

    # Move the bullet up the screen
    def update(self):
        # Update the decimal position of the bullet
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    # Draw the bullet to the screen
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        #       ^ fills the part of the screen defined by the bullet’s
        #           -rect with the color stored
