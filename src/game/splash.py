import pygame

from ..config.funcs import handle_exit
from .screen import Screen


class SplashScreen(Screen):
    """Splash screen shown at game startup."""

    def __init__(self, high_scores_list=None):
        super().__init__(
            title_content="ASTEROIDS",
            prompt_content="Hit Enter to Play",
            high_scores_list=high_scores_list if high_scores_list else [],
        )

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
