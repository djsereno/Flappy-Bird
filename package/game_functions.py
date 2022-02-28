# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING

# Import standard modules
import sys
import random

# Import non-standard modules
import pygame as pg

# Import local classes and methods
from pipe import Pipe

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    from bird import Bird
    from settings import Settings
    from button import Button
    from stats import Stats


def check_events(bird: Bird, pipes: pg.sprite.Group, buttons: Button,
                 screen: pg.Surface, stats: Stats, settings: Settings):
    """Check for key events. Called once per frame."""

    # Go through events that are passed to the script by the window.
    for event in pg.event.get():

        # Check if user quits
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        # Check if user clicks
        elif event.type == pg.KEYDOWN:
            check_keydown_events(bird, event, settings)

        elif event.type == pg.KEYUP:
            check_keyup_events(event)

        elif event.type == pg.MOUSEBUTTONDOWN:
            check_click_events(buttons, bird, pipes, screen, stats, settings)


def check_click_events(buttons: pg.sprite.Group, bird: Bird,
                       pipes: pg.sprite.Group, screen: pg.Surface,
                       stats: Stats, settings: Settings):
    """Respond to mouse clicks"""

    left, middle, right = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()

    # Check for clicked buttons
    button: Button
    for button in buttons:
        if button.rect.collidepoint(mouse_pos) and left:

            # New Game button clicked
            if not settings.game_active and button.msg == "New Game":
                reset_game(bird, pipes, screen, stats, settings)


def check_keydown_events(bird: Bird, event: pg.event.Event,
                         settings: Settings):
    """Respond to keypresses"""

    # Quit the game
    if event.key == pg.K_q:
        sys.exit()

    # Flap / start the game
    elif event.key == pg.K_SPACE:

        # Start the game if inactive
        if settings.game_active is None:
            start_game(settings)

        if settings.flying:
            bird.flap()


def check_keyup_events(event: pg.event.Event):
    """Respond to key releases"""
    return


def update_world(pipes: Pipe, dt: int, screen: pg.Surface, settings: Settings):
    """Moves the pipes accross the screen and adds new pipes as necessary"""

    # Update the pipe locations and spawn new pipes as necessary
    pipes.update()

    # Add new pipes if traveled more than pipe spacing limit
    settings.travel_distance += settings.world_velocity
    if settings.travel_distance > settings.pipe_spacing:
        create_new_pipes(pipes, screen, settings)
        settings.travel_distance = 0


def draw(bird: Bird, pipes: pg.sprite.Group, buttons: Button,
         screen: pg.Surface, stats: Stats, settings: Settings):
    """Draw things to the window. Called once per frame."""

    screen.fill(settings.bg_color)

    # Draw the pipes to the screen
    pipe: Pipe
    for pipe in pipes:
        pipe.blitme()

    # Draw the bird to the screen
    bird.blitme()

    # Draw the score to the screen

    # Display the buttons if the game is inactive
    if settings.game_active == False:
        button: Button

        mouse_pos = pg.mouse.get_pos()
        for button in buttons:
            button.draw(mouse_pos)

    pg.display.flip()


def create_new_pipes(pipes: pg.sprite.Group, screen: pg.Surface,
                     settings: Settings):
    """Creates a new randomized pair of pipes and adds them to pipe sprite group"""

    gap_y = random.randint(settings.gap_y_min, settings.gap_y_max)
    top_pipe = Pipe(gap_y, "top", screen, settings)
    bot_pipe = Pipe(gap_y, "bottom", screen, settings)
    pipes.add(top_pipe)
    pipes.add(bot_pipe)


def check_score(bird: Bird, pipes: pg.sprite.Group, stats: Stats):
    """Checks if the bird has cleared a pair of pipes"""

    pipe: Pipe
    for pipe in pipes:
        if bird.rect.left > pipe.rect.right and pipe not in stats.pipes_cleared \
            and pipe.location == "top":

            stats.score += 1
            stats.pipes_cleared.add(pipe)
            stats.check_high_score()
            print(f"Score: {stats.score}, High: {stats.high_score}")


def check_collisions(bird: Bird, pipes: Pipe, settings: Settings):
    """Checks for collisions with the bird and the world. Sets flying to false 
    upon collision with world object. Sets the game to inactive once the bird has
    landed on the ground."""

    # Check for collisions with pipes and world
    collision: Pipe = pg.sprite.spritecollideany(bird, pipes)
    if collision or bird.rect.bottom > bird.screen_rect.bottom \
        or bird.rect.top < bird.screen_rect.top:

        # Collisions with pipes
        if collision:
            # Bird hit side of pipe, adjust so that bird is shifted to left of the pipe rect
            # If bird hits bottom or top of pipes but overhangs edge of pipe by less than some limit
            # the bird will still be shifted to left of pipe
            if bird.rect.right - collision.rect.left < bird.rect.width / 4:
                bird.rect.right = collision.rect.left

            # Bird hit bottom of top pipe
            elif bird.rect.top > collision.rect.bottom - bird.max_velocity:
                bird.rect.top = collision.rect.bottom

            # Bird hit top of bottom pipe
            elif bird.rect.bottom > collision.rect.top:
                bird.rect.bottom = collision.rect.top
                settings.game_active = False

        # Collision with ceiling
        if bird.rect.top < bird.screen_rect.top:
            bird.rect.top = bird.screen_rect.top

        # Collision with ground
        if bird.rect.bottom > bird.screen_rect.bottom:
            bird.rect.bottom = bird.screen_rect.bottom
            settings.game_active = False

        bird.x = bird.rect.centerx
        bird.y = bird.rect.centery
        bird.velocity = 0
        settings.flying = False


def reset_game(bird: Bird, pipes: pg.sprite.Group, screen: pg.Surface,
               stats: Stats, settings: Settings):
    """Reset all the game parameters"""

    settings.init_dynamic_variables()
    stats.init_dynamic_variables()
    bird.init_dynamic_variables()
    pipes.empty()
    create_new_pipes(pipes, screen, settings)
    # start_game(settings)


def start_game(settings: Settings):
    """Starts the game"""
    settings.game_active = True
    settings.flying = True


def clamp(value, min_val, max_val):
    """Clamps a value to a given range"""
    return max(min_val, min(max_val, value))