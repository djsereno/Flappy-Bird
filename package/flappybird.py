# ==============
# FALPPY BIRD
# ==============
# Author: Derek Sereno
# Images courtesy of
# Audio curtesy of
#
# Future updates or improvements:
#   - Implement frame rate independence

# Allow for type hinting while preventing circular imports
from __future__ import annotations
from email.headerregistry import Group
from typing import TYPE_CHECKING

# Import standard modules
import sys
import random

# Import non-standard modules
import pygame as pg

# Import local classes and methods
from settings import Settings
from bird import Bird
from pipe import Pipe
from button import Button
from stats import Stats
import game_functions as gf

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    pass


def runPyGame():

    # Initialise PyGame
    pg.init()

    # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate.
    fps = 60.0
    fpsClock = pg.time.Clock()

    # Create stats and settings
    settings = Settings()
    stats = Stats()
    print(f"Score: {stats.score}, High: {stats.high_score}")

    # Set up the window.
    width, height = settings.screen_width, settings.screen_height
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Flappy Bird")

    # Create bird
    bird = Bird(screen, settings)

    # Create pipes
    pipes = pg.sprite.Group()
    gf.create_new_pipes(pipes, screen, settings)

    # Create game buttons
    buttons = pg.sprite.Group()
    button_loc = (screen.get_width() // 2, screen.get_height() // 2)
    new_game_button = Button(screen, settings, "New Game", button_loc)
    buttons.add(new_game_button)

    # Main game loop
    # dt is the time since last frame
    dt = 1 / fps
    while True:
        gf.check_events(bird, pipes, buttons, screen, stats, settings)

        if settings.flying:
            gf.update_world(pipes, dt, screen, settings)

        if settings.game_active:
            bird.update()
            gf.check_collisions(bird, pipes, settings)
            gf.check_score(bird, pipes, stats)

        gf.draw(bird, pipes, buttons, screen, stats, settings)
        dt = fpsClock.tick(fps)


runPyGame()