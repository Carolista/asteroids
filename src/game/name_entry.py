import pygame

from ..config.constants import (
    BLACK,
    FONT_REGULAR,
    FONT_TITLE,
    GAME_OVER_COLOR,
    PROMPT_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class NameEntryOverlay:
    def __init__(self):
        self.name = ""
        self.max_length = 16

    def draw(self, screen):
        """Draw the name entry overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # "New High Score!" text
        title_font = pygame.font.Font(FONT_TITLE, 48)
        title_text = title_font.render("NEW HIGH SCORE!", True, GAME_OVER_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80))
        screen.blit(title_text, title_rect)

        # "Enter Your Name:" prompt
        prompt_font = pygame.font.Font(FONT_REGULAR, 32)
        prompt_text = prompt_font.render("Enter Your Name:", True, PROMPT_COLOR)
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 10))
        screen.blit(prompt_text, prompt_rect)

        # Name input field with cursor
        input_font = pygame.font.Font(FONT_REGULAR, 40)
        display_name = self.name if self.name else "_"
        input_text = input_font.render(display_name, True, (100, 200, 255))
        input_rect = input_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        screen.blit(input_text, input_rect)

        # Instructions
        instructions_font = pygame.font.Font(FONT_REGULAR, 20)
        instructions_text = instructions_font.render(
            "(Max 16 characters - Press ENTER to confirm)", True, PROMPT_COLOR
        )
        instructions_rect = instructions_text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 110)
        )
        screen.blit(instructions_text, instructions_rect)

    def run(self, screen, clock):
        """Run the name entry overlay until player presses Enter."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None  # Signal to quit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(self.name) > 0:
                        return self.name  # Return the entered name
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif (
                        event.unicode.isprintable()
                        and len(self.name) < self.max_length
                        and not (len(self.name) == 0 and event.unicode == " ")
                    ):
                        self.name += event.unicode

            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)
