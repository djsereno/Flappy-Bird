# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING

# Import standard modules
import math
from math import pi as PI

# Import non-standard modules
import pygame as pg
from pygame.sprite import Sprite

# Import local classes and methods
import helper_functions as hf

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
        self.color = 0  # 0 = Yellow, 1 = Red, 2 = Blue
        self.frames = settings.bird_frames
        self.image_orig = self.frames[self.color][0]
        self.image = self.image_orig.copy()
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.animation_speed = 75
        self.idle_period = 3000
        self.idle_amp = 50
        self.y_0 = self.screen_rect.centery

        # Sound effects
        self.sfx_flap = settings.sfx_flap
        self.sfx_hit = settings.sfx_hit
        self.sfx_fall = settings.sfx_fall
        self.sfx_pop = settings.sfx_pop

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
        self.sfx_flap.play()

    def change_color(self):
        """Changes the color of the bird by updating the reference to a new spritesheet and plays the sound effect"""
        
        self.color = (self.color + 1) % len(self.frames)
        self.sfx_pop.stop()
        self.sfx_pop.play()

    def update(self, dt: int, settings: Settings):
        """Update the bird's animation and location"""

        # Update the animation
        if settings.current_state != 'GAMEOVER':
            self.animation_time += dt
            if self.animation_time > self.animation_speed:
                self.animation_time = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames[0])
                self.image_orig = self.frames[self.color][self.current_frame]

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
                new_velocity = self.velocity + self.accel * dt
                self.velocity = hf.clamp(new_velocity, -self.max_velocity, self.max_velocity)
                self.y += self.velocity * dt

                # Rotate the bird based on previous jump elevation
                self.angle = hf.translate(self.y, self.prev_jump_elev, self.prev_jump_elev + 150, 20, -90)

        # Update the rect
        self.image = pg.transform.rotate(self.image_orig, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.mask = pg.mask.from_surface(self.image)

    def blitme(self):
        """Draw the bird at its current location"""
        
        self.screen.blit(self.image, self.rect)
