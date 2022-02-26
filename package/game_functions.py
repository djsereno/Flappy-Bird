# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING

# Import standard modules
import sys

# Import non-standard modules
import pygame as pg

# Import local classes and methods

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    from bird import Bird
    from settings import Settings


def checkEvents(bird: Bird, settings: Settings):
    """Check for key events. Called once per frame."""

    # Go through events that are passed to the script by the window.
    for event in pg.event.get():

        # Check if user quits
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        # Check if user clicks
        elif event.type == pg.KEYDOWN:
            check_keydown_events(bird, event)

        elif event.type == pg.KEYUP:
            check_keyup_events(event)

        elif event.type == pg.MOUSEBUTTONDOWN:
            left, middle, right = pg.mouse.get_pressed()
            mouse_x, mouse_y = pg.mouse.get_pos()


def check_keydown_events(bird: Bird, event):
    """Respond to keypresses"""

    if event.key == pg.K_q:
        sys.exit()

    elif event.key == pg.K_SPACE:
        bird.flap()


def check_keyup_events(event):
    """Respond to key releases"""
    return


def update(bird: Bird, dt: int, settings: Settings):
    """Updates the game items"""

    bird.update(settings)


def draw(bird: Bird, screen: pg.Surface, settings: Settings):
    """Draw things to the window. Called once per frame."""
    screen.fill(settings.bg_color)

    bird.blitme()
    pg.display.flip()


def reset_game(settings: Settings):
    """Start a new game"""

    settings.init_dynamic_variables()


def clamp(value, min_val, max_val):
    """Clamps a value to a given range"""
    return max(min_val, min(max_val, value))