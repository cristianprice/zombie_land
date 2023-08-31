import os
import random
from time import time
from typing import Any

import pygame
from pygame import Surface
from pygame.image import load
from pygame.sprite import Sprite

from game_constants import *
from sprites import get_name_from_file, SpriteSheet, _revert_sprites, _get_sprites, SpriteSequence

random.seed(time())


class StaticObject(Sprite):

    def __init__(self, file_name, speed) -> None:
        super().__init__(*[])

        sheet = SpriteSheet(file_name)
        self.rect = sheet.sheet.get_rect()

        self.right_image = sheet.image_at(self.rect)
        self.left_image = _revert_sprites([self.right_image])[0]

        self.image = self.right_image
        self.direction = DIRECTION_RIGHT
        self.speed = speed

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def position(self):
        return self.rect.x, self.rect.y

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.direction == DIRECTION_RIGHT:
            self.rect.x += self.speed
        elif self.direction == DIRECTION_LEFT:
            self.rect.x -= self.speed


class Arrow(StaticObject):
    def __init__(self, file_name, speed) -> None:
        super().__init__(file_name, speed)

    def fire_left(self):
        self.direction = DIRECTION_LEFT
        self.image = self.left_image

    def fire_right(self):
        self.direction = DIRECTION_RIGHT
        self.image = self.right_image

    def it_hit(self, actor):
        return self.rect.colliderect(actor.rect)


class Actor(Sprite):
    def __init__(self, asset_dir, width, height) -> None:
        super().__init__(*[])
        self._init_sprites(asset_dir, width, height)

    def _init_sprites(self, asset_dir, width, height):
        images = [file for file in os.listdir(
            asset_dir) if file.endswith(".png")]

        self.sequences = dict()
        self.sequences[DIRECTION_LEFT] = dict()
        self.sequences[DIRECTION_RIGHT] = dict()

        for img in images:
            can_be_interrupted = ('attack' not in img) and ('shot' not in img)
            self.sequences[DIRECTION_RIGHT][get_name_from_file(img)] = SpriteSequence(
                f'{asset_dir}/{img}', width, height, can_be_interrupted)
            self.sequences[DIRECTION_LEFT][get_name_from_file(img)] = SpriteSequence(
                f'{asset_dir}/{img}', width, height, can_be_interrupted, True)


class NewActor(Actor):
    def __init__(self, asset_dir, width, height, pos=(0, 0)) -> None:
        super().__init__(asset_dir, width, height)

        self.state = STATE_IDLE
        self.direction = DIRECTION_RIGHT
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.state_sequence = self.sequences[self.direction][self.state]

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.state_sequence.done():
            return

        self.image = self.state_sequence.next()

    def _same_action_not_done(self, state):
        return self.state == state and not self.state_sequence.done()

    def idle(self):
        if not self._same_action_not_done(STATE_IDLE):
            self.state = STATE_IDLE
            self.state_sequence = self.sequences[self.direction][self.state].reset(
            )

    def move_right(self):
        direction = DIRECTION_RIGHT
        step = HERO_STEP
        return self._move(direction, step)

    def move_left(self):
        direction = DIRECTION_LEFT
        step = -HERO_STEP
        return self._move(direction, step)

    def _move(self, direction, step):
        if not self.state_sequence.interruptible():
            return
        if self.direction == direction and self._same_action_not_done(STATE_WALK):
            self.move(step, 0)
            return
        else:
            self.direction = direction
            self.state = STATE_WALK
            self.state_sequence = self.sequences[self.direction][self.state].reset(
            )
            self.move(step, 0)
            return

    def move(self, x, y):
        self.rect.move_ip(x, y)
        return self
