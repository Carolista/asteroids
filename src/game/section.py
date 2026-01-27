import pygame

from src.config.constants import SCREEN_WIDTH, WHITE


class Section:

    def __init__(self, text_content, font_name, font_size, colors, gap=30):
        self.text_content = text_content
        self.font_name = font_name
        self.font_size = font_size
        self.colors = colors # list
        self.current_color = WHITE
        self.gap = gap

        self.render_text = None
        self.height = None
        self.rectangle = None

    def update_text_content(self, text_content):
        self.text_content = text_content

    def update_current_color(self, color_index):
        print(f'current index for {self.text_content} is {color_index}')
        self.current_color = self.colors[color_index]

    def update_render_text(self):
        font = pygame.font.Font(self.font_name, self.font_size)
        self.render_text = font.render(self.text_content, True, self.current_color)

    def update_height(self):
        self.height = self.render_text.get_height()

    def update_gap(self, gap):
        self.gap = gap

    def update_rectangle(self, current_y):
        self.rectangle = self.render_text.get_rect(center=(SCREEN_WIDTH / 2, current_y))

    def get_y_adjustment(self):
        self.update_render_text()
        self.update_height()
        return self.height + self.gap
