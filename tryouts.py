import os
from typing import Any, Callable

import pygame

from sprites import SpriteSequence, get_name_from_file


class Action(pygame.sprite.Sprite):
    def __init__(self, asset_dir: str, rect=pygame.Rect(0, 0, 0, 0), can_be_interrupted=True) -> None:
        super().__init__(*())

        # Required.
        self.rect = rect
        self.image = None

        self.done_handlers = []
        self.start_handlers = []
        self._init_sprites(asset_dir, rect.width, rect.height)

    def _init_sprites(self, asset_dir, width, height):
        images = [file for file in os.listdir(
            asset_dir) if file.endswith(".png")]

        self.sequences = dict()

        for img in images:
            can_be_interrupted = ('attack' not in img) and (
                'shot' not in img) and ('hurt' not in img) and ('dead' not in img)
            self.sequences[get_name_from_file(img)] = SpriteSequence(
                f'{asset_dir}/{img}', width, height, can_be_interrupted)

    def done(self) -> bool:
        return False

    def interruptible(self) -> bool:
        return False

    def _on_done(self, callable: Callable) -> None:
        self.done_handlers.append(callable)

    def _on_start(self, callable: Callable) -> None:
        self.start_handlers.append(callable)

    def reset(self, clear_handlers=False) -> pygame.sprite.Group:
        if clear_handlers:
            self.done_handlers.clear()
            self.start_handlers.clear()

        return self

    def update(self, *args: Any, **kwargs: Any) -> None:
        # Delegate this to Actor(Group)
        return super().update(*args, **kwargs)


if __name__ == '__main__':
    print(Action(None))
