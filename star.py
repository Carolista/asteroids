import pygame
import random
from circleshape import CircleShape
from constants import STAR_COLORS


class Star(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, radius=1)
        self.color = random.choice(STAR_COLORS)
        self.twinkle_timer = random.uniform(0, 0.5)
        self.twinkle_interval = random.uniform(0.1, 0.5)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def update(self, dt):
        self.twinkle_timer += dt
        if self.twinkle_timer > self.twinkle_interval:
            self.twinkle_timer = 0
            self.color = random.choice(STAR_COLORS)
            self.twinkle_interval = random.uniform(0.1, 0.5)
