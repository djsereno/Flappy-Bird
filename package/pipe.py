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
    from .settings import Settings


class Pipe(Sprite):
    """A class for the pipes"""

    def __init__(self, gap_y: int, location: int, screen: pg.Surface, settings: Settings):
        """Initialize the pipe's settings"""

        super(Pipe, self).__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Positioning, x = center of pipe, y = center of gap
        self.width = settings.pipe_width
        self.x = self.screen_rect.right + self.width / 2
        self.y = gap_y
        self.velocity = settings.world_velocity
        self.gap_height = settings.gap_height
        self.location = location  # 0 = Bottom, 1 = Top

        # Image
        self.color = settings.pipe_color
        self.images: List[List[pg.Surface]] = settings.pipe_imgs
        self.image: pg.Surface = self.images[self.location][self.color]
        self.rect: pg.Rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

        if location == 1:
            self.rect.centerx = self.x
            self.rect.bottom = self.y - self.gap_height / 2
        else:
            self.rect.centerx = self.x
            self.rect.top = self.y + self.gap_height / 2

    def update(self, dt: int):
        """Update the pipe's location"""

        # Update the pipe's position
        self.x -= self.velocity * dt
        self.rect.centerx = self.x

        # Check if pipe is still visible, kill if not
        if self.rect.right < self.screen_rect.left:
            self.kill()