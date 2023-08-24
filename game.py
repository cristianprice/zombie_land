import pygame
import sprite_utils as su
from sprite_utils import States, Direction


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
        self.skelly = su.SkeletonArcher(self.hero_group)

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
                self.skelly.update(state=States.WALK, direction=Direction.LEFT)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.skelly.update(state=States.WALK,
                                   direction=Direction.RIGHT)
            elif event.type == pygame.KEYUP:
                self.skelly.update(state=States.IDLE,
                                   direction=self.skelly.direction)

    def _process_game_logic(self):
        self.skelly.update(state=self.skelly.current_state,
                           direction=self.skelly.direction)

    def _draw(self):

        # self.screen.blit(self.background, (0, 0))
        self.screen.fill(BACKGROUND_COLOR)
        self.hero_group.draw(self.screen)

        pygame.display.flip()
