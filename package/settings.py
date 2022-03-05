# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING, List

# Import standard modules
import os
from pathlib import Path

# Import non-standard modules
import pygame as pg

# Import local classes and methods
import game_functions as gf

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    pass

GREY = (125, 125, 125)
BLACK = (0, 0, 0)
PINK = (255, 105, 180)


class Settings():
    """A class to store game settings"""

    def __init__(self):
        """Initialize the game's static settings"""

        # File paths
        # self.common_dir = os.path.dirname(os.path.dirname(__file__))
        self.common_dir = str(Path(__file__).parents[1])
        self.images_dir = self.common_dir + "\\assets\\images\\"
        self.sounds_dir = self.common_dir + "\\assets\\sounds\\"

        # # Color dictionary
        # self.colors = {}
        # self.colors["GREY"] = (125, 125, 125)
        # self.colors["BLACK"] = (0, 0, 0)

        # World settings
        self.gravity = 0.5
        self.world_velocity = 3  # default = 3

        # Background settings
        self.bg_velocity = 1
        self.img_scale = 3
        self.bg_img = gf.scale_image(self.images_dir + "background_day.png",
                                     self.img_scale)
        self.bg_rects = [self.bg_img.get_rect(), self.bg_img.get_rect()]
        self.bg_rects[1].left = self.bg_rects[0].right

        # Ground settings
        self.ground_elev = self.bg_rects[0].bottom - 100
        self.ground_img = gf.scale_image(self.images_dir + "ground.png",
                                         self.img_scale)
        self.ground_rects = [self.bg_img.get_rect(), self.bg_img.get_rect()]
        self.ground_rects[0].top = self.ground_elev
        self.ground_rects[1].top = self.ground_elev
        self.ground_rects[1].left = self.ground_rects[0].right

        # Screen layout settings
        self.screen_width = self.bg_rects[0].width
        self.screen_height = self.bg_rects[0].height
        self.bg_color = GREY

        # Bird settings
        self.max_velocity = 9  # 14
        self.jump_velocity = 2 * self.max_velocity
        self.bird_sheet = pg.image.load(self.images_dir + "bird_sheet.png")
        self.bird_frames = gf.get_frames(self.bird_sheet, 3, self.img_scale, BLACK)

        # Pipe settings
        self.pipe_width = 100
        self.gap_height = 220  # default = 220
        self.min_pipe_height = 50
        self.gap_y_min = self.gap_height / 2 + 50
        self.gap_y_max = self.screen_height - self.gap_height / 2 - 50
        self.pipe_spacing = 400
        self.pipe_img = gf.scale_image(self.images_dir + "pipe_green.png",
                                       self.img_scale)

        # UI settings
        self.score_sheet = pg.image.load(self.images_dir + "numbers_big.png")
        self.score_imgs = gf.get_frames(self.score_sheet, 10, self.img_scale, PINK)

        # Initialize dynamic variables
        self.init_dynamic_variables()

    def init_dynamic_variables(self):
        """Initializes the game's dynamic variables"""

        # Starting game as None allows user to start flying by pressing space
        # but at the beginning of the game only
        self.game_active = None
        self.flying = False
        self.travel_distance = 0