# Allow for type hinting while preventing circular imports
from __future__ import annotations
from typing import TYPE_CHECKING, List

# Import standard modules
import os

# Import non-standard modules
import pygame as pg

# Import local classes and methods

# Import local class and methods that are only used for type hinting
if TYPE_CHECKING:
    pass


def clamp(value, min_val, max_val):
    """Clamps a value to a given range"""

    return max(min_val, min(max_val, value))


def fade_surface(surface: pg.Surface, end_alpha: int, alpha_inc: int):
    """Updates a surface's alpha value by alpha_inc. Returns True if fade is complete."""

    alpha = surface.get_alpha()
    if (alpha_inc > 0 and alpha < end_alpha) or (alpha_inc < 0 and alpha > end_alpha):
        alpha += alpha_inc
        surface.set_alpha(alpha)
        return False
    return True


def load_frames(sheet: pg.Surface, n_frames: int, color_key: pg.Color) -> List[pg.Surface]:
    """Returns a list of frames from a sprite sheet of size (width, height)."""

    images = []
    width, height = sheet.get_width() / n_frames, sheet.get_height()
    for i in range(n_frames):
        image = pg.Surface((width, height))
        image.blit(sheet, (0, 0), (i * width, 0, width, height))
        image.convert_alpha()
        image.set_colorkey(color_key)
        images.append(image)
    return images


def load_image(file_name: str, scale: float, path: str, color_key: pg.Color = None):
    """Loads an image (file_name) saved at path, scales by a given scale factor, and returns the resulting image.
    An RGB color key may be included."""

    full_path = os.path.abspath(os.path.join(path, file_name))
    image: pg.Surface = pg.image.load(full_path)
    image = scale_image(image, scale, color_key)
    return image


def load_sound(file_name: str, path: str, group: List[pg.mixer.Sound] = -1):
    """Loads a sound (file_name) saved at path and returns the resulting sound. If a group has been included, the sound will be added to that group."""

    full_path = os.path.abspath(os.path.join(path, file_name))
    sound = pg.mixer.Sound(full_path)

    if group != -1:
        group.append(sound)

    return sound


def scale_image(image: pg.Surface, scale: float, color_key: pg.Color = None):
    """Scales an image by a given scale factor, and returns the resulting image.
    An RGB color key may be included."""

    width, height = image.get_rect().size
    image = pg.transform.scale(image, (width * scale, height * scale)).convert_alpha()
    if color_key:
        image.set_colorkey(color_key)
    return image


def update_volume(sounds: List[pg.mixer.Sound], volume: float):
    """Sets the volume for all elements in a given sound bank"""

    volume = clamp(volume, 0.0, 1.0)
    for sound in sounds:
        sound.set_volume(volume)


def translate(val, in_min, in_max, out_min, out_max):
    """Translates or maps a value from one range [in_min, in_max] to a resulting
    output range [out_min, out_max]"""

    input_range = in_max - in_min
    output_range = out_max - out_min
    capped_val = min(max(val, in_min), in_max)
    return (capped_val - in_min) / input_range * output_range + out_min