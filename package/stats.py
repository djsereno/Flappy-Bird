# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING, List

# Import standard modules

# Import non-standard modules
import pygame as pg
from pygame.sprite import Sprite

# Import local classes and methods
from .game_functions import *

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    from .settings import Settings


class Stats(Sprite):
    """A class to store game stats and handle scoring"""

    def __init__(self, screen: pg.Surface, settings: Settings):
        """Initialize the game's stats"""
        
        super(Stats, self).__init__()
        self.screen = screen
        self.pipes_cleared = pg.sprite.Group()

        # Images
        self.big_nums_imgs = settings.big_nums_imgs
        self.high_score = 0
        self.x_current_score = self.screen.get_width() // 2
        self.y_current_score = 100

        self.plaque_orig = settings.score_plaque_img
        self.plaque_rect = self.plaque_orig.get_rect()
        self.plaque_rect.center = self.screen.get_rect().center

        self.medal_imgs = settings.medal_imgs
        self.medal_rect = self.medal_imgs[0].get_rect()
        self.medal_rect.topleft = 39, 63

        self.small_nums_imgs = settings.small_nums_imgs
        self.final_score_rect = self.small_nums_imgs[0].get_rect()
        self.final_score_rect.topright = 309, 51
        self.high_score_rect = self.small_nums_imgs[0].get_rect()
        self.high_score_rect.topright = 309, 114

        self.new_hs_img = settings.new_high_score_img
        self.new_hs_img_rect = self.new_hs_img.get_rect()
        self.new_hs_img_rect.topleft = 201, 87

        self.fade_in_time = 500

        # Sound effects
        self.sfx_point = settings.sfx_point

        self.init_dynamic_variables()

    def init_dynamic_variables(self):
        """Initializes the game's dynamic stat variables"""
        
        self.score = 0
        self.new_high_score = False
        self.plaque = self.plaque_orig.copy()
        self.blit_sequence = self.create_blit_sequence(self.score, self.x_current_score, self.y_current_score,
                                                       self.big_nums_imgs, 'center')
        self.medal = None
        self.current_time = 0
        self.animating = False

    def blit_current_score(self):
        """Draws the current score at the top of the screen"""
        
        self.screen.blits(self.blit_sequence)

    def prep_score_plaque(self):
        """Preps the score plaque for display at the end of the game"""

        self.animating = True

        # Award the medal
        self.award_medal()
        if self.medal:
            self.plaque.blit(self.medal, self.medal_rect)

        # Check high score
        self.check_high_score()
        if self.new_high_score:
            self.plaque.blit(self.new_hs_img, self.new_hs_img_rect)

        # Blit the scores to the plaque
        final_score = self.create_blit_sequence(self.score, 309, 51, self.small_nums_imgs, 'right')
        high_score = self.create_blit_sequence(self.high_score, 309, 114, self.small_nums_imgs, 'right')
        self.plaque.blits(final_score)
        self.plaque.blits(high_score)

    def create_blit_sequence(self, value: int, x: int, y: int, imgs: List[pg.Surface], justify: str = 'left'):
        """Creates and returns a blit sequence for score digits for the input score 'value' using the 
        digit sprites stored in an 'imgs' list. By default, the top-left of the sequence will be located at x, y. Justify may optionally be set to 'center' or 'right'."""

        blit_sequence = []
        num_digits = len(str(value))
        digit_width = imgs[0].get_width()
        sequence_width = num_digits * digit_width

        # Offset text by justification
        if justify == 'left':
            x_off = 0
        elif justify == 'center':
            x_off = sequence_width // 2
        elif justify == 'right':
            x_off = sequence_width
        else:
            print("Invalid justification input (left, center, or right).")
            return False

        # Populate the blit sequence
        prev_rect = pg.Rect(0, 0, 0, 0)
        for digit in str(value):
            img: pg.Surface = imgs[int(digit)]
            img_rect = img.get_rect()

            if len(blit_sequence) == 0:
                img_rect.topleft = x - x_off, y
            else:
                img_rect.topleft = prev_rect.topright

            blit_sequence.append([img, img_rect])
            prev_rect = img_rect

        return blit_sequence

    def blit_score_plaque(self, dt: int, surface: pg.Surface):
        """Draws the end game score plaque"""

        if self.current_time < self.fade_in_time:
            self.current_time += dt
            y_off = ((self.fade_in_time - self.current_time) / self.fade_in_time) * 20
            self.plaque_rect.centery = self.screen.get_height() // 2 - y_off
            alpha = translate(self.current_time, 0, self.fade_in_time, 0, 255)
            self.plaque.set_alpha(alpha)
        else:
            self.animating = False

        surface.blit(self.plaque, self.plaque_rect)

    def increase_score(self):
        """Increases the current score and updates the blit sequence"""

        self.score += 1
        self.sfx_point.play()

        # Check if a new digit needs to be added to the blit sequence
        if len(str(self.score)) > len(self.blit_sequence):
            self.blit_sequence = self.create_blit_sequence(self.score, self.x_current_score, self.y_current_score,
                                                           self.big_nums_imgs, 'center')
        # Update the blit sequence
        else:
            score = str(self.score)
            for i in range(len(score)):
                self.blit_sequence[i][0] = self.big_nums_imgs[int(score[i])]

    def check_high_score(self):
        """Checks if the current score is the high score. Updates and returns
        True if so."""

        if self.score > self.high_score:
            self.high_score = self.score
            self.new_high_score = True
            return True

        return False

    def award_medal(self):
        """Updates the medal to display based on the final score."""

        # Bronze >= 10, Silver >= 20, Gold >= 30, Plat >= 40
        if self.score >= 10:
            self.medal = self.medal_imgs[min(self.score // 10 - 1, 3)]