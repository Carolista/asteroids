import pygame

from ..config.constants import SHOT_COLORS, STAR_COLORS
from .screen import Screen


class SplashScreen(Screen):
    """Splash screen shown at game startup."""

    def __init__(self, high_scores=None):
        super().__init__(
            title="ASTEROIDS",
            prompt="Hit Enter to Play",
            title_font_size=100,
            regular_font_size=32,
            scores_font_size=24,
            title_color=SHOT_COLORS,
            text_color=STAR_COLORS,
            high_scores=high_scores if high_scores else [],
        )

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
