import random

import pygame

from ..config.constants import (
    PLAYER_COLOR,
    PLAYER_FRICTION,
    PLAYER_MOVE_SPEED,
    PLAYER_RADIUS,
    PLAYER_ROTATE_SPEED,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
)
from .circleshape import CircleShape
from .shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.current_rotation_speed = 0
        self.shot_timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def thruster_flame(self):
        # This is the opposite direction of the nose
        backward = pygame.Vector2(0, 1).rotate(self.rotation)

        # Calculate the base of the ship (the rear)
        # We use a slightly smaller radius so it starts 'inside' the ship
        flame_root = self.position + backward * (self.radius * 0.8)

        # Calculate the 'tip' of the flame
        # random.uniform adds the 'flicker' effect
        flame_length = self.radius * random.uniform(0.5, 1.2)
        flame_tip = flame_root + backward * flame_length

        # Side points for the flame triangle
        side_width = self.radius / 3
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * side_width

        a = flame_root - right
        b = flame_root + right
        c = flame_tip

        return [a, b, c]

    def draw(self, screen):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            pygame.draw.polygon(screen, (255, 165, 0), self.thruster_flame(), 0)

        pygame.draw.polygon(screen, PLAYER_COLOR, self.triangle(), 0)

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_MOVE_SPEED * dt
        self.position += rotated_with_speed_vector

    def update(self, dt):
        keys = pygame.key.get_pressed()

        target_speed = 0

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt * -1)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            target_speed -= PLAYER_ROTATE_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            target_speed += PLAYER_ROTATE_SPEED
        if keys[pygame.K_SPACE]:
            self.shoot()

        diff = target_speed - self.current_rotation_speed
        self.current_rotation_speed += diff * PLAYER_FRICTION
        self.rotation += self.current_rotation_speed * dt

        self.shot_timer -= dt

    def shoot(self):
        if self.shot_timer <= 0:
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = pygame.Vector2(0, -1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            self.shot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
