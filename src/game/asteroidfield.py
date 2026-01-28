import random

import pygame

from ..config.constants import (
    ASTEROID_COLORS,
    ASTEROID_KINDS,
    ASTEROID_MAX_RADIUS,
    ASTEROID_MAX_SPEED,
    ASTEROID_MIN_RADIUS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from .asteroid import Asteroid


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        color = random.choice(ASTEROID_COLORS)
        asteroid = Asteroid(position.x, position.y, radius, color)
        asteroid.velocity = velocity

    def spawn_wave(self, count, wave_number=1):
        for _ in range(count):
            edge = random.choice(self.edges)
            base_speed = min(30 + (wave_number * 5), ASTEROID_MAX_SPEED)
            speed = random.randint(base_speed, base_speed + 40)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))

            # Use a random size (kind) for the new wave
            if wave_number < 3:
                kind = ASTEROID_KINDS
            elif wave_number < 5:
                kind = random.randint(2, ASTEROID_KINDS)
            else:
                kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)

    def update(self, dt):
        pass
