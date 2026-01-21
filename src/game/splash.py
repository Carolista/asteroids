import math
import random

import pygame

from ..config.constants import (
    ASTEROID_COLORS,
    ASTEROID_MAX_RADIUS,
    ASTEROID_MIN_RADIUS,
    FONT_SCORE,
    FONT_SPECIAL,
    SCREEN_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHOT_COLORS,
    STAR_COLORS,
)
from .asteroid import Asteroid
from .star import Star
from .starfield import StarField


class SplashScreen:
    def __init__(self):
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()

        # Set up containers for Star and Asteroid classes
        Star.containers = self.updatable, self.drawable
        Asteroid.containers = self.updatable, self.drawable, self.asteroids

        # Create star field
        self.star_field = StarField()

        # Create asteroids (2-3 big, 4-5 medium, 6-8 small)
        self.create_splash_asteroids()

        # Color cycling state
        self.color_index = 0
        self.frames_per_color = 8  # Change color every 8 frames at 60 fps (~130ms)
        self.frame_counter = 0
        self.forward = True  # Direction of color cycling

    def create_splash_asteroids(self):
        """Create asteroids for the splash screen."""
        # Big asteroids (size 3, radius ASTEROID_MAX_RADIUS)
        for _ in range(random.randint(2, 3)):
            x = random.uniform(0, SCREEN_WIDTH)
            y = random.uniform(0, SCREEN_HEIGHT)
            color = random.choice(ASTEROID_COLORS)
            asteroid = Asteroid(x, y, ASTEROID_MAX_RADIUS, color)
            # Add random velocity for drift
            speed = random.uniform(20, 60)
            angle = random.uniform(0, 2 * math.pi)
            asteroid.velocity = pygame.Vector2(
                speed * math.cos(angle), speed * math.sin(angle)
            )
            self.asteroids.add(asteroid)

        # Medium asteroids (size 2, radius ASTEROID_MIN_RADIUS * 2)
        for _ in range(random.randint(4, 5)):
            x = random.uniform(0, SCREEN_WIDTH)
            y = random.uniform(0, SCREEN_HEIGHT)
            color = random.choice(ASTEROID_COLORS)
            asteroid = Asteroid(x, y, ASTEROID_MIN_RADIUS * 2, color)
            speed = random.uniform(20, 60)
            angle = random.uniform(0, 2 * math.pi)
            asteroid.velocity = pygame.Vector2(
                speed * math.cos(angle), speed * math.sin(angle)
            )
            self.asteroids.add(asteroid)

        # Small asteroids (size 1, radius ASTEROID_MIN_RADIUS)
        for _ in range(random.randint(6, 8)):
            x = random.uniform(0, SCREEN_WIDTH)
            y = random.uniform(0, SCREEN_HEIGHT)
            color = random.choice(ASTEROID_COLORS)
            asteroid = Asteroid(x, y, ASTEROID_MIN_RADIUS, color)
            speed = random.uniform(20, 60)
            angle = random.uniform(0, 2 * math.pi)
            asteroid.velocity = pygame.Vector2(
                speed * math.cos(angle), speed * math.sin(angle)
            )
            self.asteroids.add(asteroid)

    def get_current_color(self, colors_list):
        """Get current color from list, cycling forward and backward."""
        return colors_list[self.color_index]

    def update_color_cycle(self):
        """Update color cycling state."""
        self.frame_counter += 1
        if self.frame_counter >= self.frames_per_color:
            self.frame_counter = 0
            if self.forward:
                self.color_index += 1
                if self.color_index >= len(SHOT_COLORS) - 1:
                    self.forward = False
            else:
                self.color_index -= 1
                if self.color_index <= 0:
                    self.forward = True

    def draw(self, screen, game_surface):
        """Draw the splash screen."""
        game_surface.fill(SCREEN_COLOR)

        # Update and draw game objects
        self.updatable.update(1 / 60)  # Update with fixed dt
        for obj in self.drawable:
            obj.draw(game_surface)

        # Blit game surface to screen
        screen.blit(game_surface, (0, 0))

        # Draw "ASTEROIDS" title
        title_font = pygame.font.Font(FONT_SPECIAL, 100)
        title_color = self.get_current_color(SHOT_COLORS)
        title_text = title_font.render("ASTEROIDS", True, title_color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))
        screen.blit(title_text, title_rect)

        # Draw "Hit Enter to Play" prompt
        prompt_font = pygame.font.Font(FONT_SCORE, 32)
        prompt_color = self.get_current_color(STAR_COLORS)
        prompt_text = prompt_font.render("Hit Enter to Play", True, prompt_color)
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80))
        screen.blit(prompt_text, prompt_rect)

        pygame.display.flip()
        self.update_color_cycle()

    def run(self, screen, game_surface, clock):
        """Run the splash screen until Enter is pressed."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False  # Signal to quit the entire game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True  # Signal to start the game

            self.draw(screen, game_surface)
            clock.tick(60)
