import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Class for handling bullets from ship."""

    def __init__(self, ai_game):
        """Making object of bullets in the current position of ship."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Spawning bullet in 0:0 position and changing postition to correct.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Changing bullet coordinates to float number.
        self.y = float(self.rect.y)

    def update(self):
        """Moving bullet up on the screen."""
        # Changing the float coordinate of the bullet.
        self.y -= self.settings.bullet_speed
        # Changing rectangle coordinate.
        self.rect.y = self.y

    def draw_bullet(self):
        """Rendering bullet on the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)