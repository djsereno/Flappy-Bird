# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING, List

# Import standard modules

# Import non-standard modules
import pygame as pg
from pygame.sprite import Sprite

# Import local classes and methods
import game_functions as gf

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    from settings import Settings


class Bird(Sprite):
    """A class for the bird"""

    def __init__(self, screen: pg.Surface, settings: Settings):
        """Initialize the bird's settings"""

        super(Bird, self).__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Physics parameters
        self.accel = settings.gravity
        self.max_velocity = settings.max_velocity
        self.jump_velocity = settings.jump_velocity

        # Image
        self.image_orig = settings.bird_img
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()

        self.init_dynamic_variables()

    def init_dynamic_variables(self):
        """Initializes the birds's dynamic variables"""

        # Positioning
        self.x = 150
        self.y = self.screen_rect.centery
        self.rect.center = (self.x, self.y)
        self.velocity = 0
        self.angle = 0
        self.prev_jump_elev = 0

    def flap(self):
        """Jump the bird"""

        # Update the bird's velocity
        self.velocity = -self.jump_velocity
        self.prev_jump_elev = self.y

    def update(self):
        """Update the bird"""

        # Update the bird's velocity and position
        new_velocity = self.velocity + self.accel
        self.velocity = gf.clamp(new_velocity, -self.max_velocity,
                                 self.max_velocity)
        self.y += self.velocity

        # Rotate the bird
        self.angle = gf.translate(self.y, self.prev_jump_elev, self.prev_jump_elev + 150, 20, -90)
        self.image = pg.transform.rotate(self.image_orig, self.angle)

        # Update the rect
        self.rect.centery = self.y

    def blitme(self):
        """Draw the bird at its current location"""
        self.screen.blit(self.image, self.rect)
        # pg.draw.rect(self.screen, (0, 0, 255), self.rect)
        # pg.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), 3)
