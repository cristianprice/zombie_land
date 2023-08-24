import pygame
from actors import Skeleton


BACKGROUND_COLOR = pygame.Color('white')
FRAMERATE = 15


class ZombieLand:
    def __init__(self, window_size=(800, 600)):
        self._init_pygame()
        self.clock = pygame.time.Clock()

        self.flags = pygame.SCALED  # | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(window_size, self.flags)

        # self.background = su.load_sprite("space", False)

        self.hero_group = pygame.sprite.Group()
        self.skelly = Skeleton('assets/sprites/archer')

        self.hero_group.add(self.skelly)

    def main_loop(self):
        pygame.key.set_repeat(0, FRAMERATE)

        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()
            self.clock.tick(FRAMERATE)

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("ZombieLand")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.skelly.left_walk()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.skelly.right_walk()
            elif event.type == pygame.KEYUP:
                self.skelly.idle()

    def _process_game_logic(self):
        self.skelly.update()

    def _draw(self):
        # self.screen.blit(self.background, (0, 0))
        self.screen.fill(BACKGROUND_COLOR)
        self.hero_group.draw(self.screen)

        pygame.display.flip()
