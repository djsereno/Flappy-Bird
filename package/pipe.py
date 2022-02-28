# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING

# Import standard modules

# Import non-standard modules
import pygame as pg
from pygame.sprite import Sprite

# Import local classes and methods

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    from settings import Settings


class Pipe(Sprite):
    """A class for the pipes"""

    def __init__(self, gap_y: int, location: str, screen: pg.Surface,
                 settings: Settings):
        """Initialize the pipe's settings"""

        # super(Pipe, self).__init__()
        Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Positioning, x = center of pipe, y = center of gap
        self.width = settings.pipe_width
        self.x = self.screen_rect.right + self.width / 2
        self.y = gap_y
        self.velocity = settings.world_velocity
        self.gap_height = settings.gap_height
        self.location = location

        # Image
        if location == "top":
            height = self.y - self.gap_height / 2
            self.image = pg.Surface((self.width, height))
            self.rect = self.image.get_rect()
            self.rect.centerx = self.x
            self.rect.bottom = self.y - self.gap_height / 2
        else:
            height = self.screen_rect.height - self.y - self.gap_height / 2
            self.image = pg.Surface((self.width, height))
            self.rect = self.image.get_rect()
            self.rect.centerx = self.x
            self.rect.top = self.y + self.gap_height / 2

    def update(self):
        """Update the pipe's location"""

        # Update the pipe's position
        self.x -= self.velocity
        self.rect.centerx = self.x

        # Check if pipe is still visible, kill if not
        if self.rect.right < self.screen_rect.left:
            self.kill()

    def blitme(self):
        """Draw the pipe at its current location"""
        # self.screen.blit(self.image, self.rect)
        pg.draw.rect(self.screen, (255, 0, 0), self.rect)
        pg.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), 3)