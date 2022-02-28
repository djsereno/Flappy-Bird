# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING

# Import standard modules

# Import non-standard modules
import pygame as pg

# Import local classes and methods
import game_functions as gf

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    from settings import Settings


class Bird(pg.sprite.Sprite):
    """A class for the bird"""

    def __init__(self, screen: pg.Surface, settings: Settings):
        """Initialize the bird's settings"""

        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Positioning
        self.x = 150
        self.y = self.screen_rect.centery
        self.accel = settings.gravity
        self.velocity = 0
        self.max_velocity = settings.max_velocity
        self.jump_velocity = settings.jump_velocity

        # Image
        self.image = pg.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def flap(self):
        """Jump the bird"""

        # Update the bird's velocity
        self.velocity = -self.jump_velocity

    def update(self):
        """Update the bird"""

        # Update the bird's velocity and position
        new_velocity = self.velocity + self.accel
        self.velocity = gf.clamp(new_velocity, -self.max_velocity,
                                 self.max_velocity)
        self.y += self.velocity

        # Update the rect
        self.rect.centery = self.y

    def blitme(self):
        """Draw the bird at its current location"""
        # self.screen.blit(self.image, self.rect)
        pg.draw.rect(self.screen, (0, 0, 255), self.rect)
        pg.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), 3)
