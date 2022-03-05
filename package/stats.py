# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING, List, Tuple

# Import standard modules

# Import non-standard modules
import pygame as pg
from pygame.sprite import Sprite

# Import local classes and methods

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    from settings import Settings


class Stats(Sprite):
    """A class to store game stats"""

    def __init__(self, screen: pg.Surface, settings: Settings):
        """Initialize the game's stats"""
        super(Stats, self).__init__()
        self.screen = screen
        self.high_score = 0
        self.pipes_cleared = pg.sprite.Group()

        # Images
        self.frames = settings.score_imgs
        self.y = 100

        self.init_dynamic_variables()

    def init_dynamic_variables(self):
        """Initializes the game's dynamic variables"""
        self.score = 0
        self.blit_sequence: List[Tuple[pg.Surface, pg.Rect]] = []
        self.add_digit()

    def blitme(self):
        """Draws the current score to the screen"""
        self.screen.blits(self.blit_sequence)

    def increase_score(self):
        """Increases the current score and updates the blit sequence"""

        self.score += 1

        # Check if a new digit needs to be added to the blit sequence
        if len(str(self.score)) > len(self.blit_sequence):
            self.add_digit()

        # Update the blit sequence
        score = str(self.score)
        for i in range(len(score)):
            self.blit_sequence[i][0] = self.frames[int(score[i])]

    def check_high_score(self):
        """Checks if the current score is the high score. Updates and returns
        True if so."""

        if self.score > self.high_score:
            self.high_score = self.score
            return True

        return False

    def add_digit(self):
        """Adds a new digit to the blit sequence and updates all the image rects such 
        that the full sequence is centered on screen with the top of the sequence at y"""

        # Add to the blit sequence
        img = self.frames[0]
        img_rect = img.get_rect()
        self.blit_sequence.append([img, img_rect])

        num_digits = len(self.blit_sequence)
        digit_width = img_rect.width
        sequence_width = num_digits * digit_width
        screen_width = self.screen.get_width()

        # Update the digit rects
        for i in range(num_digits):
            x = (screen_width - sequence_width) // 2 + i * digit_width
            self.blit_sequence[i][1].topleft = x, self.y