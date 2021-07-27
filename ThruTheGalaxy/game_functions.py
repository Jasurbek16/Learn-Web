# manage events separately
# -from other aspects of the game, like updating the screen.
import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, get_settings, screen, ship, bullets):
    # respond to key presses
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        # Move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        # Move the ship to the left
        ship.moving_left = True
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        # Move the ship to up
        ship.moving_up = True
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        # Move the ship down
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(get_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullets(get_settings, screen, ship, bullets):
    # When the spacebar is pressed
    # Create a new bullet and add it to the bullets group
    # fire bullets only in groups of three
    if len(bullets) < get_settings.bullets_allowed:
        new_bullet = Bullet(get_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    # respond to key releases
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        # Stop moving the ship to the right
        ship.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        # Stop moving the ship to the left
        ship.moving_left = False
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        # Stop moving the ship to up
        ship.moving_up = False
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        # Stop moving the ship down
        ship.moving_down = False


def check_events(get_settings, screen, sc_bd, stats, button,
                 ship, aliens, bullets):
    # Watch for keyboard and mouse events
    for event in pygame.event.get():  # action that the user performs while playing the game
        # ^ event loop.
        # when the player clicks the game window’s close button
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # pygame.mouse.get_pos returns a tuple containing the x-
            # and y-coordinates of the mouse
            # cursor when the mouse button is clicked
            check_button_active(get_settings, screen, stats, sc_bd, button, ship, aliens,
                                bullets, mouse_x, mouse_y)

        # for activating a continuous movement
        elif event.type == pygame.KEYDOWN:  # when each keypress is detected
            check_keydown_events(event, get_settings, screen, ship, bullets)

        # for deactivating a continuous movement
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

# Start a new game when the player clicks the button


def check_button_active(get_settings, screen, stats, sc_bd, button, ship, aliens,
                        bullets, mouse_x, mouse_y):
    clicked_button = button.rect.collidepoint(mouse_x, mouse_y)
    # ^ returns now a bool
    if clicked_button and not stats.game_active:

        # Reset the game speed
        get_settings.initialize_dynamic_settings()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
        # hide the cursor when the mouse is over the game window

        # Reset everything
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sc_bd.prep_score()
        sc_bd.prep_high_score()
        sc_bd.prep_lvl()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        sc_bd.prep_ships()

        # Create a new fleet and center the ship.
        create_fleet(get_settings, screen, ship, aliens)
        ship.center_ship()

# Update images on the screen and flip to the new screen


def update_screen(get_settings, screen, sc_bd, ship, stats,
                  aliens, bullets, button):
    # Redraw the screen during each pass through the loop.
    screen.fill(get_settings.b_ground_color)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        #             ^ returns a list of all sprites in the group bullets
        bullet.draw_bullet()

    ship.blitme()

    # Draw the score information.
    sc_bd.show_score()

    aliens.draw(screen)
    # ^ draws each element in the group at the position defined by its rect attribute

    if not stats.game_active:
        button.draw_button()

    pygame.display.flip()
    # ^ Make the most recently drawn screen visible


def update_bullets(get_settings, screen, sc_bd, ship, stats, aliens, bullets):
    # Update position of bullets and get rid of old bullets
    # Update bullet positions
    bullets.update()  # the group automatically calls update() for each sprite in the group
    # ^ calls bullet.update() for each bullet we place in the group bullets
    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))
    # ^ verify that bullets are removed (needs to be commented,
    # -coz that's only for checking)
    # ------------------------------------------------------------
    check_collisions(get_settings, screen, sc_bd, ship, stats, aliens, bullets)


def check_collisions(get_settings, screen, sc_bd, ship, stats, aliens, bullets):

    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    # to look for collisions between members of two groups.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # ^ loops thru each of the provided groups' obj.s
    # ^ returns a dict of key-val pairs of two overlapped obj.s' rects
    # True, True <- whether to del collided things or not

    if collisions:
        for aliens in collisions.values():
            stats.score += get_settings.alien_pts * len(aliens)
            sc_bd.prep_score()
            # ^ create a new img for the updated score
        check_high_score(stats, sc_bd)

    if len(aliens) == 0:
        # Destroy existing bullets, speed up game, and create new fleet
        # cancel existing bullets and create a new fleet
        bullets.empty()
        # ^ removes all the remaining sprites from a group
        get_settings.increase_speed()

        # Show the increased lvl
        stats.game_lvl += 1
        sc_bd.prep_lvl()

        create_fleet(get_settings, screen, ship, aliens)


def check_high_score(stats, sc_bd):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sc_bd.prep_high_score()

# Create a full fleet of aliens


def get_number_aliens_x(get_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    # Spacing between each alien is equal to one alien width
    available_space_x = get_settings.width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(get_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = get_settings.height - 3*alien_height - ship_height
    number_rows = int(available_space_y/(2*alien_height)) - 2
    return number_rows


def create_alien(get_settings, screen, aliens, alien_number, row_number):
    # Create an alien and find the number of aliens in a row
    alien = Alien(get_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)


def create_fleet(get_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(get_settings, screen)
    number_aliens_x = get_number_aliens_x(get_settings, alien.rect.width)
    number_rows = get_number_rows(
        get_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens
    for row_number in range(number_rows):
        # Create the first row of aliens.
        for alien_number in range(number_aliens_x):
            create_alien(get_settings, screen, aliens,
                         alien_number, row_number)
# eachRow canBe placed fartherDown the screen ^


def check_fleet_edges(get_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():  # <- loop through the fleet
        if alien.check_edges():
            change_fleet_direction(get_settings, aliens)
            break


def change_fleet_direction(get_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += get_settings.fleet_drop_speed
    get_settings.fleet_direction *= -1


def ship_hit(get_settings, stats, screen, sc_bd, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:

        # Decrement ships_left.
        stats.ships_left -= 1

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        # Updating the number of ships displayed as lives left
        sc_bd.prep_ships()
        # Create a new fleet and center the ship.
        create_fleet(get_settings, screen, ship, aliens)
        ship.center_ship()
        # Pause
        sleep(0.45)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        # ^ the coursor appears when the game ends


def check_aliens_bottom(get_settings, stats, screen, sc_bd, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom == screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(get_settings, stats, screen, sc_bd, ship, aliens, bullets)
            break


def update_aliens(get_settings, ship, aliens, stats, screen, sc_bd, bullets):
    """
Check if the fleet is at an edge,
and then update the postions of all aliens in the fleet.
"""
    check_fleet_edges(get_settings, aliens)
    aliens.update()  # automatically calls each alien’s update() method.
    # Look for alien-ship collisions.

    if pygame.sprite.spritecollideany(ship, aliens):
        # print(" ): Storming down the ship :( ")
        ship_hit(get_settings, stats, screen, sc_bd, ship, aliens, bullets)
    # ^ looks for any member of the group that’s collided with
    # -the sprite and stops looping through the group
    # ^ returns the first alien it finds that has collided with ship. No collison, return None
        # Look for aliens hitting the bottom of the screen
        check_aliens_bottom(get_settings, stats, screen,
                            sc_bd, ship, aliens, bullets)
