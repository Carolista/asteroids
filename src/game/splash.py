import pygame

from src.config.constants import FONT_REGULAR, FONT_TITLE, PROMPT_COLORS, TITLE_COLORS

from ..config.funcs import handle_exit
from .screen import Screen
from .section import Section


class SplashScreen(Screen):
    """Splash screen shown at game startup."""

    def __init__(self, high_score_manager):
        super().__init__()

        self.title_section = Section(text_content="ASTEROIDS", font_name=FONT_TITLE, font_size=100, colors=TITLE_COLORS, gap=0)  # noqa: E501
        self.prompt_section = Section(text_content="Hit Enter to Play", font_name=FONT_REGULAR, font_size=36, colors=PROMPT_COLORS)  # noqa: E501
        self.high_score_sections = high_score_manager.get_high_score_sections()

        self.sections.append(self.title_section)
        self.sections.append(self.prompt_section)

        self.sections += self.high_score_sections

    def run(self, screen, game_surface, clock):
        """Run the splash screen until Enter is pressed."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    handle_exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True  # Signal to start the game

            self.draw(screen, game_surface)
            clock.tick(60)
