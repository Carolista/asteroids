import pygame
import random

from .logger import log_event
from .circleshape import CircleShape
from ..config.constants import LINE_WIDTH, ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, color):
        super().__init__(x, y, radius)
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += dt * self.velocity

    def split(self):
        if self.radius > ASTEROID_MIN_RADIUS:
            log_event("asteroid_split")

            x = self.position.x
            y = self.position.y
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            new_asteroid_1 = Asteroid(x, y, new_radius, self.color)
            new_asteroid_2 = Asteroid(x, y, new_radius, self.color)

            random_angle = random.uniform(20, 50)
            new_vector_1 = self.velocity.rotate(random_angle)
            new_vector_2 = self.velocity.rotate(random_angle * -1)
            new_asteroid_1.velocity = 1.2 * new_vector_1
            new_asteroid_2.velocity = 1.2 * new_vector_2
        self.kill()
