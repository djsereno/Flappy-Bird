# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

# Import standard modules

# Import non-standard modules
import pygame as pg
from pygame.sprite import Sprite

# Import local classes and methods
from .game_functions import *

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    pass


class Button(Sprite):
    """A button class drawn with images"""

    def __init__(self, action: str, screen: pg.Surface, image: pg.Surface, center_loc: Tuple[int, int],
                 sfx: pg.mixer.Sound):
        """Initialize button attributes"""
        
        super(Button, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button
        self.action = action
        self.location = center_loc

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.location

        hover_scale = 1.1
        self.image_hover = scale_image(self.image, hover_scale)
        self.rect_hover = self.image_hover.get_rect()
        self.rect_hover.center = self.location
        self.hover = False

        # Sound effects
        self.sfx_hover = sfx

        self.init_dynamic_variables()

    def init_dynamic_variables(self):
        """Initializes the button's dynamic variables"""

        self.active = False  # Controls if button is clickable (doesn't control visibility)
        self.image.set_alpha(0)  # Button will be faded in later in draw function

    def draw(self, mouse_pos: tuple):
        """Draw the button to the screen. Mouse_pos will affect hover behavior"""

        # Prep the message with button highlighting as necessary
        if self.rect.collidepoint(mouse_pos) and self.active:
            if not self.hover:
                self.hover = True
                self.sfx_hover.stop()
                self.sfx_hover.play()
            self.screen.blit(self.image_hover, self.rect_hover)
        else:
            self.hover = False
            self.screen.blit(self.image, self.rect)
