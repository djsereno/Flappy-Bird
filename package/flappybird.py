# ==============
# FALPPY BIRD
# ==============
# Author: Derek Sereno
# Images courtesy of "The VG Resource", https://www.spriters-resource.com/mobile/flappybird/sheet/59894/
# Audio curtesy of "The VG Resource", https://www.sounds-resource.com/mobile/flappybird/sound/5309/
# Music curtesy of Minetrackmania, https://www.youtube.com/watch?v=vLVRmC-q9Oc&ab_channel=DaviddTech
#
# Future updates or improvements:
#   - Leaderboard
#   - Window scaling

# Allow for type hinting while preventing circular imports
from __future__ import annotations

# Import standard modules

# Import non-standard modules
import pygame as pg

# Import local classes and methods
from .settings import Settings
from .bird import Bird
from .button import Button
from .stats import Stats
from .splash import Splash
from .scroll_element import ScrollElem
from .game_functions import *


def runPyGame():

    # Initialise PyGame
    pg.init()

    # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate.
    fps = 120.0
    fpsClock = pg.time.Clock()

    # Set up the window.
    screen_width, screen_height = 480, 720
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption('Flappy Bird')

    # Create stats and settings
    settings = Settings(screen)
    pg.display.set_icon(settings.icon)
    stats = Stats(screen, settings)
    splash = Splash(screen, settings.splash_img, settings.splash_loc)

    # Create bird
    bird = Bird(screen, settings)

    # Create pipes
    pipes = pg.sprite.Group()

    # Create background and ground elements
    background = ScrollElem(settings.bg_imgs, 0, settings.bg_velocity, screen)
    ground = ScrollElem([settings.ground_img], settings.ground_elev, settings.world_velocity, screen)

    # Create game buttons
    buttons = pg.sprite.Group()

    # ~~~ Uncomment for leaderboard button. Leaderboard functionality not implemented currently.
    # x = stats.plaque_rect.right - settings.leader_button_img.get_width() // 2
    # y = stats.plaque_rect.bottom + 27 + settings.leader_button_img.get_height() // 2
    # button = Button('leaderboard', screen, settings.leader_button_img, (x, y), settings.sfx_pop)
    # buttons.add(button)

    # x = stats.plaque_rect.left + settings.play_button_img.get_width() // 2
    x = screen_width // 2
    y = stats.plaque_rect.bottom + 27 + settings.play_button_img.get_height() // 2
    button = Button('new_game', screen, settings.play_button_img, (x, y), settings.sfx_pop)
    buttons.add(button)

    # Main game loop
    dt = 1 / fps
    while True:
        check_events(bird, pipes, background, buttons, screen, stats, settings)
        update_world(pipes, background, ground, dt, screen, settings)
        bird.update(dt, settings)

        if settings.current_state == 'SPLASH':
            splash.update(dt)
            if not splash.animating:
                settings.current_state = 'READY'

        # Collisions and score only need to be checked in PLAY state
        elif settings.current_state == 'PLAY':
            check_collisions(bird, pipes, stats, settings)
            check_score(bird, pipes, stats)

        draw(dt, bird, pipes, background, ground, buttons, screen, stats, settings, splash)
        dt = fpsClock.tick(fps)


runPyGame()