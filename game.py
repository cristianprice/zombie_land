import pygame
from actors import SkeletonArcher, SkeletonSpearman


BACKGROUND_COLOR = pygame.Color('white')
FRAMERATE = 20


class ZombieLand:
    def __init__(self, window_size=(800, 600)):
        self._init_pygame()
        self.clock = pygame.time.Clock()

        self.flags = pygame.SCALED  # | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(window_size, self.flags)

        self.hero_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()

        self.skelly_archer = SkeletonArcher(self.projectile_group)
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
            for hero in self.hero_group:
                hero.right_walk()
                hero.attack()

        elif keys[pygame.K_SPACE] and keys[pygame.K_LEFT]:
            for hero in self.hero_group:
                hero.left_walk()
                hero.attack()

        elif keys[pygame.K_RIGHT]:
            for hero in self.hero_group:
                hero.right_walk()

        if keys[pygame.K_LEFT]:
            for hero in self.hero_group:
                hero.left_walk()

        elif keys[pygame.K_SPACE]:
            for hero in self.hero_group:
                hero.attack()

        elif not any(keys):
            for hero in self.hero_group:
                hero.idle()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit()
            self._handle_keys_pressed(pygame.key.get_pressed())

    def _process_projectiles(self):
        to_be_deleted = []

        for proj in self.projectile_group:
            if proj.position()[0] > (pygame.display.get_window_size()[0] + proj.rect.width):
                to_be_deleted.append(proj)
            proj.update()

        if len(to_be_deleted) > 0:
            for p in to_be_deleted:
                print('Removing projectile.')
                self.projectile_group.remove(p)

    def _process_game_logic(self):
        self.skelly_archer.update()
        self.skelly_spearman.update()

        self._process_projectiles()

    def _draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.hero_group.draw(self.screen)
        self.projectile_group.draw(self.screen)

        pygame.display.flip()
