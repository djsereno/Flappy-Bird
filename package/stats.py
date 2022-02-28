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


class Stats():
    """A class to store game stats"""

    def __init__(self):
        """Initialize the game's stats"""
        self.high_score = 0
        self.pipes_cleared = pg.sprite.Group()
        self.init_dynamic_variables()

    def init_dynamic_variables(self):
        """Initializes the game's dynamic variables"""
        self.score = 0

    def check_high_score(self):
        """Checks if the current score is the high score. Updates and returns
        True if so."""

        if self.score > self.high_score:
            self.high_score = self.score
            return True

        return False