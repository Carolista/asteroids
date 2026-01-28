import pygame

from src.game.section import Section

from ..config.constants import (
    FINAL_SCORE_COLORS,
    FONT_REGULAR,
    FONT_SCORE,
    FONT_TITLE,
    INSTRUCTION_COLORS,
    NAME_ENTRY_COLORS,
    PROMPT_COLORS,
    TITLE_COLORS,
)
from ..config.funcs import handle_exit
from .screen import Screen


class GameOverScreen(Screen):
    """Game over screen with optional high score name entry."""

    def __init__(self, final_score, high_score_manager):
        super().__init__()

        self.final_score = final_score
        self.high_score_manager = high_score_manager
        self.is_high_score = high_score_manager.is_high_score(final_score)

        self.player_name = ""
        self.name_entry_mode = self.is_high_score and final_score > 0

        self.title_section = Section(
            text_content="G A M E  O V E R",
            font_name=FONT_TITLE,
            font_size=80,
            colors=TITLE_COLORS,
            gap=0,
        )

        self.final_score_section = Section(
            text_content=f"FINAL SCORE: {final_score}",
            font_name=FONT_SCORE,
            font_size=40,
            colors=FINAL_SCORE_COLORS,
        )

        self.name_entry_prompt_section = Section(
            text_content="You got a high score! Enter your name below:",
            font_name=FONT_REGULAR,
            font_size=32,
            colors=PROMPT_COLORS,
        )

        self.replay_prompt_section = Section(
            text_content="Play Again?  Y / N",
            font_name=FONT_REGULAR,
            font_size=32,
            colors=PROMPT_COLORS,
        )

        name_entry_content = self.player_name if self.player_name else "_"
        self.name_entry_section = Section(
            text_content=name_entry_content,
            font_name=FONT_REGULAR,
            font_size=32,
            colors=NAME_ENTRY_COLORS,
        )

        self.instruction_section = Section(
            text_content="Press ENTER to confirm",
            font_name=FONT_REGULAR,
            font_size=18,
            colors=INSTRUCTION_COLORS,
        )

        self.name_entry_mode_sections = [
            self.title_section,
            self.final_score_section,
            self.name_entry_prompt_section,
            self.name_entry_section,
            self.instruction_section,
        ]

        self.replay_mode_sections = [
            self.title_section,
            self.final_score_section,
            self.replay_prompt_section,
            # high scores added after calculation if new high score
        ]

        if self.name_entry_mode:
            self.sections = self.name_entry_mode_sections
        else:
            self.sections = (
                self.replay_mode_sections + self.high_score_manager.get_high_score_sections()
            )  # noqa: E501

    def run(self, screen, game_surface, clock):
        """Handle name entry and replay prompt."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    handle_exit()
                if event.type == pygame.KEYDOWN:
                    if self.name_entry_mode:
                        if event.key == pygame.K_RETURN and len(self.player_name) > 0:
                            self.high_score_manager.add_score(self.player_name, self.final_score)
                            self.sections = (
                                self.replay_mode_sections
                                + self.high_score_manager.get_high_score_sections()
                            )  # noqa: E501
                            self.name_entry_mode = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        elif (
                            event.unicode.isprintable()
                            and len(self.player_name) < 16
                            and not (len(self.player_name) == 0 and event.unicode == " ")
                        ):
                            self.player_name += event.unicode

                        # Display underscore placeholder when empty, but don't store it
                        display_name = self.player_name if self.player_name else "_"
                        self.name_entry_section.text_content = display_name
                    else:
                        if event.key == pygame.K_y:
                            return True
                        elif event.key == pygame.K_n:
                            return False

            self.draw(screen, game_surface)
            clock.tick(60)
