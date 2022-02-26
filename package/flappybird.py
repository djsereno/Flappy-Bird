# ==============
# FALPPY BIRD
# ==============
# Author: Derek Sereno
# Images courtesy of
# Audio curtesy of
#
# Future updates or improvements:

# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING

# Import standard modules
import sys

# Import non-standard modules
import pygame as pg

# Import local classes and methods
from settings import Settings
from bird import Bird
import game_functions as gf

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    pass

def runPyGame():

    # Initialise PyGame
    pg.init()

    # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
    fps = 60.0
    fpsClock = pg.time.Clock()

    # Create settings
    settings = Settings()

    # Set up the window.
    width, height = settings.screen_width, settings.screen_height
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Flappy Bird")

    # Create bird
    bird = Bird(screen, settings)

    # Main game loop
    dt = 1 / fps  # dt is the time since last frame
    while True:
        gf.checkEvents(bird,settings)
        gf.update(bird, dt, settings)
        gf.draw(bird, screen, settings)
        dt = fpsClock.tick(fps)


runPyGame()