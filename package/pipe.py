# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING, List

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

    def __init__(self, gap_y: int, location: str, screen: pg.Surface, settings: Settings):
        """Initialize the pipe's settings"""

        super(Pipe, self).__init__()
        # Sprite.__init__(self)
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
        self.image: pg.Surface = settings.pipe_img
        self.rect: pg.Rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        # pg.draw.lines(self.image, (255, 0, 255), True, self.mask.outline())

        if location == 'top':
            self.image = pg.transform.flip(self.image, False, True)
            self.rect.centerx = self.x
            self.rect.bottom = self.y - self.gap_height / 2
        else:
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