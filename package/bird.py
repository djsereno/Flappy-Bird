# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING, List

# Import standard modules
import math
from math import pi as PI

# Import non-standard modules
import pygame as pg
from pygame.sprite import Sprite

# Import local classes and methods
import game_functions as gf

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    from settings import Settings


class Bird(Sprite):
    """A class for the bird"""

    def __init__(self, screen: pg.Surface, settings: Settings):
        """Initialize the bird's settings"""

        super(Bird, self).__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Physics parameters
        self.accel = settings.gravity
        self.max_velocity = settings.max_velocity
        self.jump_velocity = settings.jump_velocity

        # Image
        self.frames = settings.bird_frames
        self.image_orig = self.frames[0]
        self.image = self.image_orig.copy()
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.animation_speed = 75
        self.idle_period = 3000
        self.idle_amp = 50
        self.y_0 = self.screen_rect.centery

        self.init_dynamic_variables()

    def init_dynamic_variables(self):
        """Initializes the birds's dynamic variables"""

        # Positioning
        self.x = 150
        self.y = self.y_0
        self.rect.center = (self.x, self.y)
        self.velocity = 0
        self.angle = 0
        self.prev_jump_elev = 0
        self.current_frame = 0
        self.animation_time = 0
        self.idle_time = 0

    def flap(self):
        """Jump the bird"""

        # Update the bird's velocity
        self.velocity = -self.jump_velocity
        self.prev_jump_elev = self.y

    def update(self, dt: int, settings: Settings):
        """Update the bird"""

        # Update the animation
        if settings.current_state != 'GAMEOVER':
            self.animation_time += dt
            if self.animation_time > self.animation_speed:
                self.animation_time = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image_orig = self.frames[self.current_frame]

        # At beginning of game, bird animates smoothly up and down
        if settings.current_state in ['SPLASH', 'READY']:
            self.idle_time = (self.idle_time + dt) % self.idle_period
            theta = self.idle_time / self.idle_period * 2 * PI
            self.y = self.y_0 + self.idle_amp * math.sin(theta)
            self.angle = -45 * math.cos(theta)

        # During PLAY state, bird is affected by gravity and rotates based on flaps
        elif settings.current_state in ['PLAY', 'GAMEOVER']:

            # Update the bird's velocity and position
            if self.y < settings.ground_elev:
                new_velocity = self.velocity + self.accel
                self.velocity = gf.clamp(new_velocity, -self.max_velocity, self.max_velocity)
                self.y += self.velocity

                # Rotate the bird based on previous jump elevation
                self.angle = gf.translate(self.y, self.prev_jump_elev, self.prev_jump_elev + 150, 20, -90)

        # Update the rect
        self.image = pg.transform.rotate(self.image_orig, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.mask = pg.mask.from_surface(self.image)

    def blitme(self):
        """Draw the bird at its current location"""
        # pg.draw.lines(self.image, (255, 0, 255), True, self.mask.outline())
        # temp_rect = self.mask.get_bounding_rects()[0]
        # temp_rect.x += self.rect.x
        # temp_rect.y += self.rect.y
        # temp_rect.center = (self.x, self.y)
        # pg.draw.rect(self.screen, (0, 0, 0), temp_rect)

        self.screen.blit(self.image, self.rect)

        # [x, y] = self.mask.centroid()
        # x += self.rect.x
        # y += self.rect.y
        # pg.draw.circle(self.screen, (255, 0, 255), [x, y], 3)
