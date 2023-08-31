import pygame
from pygame.sprite import Sprite


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


def get_name_from_file(file_name):
    idx = file_name.index('.')
    return file_name[0:idx]


def _get_sprites(file_name, width, height, mirrored=False):
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
                surf = sheet.image_at((w*width, h*height, width, height))
                if mirrored:
                    sprites.append(pygame.transform.flip(surf, True, False))
                else:
                    sprites.append(surf)
    return sprites


def _revert_sprites(sprites_collection):
    return [pygame.transform.flip(
            img, True, False) for img in sprites_collection]


class SpriteSequence:
    def __init__(self, file_name, width, height, can_be_interrupted=True, reverted=False) -> None:
        self.can_be_interrupted = can_be_interrupted
        self.steps = [sprite for sprite in _get_sprites(
            file_name, width, height, reverted)]
        self.index = 0
        self.rect = self.steps[self.index].get_rect()
        self.name = get_name_from_file(file_name)

    def interruptible(self) -> bool:
        return self.can_be_interrupted

    def reset(self) -> object:
        self.index = 0
        return self

    def get_rect(self):
        return self.rect

    def done(self) -> bool:
        return self.index >= len(self.steps)

    def next(self):
        if not self.done():
            step = self.steps[self.index]
            self.index += 1
            return step
        else:
            return self.steps[-1]  # Return last element.
