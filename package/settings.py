# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING

# Import standard modules

# Import non-standard modules
import pygame as pg

# Import local classes and methods

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    pass


class Settings():
    """A class to store game settings"""

    def __init__(self):
        """Initialize the game's static settings"""

        self.gravity = 1
        self.max_velocity = 18
        self.jump_velocity = 2 * self.max_velocity

        # Color dictionary
        self.colors = {}
        self.colors["GREY"] = (125, 125, 125)

        # Screen layout settings
        self.screen_width = 800
        self.screen_height = 800
        self.bg_color = self.colors["GREY"]

        # Initialize dynamic variables
        self.init_dynamic_variables()

    def init_dynamic_variables(self):
        """Initializes the game's dynamic variables"""

        return