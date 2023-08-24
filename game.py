import pygame
from actors import SkeletonArcher, SkeletonSpearman


BACKGROUND_COLOR = pygame.Color('white')
FRAMERATE = 20
WIDTH = 800
HEIGHT = 600


class ZombieLand:
    def __init__(self, window_size=(WIDTH, HEIGHT)):
        self._init_pygame()
        self.clock = pygame.time.Clock()

        self.flags = pygame.SCALED  # | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(window_size, self.flags)

        self.hero_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()
        self.zombie_group = pygame.sprite.Group()

        self.background = pygame.transform.scale(pygame.image.load(
            'assets/sprites/game_background.png'), (WIDTH, HEIGHT))

        self.skelly_archer = SkeletonArcher(self.projectile_group, (0, 200))
        # self.skelly_spearman = SkeletonSpearman((200, 0))

        self.hero_group.add(self.skelly_archer)
        # self.hero_group.add(self.skelly_spearman)

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
            return

        if keys[pygame.K_SPACE] and keys[pygame.K_LEFT]:
            for hero in self.hero_group:
                hero.left_walk()
                hero.attack()
            return

        if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            for hero in self.hero_group:
                hero.left_jump()
            return

        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            for hero in self.hero_group:
                hero.right_jump()
            return

        if keys[pygame.K_SPACE] and keys[pygame.K_DOWN]:
            for hero in self.hero_group:
                hero.low_attack()
            return

        if keys[pygame.K_SPACE] and keys[pygame.K_DOWN]:
            for hero in self.hero_group:
                hero.low_attack()
            return

        if keys[pygame.K_RIGHT]:
            for hero in self.hero_group:
                hero.right_walk()
            return

        if keys[pygame.K_LEFT]:
            for hero in self.hero_group:
                hero.left_walk()
            return

        if keys[pygame.K_SPACE]:
            for hero in self.hero_group:
                hero.attack()
            return

        for hero in self.hero_group:
            hero.idle()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit()

            keys_pressed = pygame.key.get_pressed()
            print(any(keys_pressed))
            self._handle_keys_pressed(keys_pressed)
            print(event)

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
        for hero in self.hero_group:
            hero.update()

        self._process_projectiles()

    def _draw(self):
        self.screen.blit(self.background, self.background.get_rect())
        self.hero_group.draw(self.screen)
        self.projectile_group.draw(self.screen)

        pygame.display.flip()
