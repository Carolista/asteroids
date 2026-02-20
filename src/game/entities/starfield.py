import random

import pygame

from ...config.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from .star import Star


class StarField(pygame.sprite.Sprite):
    def __init__(self, num_stars=100):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.num_stars = num_stars
        self.spawn_stars()

    def spawn_stars(self):
        for _ in range(self.num_stars):
            x = random.uniform(0, SCREEN_WIDTH)
            y = random.uniform(0, SCREEN_HEIGHT)
            # Managed through containers
            star = Star(x, y)  # noqa: F841

    def update(self, dt):
        pass
