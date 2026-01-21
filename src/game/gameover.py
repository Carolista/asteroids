import pygame

from ..config.constants import (
    FONT_REGULAR,
    FONT_TITLE,
    GAME_OVER_COLOR,
    LIGHT_GRAY,
    STAR_COLORS,
    WHITE,
)
from .screen import Screen


class GameOverScreen(Screen):
    """Game over screen with optional high score name entry."""

    def __init__(self, final_score, high_score_manager):
        self.final_score = final_score
        self.high_score_manager = high_score_manager
        self.is_high_score = high_score_manager.is_high_score(final_score)
        self.player_name = ""
        # Skip name entry if score is 0 (crashed without any hits)
        self.name_entry_mode = self.is_high_score and final_score > 0

        final_score_section = f"FINAL SCORE: {final_score}"

        # Initialize parent with appropriate text
        if self.name_entry_mode:
            prompt = "You got a high score! Enter your name below:"
        else:
            prompt = "Play Again?  Y / N"

        super().__init__(
            title="G A M E   O V E R",
            final_score_section=final_score_section,
            prompt=prompt,
            title_font_size=60,
            regular_font_size=32,
            scores_font_size=24,
            title_color=GAME_OVER_COLOR,
            text_color=STAR_COLORS,
            high_scores=high_score_manager.get_scores() if not self.name_entry_mode else [],
        )

    def draw_name_entry(self, screen, game_surface):
        """Draw the game over screen with name entry field."""
        game_surface.fill((0, 0, 0))

        # Update and draw background objects
        self.updatable.update(1 / 60)
        for obj in self.drawable:
            obj.draw(game_surface)

        # Blit game surface to screen
        screen.blit(game_surface, (0, 0))

        # Set up fonts
        title_font = pygame.font.Font(FONT_TITLE, 60)
        regular_font = pygame.font.Font(FONT_REGULAR, 32)

        # Measure heights
        title_text_dummy = title_font.render(self.title, True, WHITE)
        title_height = title_text_dummy.get_height()
        section_text_dummy = regular_font.render(self.final_score_section, True, WHITE)
        section_height = section_text_dummy.get_height()
        prompt_text_dummy = regular_font.render(self.prompt, True, WHITE)
        prompt_height = prompt_text_dummy.get_height()
        display_name_input = self.player_name if self.player_name else "_"
        name_text_dummy = regular_font.render(display_name_input, True, WHITE)
        name_height = name_text_dummy.get_height()

        # Calculate total height for centering
        total_height = title_height + 30 + section_height + 30 + prompt_height + 30 + name_height

        # Calculate starting y position to center vertically
        start_y = (screen.get_height() - total_height) // 2

        # Draw title
        title_color = self.get_current_color(self.title_colors)
        title_text = title_font.render(self.title, True, title_color)
        title_rect = title_text.get_rect(center=(screen.get_width() / 2, start_y))
        screen.blit(title_text, title_rect)

        # Draw high score section
        section_color = self.get_current_color(self.text_colors)
        section_text = regular_font.render(self.final_score_section, True, section_color)
        section_y = start_y + title_height + 30
        section_rect = section_text.get_rect(center=(screen.get_width() / 2, section_y))
        screen.blit(section_text, section_rect)

        # Draw prompt
        prompt_color = self.get_current_color(self.text_colors)
        prompt_text = regular_font.render(self.prompt, True, prompt_color)
        prompt_y = section_y + section_height + 30
        prompt_rect = prompt_text.get_rect(center=(screen.get_width() / 2, prompt_y))
        screen.blit(prompt_text, prompt_rect)

        # Draw name input with cursor
        display_name = self.player_name if self.player_name else "_"
        name_text = regular_font.render(display_name, True, (100, 200, 255))
        name_y = prompt_y + prompt_height + 30
        name_rect = name_text.get_rect(center=(screen.get_width() / 2, name_y))
        screen.blit(name_text, name_rect)

        # Draw instructions
        instructions_font = pygame.font.SysFont("monospace", 16)
        instructions_text = instructions_font.render(
            "(Max 16 characters - Press ENTER to confirm)",
            True,
            LIGHT_GRAY,
        )
        instructions_rect = instructions_text.get_rect(
            center=(screen.get_width() / 2, name_y + name_height + 20)
        )
        screen.blit(instructions_text, instructions_rect)

        pygame.display.flip()
        self.update_color_cycle()

    def run(self, screen, game_surface, clock):
        """Run the game over screen, handling name entry if needed."""
        if self.name_entry_mode:
            # Handle name entry mode
            name_entry_complete = False
            while not name_entry_complete:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and len(self.player_name) > 0:
                            # Save the score and switch to play again mode
                            self.high_score_manager.add_score(self.player_name, self.final_score)
                            self.name_entry_mode = False
                            # Update screen for play again mode
                            self.final_score_section = f"FINAL SCORE: {self.final_score}"
                            self.prompt = "Play Again?  Y / N"
                            self.high_scores = self.high_score_manager.get_scores()
                            name_entry_complete = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        elif (
                            event.unicode.isprintable()
                            and len(self.player_name) < 16
                            and not (len(self.player_name) == 0 and event.unicode == " ")
                        ):
                            self.player_name += event.unicode

                self.draw_name_entry(screen, game_surface)
                clock.tick(60)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return True
                    elif event.key == pygame.K_n:
                        return False

            self.draw(screen, game_surface)
            clock.tick(60)
