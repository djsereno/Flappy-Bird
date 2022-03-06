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
        self.big_nums_imgs = settings.big_nums_imgs
        self.y_current_score = 100

        self.plaque = settings.score_plaque
        self.plaque_rect = self.plaque.get_rect()
        self.plaque_rect.center = self.screen.get_width() // 2, 400

        self.medal_imgs = settings.medal_imgs
        self.medal_rect = self.medal_imgs[0].get_rect()
        self.medal_rect.topleft = self.plaque_rect.left + 39, self.plaque_rect.top + 63

        self.small_nums_imgs = settings.small_nums_imgs
        self.final_score_rect = self.small_nums_imgs[0].get_rect()
        self.final_score_rect.topright = self.plaque_rect.left + 309, self.plaque_rect.top + 51
        self.high_score_rect = self.small_nums_imgs[0].get_rect()
        self.high_score_rect.topright = self.plaque_rect.left + 309, self.plaque_rect.top + 114

        self.init_dynamic_variables()

    def init_dynamic_variables(self):
        """Initializes the game's dynamic variables"""
        self.score = 0
        self.blit_sequence: List[Tuple[pg.Surface, pg.Rect]] = []
        self.add_digit()
        self.medal = self.medal_imgs[0]

    def blit_current_score(self):
        """Draws the current score at the top of the screen"""
        self.screen.blits(self.blit_sequence)

    def blit_score_plaque(self):
        """Draws the end game score plaque"""
        self.screen.blit(self.plaque, self.plaque_rect)

        if self.medal:
            self.screen.blit(self.medal, self.medal_rect)

        self.screen.blit(self.small_nums_imgs[0], self.final_score_rect)
        self.screen.blit(self.small_nums_imgs[0], self.high_score_rect)

    def increase_score(self):
        """Increases the current score and updates the blit sequence"""

        self.score += 1

        # Check if a new digit needs to be added to the blit sequence
        if len(str(self.score)) > len(self.blit_sequence):
            self.add_digit()

        # Update the blit sequence
        score = str(self.score)
        for i in range(len(score)):
            self.blit_sequence[i][0] = self.big_nums_imgs[int(score[i])]

    def check_high_score(self):
        """Checks if the current score is the high score. Updates and returns
        True if so."""

        if self.score > self.high_score:
            self.high_score = self.score
            return True

        return False

    def update_medal(self):
        """Updates the medal to display based on the final score."""
        self.medal = self.medal_imgs[0]

    def add_digit(self):
        """Adds a new digit to the blit sequence and updates all the image rects such 
        that the full sequence is centered on screen with the top of the sequence at y"""

        # Add to the blit sequence
        img = self.big_nums_imgs[0]
        img_rect = img.get_rect()
        self.blit_sequence.append([img, img_rect])

        num_digits = len(self.blit_sequence)
        digit_width = img_rect.width
        sequence_width = num_digits * digit_width
        screen_width = self.screen.get_width()

        # Update the digit rects
        for i in range(num_digits):
            x = (screen_width - sequence_width) // 2 + i * digit_width
            self.blit_sequence[i][1].topleft = x, self.y_current_score