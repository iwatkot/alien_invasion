import pygame

from pygame.sprite import Sprite

class Ship(Sprite):
    """Class for ship controls."""
    def __init__(self, ai_game):
        super().__init__()
        """Ship and initial coordinates initialization."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Loading ship image and putting it into a rectangular.
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        # New ship spawning at the bottom of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Saving the floating coodinate of the ship.
        self.x = float(self.rect.x)

        # Movement flag.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Updating ship's position according to flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        # Updating rect attribute with self.x.
        self.rect.x = self.x

    def blitme(self):
        """Drawing ship in current position."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)