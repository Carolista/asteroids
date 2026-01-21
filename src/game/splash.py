import math
import random

import pygame

from ..config.constants import (
    ASTEROID_COLORS,
    ASTEROID_MAX_RADIUS,
    ASTEROID_MIN_RADIUS,
    BLUE,
    FONT_REGULAR,
    FONT_TITLE,
    SCREEN_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHOT_COLORS,
    STAR_COLORS,
    WHITE,
)
from .asteroid import Asteroid
from .highscores import draw_high_scores_centered
from .star import Star
from .starfield import StarField


class SplashScreen:
    def __init__(self, high_scores=None):
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.high_scores = high_scores if high_scores else []

        # Set up containers for Star and Asteroid classes
        Star.containers = self.updatable, self.drawable
        Asteroid.containers = self.updatable, self.drawable, self.asteroids

        # Create star field
        self.star_field = StarField()

        # Create asteroids (2-3 big, 4-5 medium, 6-8 small)
        self.create_splash_asteroids()

        # Color cycling state
        self.color_index = 0
        self.frames_per_color = 10  # Change color every 10 frames at 60 fps
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
            asteroid.velocity = pygame.Vector2(speed * math.cos(angle), speed * math.sin(angle))
            self.asteroids.add(asteroid)

        # Medium asteroids (size 2, radius ASTEROID_MIN_RADIUS * 2)
        for _ in range(random.randint(4, 5)):
            x = random.uniform(0, SCREEN_WIDTH)
            y = random.uniform(0, SCREEN_HEIGHT)
            color = random.choice(ASTEROID_COLORS)
            asteroid = Asteroid(x, y, ASTEROID_MIN_RADIUS * 2, color)
            speed = random.uniform(20, 60)
            angle = random.uniform(0, 2 * math.pi)
            asteroid.velocity = pygame.Vector2(speed * math.cos(angle), speed * math.sin(angle))
            self.asteroids.add(asteroid)

        # Small asteroids (size 1, radius ASTEROID_MIN_RADIUS)
        for _ in range(random.randint(6, 8)):
            x = random.uniform(0, SCREEN_WIDTH)
            y = random.uniform(0, SCREEN_HEIGHT)
            color = random.choice(ASTEROID_COLORS)
            asteroid = Asteroid(x, y, ASTEROID_MIN_RADIUS, color)
            speed = random.uniform(20, 60)
            angle = random.uniform(0, 2 * math.pi)
            asteroid.velocity = pygame.Vector2(speed * math.cos(angle), speed * math.sin(angle))
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

        # Calculate vertical spacing for centered layout
        # ASTEROIDS + gap + HIT ENTER + gap + high scores (5 lines)
        title_font = pygame.font.Font(FONT_TITLE, 120)
        prompt_font = pygame.font.Font(FONT_REGULAR, 36)
        scores_font = pygame.font.Font(FONT_REGULAR, 24)

        # Measure heights
        title_text_dummy = title_font.render("ASTEROIDS", True, WHITE)
        title_height = title_text_dummy.get_height()
        prompt_text_dummy = prompt_font.render("HIT ENTER TO PLAY", True, WHITE)
        prompt_height = prompt_text_dummy.get_height()
        scores_height = scores_font.get_linesize()

        # Calculate total height of all elements
        num_scores = len(self.high_scores) if self.high_scores else 0
        total_height = (
            title_height
            # No gap needed here
            + prompt_height
            + 30  # Gap after prompt
            + (scores_height * num_scores)
        )

        # Calculate starting y position to center vertically
        start_y = (SCREEN_HEIGHT - total_height) // 2

        # Draw "ASTEROIDS" title
        title_color = self.get_current_color(SHOT_COLORS)
        title_text = title_font.render("ASTEROIDS", True, title_color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, start_y))
        screen.blit(title_text, title_rect)

        # Draw "Hit Enter to Play" prompt
        prompt_color = self.get_current_color(STAR_COLORS)
        prompt_text = prompt_font.render("HIT ENTER TO PLAY", True, prompt_color)
        prompt_y = start_y + title_height # No gap needed here
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH / 2, prompt_y))
        screen.blit(prompt_text, prompt_rect)

        # Draw high scores if available (centered)
        if self.high_scores:
            scores_y = prompt_y + prompt_height + 30
            draw_high_scores_centered(screen, self.high_scores, SCREEN_WIDTH / 2, scores_y, BLUE)

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
