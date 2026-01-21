import random

import pygame

from ..config.constants import PARTICLE_COLORS, PARTICLE_LIFESPAN
from .circleshape import CircleShape


class Particle(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PARTICLE_LIFESPAN * 8)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(
            random.uniform(-1, 1), random.uniform(-1, 1)
        ).normalize() * random.uniform(50, 150)  # noqa: E501
        self.lifespan = PARTICLE_LIFESPAN
        self.color = random.choice(PARTICLE_COLORS)

    def update(self, dt):
        self.position += self.velocity * dt
        self.lifespan -= dt
        if self.lifespan <= 0:
            self.kill()

    def draw(self, screen):
        if self.radius > 0:
            pygame.draw.circle(screen, self.color, self.position, self.radius)
        # As it dies, it gets smaller
        self.radius = int(self.lifespan * 8)
