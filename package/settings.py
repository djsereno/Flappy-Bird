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
        self.idle_msg_delay = 1000

        # Screen layout settings
        self.screen_width, self.screen_height = screen.get_size()
        self.bg_color = GREY

        # Background settings
        self.bg_imgs = [self.bg_img_day, self.bg_img_night]
        self.bg_velocity = 1 * 60 / 1000  # default = 1

        # Ground settings
        self.ground_elev = self.screen_height - 100

        # Bird settings
        # self.bird_sheet = self.bird_sheet_yellow
        self.bird_frames = [self.bird_frames_yellow, self.bird_frames_red, self.bird_frames_blue]
        self.max_velocity = 9 * 60 / 1000  # default = 9
        self.jump_velocity = 2 * self.max_velocity
        # self.bird_frames = gf.load_frames(self.bird_sheet, 3, BLACK)

        # Pipe settings
        self.pipe_imgs = [self.pipe_img_green, self.pipe_img_red]
        self.pipe_width = 100
        self.gap_height = 220  # default = 220
        self.min_pipe_height = 50
        self.gap_y_min = self.gap_height / 2 + 50
        self.gap_y_max = self.screen_height - self.gap_height / 2 - 50
        self.pipe_spacing = 400

        # UI settings
        self.splash_loc = (self.screen_width // 2, 200)

        self.get_ready_rect = self.get_ready_img.get_rect()
        self.get_ready_rect.center = self.screen_width // 2, 200

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

        # Dynamic variable initilization (for game start only)
        self.current_state = 'SPLASH'
        self.dimmer.set_alpha(255)
        self.start_delay = 0

    def init_dynamic_variables(self):
        """Initializes the game's dynamic variables"""

        self.sfx_music.play(loops=-1, fade_ms=2000)
        self.current_state = 'READY'
        self.travel_distance = 0
        self.idle_time = 0
        self.get_ready_img.set_alpha(0)
        self.idle_msg_img.set_alpha(0)
        self.game_over_img.set_alpha(0)
        self.dimmer.set_alpha(0)

    def load_image_assets(self):
        """Load the game's image assets"""

        # Game images
        self.bg_img_day = gf.load_image('background_day.png', self.img_scale, self.images_dir)
        self.bg_img_night = gf.load_image('background_night.png', self.img_scale, self.images_dir)

        self.ground_img = gf.load_image('ground.png', self.img_scale, self.images_dir)

        self.bird_sheet_yellow = gf.load_image('bird_sheet_yellow.png', self.img_scale, self.images_dir)
        self.bird_frames_yellow = gf.load_frames(self.bird_sheet_yellow, 3, BLACK)
        self.bird_sheet_red = gf.load_image('bird_sheet_red.png', self.img_scale, self.images_dir)
        self.bird_frames_red = gf.load_frames(self.bird_sheet_red, 3, BLACK)
        self.bird_sheet_blue = gf.load_image('bird_sheet_blue.png', self.img_scale, self.images_dir)
        self.bird_frames_blue = gf.load_frames(self.bird_sheet_blue, 3, BLACK)

        self.pipe_img_green = gf.load_image('pipe_green.png', self.img_scale, self.images_dir)
        self.pipe_img_red = gf.load_image('pipe_red.png', self.img_scale, self.images_dir)

        # Scoreboard images
        self.score_plaque_img = gf.load_image('score_plaque.png', self.img_scale, self.images_dir, PINK)
        self.big_nums_sheet = gf.load_image('numbers_big.png', self.img_scale, self.images_dir)
        self.small_nums_sheet = gf.load_image('numbers_small.png', self.img_scale, self.images_dir)
        self.medal_sheet = gf.load_image('medal_sheet.png', self.img_scale, self.images_dir)
        self.new_high_score_img = gf.load_image('new.png', self.img_scale, self.images_dir)

        # UI Images
        self.icon = gf.load_image('bird_icon.png', self.img_scale, self.images_dir)
        self.splash_img = gf.load_image('splash.png', self.img_scale, self.images_dir)
        self.get_ready_img = gf.load_image('get_ready.png', self.img_scale, self.images_dir)
        self.game_over_img = gf.load_image('game_over.png', self.img_scale, self.images_dir)
        self.idle_msg_img = gf.load_image('click_mouse.png', self.img_scale, self.images_dir, PINK)

        # Buttons
        self.play_button_img = gf.load_image('play_button.png', self.img_scale, self.images_dir, PINK)
        self.leader_button_img = gf.load_image('leaderboard_button.png', self.img_scale, self.images_dir, PINK)

    def load_sound_assets(self):
        """Load the game's sound assets"""

        self.sfx_fall = gf.load_sound('sfx_fall_delayed.wav', self.sounds_dir)
        self.sfx_hit = gf.load_sound('sfx_hit.wav', self.sounds_dir)
        self.sfx_point = gf.load_sound('sfx_point.wav', self.sounds_dir)
        self.sfx_swoosh = gf.load_sound('sfx_swoosh.wav', self.sounds_dir)
        self.sfx_flap = gf.load_sound('sfx_flap.wav', self.sounds_dir)
        self.sfx_pop = gf.load_sound('sfx_pop.wav', self.sounds_dir)
        self.sfx_music = gf.load_sound('sfx_music.wav', self.sounds_dir)
        self.sfx_music_end = gf.load_sound('sfx_music_end.wav', self.sounds_dir)

        self.sfx_music.set_volume(0.5)
        self.sfx_music_end.set_volume(0.5)
