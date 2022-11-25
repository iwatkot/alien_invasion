import sys

import pygame
import pygame.mixer

from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Class for resource and game management."""
    def __init__(self):
        """Game initialization and preparing game resources."""
        pygame.init()
        self.settings = Settings()
        # Enables fullscreen option.
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.screen_rect = self.screen.get_rect()
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.sb = Scoreboard(self)
        self.play_button = Button(self, "PLAY")
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Launching the game cycle."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _fire_bullet(self):
        """Spawning new bullet and put it into group bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            if self.stats.game_active:
                bullet_sound = pygame.mixer.Sound("sounds/bullet.wav")
                pygame.mixer.Sound.play(bullet_sound)

    def _update_screen(self):
        # Rerender of screen.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        # Showing the last rendered screen.
        pygame.display.flip()

    def _update_bullets(self):
        self.bullets.update()
        # Deleting bullets which are not on the screen.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_allien_collision()

    def _check_bullet_allien_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                True, True)
        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.alien_points * len(alien)
            # alien_hit_sound = pygame.mixer.Sound("sounds/alien_hit.wav")
            # pygame.mixer.Sound.play(alien_hit_sound)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            new_level_sound = pygame.mixer.Sound("sounds/new_level.wav")
            pygame.mixer.Sound.play(new_level_sound)
            self.bullets.empty
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _check_events(self):
        # Mouse and keyboard input.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.write_highscore()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        play_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if play_clicked and not self.stats.game_active:
            # new_game_sound = pygame.mixer.Sound("sounds/new_game.wav")
            # pygame.mixer.Sound.play(new_game_sound)
            self.stats.game_active = True
            self.stats.reset_stats()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        # Handles operations when key is pressed down.
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        # Handles operations when key is up.
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_ESCAPE:
            self.stats.write_highscore()
            sys.exit()

    def _create_fleet(self):
        """Creating invasion fleet."""
        # Creating alien and counting number of aliens in a row.
        # Interval between aliens equals alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Counting number of rows on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height) - 1

        # Creating the first row of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Creating the alien and putting it into the row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = (2 * alien.rect.height +
                        2 * alien.rect.height * row_number)
        self.aliens.add(alien)

    def _update_aliens(self):
        self.aliens.update()
        self._check_fleet_edges()
        self._check_aliens_bottom()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        ship_hit_sound = pygame.mixer.Sound("sounds/ship_hit.wav")
        pygame.mixer.Sound.play(ship_hit_sound)
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _change_fleet_direction(self):
        """Moving fleet down and changing direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        """Checking when alien ship is near the edge of the screen."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


if __name__ == '__main__':
    # Creating example and launching the game.
    ai = AlienInvasion()
    ai.run_game()
