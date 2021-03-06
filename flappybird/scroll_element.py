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
    pass


class ScrollElem(Sprite):
    """A class for continuously scrolling images (e.g. background, ground)"""

    def __init__(self, images: List[pg.Surface], y: float, velocity: float, screen: pg.Surface):
        """Initialize the element's settings"""

        super(ScrollElem, self).__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Image
        self.scene = 0
        self.images: List[pg.Surface] = images
        self.image: pg.Surface = self.images[self.scene]
        self.num_tiles = self.screen_rect.width // self.image.get_width() + 2
        self.rects: List[pg.Rect] = []
        self.x = []
        self.y = y
        self.velocity = velocity

        for i in range(self.num_tiles):
            x = self.image.get_width() * i
            rect = self.image.get_rect(x=x, y=y)
            self.x.append(x)
            self.rects.append(rect)

    def change_scene(self):
        """Changes the scene by updating the index within the images list"""
        
        self.scene = (self.scene + 1) % len(self.images)
        self.image = self.images[self.scene]

    def update(self, dt: int):
        """Update the element's location"""

        # Update all x coordinates and rects
        for i in range(self.num_tiles):
            self.x[i] -= self.velocity * dt
            self.rects[i].x = int(self.x[i])

        # Check if any rects have scrolled off screen and move to end of the line
        for i in range(self.num_tiles):
            if self.rects[i].right < 0:
                self.rects[i].left = self.x[i] = self.rects[i - 1].right
                break

    def blitme(self):
        """Draws the scrolling images to the screen"""
        
        for i in range(self.num_tiles):
            self.screen.blit(self.image, self.rects[i])