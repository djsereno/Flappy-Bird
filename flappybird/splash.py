# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

# Import standard modules

# Import non-standard modules
import pygame as pg
from pygame.sprite import Sprite

# Import local classes and methods
import helper_functions as hf

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    pass


class Splash(Sprite):
    """A splash screen class"""

    def __init__(self, screen: pg.Surface, image: pg.Surface, center_loc: Tuple[int, int]):
        """Initialize splash screen attributes"""
        super(Splash, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = center_loc
        self.fade_speed = 10
        self.delay = [2000, 2000, 0]  # before fade-in, after fade-in, after fade-out

        self.init_dynamic_variables()

    def init_dynamic_variables(self):
        """Initializes the splash screen's dynamic variables"""

        self.fade_in = False
        self.fade_out = False
        self.animation_time = [0, 0, 0]
        self.animating = True
        self.image.set_alpha(0)

    def update(self, dt: int):
        """Update the splash screen animation"""

        # Delay before fade-in
        if self.animation_time[0] < self.delay[0]:
            self.animation_time[0] += dt
        # Fade-in
        elif not self.fade_in:
            self.fade_in = hf.fade_surface(self.image, 255, self.fade_speed)
        # Display splash / delay before fade out
        elif self.animation_time[1] < self.delay[1]:
            self.animation_time[1] += dt
        # Fade-out
        elif not self.fade_out:
            self.fade_out = hf.fade_surface(self.image, 0, -self.fade_speed)
        # Delay after fade out
        elif self.animation_time[2] < self.delay[2]:
            self.animation_time[2] += dt
        # Done
        else:
            self.animating = False

    def blitme(self):
        """Draw the splash screen to the screen"""
        
        self.screen.blit(self.image, self.rect)
