import os
import random
from functools import lru_cache
from typing import Any

import pygame
from pygame import Surface
from pygame.image import load
from pygame.sprite import Sprite
from time import time

HERO_STEP = 5
ARROW_SPEED = 50

DIRECTION_LEFT = 'left'
DIRECTION_RIGHT = 'right'

STATE_IDLE = 'idle'
STATE_WALK = 'walk'
STATE_ATTACK_1 = 'attack_1'
STATE_ATTACK_2 = 'attack_2'
STATE_ATTACK_3 = 'attack_3'
STATE_EVASION = 'evasion'

STATE_SHOT_1 = 'shot_1'
STATE_SHOT_2 = 'shot_2'

random.seed(time())


class SpriteSheet:
    def __init__(self, file_name):
        self.sheet = pygame.image.load(file_name)

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


class ActionActor(Actor):
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
            self._cycle_ended(self.state)
            self.index = 0

        self.image = self.sprites[self.direction][self.state][self.index]
        self._action()

    def _cycle_ended(self, current_state):
        pass

    def _action(self):
        if self.state == STATE_WALK and self.direction == DIRECTION_LEFT:
            self.rect.x -= HERO_STEP
        elif self.state == STATE_WALK and self.direction == DIRECTION_RIGHT:
            self.rect.x += HERO_STEP
        elif not self._is_in_uninterruptible_action():
            # Change of state but we are still in attacking animation.
            self.idle()

    def _is_in_uninterruptible_action(self):
        return self._is_attacking() or self._is_jumping()

    def _is_attacking(self):
        return self.state in self.attack_types() and self.index != 0

    def _is_jumping(self):
        return self.state == STATE_EVASION and self.index != 0

    def right_jump(self):
        if not self._is_in_uninterruptible_action():
            self.state = STATE_EVASION
            self.direction = DIRECTION_RIGHT

    def left_jump(self):
        if not self._is_in_uninterruptible_action():
            self.state = STATE_EVASION
            self.direction = DIRECTION_LEFT

    def left_walk(self):
        if not self._is_in_uninterruptible_action():
            self.state = STATE_WALK
            self.direction = DIRECTION_LEFT

    def right_walk(self):
        if not self._is_in_uninterruptible_action():
            self.state = STATE_WALK
            self.direction = DIRECTION_RIGHT

    def attack_types(self):
        return (STATE_ATTACK_1, STATE_ATTACK_2, STATE_ATTACK_3)

    def attack(self):
        if not self._is_in_uninterruptible_action():
            self.state = random.choice(self.attack_types())
            self.attacking = self.state

    def idle(self):
        if not self._is_in_uninterruptible_action():
            self.state = STATE_IDLE


class SkeletonArcher(ActionActor):

    def __init__(self, projectile_group, pos=(0, 0)) -> None:
        super().__init__('assets/sprites/archer')
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.projectile_group = projectile_group

    def attack_types(self):
        return (STATE_SHOT_1, STATE_SHOT_2)

    def _cycle_ended(self, current_state):
        if current_state in self.attack_types():
            self._create_projectile(current_state)

    def _create_projectile(self, crouch):
        # We create the arrow
        arrow = Arrow('assets/sprites/archer/arrow.png', ARROW_SPEED)
        if self.direction == DIRECTION_LEFT:
            arrow.fire_left()
        elif self.direction == DIRECTION_RIGHT:
            arrow.fire_right()

        correction_x = 28
        correction_y = 7

        ax = 0
        ay = 0

        if crouch:
            if arrow.direction == DIRECTION_LEFT:
                ax = self.rect.x + correction_x
                ay = self.rect.height/2 - correction_y
            elif arrow.direction == DIRECTION_RIGHT:
                ax = self.rect.x + self.rect.width/2 - correction_x
                ay = self.rect.height/2 - correction_y
        else:
            if arrow.direction == DIRECTION_LEFT:
                ax = self.rect.x + correction_x
                ay = self.rect.height/2 + correction_y
            elif arrow.direction == DIRECTION_RIGHT:
                ax = self.rect.x + self.rect.width/2 - correction_x
                ay = self.rect.height/2 + correction_y

        arrow.set_position(ax, ay)
        self.projectile_group.add(arrow)


class SkeletonSpearman(ActionActor):

    def __init__(self, pos=(0, 0)) -> None:
        super().__init__('assets/sprites/spearman')
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def attack_types(self):
        return (STATE_ATTACK_1, STATE_ATTACK_2)

    def right_jump(self):
        pass

    def left_jump(self):
        pass
