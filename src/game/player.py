import random

import pygame

from ..config.constants import (
    PLAYER_ACCELERATION,
    PLAYER_COLOR,
    PLAYER_DRAG,
    PLAYER_FRICTION,
    PLAYER_MAX_SPEED,
    PLAYER_RADIUS,
    PLAYER_ROTATE_SPEED,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    THRUSTER_COLOR,
)
from .circleshape import CircleShape
from .shot import Shot

# TODO: Make hit box triangular instead of using circle


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.current_rotation_speed = 0
        self.acceleration = PLAYER_ACCELERATION
        self.drag = PLAYER_DRAG
        self.shot_timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def thruster_flame(self):
        backward = pygame.Vector2(0, 1).rotate(self.rotation)

        flame_root = self.position + backward * (self.radius * 0.8)
        flame_length = self.radius * random.uniform(0.5, 1.2)
        flame_tip = flame_root + backward * flame_length
        side_width = self.radius / 3
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * side_width

        a = flame_root - right
        b = flame_root + right
        c = flame_tip

        return [a, b, c]

    def draw(self, screen):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            pygame.draw.polygon(screen, THRUSTER_COLOR, self.thruster_flame(), 0)

        pygame.draw.polygon(screen, PLAYER_COLOR, self.triangle(), 0)

    def thrust(self, dt):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.velocity += forward * self.acceleration * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        target_speed = 0

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.thrust(-dt * 0.5)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.thrust(dt)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            target_speed -= PLAYER_ROTATE_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            target_speed += PLAYER_ROTATE_SPEED
        if keys[pygame.K_SPACE]:
            self.shoot()

        diff = target_speed - self.current_rotation_speed
        self.current_rotation_speed += diff * PLAYER_FRICTION
        self.rotation += self.current_rotation_speed * dt

        if self.velocity.length() > 0:
            self.velocity -= self.velocity * self.drag * dt

        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)

        self.position += self.velocity * dt

        # Screen wrap
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT

        self.shot_timer -= dt

    def shoot(self):
        if self.shot_timer <= 0:
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = pygame.Vector2(0, -1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            self.shot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
