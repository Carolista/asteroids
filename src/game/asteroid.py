import math
import random

import pygame

from ..config.constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from .circleshape import CircleShape
from .logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius, color):
        super().__init__(x, y, radius)
        self.color = color
        self.rotation = 0  # Rotation angle in degrees
        self.rotation_speed = random.uniform(-120, 120)  # Degrees per second
        self.shape_offset = self.generate_shape_offset()

    def generate_shape_offset(self):
        num_points = max(8, int(self.radius / 4))
        offsets = []
        for _ in range(num_points):
            offset = random.uniform(-self.radius * 0.15, self.radius * 0.15)
            offsets.append(offset)
        return offsets

    def get_shape_points(self):
        num_points = len(self.shape_offset)
        points = []
        for i in range(num_points):
            angle = (2 * math.pi * i) / num_points
            # Apply the pre-generated offset for this point
            r = self.radius + self.shape_offset[i]

            # Rotate the point
            rotated_angle = angle + math.radians(self.rotation)
            rotated_x = r * math.cos(rotated_angle)
            rotated_y = r * math.sin(rotated_angle)

            # Translate to world position
            world_x = self.position.x + rotated_x
            world_y = self.position.y + rotated_y
            points.append((world_x, world_y))
        return points

    def draw(self, screen):
        points = self.get_shape_points()
        pygame.draw.polygon(screen, self.color, points, LINE_WIDTH)

    def update(self, dt):
        self.position += dt * self.velocity
        self.rotation += dt * self.rotation_speed

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
