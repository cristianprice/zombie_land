import pygame
from actors import SkeletonArcher, SkeletonSpearman


BACKGROUND_COLOR = pygame.Color('white')
FRAMERATE = 10


class ZombieLand:
    def __init__(self, window_size=(800, 600)):
        self._init_pygame()
        self.clock = pygame.time.Clock()

        self.flags = pygame.SCALED  # | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(window_size, self.flags)

        self.hero_group = pygame.sprite.Group()
        self.skelly_archer = SkeletonArcher()
        self.skelly_spearman = SkeletonSpearman((200, 0))

        self.hero_group.add(self.skelly_archer)
        self.hero_group.add(self.skelly_spearman)

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
        if keys[pygame.K_SPACE] and keys[pygame.K_RIGHT]:
            self.skelly_archer.right_walk()
            self.skelly_archer.attack()

            self.skelly_spearman.right_walk()
            self.skelly_spearman.attack()

        elif keys[pygame.K_SPACE] and keys[pygame.K_LEFT]:
            self.skelly_archer.left_walk()
            self.skelly_archer.attack()

            self.skelly_spearman.left_walk()
            self.skelly_spearman.attack()

        elif keys[pygame.K_RIGHT]:
            self.skelly_archer.right_walk()
            self.skelly_spearman.right_walk()

        if keys[pygame.K_LEFT]:
            self.skelly_archer.left_walk()
            self.skelly_spearman.left_walk()

        elif keys[pygame.K_SPACE]:
            self.skelly_archer.attack()
            self.skelly_spearman.attack()

        elif not any(keys):
            self.skelly_archer.idle()
            self.skelly_spearman.idle()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit()
            self._handle_keys_pressed(pygame.key.get_pressed())

    def _process_game_logic(self):
        self.skelly_archer.update()
        self.skelly_spearman.update()

    def _draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.hero_group.draw(self.screen)

        pygame.display.flip()
