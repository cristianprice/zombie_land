import logging as log
import random

import pygame

from actors import SkeletonHero, Zombie
from game_constants import FRAMERATE, HEIGHT, WIDTH

log.basicConfig(level=log.DEBUG)


class ZombieLand:
    def __init__(self, window_size=(WIDTH, HEIGHT)):
        self._init_pygame()
        self.clock = pygame.time.Clock()

        self.flags = pygame.SCALED  # | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(window_size, self.flags)

        self.hero_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()

        self.zombie_group = pygame.sprite.Group()
        for _ in range(0, 10):
            self.zombie_group.add(Zombie())

        self.background = pygame.transform.scale(pygame.image.load(
            'assets/sprites/game_background.png'), (WIDTH, HEIGHT))

        self.hero_group.add(SkeletonHero(self.projectile_group))

        self.groups = [self.hero_group,
                       self.zombie_group, self.projectile_group]

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()
            self.clock.tick(FRAMERATE)

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Zombie Land")

    def _handle_keys_pressed(self, keys):
        right = keys[pygame.K_RIGHT]
        left = keys[pygame.K_LEFT]
        shoot = keys[pygame.K_SPACE]

        for hero in self.hero_group:
            if shoot:
                log.debug(f'Shoot: {shoot}')
                hero.shoot()
            elif right:
                log.debug(f'Right: {right}')
                hero.move_right()
            elif left:
                log.debug(f'Left: {left}')
                hero.move_left()
            else:
                hero.idle()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit()

        keys_pressed = pygame.key.get_pressed()
        self._handle_keys_pressed(keys_pressed)

    def _process_game_logic(self):
        for group in self.groups:
            for actor in group:
                if isinstance(actor, Zombie):
                    action = random.choice([actor.move_left])
                    action()

                actor.update()

    def _draw(self):
        self.screen.blit(self.background, self.background.get_rect())
        for g in self.groups:
            g.draw(self.screen)

        self.projectile_group.draw(self.screen)
        pygame.display.flip()
