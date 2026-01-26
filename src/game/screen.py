import math
import random

import pygame

from ..config.constants import (
    ASTEROID_COLORS,
    ASTEROID_MAX_RADIUS,
    ASTEROID_MIN_RADIUS,
    FINAL_SCORE_COLORS,
    FONT_REGULAR,
    FONT_SCORE,
    FONT_TITLE,
    HIGH_SCORES_LIST_COLORS,
    PROMPT_COLORS,
    SCREEN_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE_COLORS,
    WHITE,
)
from .asteroid import Asteroid
from .highscores import draw_high_scores
from .star import Star
from .starfield import StarField


class Screen:
    """Abstract base class for non-gameplay screens (splash, game-over)."""

    def __init__(
        self,
        title_content="",
        final_score_content="",
        prompt_content="",
        high_scores_list=None,
        title_font_size=100,
        final_score_font_size=40,
        prompt_font_size=28,
        high_scores_list_font_size=24,
    ):
        """
        Initialize a screen with background asteroids and text elements.

        Args:
            title_content: Main title string (flashes through title_colors)
            final_score_content: Final score string (flashes through final_score_colors)
            prompt_content: Primary prompt/action string (flashes through prompt_colors)
            high_scores_list: List of high score dicts to display
            title_font_size: Size for title font
            final_score_font_size: Size for final score font
            prompt_font_size: Size for prompt font
            high_scores_list_font_size: Size for high scores list font
        """
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()

        # Actual content to be displayed
        self.title_content = title_content
        self.final_score_content = final_score_content
        self.prompt_content = prompt_content
        self.high_scores_list = high_scores_list if high_scores_list else []

        # Font sizes
        self.title_font_size = title_font_size
        self.final_score_font_size = final_score_font_size
        self.prompt_font_size = prompt_font_size
        self.high_scores_list_font_size = high_scores_list_font_size

        # Colors - all are lists of RGB values for cycling
        self.title_colors = TITLE_COLORS
        self.final_score_colors = FINAL_SCORE_COLORS
        self.prompt_colors = PROMPT_COLORS
        self.high_scores_list_colors = HIGH_SCORES_LIST_COLORS

        # Color cycling state
        self.color_index = 0
        self.frames_per_color = 4
        self.frame_counter = 0
        self.forward = True

        # Set up containers for Star and Asteroid classes
        Star.containers = self.updatable, self.drawable
        Asteroid.containers = self.updatable, self.drawable, self.asteroids

        # Create background
        self.star_field = StarField()
        self._create_background_asteroids()

    def _create_background_asteroids(self):
        """Create asteroids (2-3 big, 4-5 medium, 6-8 small) for background."""
        # Big asteroids (size 3, radius ASTEROID_MAX_RADIUS)
        for _ in range(random.randint(2, 3)):
            x = random.uniform(0, SCREEN_WIDTH)
            y = random.uniform(0, SCREEN_HEIGHT)
            color = random.choice(ASTEROID_COLORS)
            asteroid = Asteroid(x, y, ASTEROID_MAX_RADIUS, color)
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

    def update_color_cycle(self, colors_list):
        """Update color cycling state."""
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
        """Draw the screen with title, high score section, prompt, and high scores list."""
        game_surface.fill(SCREEN_COLOR)

        # Update and draw background objects
        self.updatable.update(1 / 60)
        for obj in self.drawable:
            obj.draw(game_surface)

        # Blit game surface to screen
        screen.blit(game_surface, (0, 0))

        # Set up fonts
        title_font = pygame.font.Font(FONT_TITLE, self.title_font_size)
        final_score_font = pygame.font.Font(FONT_SCORE, self.final_score_font_size)
        prompt_font = pygame.font.Font(FONT_REGULAR, self.prompt_font_size)
        high_scores_list_font = pygame.font.Font(FONT_SCORE, self.high_scores_list_font_size)

        # Pre-measure heights (these won't be displayed)
        title_text_dummy = title_font.render(self.title_content, True, WHITE)
        title_height = title_text_dummy.get_height()
        
        has_final_score_section = bool(self.final_score_content)
        if has_final_score_section:
            final_score_text_dummy = final_score_font.render(self.final_score_content, True, WHITE)
            final_score_height = final_score_text_dummy.get_height()

        prompt_text_dummy = prompt_font.render(self.prompt_content, True, WHITE)
        prompt_height = prompt_text_dummy.get_height()

        high_scores_line_height = high_scores_list_font.get_linesize()
        num_scores = len(self.high_scores_list) if self.high_scores_list else 0

        # Calculate total height for vertical centering
        total_height = (
            title_height
            + 30
            + (final_score_height + 30 if has_final_score_section else 0)
            + prompt_height
            + (30 if num_scores > 0 else 0)
            + (high_scores_line_height * num_scores)
        )

        # Calculate starting y position to center vertically
        start_y = (SCREEN_HEIGHT - total_height) // 2

        # Draw title
        title_color = self.get_current_color(self.title_colors)
        title_text = title_font.render(self.title_content, True, title_color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, start_y))
        screen.blit(title_text, title_rect)

        # Draw final score section (if present)
        current_y = start_y + title_height + 30
        if has_final_score_section:
            final_score_color = self.get_current_color(self.final_score_colors)
            final_score_text = final_score_font.render(self.final_score_content, True, final_score_color)  # noqa: E501
            section_rect = final_score_text.get_rect(center=(SCREEN_WIDTH / 2, current_y))
            screen.blit(final_score_text, section_rect)
            current_y += final_score_height + 30

        # Draw prompt
        prompt_color = self.get_current_color(self.prompt_colors)
        prompt_text = prompt_font.render(self.prompt_content, True, prompt_color)
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH / 2, current_y))
        screen.blit(prompt_text, prompt_rect)

        # Draw high scores if available
        if self.high_scores_list:
            scores_y = current_y + prompt_height + 30
            high_scores_list_color = self.get_current_color(self.high_scores_list_colors)
            draw_high_scores(
                screen, self.high_scores_list, 
                SCREEN_WIDTH / 2, 
                scores_y, 
                high_scores_list_color
            )

        pygame.display.flip()
        self.update_color_cycle(self.high_scores_list_colors)

    def run(self, screen, game_surface, clock):
        """Run the screen. Subclasses should override."""
        raise NotImplementedError("Subclasses must implement run()")
