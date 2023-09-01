import logging as log
import os
import random
from time import time
from typing import Any

import pygame
from pygame import Surface
from pygame.sprite import Sprite

from game_constants import *
from sprites import (SpriteSequence, SpriteSheet, revert_sprites,
                     get_name_from_file)

random.seed(time())
log.basicConfig(level=log.DEBUG)


class StaticObject(Sprite):

    def __init__(self, file_name, speed) -> None:
        super().__init__(*[])

        sheet = SpriteSheet(file_name)
        self.rect = sheet.sheet.get_rect()

        self.right_image = sheet.image_at(self.rect)
        self.left_image = revert_sprites([self.right_image])[0]

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

        x = pygame.display.get_surface().get_rect().width + self.rect.width + self.speed
        if self.rect.x > x:
            log.debug(f'Killing arrow on {x}')
            self.kill()


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
    def __init__(self, asset_dir, width, height, pos=(0, 0), step=HERO_STEP) -> None:
        super().__init__(asset_dir, width, height)

        self.step = step
        self.state = STATE_IDLE
        self.direction = DIRECTION_RIGHT
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.state_sequence = self.sequences[self.direction][self.state]

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.state_sequence.done():
            log.debug(f'Action {self.state} is done.')
            self._action_done()
            return

        self.image = self.state_sequence.next()
        if self.state_sequence.done():
            self._action_done()

    def _same_action_and_done(self, state):
        return self.state == state and self.state_sequence.done()

    def _can_interrupt(self):
        log.debug(
            f'Current state: {self.state} Interruptible: {self.state_sequence.interruptible()} Is it done: {self.state_sequence.done()}')
        if not self.state_sequence.interruptible() and self.state_sequence.done():
            return True
        elif self.state_sequence.interruptible():
            return True
        else:
            return False

    def _action_done(self):
        pass

    def idle(self):
        if not self._can_interrupt():
            log.warn(
                f'Cannot idle current action cannot be interrupted {self.state}')
            return

        if self.state != STATE_IDLE:
            self.state = STATE_IDLE
            self.state_sequence = self.sequences[self.direction][self.state]
            self.state_sequence.reset()
        elif self._same_action_and_done(STATE_IDLE):
            self.state_sequence.reset()

    def move_right(self):
        if not self._can_interrupt():
            return

        direction = DIRECTION_RIGHT
        self.state = STATE_WALK
        self.state_sequence = self.sequences[self.direction][self.state]
        return self._move(direction, self.step)

    def move_left(self):
        if not self._can_interrupt():
            return

        direction = DIRECTION_LEFT
        self.state = STATE_WALK
        self.state_sequence = self.sequences[self.direction][self.state]
        return self._move(direction, -self.step)

    def _move(self, direction, step):
        log.debug(f'Direction {direction}, X: {self.rect.x + step}')

        if self.direction != direction:
            log.debug(
                f'{self.__class__.__name__} Direction changed. Old:{self.direction}, New: {direction}')
            self.state = STATE_WALK
            self.direction = direction
            self.state_sequence.reset()
        elif self._same_action_and_done(STATE_WALK):
            self.state_sequence.reset()

        self.move(step, 0)

    def move(self, x, y):
        self.rect.move_ip(x, y)
        return self


class SkeletonHero(NewActor):
    def __init__(self, projectile_group) -> None:
        super().__init__('assets/sprites/archer',
                         HERO_SIZE_W, HERO_SIZE_H, (0, HERO_Y_POSITION))
        self._projectile_group = projectile_group

    def _create_arrow(self):
        arrow = Arrow('assets/sprites/archer/arrow.png', ARROW_SPEED)
        arrow.set_position(self.rect.x, self.rect.y + self.rect.height/2 - 10)
        if self.direction == DIRECTION_LEFT:
            arrow.fire_left()
        elif self.direction == DIRECTION_RIGHT:
            arrow.fire_right()

        return arrow

    def shoot(self):
        if not self._can_interrupt():
            return

        self.state = STATE_SHOT_1
        self.state_sequence = self.sequences[self.direction][self.state]
        self.state_sequence.reset()

    def _action_done(self):
        if self.state in (STATE_SHOT_1, STATE_SHOT_2):
            arrow = self._create_arrow()
            self._projectile_group.add(arrow)


ZOMBIE_DIRS = ('assets/sprites/wild_zombie',
               'assets/sprites/zombie_man', 'assets/sprites/zombie_woman')


class Zombie(NewActor):
    INDEX = 0

    def __init__(self) -> None:
        super().__init__(ZOMBIE_DIRS[Zombie.INDEX % len(ZOMBIE_DIRS)],
                         ZOMBIE_SIZE_W, ZOMBIE_SIZE_H, (random.randint(400, 500),
                                                        HERO_Y_POSITION + (HERO_SIZE_H-ZOMBIE_SIZE_H)), 1)
        Zombie.INDEX += 1
