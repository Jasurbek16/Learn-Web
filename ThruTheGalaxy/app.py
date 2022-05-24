import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from score_board import Scoreboard
from pygame.sprite import Group


def run_game():
    # Initialize a game and create a screen object
    pygame.init()

    # an instance of settings class
    get_settings = Settings()

    screen = pygame.display.set_mode((get_settings.width, get_settings.height))
    # ^ called a surface - part of the screen where you display a game element.

    pygame.display.set_caption("Thru the Galaxy")

    # Make a button -- for starting the game
    button = Button(get_settings, screen, "Dive into :)")

    # Make a ship, a group to store bullets in, and a group of aliens
    ship = Ship(screen, get_settings)
    bullets = Group()
    aliens = Group()

    # Create the fleet of alienss
    gf.create_fleet(get_settings, screen, ship, aliens)

    # Create an instance to store game statistics and create a scoreboard
    stats = GameStats(get_settings)
    sc_bd = Scoreboard(get_settings, screen, stats)
    # Start the main loop for the game
    # !!! Tip: If your game freezes up, look carefully at what’s happening in your main while loop
    while True:

        gf.check_events(get_settings, screen, sc_bd, stats, button,
                        ship, aliens, bullets)  # checking inputs

        if stats.game_active:
            ship.update()  # updating the ship's position
            gf.update_bullets(get_settings, screen, sc_bd,
                              ship, stats, aliens, bullets)
            # update the aliens’ positions
            gf.update_aliens(get_settings, ship, aliens,
                             stats, screen, sc_bd, bullets)

        gf.update_screen(get_settings, screen, sc_bd, ship, stats,
                         aliens, bullets, button)  # updating


run_game()
