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


class Screen:
    """Abstract base class for non-gameplay screens (splash, game-over)."""

    def __init__(
        self,
        title="",
        final_score_section="",
        prompt="",
        title_font_size=100,
        regular_font_size=32,
        scores_font_size=24,
        title_color=SHOT_COLORS,
        text_color=STAR_COLORS,
        scores_color=BLUE,
        high_scores=None,
    ):
        """
        Initialize a screen with background asteroids and text elements.

        Args:
            title: Main title text (flashes through title_color)
            final_score_section: Secondary info text (flashes through text_color)
            prompt: Primary prompt/action text (flashes through text_color)
            title_font_size: Size for title font
            regular_font_size: Size for regular text font
            scores_font_size: Size for high scores font
            title_color: List of colors for title cycling (or single color tuple)
            text_color: List of colors for text cycling (or single color tuple)
            scores_color: Color for high scores list
            high_scores: List of high score dicts to display
        """
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()

        self.title = title
        self.final_score_section = final_score_section
        self.prompt = prompt
        self.high_scores = high_scores if high_scores else []
        self.scores_color = scores_color

        # Font sizes
        self.title_font_size = title_font_size
        self.regular_font_size = regular_font_size
        self.scores_font_size = scores_font_size

        # Colors - ensure they're lists for cycling
        self.title_colors = title_color if isinstance(title_color, list) else [title_color]
        self.text_colors = text_color if isinstance(text_color, list) else [text_color]

        # Color cycling state
        self.color_index = 0
        self.frames_per_color = 10
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

    def update_color_cycle(self):
        """Update color cycling state."""
        self.frame_counter += 1
        if self.frame_counter >= self.frames_per_color:
            self.frame_counter = 0
            if self.forward:
                self.color_index += 1
                if self.color_index >= len(self.title_colors):
                    self.color_index = len(self.title_colors) - 1
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
        regular_font = pygame.font.Font(FONT_REGULAR, self.regular_font_size)
        scores_font = pygame.font.SysFont("monospace", self.scores_font_size)

        # Measure heights
        title_text_dummy = title_font.render(self.title, True, WHITE)
        title_height = title_text_dummy.get_height()

        prompt_text_dummy = regular_font.render(self.prompt, True, WHITE)
        prompt_height = prompt_text_dummy.get_height()

        scores_height = scores_font.get_linesize()

        # Calculate section height only if final_score_section is present
        has_section = bool(self.final_score_section)
        section_height = 0
        if has_section:
            section_text_dummy = regular_font.render(self.final_score_section, True, WHITE)
            section_height = section_text_dummy.get_height()

        # Calculate total height for centering
        num_scores = len(self.high_scores) if self.high_scores else 0
        total_height = (
            title_height
            + 30  # Gap
            + (section_height + 30 if has_section else 0)  # Section + gap (only if present)
            + prompt_height
            + (30 if num_scores > 0 else 0)  # Gap before scores
            + (scores_height * num_scores)
        )

        # Calculate starting y position to center vertically
        start_y = (SCREEN_HEIGHT - total_height) // 2

        # Draw title
        title_color = self.get_current_color(self.title_colors)
        title_text = title_font.render(self.title, True, title_color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, start_y))
        screen.blit(title_text, title_rect)

        # Draw final score section (if present)
        current_y = start_y + title_height + 30
        if has_section:
            section_color = self.get_current_color(self.text_colors)
            section_text = regular_font.render(self.final_score_section, True, section_color)
            section_rect = section_text.get_rect(center=(SCREEN_WIDTH / 2, current_y))
            screen.blit(section_text, section_rect)
            current_y += section_height + 30

        # Draw prompt
        prompt_color = self.get_current_color(self.text_colors)
        prompt_text = regular_font.render(self.prompt, True, prompt_color)
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH / 2, current_y))
        screen.blit(prompt_text, prompt_rect)

        # Draw high scores if available
        if self.high_scores:
            scores_y = current_y + prompt_height + 30
            draw_high_scores_centered(
                screen, self.high_scores, SCREEN_WIDTH / 2, scores_y, self.scores_color
            )

        pygame.display.flip()
        self.update_color_cycle()

    def run(self, screen, game_surface, clock):
        """Run the screen. Subclasses should override."""
        raise NotImplementedError("Subclasses must implement run()")
