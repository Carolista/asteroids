import math
import random

import pygame

from ..config.constants import (
    ASTEROID_COLORS,
    ASTEROID_MAX_RADIUS,
    ASTEROID_MIN_RADIUS,
    SCREEN_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WHITE_MIX,
)
from .asteroid import Asteroid
from .star import Star
from .starfield import StarField


# Abstract parent class for various non-gameplay screens
class Screen:
    def __init__(self):
        # Manage objects through groups
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()

        # Create list of Section objects to be rendered
        self.sections = []
        # Subclasses should define and append specific objects

        # Color cycling state
        self.color_index = 0
        self.frames_per_color = 4
        self.frame_counter = 0
        self.forward = True

        # Set up containers for Star and Asteroid classes
        Star.containers = self.updatable, self.drawable
        Asteroid.containers = self.updatable, self.drawable, self.asteroids

        # Create background objects
        self.star_field = StarField()
        self._create_background_asteroids(2, 3, ASTEROID_MAX_RADIUS)
        self._create_background_asteroids(4, 5, 2 * ASTEROID_MIN_RADIUS)
        self._create_background_asteroids(6, 8, ASTEROID_MIN_RADIUS)

    def _create_background_asteroids(self, min_n, max_n, radius):
        for _ in range(random.randint(min_n, max_n)):
            x = random.uniform(0, SCREEN_WIDTH)
            y = random.uniform(0, SCREEN_HEIGHT)
            color = random.choice(ASTEROID_COLORS)
            asteroid = Asteroid(x, y, radius, color)
            speed = random.uniform(20, 60)
            angle = random.uniform(0, 2 * math.pi)
            asteroid.velocity = pygame.Vector2(speed * math.cos(angle), speed * math.sin(angle))
            self.asteroids.add(asteroid)

    def update_color_cycle(self, colors_list):
        self.frame_counter += 1
        if self.frame_counter >= self.frames_per_color:
            self.frame_counter = 0
            if self.forward:
                self.color_index += 1
                if self.color_index >= len(colors_list):
                    self.color_index = len(colors_list) - 1
                    self.forward = False
            else:
                self.color_index -= 1
                if self.color_index < 0:
                    self.color_index = 0
                    self.forward = True

    def draw(self, screen, game_surface):
        # Blank out game surface for re-rendering
        game_surface.fill(SCREEN_COLOR)

        # Update and draw background objects
        self.updatable.update(1 / 60)
        for obj in self.drawable:
            obj.draw(game_surface)

        # Blit game surface to screen
        screen.blit(game_surface, (0, 0))

        # Calculate starting y position to center vertically
        total_height = sum(section.get_y_adjustment() for section in self.sections)
        current_y = (SCREEN_HEIGHT - total_height) // 2

        for section in self.sections:
            section.update_current_color(self.color_index)
            section.update_render_text()
            section.update_rectangle(current_y)
            screen.blit(section.render_text, section.rectangle)
            current_y += section.height + section.gap

        pygame.display.flip()
        self.update_color_cycle(WHITE_MIX)

    def run(self, screen, game_surface, clock):
        """Run the screen. Subclasses should override."""
        raise NotImplementedError("Subclasses must implement run()")
