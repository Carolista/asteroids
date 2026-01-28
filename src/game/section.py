import pygame

from src.config.constants import DEFAULT_SECTION_GAP, SCREEN_WIDTH, WHITE


class Section:
    """Renderable text section with color cycling."""

    def __init__(self, text_content, font_name, font_size, colors, gap=DEFAULT_SECTION_GAP):
        self.text_content = text_content
        self.font_name = font_name
        self.font_size = font_size
        self.colors = colors  # list
        self.current_color = WHITE
        self.gap = gap

        self.render_text = None
        self.height = None
        self.rectangle = None

    def update_current_color(self, color_index):
        """Set color from list based on cycle index."""
        self.current_color = self.colors[color_index]

    def update_render_text(self):
        """Render text with current color."""
        font = pygame.font.Font(self.font_name, self.font_size)
        self.render_text = font.render(self.text_content, True, self.current_color)

    def update_height(self):
        """Calculate rendered text height."""
        self.height = self.render_text.get_height()

    def update_rectangle(self, current_y):
        """Position text at vertical coordinate."""
        self.rectangle = self.render_text.get_rect(center=(SCREEN_WIDTH / 2, current_y))

    def get_y_adjustment(self):
        """Calculate total vertical space needed."""
        self.update_render_text()
        self.update_height()
        return self.height + self.gap
