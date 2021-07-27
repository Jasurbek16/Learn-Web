import pygame.font
# ^ lets Pygame render
# text to the screen


class Button():

    def __init__(self, get_settings, screen, msg):
        # Initialize button attributes
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (255, 255, 255)
        self.txt_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)
        # prepare a font attribute for rendering text
        # args -> None - use the default font
        #      -> 48 size of the txt

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx, self.rect.centery = self.screen_rect.center
        self.rect.centery += 100
        # The button message needs to be prepped only once.
        self.prep_msg(msg)
        # Pygame works with text by rendering the string you want to
        # display as an image

    def prep_msg(self, msg):
        # Turn msg into a rendered image and center text on the button
        self.msg_img = self.font.render(
            msg, True, self.txt_color, self.button_color)
        # args:   ^ turn antialiasing on or off (makes the edges of the text smoother)
        # if no back color is set Pygame will try to render the font
        # with a transparent background
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_img, self.msg_img_rect)
