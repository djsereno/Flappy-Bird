# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING, List

# Import standard modules
import sys
import random

# Import non-standard modules
import pygame as pg

# Import local classes and methods
from pipe import Pipe
import helper_functions as hf

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    from bird import Bird
    from settings import Settings
    from button import Button
    from stats import Stats
    from splash import Splash
    from scroll_element import ScrollElem


def check_events(bird: Bird, pipes: pg.sprite.Group, background: ScrollElem, buttons: Button, screen: pg.Surface,
                 stats: Stats, settings: Settings):
    """Check for key events"""

    # Go through events that are passed to the script by the window.
    for event in pg.event.get():

        # Check if user quits
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        # Check if user clicks
        elif event.type == pg.KEYDOWN:
            check_keydown_events(bird, pipes, event, screen, settings)

        elif event.type == pg.KEYUP:
            check_keyup_events(event)

        elif event.type == pg.MOUSEBUTTONDOWN:
            check_click_events(buttons, bird, pipes, background, screen, stats, settings)


def check_click_events(buttons: pg.sprite.Group, bird: Bird, pipes: pg.sprite.Group, background: ScrollElem,
                       screen: pg.Surface, stats: Stats, settings: Settings):
    """Respond to mouse clicks"""

    left, middle, right = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()

    if settings.current_state in ['SPLASH', 'READY']:

        # Start the game if in READY mode
        if left and settings.current_state == 'READY':
            start_game(pipes, screen, settings)

        # Change bird color
        elif right:
            bird.change_color()

        # Change background night/day and pipe color
        elif middle:
            change_world_scene(background, settings)

    if settings.current_state == 'PLAY' and left:
        bird.flap()

    else:
        # Check for clicked buttons
        button: Button
        for button in buttons:
            if button.rect.collidepoint(mouse_pos) and left:

                # New Game button clicked
                if settings.current_state == 'GAMEOVER' and button.action == 'new_game' and button.active:
                    reset_game(bird, pipes, buttons, stats, settings)


def check_keydown_events(bird: Bird, pipes: pg.sprite.Group, event: pg.event.Event, screen: pg.Surface,
                         settings: Settings):
    """Respond to key presses"""

    # Quit the game
    if event.key == pg.K_q:
        sys.exit()

    # Flap / start the game
    elif event.key == pg.K_SPACE:

        # Start the game if in READY mode
        if settings.current_state == 'READY':
            start_game(pipes, screen, settings)

        if settings.current_state == 'PLAY':
            bird.flap()


def check_keyup_events(event: pg.event.Event):
    """Respond to key releases"""
    return


def update_world(pipes: Pipe, background: ScrollElem, ground: ScrollElem, dt: int, screen: pg.Surface,
                 settings: Settings):
    """Moves the pipes and background across the screen and adds new pipes as necessary"""

    if settings.current_state != 'GAMEOVER':

        # Update background and ground images
        background.update(dt)
        ground.update(dt)

        # Update the pipe locations and spawn new pipes as necessary
        if settings.current_state == 'PLAY':

            if settings.start_delay < settings.max_start_delay:
                settings.start_delay += dt

            else:
                pipes.update(dt)

                # Add new pipes if traveled more than pipe spacing limit
                settings.travel_distance += settings.world_velocity * dt
                if settings.travel_distance > settings.pipe_spacing:
                    create_new_pipes(pipes, screen, settings)
                    settings.travel_distance = 0


def draw(dt: int, bird: Bird, pipes: pg.sprite.Group, background: ScrollElem, ground: ScrollElem, buttons: Button,
         screen: pg.Surface, stats: Stats, settings: Settings, splash: Splash):
    """Draw to the window"""

    screen.fill(settings.bg_color)
    background.blitme()
    pipes.draw(screen)
    ground.blitme()
    bird.blitme()

    # Draw the splash screen
    if settings.current_state == 'SPLASH':

        # Fade in and show splash screen
        screen.blit(settings.dimmer, settings.dimmer_rect)
        hf.fade_surface(settings.dimmer, 0, -3)
        splash.blitme()

    # Display the Get Ready image:
    elif settings.current_state == 'READY':

        if settings.idle_time < settings.get_ready_delay:
            settings.idle_time += dt

        else:
            screen.blit(settings.get_ready_img, settings.get_ready_rect)
            screen.blit(settings.idle_msg_img, settings.idle_msg_rect)
            hf.fade_surface(settings.get_ready_img, 255, 20)
            hf.fade_surface(settings.idle_msg_img, 255, 20)

    # Draw the score to the screen
    elif settings.current_state == 'PLAY':
        stats.blit_current_score()

    # Display the buttons if the game is inactive
    elif settings.current_state == 'GAMEOVER':

        # Dim background content and show score plaque
        screen.blit(settings.dimmer, settings.dimmer_rect)
        stats.blit_score_plaque(dt, screen)
        fade_out_done = hf.fade_surface(settings.dimmer, settings.dimmer_max_opacity, 3)

        # Display buttons after stats and dimmer are done animating
        if fade_out_done and not stats.animating:

            # Fade in 'Game Over' image
            screen.blit(settings.game_over_img, settings.game_over_rect)
            hf.fade_surface(settings.game_over_img, 255, 5)

            # Fade in buttons and activate button once done fading in
            button: Button
            mouse_pos = pg.mouse.get_pos()
            for button in buttons:
                button.draw(mouse_pos)
                button_done = hf.fade_surface(button.image, 255, 5)
                if button_done:
                    button.active = True

    pg.display.flip()


def change_world_scene(background: ScrollElem, settings: Settings):
    """Updates the background and pipe colors"""

    # Update the pipe images
    settings.pipe_color = (settings.pipe_color + 1) % len(settings.pipe_imgs[0])

    # Update the background images
    background.change_scene()

    # Play sound effects
    settings.sfx_swoosh.stop()
    settings.sfx_swoosh.play()


def check_collisions(bird: Bird, pipes: Pipe, stats: Stats, settings: Settings):
    """Checks for collisions with the bird and the world. Updates the game state 
    upon collision with world object."""

    # Check for collisions with pipes/world
    collision: Pipe = pg.sprite.spritecollideany(bird, pipes, pg.sprite.collide_mask)
    if collision or bird.rect.bottom > settings.ground_elev \
        or bird.rect.top < bird.screen_rect.top:

        settings.sfx_music.stop()
        settings.sfx_music_end.play()
        bird.sfx_hit.play()

        # Fall sound effect not played if hitting the ground directly
        if not bird.rect.bottom > settings.ground_elev:
            bird.sfx_fall.play()

        bird.x = bird.rect.centerx
        bird.y = bird.rect.centery
        bird.velocity = 0
        stats.prep_score_plaque()
        settings.current_state = 'GAMEOVER'


def check_score(bird: Bird, pipes: pg.sprite.Group, stats: Stats):
    """Checks if the bird has cleared a pair of pipes"""

    pipe: Pipe
    for pipe in pipes:
        if bird.rect.left > pipe.rect.right and pipe not in stats.pipes_cleared \
            and pipe.location == 0:

            stats.pipes_cleared.add(pipe)
            stats.increase_score()


def create_new_pipes(pipes: pg.sprite.Group, screen: pg.Surface, settings: Settings):
    """Creates a new randomized pair of pipes and adds them to pipe sprite group"""

    gap_y = random.randint(settings.gap_y_min, settings.gap_y_max)
    bot_pipe = Pipe(gap_y, 0, screen, settings)
    top_pipe = Pipe(gap_y, 1, screen, settings)
    pipes.add(bot_pipe)
    pipes.add(top_pipe)


def start_game(pipes: pg.sprite.Group, screen: pg.Surface, settings: Settings):
    """Starts the game and creates the initial set of pipes"""

    settings.current_state = 'PLAY'
    create_new_pipes(pipes, screen, settings)


def reset_game(bird: Bird, pipes: pg.sprite.Group, buttons: pg.sprite.Group, stats: Stats, settings: Settings):
    """Reset all the game parameters to their initial values"""

    settings.sfx_swoosh.play()
    settings.init_dynamic_variables()
    stats.init_dynamic_variables()
    bird.init_dynamic_variables()
    pipes.empty()

    button: Button
    for button in buttons:
        button.init_dynamic_variables()