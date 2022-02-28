# Allow for type hinting while preventing circular imports
from __future__ import annotations
from turtle import distance
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

        # Color dictionary
        self.colors = {}
        self.colors["GREY"] = (125, 125, 125)

        # Screen layout settings
        self.screen_width = 800
        self.screen_height = 800
        self.bg_color = self.colors["GREY"]

        # World settings
        self.gravity = 1
        self.world_velocity = 8  # default = 10

        # Bird settings
        self.max_velocity = 14
        self.jump_velocity = 2 * self.max_velocity

        # Pipe settings
        self.pipe_width = 100
        self.gap_height = 240  # default = 220
        self.min_pipe_height = 50
        self.gap_y_min = self.gap_height / 2 + 50
        self.gap_y_max = self.screen_height - self.gap_height / 2 - 50
        self.pipe_spacing = 400

        # Initialize dynamic variables
        self.init_dynamic_variables()

    def init_dynamic_variables(self):
        """Initializes the game's dynamic variables"""

        # Starting game as None allows user to start flying by pressing space
        # but at the beginning of the game only
        self.game_active = None
        self.flying = False
        self.travel_distance = 0