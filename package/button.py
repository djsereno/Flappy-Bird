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


class Button(Sprite):

    def __init__(self, screen: pg.Surface, settings: Settings, message: str,
                 location):
        """Initialize button attributes"""
        Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (200, 200, 200)
        self.text_color = (0, 255, 0)
        self.text_color_hover = (255, 255, 0)
        self.font = pg.font.SysFont(None, 48)
        self.location = location
        self.msg = message

        # Prep the button messgae
        self.prep_message(False)

        # Build the button's rect object and center it
        self.width = self.msg_img_rect.width + 20
        self.height = self.msg_img_rect.height + 20
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = self.location

    def prep_message(self, hover: bool):
        """Turn message into a rendered image and center text on the button"""

        # Change text color if hovering or not
        if hover:
            color = self.text_color_hover
        else:
            color = self.text_color

        self.msg_img = self.font.render(self.msg, True, color,
                                        self.button_color)
        self.msg_img_rect: pg.Rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.location

    def draw(self, mouse_pos: tuple):
        """Draw the button to the screen"""

        # Draw blank button and then draw the message
        pg.draw.rect(self.screen, self.button_color, self.rect)
        pg.draw.rect(self.screen, (0, 0, 0), self.rect, 3)

        # Prep the message with button highlighting as necessary
        if self.rect.collidepoint(mouse_pos):
            self.prep_message(True)
        else:
            self.prep_message(False)

        # Draw the message to screen
        self.screen.blit(self.msg_img, self.msg_img_rect)
