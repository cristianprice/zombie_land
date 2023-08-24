from functools import lru_cache
from typing import Any
import pygame

from pygame import Surface
from pygame.image import load
from pygame.sprite import Sprite
import os


STEP = 5

DIRECTION_LEFT = 'left'
DIRECTION_RIGHT = 'right'

STATE_IDLE = 'idle'
STATE_WALK = 'walk'


class SpriteSheet:
    def __init__(self, fileName):
        self.sheet = pygame.image.load(fileName)

    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        return image

    def size(self):
        return self.sheet.get_width(), self.sheet.get_height()


def _get_name_from_file(file_name):
    idx = file_name.index('.')
    return file_name[0:idx]


def _get_sprites(file_name, width, height):
    sprites = []
    sheet = SpriteSheet(file_name)
    sheet_w, sheet_h = sheet.size()

    # For images smaller
    if sheet_w < width and sheet_h < height:
        sprites.append(sheet.image_at((0, 0, sheet_w, sheet_h)))
    else:
        w_count = int(sheet_w/width)
        h_count = int(sheet_h/height)

        for w in range(0, w_count):
            for h in range(0, h_count):
                sprites.append(sheet.image_at(
                    (w*width, h*height, width, height)))

    return sprites


def _revert_sprites(sprites_collection):
    return [pygame.transform.flip(
            img, True, False) for img in sprites_collection]


class Actor(Sprite):
    def __init__(self, asset_dir, width, height) -> None:
        super().__init__(*[])
        self._init_sprites(asset_dir, width, height)

    def _init_sprites(self, asset_dir, width, height):
        images = [file for file in os.listdir(
            asset_dir) if file.endswith(".png")]

        self.sprites = dict()
        self.sprites[DIRECTION_LEFT] = dict()
        self.sprites[DIRECTION_RIGHT] = dict()

        for img in images:
            self.sprites[DIRECTION_RIGHT][_get_name_from_file(img)] = _get_sprites(
                f'{asset_dir}/{img}', width, height)

        for img in images:
            self.sprites[DIRECTION_LEFT][_get_name_from_file(img)] = _revert_sprites(
                self.sprites[DIRECTION_RIGHT][_get_name_from_file(img)])


class Skeleton(Actor):
    WIDTH = 128
    HEIGHT = 128

    def __init__(self,  asset_dir) -> None:
        super().__init__(asset_dir, self.WIDTH, self.HEIGHT)

        self.index = 0
        self.state = STATE_IDLE
        self.direction = DIRECTION_RIGHT
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.image = self.sprites[self.direction][self.state][self.index]

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.index += 1
        # if the index is larger than the total images
        if self.index >= len(self.sprites[self.direction][self.state]):
            # we will make the index to 0 again
            self.index = 0
        self.image = self.sprites[self.direction][self.state][self.index]
        self._advance()

    def _advance(self):
        if self.state == STATE_WALK and self.direction == DIRECTION_LEFT:
            self.rect.x -= STEP
        elif self.state == STATE_WALK and self.direction == DIRECTION_RIGHT:
            self.rect.x += STEP

    def left_walk(self):
        self.state = STATE_WALK
        self.direction = DIRECTION_LEFT

    def right_walk(self):
        self.state = STATE_WALK
        self.direction = DIRECTION_RIGHT

    def idle(self):
        self.state = STATE_IDLE
