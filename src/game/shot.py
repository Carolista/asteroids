import random

import pygame

from ..config.constants import PARTICLE_COLORS, SHOT_LIFESPAN, SHOT_RADIUS
from .circleshape import CircleShape


class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.lifespan = SHOT_LIFESPAN
        self.color = random.choice(PARTICLE_COLORS)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, 0)

    def update(self, dt):
        self.position += dt * self.velocity
        self.lifespan -= dt
        if self.lifespan <= 0:
            self.kill()
