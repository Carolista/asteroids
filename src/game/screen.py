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

        # # Actual content to be displayed
        # self.title_content = title_content
        # self.final_score_content = final_score_content
        # self.prompt_content = prompt_content
        # self.high_scores_list = high_scores_list if high_scores_list else []

        # # Font sizes
        # self.title_font_size = title_font_size
        # self.final_score_font_size = final_score_font_size
        # self.prompt_font_size = prompt_font_size
        # self.high_scores_list_font_size = high_scores_list_font_size

        # # Colors - all are lists of RGB values for cycling
        # self.title_colors = TITLE_COLORS
        # self.final_score_colors = FINAL_SCORE_COLORS
        # self.prompt_colors = PROMPT_COLORS
        # self.high_scores_list_colors = HIGH_SCORES_LIST_COLORS

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

    # def get_current_color(self, colors_list):
    #     """Get current color from list, cycling forward and backward."""
    #     return colors_list[self.color_index]

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

        # # Set up fonts
        # title_font = pygame.font.Font(FONT_TITLE, self.title_font_size)
        # final_score_font = pygame.font.Font(FONT_SCORE, self.final_score_font_size)
        # prompt_font = pygame.font.Font(FONT_REGULAR, self.prompt_font_size)
        # high_scores_list_font = pygame.font.Font(FONT_SCORE, self.high_scores_list_font_size)

        # # Pre-measure heights (these won't be displayed)
        # title_text_dummy = title_font.render(self.title_content, True, WHITE)
        # title_height = title_text_dummy.get_height()

        # has_final_score_section = bool(self.final_score_content)
        # if has_final_score_section:
        #     final_score_text_dummy = final_score_font.render(self.final_score_content, True, WHITE)
        #     final_score_height = final_score_text_dummy.get_height()

        # prompt_text_dummy = prompt_font.render(self.prompt_content, True, WHITE)
        # prompt_height = prompt_text_dummy.get_height()

        # high_scores_line_height = high_scores_list_font.get_linesize()
        # num_scores = len(self.high_scores_list) if self.high_scores_list else 0

        # # Calculate total height for vertical centering
        # total_height = (
        #     title_height
        #     + 30
        #     + (final_score_height + 30 if has_final_score_section else 0)
        #     + prompt_height
        #     + (30 if num_scores > 0 else 0)
        #     + (high_scores_line_height * num_scores)
        # )

        # # Calculate starting y position to center vertically
        # start_y = (SCREEN_HEIGHT - total_height) // 2

        # Draw title
        # title_color = self.get_current_color(self.title_colors)
        # title_text = title_font.render(self.title_content, True, title_color)
        # title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, start_y))
        # screen.blit(title_text, title_rect)

        # Draw final score section (if present)
        # current_y = start_y + title_height + 30
        # if has_final_score_section:
        #     final_score_color = self.get_current_color(self.final_score_colors)
        #     final_score_text = final_score_font.render(self.final_score_content, True, final_score_color)  # noqa: E501
        #     section_rect = final_score_text.get_rect(center=(SCREEN_WIDTH / 2, current_y))
        #     screen.blit(final_score_text, section_rect)
        #     current_y += final_score_height + 30

        # Draw prompt
        # prompt_color = self.get_current_color(self.prompt_colors)
        # prompt_text = prompt_font.render(self.prompt_content, True, prompt_color)
        # prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH / 2, current_y))
        # screen.blit(prompt_text, prompt_rect)

        # Draw high scores if available
        # if self.high_scores_list:
        #     scores_y = current_y + prompt_height + 30
        #     high_scores_list_color = self.get_current_color(self.high_scores_list_colors)
        #     draw_high_scores(
        #         screen, self.high_scores_list,
        #         SCREEN_WIDTH / 2,
        #         scores_y,
        #         high_scores_list_color
        #     )

        pygame.display.flip()
        self.update_color_cycle(WHITE_MIX)

    def run(self, screen, game_surface, clock):
        """Run the screen. Subclasses should override."""
        raise NotImplementedError("Subclasses must implement run()")
