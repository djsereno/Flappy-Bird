# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING, List, Tuple

# Import standard modules

# Import non-standard modules
import pygame as pg
from pygame.sprite import Sprite

# Import local classes and methods
import game_functions as gf

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    from settings import Settings


class Button(Sprite):
    """A button class drawn with images"""

    def __init__(self, action: str, screen: pg.Surface, image: pg.Surface, center_loc: Tuple[int, int]):
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
        self.image_hover = gf.scale_image(self.image, hover_scale)
        self.rect_hover = self.image_hover.get_rect()
        self.rect_hover.center = self.location

        self.init_dynamic_variables()

    def init_dynamic_variables(self):
        """Initializes the birds's dynamic variables"""

        self.active = False  # Controls if button is clickable (doesn't control visibility)
        self.image.set_alpha(0)  # Button will be faded in later in draw function

    def draw(self, mouse_pos: tuple):
        """Draw the button to the screen"""

        # Prep the message with button highlighting as necessary
        if self.rect.collidepoint(mouse_pos) and self.active:
            self.screen.blit(self.image_hover, self.rect_hover)
        else:
            self.screen.blit(self.image, self.rect)
