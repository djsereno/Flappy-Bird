# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING

# Import standard modules
import random

# Import non-standard modules
import pygame as pg

# Import local classes and methods
import game_functions as gf

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    from settings import Settings


class Pipe(pg.sprite.Sprite):
    """A class for the pipes"""

    def __init__(self, screen: pg.Surface, settings: Settings):
        """Initialize the pipes' settings"""

        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Positioning, x = center of pipe, y = center of gap
        self.width = settings.pipe_width
        self.x = self.screen_rect.right + self.width / 2
        self.y = self.screen_rect.centery
        self.velocity = settings.world_velocity
        self.gap_height = settings.gap_height

        # Image
        self.y_min = self.gap_height / 2 + 50
        self.y_max = self.screen_rect.height - self.gap_height / 2 - 50
        self.init_heights()

    def update(self):
        """Update the pipes' location"""

        # Update the pipes' position
        self.x -= self.velocity
        self.top_rect.centerx = self.x
        self.bot_rect.centerx = self.x

        # Recycle the pipe once it goes off screen
        if self.top_rect.right < 0:
            self.x = self.screen_rect.right + self.width / 2
            self.y = random.randint(self.y_min, self.y_max)
            self.init_heights()

    def init_heights(self):
        """Set the new pipe heights"""

        # Pick a new pipe height
        top_height = self.y - self.gap_height / 2
        self.top_image = pg.Surface((self.width, top_height))
        self.top_rect = self.top_image.get_rect()
        self.top_rect.centerx = self.x
        self.top_rect.bottom = self.y - self.gap_height / 2

        bot_height = self.screen_rect.height - self.y - self.gap_height / 2
        self.bot_image = pg.Surface((self.width, bot_height))
        self.bot_rect = self.bot_image.get_rect()
        self.bot_rect.centerx = self.x
        self.bot_rect.top = self.y + self.gap_height / 2

    def blitme(self):
        """Draw the bird at its current location"""
        self.screen.blit(self.top_image, self.top_rect)
        self.screen.blit(self.bot_image, self.bot_rect)