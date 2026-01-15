import pygame

from ..config.constants import LINE_WIDTH, SHOT_COLOR, SHOT_RADIUS
from .circleshape import CircleShape


class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, SHOT_COLOR, self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += dt * self.velocity
