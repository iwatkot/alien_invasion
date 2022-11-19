import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class for one alien."""

    def __init__(self, ai_game):
        """Alien initialization and put it into the start position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Loading alien image and preparing rect attribute.
        self.image = pygame.image.load("images/tv.png")
        self.rect = self.image.get_rect()

        # Spawning new aliens in the top left bottom of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Saving horizontal position of the alien.
        self.x = float(self.rect.x)
        
    def update(self):
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Returns True if alien ship is near edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True