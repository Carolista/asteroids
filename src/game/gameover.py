import pygame

from ..config.constants import (
    FONT_REGULAR,
    FONT_SCORE,
    FONT_TITLE,
    NAME_ENTRY_COLORS,
    SCREEN_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WHITE,
)
from ..config.funcs import handle_exit
from .screen import Screen


class GameOverScreen(Screen):
    """Game over screen with optional high score name entry."""

    def __init__(self, final_score, high_score_manager):
        self.final_score = final_score
        self.high_score_manager = high_score_manager
        self.is_high_score = high_score_manager.is_high_score(final_score)
        self.player_name = ""
        self.name_entry_mode = self.is_high_score and final_score > 0
        self.name_entry_font_size = 28
        self.name_entry_colors = NAME_ENTRY_COLORS

        # Initialize parent with appropriate text
        if self.name_entry_mode:
            prompt = "You got a high score! Enter your name below:"
        else:
            prompt = "Play Again?  Y / N"

        super().__init__(
            title_content="G A M E  O V E R",
            final_score_content=f"FINAL SCORE: {final_score}",
            prompt_content=prompt,
            high_scores_list=high_score_manager.get_scores() if not self.name_entry_mode else [],
            title_font_size=80,
        )

    def draw_name_entry(self, screen, game_surface):
        """Draw the game over screen with name entry field."""
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
        name_entry_font = pygame.font.Font(FONT_REGULAR, self.name_entry_font_size)

        # Pre-measure heights (these won't be displayed)
        title_text_dummy = title_font.render(self.title_content, True, WHITE)
        title_height = title_text_dummy.get_height()

        final_score_text_dummy = final_score_font.render(self.final_score_content, True, WHITE)
        final_score_height = final_score_text_dummy.get_height()

        prompt_text_dummy = prompt_font.render(self.prompt_content, True, WHITE)
        prompt_height = prompt_text_dummy.get_height()

        name_entry_content = self.player_name if self.player_name else "_"
        name_text_dummy = name_entry_font.render(name_entry_content, True, WHITE)
        name_entry_height = name_text_dummy.get_height()

        # Calculate total height for vertical centering
        total_height = (
            title_height
            + 30
            + final_score_height + 30
            + prompt_height
            + 30
            + name_entry_height
        )

        # Calculate starting y position to center vertically
        start_y = (SCREEN_HEIGHT - total_height) // 2

        # Draw title
        title_color = self.get_current_color(self.title_colors)
        title_text = title_font.render(self.title_content, True, title_color)
        title_rect = title_text.get_rect(center=(screen.get_width() / 2, start_y))
        screen.blit(title_text, title_rect)

        # Draw final score section
        current_y = start_y + title_height + 30
        final_score_color = self.get_current_color(self.final_score_colors)
        final_score_text = final_score_font.render(self.final_score_content, True, final_score_color)  # noqa: E501
        final_score_section_rect = final_score_text.get_rect(center=(SCREEN_WIDTH / 2, current_y))
        screen.blit(final_score_text, final_score_section_rect)

        # Draw prompt
        current_y += final_score_height + 30
        prompt_color = self.get_current_color(self.prompt_colors)
        prompt_text = prompt_font.render(self.prompt_content, True, prompt_color)
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH / 2, current_y))
        screen.blit(prompt_text, prompt_rect)

        # Draw name input with cursor
        current_y += prompt_height + 30
        name_entry_content = self.player_name if self.player_name else "_"
        name_entry_color = self.get_current_color(self.name_entry_colors)
        name_entry_text = name_entry_font.render(name_entry_content, True, name_entry_color)
        name_rect = name_entry_text.get_rect(center=(screen.get_width() / 2, current_y))
        screen.blit(name_entry_text, name_rect)

        # Draw instructions
        current_y += name_entry_height + 30
        instructions_font = pygame.font.SysFont("monospace", 16)
        instructions_text = instructions_font.render(
            "(Max 16 characters - Press ENTER to confirm)",
            True,
            WHITE,
        )
        instructions_rect = instructions_text.get_rect(
            center=(screen.get_width() / 2, current_y)
        )
        screen.blit(instructions_text, instructions_rect)

        pygame.display.flip()
        self.update_color_cycle(self.high_scores_list_colors)

    def run(self, screen, game_surface, clock):
        """Run the game over screen, handling name entry if needed."""
        if self.name_entry_mode:
            # Handle name entry mode
            name_entry_complete = False
            while not name_entry_complete:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        handle_exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and len(self.player_name) > 0:
                            # Save the score and switch to play again mode
                            self.high_score_manager.add_score(self.player_name, self.final_score)  # noqa: E501
                            self.name_entry_mode = False
                            # Update screen for play again mode
                            self.prompt_content = "Play Again?  Y / N"
                            self.high_scores_list = self.high_score_manager.get_scores()
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
                    handle_exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return True
                    elif event.key == pygame.K_n:
                        return False

            self.draw(screen, game_surface)
            clock.tick(60)
