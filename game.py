import logging as log
import random

import pygame

from actors import SkeletonHero, Zombie
from game_constants import *

log.basicConfig(level=log.DEBUG)


class ZombieLand:
    def __init__(self, window_size=(WIDTH, HEIGHT)):
        self._init_pygame()
        self.clock = pygame.time.Clock()

        self.flags = pygame.SCALED  # | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(window_size, self.flags)

        self.hero_group = self._create_group('hero')
        self.projectile_group = self._create_group('projectile')
        self.zombie_group = self._create_group('zombie')

        for _ in range(0, 3):
            self._create_zombie()

        self.background = pygame.transform.scale(pygame.image.load(
            'assets/sprites/game_background.png'), (WIDTH, HEIGHT))

        self.hero_group.add(SkeletonHero(self.projectile_group))

        self.groups = [self.hero_group,
                       self.zombie_group,
                       self.projectile_group]

    def _create_zombie(self):
        self.zombie_group.add(Zombie(self.hero_group, ZOMBIE_STEP))

    def _create_group(self, name):
        g = pygame.sprite.Group()
        setattr(g, 'name', name)
        return g

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

        make_zombie = keys[pygame.K_c]
        clear_dead_zombies = keys[pygame.K_k]

        for hero in self.hero_group:
            if make_zombie:
                log.debug('Creating a zombie.')
                self._create_zombie()
            elif clear_dead_zombies:
                log.debug('Clearing dead zombies.')
                self._clear_zombies()
            elif shoot:
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

    def _clear_zombies(self):
        for z in self.zombie_group:
            if z.is_dead():
                z.kill()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit()

        keys_pressed = pygame.key.get_pressed()
        self._handle_keys_pressed(keys_pressed)

    def _process_game_logic(self):

        self._zombie_projectile_logic(self.zombie_group, self.projectile_group)
        for group in self.groups:
            group.update()

    def _zombie_projectile_logic(self, zombie_group, projectile_group):
        # remove outside projectiles
        screen_rect = pygame.display.get_surface().get_rect()
        for projectile in projectile_group:
            if not projectile.rect in screen_rect:
                projectile.kill()

        for projectile in projectile_group:
            for zombie in [z for z in zombie_group if not z.is_dead()]:
                if projectile.rect.colliderect(zombie.rect):
                    zombie.hit()
                    projectile.kill()

    def _draw(self):
        self.screen.blit(self.background, self.background.get_rect())
        for g in self.groups:
            g.draw(self.screen)

        self.projectile_group.draw(self.screen)
        pygame.display.flip()
