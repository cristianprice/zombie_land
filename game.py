import pygame
from actors import NewActor
from game_constants import WIDTH, HEIGHT, FRAMERATE


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

        self.skelly_archer = NewActor(
            'assets/sprites/archer', 128, 128, (0, 200))
        self.groups = [self.hero_group, self.zombie_group]

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
        no_keys = any(keys)

        for hero in self.hero_group:
            hero.idle()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit()

            keys_pressed = pygame.key.get_pressed()
            print(len(keys_pressed))
            self._handle_keys_pressed(keys_pressed)
            print(event)

    def _process_game_logic(self):

        for group in self.groups:
            for actor in group:
                actor.update()

        self._process_projectiles()

    def _draw(self):
        self.screen.blit(self.background, self.background.get_rect())
        for g in self.groups:
            g.draw(self.screen)

        self.projectile_group.draw(self.screen)

        pygame.display.flip()
