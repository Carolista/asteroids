import pygame
import random
from star import Star
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class StarField(pygame.sprite.Sprite):
    def __init__(self, num_stars=100):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.num_stars = num_stars
        self.spawn_stars()

    def spawn_stars(self):
        for _ in range(self.num_stars):
            x = random.uniform(0, SCREEN_WIDTH)
            y = random.uniform(0, SCREEN_HEIGHT)
            star = Star(x, y)

    def update(self, dt):
        pass
