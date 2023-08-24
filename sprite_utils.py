from functools import lru_cache
import pygame

from pygame import Surface
from pygame.image import load
from pygame.sprite import Sprite


def load_sprite(name, with_alpha=True) -> Surface:
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


class SpriteSheet:
    def __init__(self, fileName):
        self.sheet = pygame.image.load(fileName)

    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        return image


STEP = 5


class Direction:
    LEFT = 0
    RIGHT = 1


class States:
    IDLE = 0
    WALK = 1
    DEAD = 2
    ATACK1 = 3
    ATACK2 = 4
    ATACK3 = 5
    SHOT1 = 6
    SHOT2 = 7


class SkeletonArcher(Sprite):
    def __init__(self, group: pygame.sprite.Group) -> None:
        super().__init__([group])

        self.WIDTH = 128
        self.HEIGHT = 128

        self.init_sprites()

    def init_sprites(self):
        attack1 = SpriteSheet('assets/sprites/archer/attack_1.png')
        self.attack1 = tuple(attack1.image_at((x*self.WIDTH, 0, self.WIDTH, self.HEIGHT))
                             for x in range(0, 5))

        attack2 = SpriteSheet('assets/sprites/archer/attack_2.png')
        self.attack2 = tuple(attack2.image_at((x*self.WIDTH, 0, self.WIDTH, self.HEIGHT))
                             for x in range(0, 4))

        attack3 = SpriteSheet('assets/sprites/archer/attack_3.png')
        self.attack3 = tuple(attack3.image_at((x*self.WIDTH, 0, self.WIDTH, self.HEIGHT))
                             for x in range(0, 3))

        dead = SpriteSheet('assets/sprites/archer/dead.png')
        self.dead = tuple(dead.image_at((x*self.WIDTH, 0, self.WIDTH, self.HEIGHT))
                          for x in range(0, 5))

        evasion = SpriteSheet('assets/sprites/archer/evasion.png')
        self.evasion = tuple(evasion.image_at((x*self.WIDTH, 0, self.WIDTH, self.HEIGHT))
                             for x in range(0, 6))

        hurt = SpriteSheet('assets/sprites/archer/hurt.png')
        self.hurt = tuple(hurt.image_at((x*self.WIDTH, 0, self.WIDTH, self.HEIGHT))
                          for x in range(0, 2))

        idle = SpriteSheet('assets/sprites/archer/idle.png')
        self.idle = tuple(idle.image_at((x*self.WIDTH, 0, self.WIDTH, self.HEIGHT))
                          for x in range(0, 7))

        walk = SpriteSheet('assets/sprites/archer/walk.png')
        self.walk = tuple(walk.image_at((x*self.WIDTH, 0, self.WIDTH, self.HEIGHT))
                          for x in range(0, 8))

        shot1 = SpriteSheet('assets/sprites/archer/shot_1.png')
        self.shot1 = tuple(shot1.image_at((x*self.WIDTH, 0, self.WIDTH, self.HEIGHT))
                           for x in range(0, 15))

        shot2 = SpriteSheet('assets/sprites/archer/shot_2.png')
        self.shot2 = tuple(shot2.image_at((x*self.WIDTH, 0, self.WIDTH, self.HEIGHT))
                           for x in range(0, 15))

        self.current_state = States.IDLE
        self.direction = Direction.RIGHT

        self.current_sprites = self.idle
        self.index = 0

        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.image = self.current_sprites[self.index]

    def _revert_sprites(self, sprites_collection):
        return [pygame.transform.flip(
                img, True, False) for img in sprites_collection]

    def _get_sprites(self, new_state):
        sprites = None
        if new_state == States.WALK:
            sprites = self.walk
        elif new_state == States.IDLE:
            sprites = self.idle

        if self.direction == Direction.LEFT:
            sprites = self._revert_sprites(sprites)

        return sprites

    def _change_state(self, new_state, new_direction):
        if new_state != self.current_state or self.direction != new_direction:
            self.direction = new_direction
            self.current_state = new_state
            self.current_sprites = self._get_sprites(new_state)
            self.index = 0

    def _handle_walk(self):
        if self.direction == Direction.LEFT:
            self.rect.x -= STEP
        elif self.direction == Direction.RIGHT:
            self.rect.x += STEP

    def update(self, *args, **kwargs):
        self._change_state(kwargs['state'], kwargs['direction'])
        if kwargs['state'] == States.WALK:
            self._handle_walk()

        print(
            f'update state: {self.current_state}, Img index: {self.index} rect: {self.rect}')
        self.index += 1
        # if the index is larger than the total images
        if self.index >= len(self.current_sprites):
            # we will make the index to 0 again
            self.index = 0
        self.image = self.current_sprites[self.index]
