# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING, List, Tuple

# Import standard modules
import os

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

    def __init__(self, screen: pg.Surface):
        """Initialize the game's static settings"""

        # File paths
        self.root = os.path.abspath(os.path.join(__file__, '../..'))
        self.images_dir = os.path.abspath(os.path.join(self.root, 'assets/images'))
        self.sounds_dir = os.path.abspath(os.path.join(self.root, 'assets/sounds'))

        self.img_scale = 3
        self.load_image_assets()
        self.load_sound_assets()

        # World settings
        self.gravity = 0.5 * 3600 / 1000000  # default = 0.5
        self.world_velocity = 3 * 60 / 1000  # default = 3
        self.max_start_delay = 1500
        self.idle_msg_delay = 4000

        # Screen layout settings
        self.screen_width, self.screen_height = screen.get_size()
        self.bg_color = GREY

        # Background settings
        self.bg_velocity = 1 * 60 / 1000  # default = 1

        # Ground settings
        self.ground_elev = self.screen_height - 100

        # Bird settings
        self.max_velocity = 9 * 60 / 1000  # default = 9
        self.jump_velocity = 2 * self.max_velocity
        self.bird_frames = gf.load_frames(self.bird_sheet, 3, BLACK)

        # Pipe settings
        self.pipe_width = 100
        self.gap_height = 220  # default = 220
        self.min_pipe_height = 50
        self.gap_y_min = self.gap_height / 2 + 50
        self.gap_y_max = self.screen_height - self.gap_height / 2 - 50
        self.pipe_spacing = 400

        # UI settings
        self.splash_loc = (self.screen_width // 2, 250)
        self.idle_msg_rect = self.idle_msg_img.get_rect()
        self.idle_msg_rect.midbottom = self.screen_width // 2, self.screen_height - 125
        self.game_over_rect = self.game_over_img.get_rect()
        self.game_over_rect.midbottom = self.screen_width // 2, 250
        self.big_nums_imgs = gf.load_frames(self.big_nums_sheet, 10, PINK)
        self.small_nums_imgs = gf.load_frames(self.small_nums_sheet, 10, PINK)
        self.medal_imgs = gf.load_frames(self.medal_sheet, 4, PINK)
        self.game_states = ('SPLASH', 'READY', 'PLAY', 'GAMEOVER')
        self.dimmer = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)
        self.dimmer.fill((0, 0, 0))
        self.dimmer_max_opacity = 100

        # Initialize dynamic variables
        self.init_dynamic_variables()
        self.current_state = 'SPLASH'
        self.start_delay = 0

    def init_dynamic_variables(self):
        """Initializes the game's dynamic variables"""

        self.current_state = 'READY'
        self.travel_distance = 0
        self.dimmer.set_alpha(0)
        self.game_over_img.set_alpha(0)
        self.idle_time = 0
        self.idle_msg_img.set_alpha(0)

    def load_image_assets(self):
        """Load the game's image assets"""

        # Game images
        self.bg_img = gf.load_image('background_day.png', self.img_scale, self.images_dir)
        self.ground_img = gf.load_image('ground.png', self.img_scale, self.images_dir)
        self.bird_sheet = gf.load_image('bird_sheet.png', self.img_scale, self.images_dir)
        self.pipe_img = gf.load_image('pipe_green.png', self.img_scale, self.images_dir)

        # Scoreboard images
        self.score_plaque_img = gf.load_image('score_plaque.png', self.img_scale, self.images_dir, PINK)
        self.big_nums_sheet = gf.load_image('numbers_big.png', self.img_scale, self.images_dir)
        self.small_nums_sheet = gf.load_image('numbers_small.png', self.img_scale, self.images_dir)
        self.medal_sheet = gf.load_image('medal_sheet.png', self.img_scale, self.images_dir)
        self.new_high_score_img = gf.load_image('new.png', self.img_scale, self.images_dir)

        # UI Images
        self.icon = gf.load_image('bird_icon.png', self.img_scale, self.images_dir)
        self.splash_img = gf.load_image('splash.png', self.img_scale, self.images_dir)
        self.game_over_img = gf.load_image('game_over.png', self.img_scale, self.images_dir)
        self.idle_msg_img = gf.load_image('press_space.png', self.img_scale, self.images_dir, PINK)

        # Buttons
        self.play_button_img = gf.load_image('play_button.png', self.img_scale, self.images_dir, PINK)
        self.leader_button_img = gf.load_image('leaderboard_button.png', self.img_scale, self.images_dir, PINK)

    def load_sound_assets(self):
        """Load the game's sound assets"""
        pass
