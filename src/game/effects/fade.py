import pygame

from ...config.constants import BLACK, SCREEN_HEIGHT, SCREEN_WIDTH


class Fade:
    """Screen fade-in/fade-out transition effect."""

    def __init__(self, duration=1.0):
        """
        Initialize fade effect.

        Args:
            duration: Time in seconds for fade transition
        """
        self.duration = duration
        self.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface.fill(BLACK)

    def fade_out(self, screen, game_surface, drawable, clock):
        """
        Fade to black while keeping game objects stationary.

        Args:
            screen: Display surface
            game_surface: Game rendering surface
            drawable: Sprite group to render
            clock: Pygame clock
        """
        elapsed = 0
        while elapsed < self.duration:
            dt = clock.tick(60) / 1000
            elapsed += dt

            # Render game without updating positions
            game_surface.fill(BLACK)
            for obj in drawable:
                obj.draw(game_surface)
            screen.blit(game_surface, (0, 0))

            # Apply fade overlay
            alpha = int((elapsed / self.duration) * 255)
            self.surface.set_alpha(alpha)
            screen.blit(self.surface, (0, 0))

            pygame.display.flip()

    def fade_in(self, screen, game_surface, drawable, clock):
        """
        Fade from black while keeping game objects stationary.

        Args:
            screen: Display surface
            game_surface: Game rendering surface
            drawable: Sprite group to render
            clock: Pygame clock
        """
        elapsed = 0
        while elapsed < self.duration:
            dt = clock.tick(60) / 1000
            elapsed += dt

            # Render game without updating positions
            game_surface.fill(BLACK)
            for obj in drawable:
                obj.draw(game_surface)
            screen.blit(game_surface, (0, 0))

            # Apply fade overlay (inverse)
            alpha = int((1 - elapsed / self.duration) * 255)
            self.surface.set_alpha(alpha)
            screen.blit(self.surface, (0, 0))

            pygame.display.flip()

    def fade_text_out(
        self, screen, game_surface, drawable, updatable, sections, color_index, clock
    ):
        """
        Fade text sections to transparent while keeping background visible.

        Args:
            screen: Display surface
            game_surface: Game rendering surface (for stars)
            drawable: Background objects to keep visible
            updatable: Objects to update (asteroids, etc.)
            sections: List of Section objects to fade out
            color_index: Current color index for sections
            clock: Pygame clock
        """
        from ...config.constants import SCREEN_HEIGHT

        elapsed = 0
        # Create a surface for text with per-pixel alpha
        text_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

        while elapsed < self.duration:
            dt = clock.tick(60) / 1000
            elapsed += dt

            # Update object positions
            updatable.update(dt)

            # Draw background (stars and asteroids) to game_surface then to screen
            from ...config.constants import SCREEN_COLOR

            game_surface.fill(SCREEN_COLOR)
            for obj in drawable:
                obj.draw(game_surface)
            screen.blit(game_surface, (0, 0))

            # Calculate alpha (255 to 0)
            alpha = int((1 - elapsed / self.duration) * 255)

            # Clear text surface and render sections with alpha
            text_surface.fill((0, 0, 0, 0))

            # Calculate starting y position to center vertically
            total_height = sum(section.get_y_adjustment() for section in sections)
            current_y = (SCREEN_HEIGHT - total_height) // 2

            for section in sections:
                section.update_current_color(color_index)
                section.update_render_text()
                section.update_rectangle(current_y)
                # Set alpha on the rendered text
                section.render_text.set_alpha(alpha)
                text_surface.blit(section.render_text, section.rectangle)
                current_y += section.height + section.gap

            # Blit text surface to screen
            screen.blit(text_surface, (0, 0))
            pygame.display.flip()

    def fade_text_in(self, screen, game_surface, drawable, updatable, sections, color_index, clock):
        """
        Fade text sections from transparent to opaque while keeping background visible.

        Args:
            screen: Display surface
            game_surface: Game rendering surface (for stars)
            drawable: Background objects to keep visible
            updatable: Objects to update (asteroids, etc.)
            sections: List of Section objects to fade in
            color_index: Current color index for sections
            clock: Pygame clock
        """
        from ...config.constants import SCREEN_HEIGHT

        elapsed = 0
        # Create a surface for text with per-pixel alpha
        text_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

        while elapsed < self.duration:
            dt = clock.tick(60) / 1000
            elapsed += dt

            # Update object positions
            updatable.update(dt)

            # Draw background (stars and asteroids) to game_surface then to screen
            from ...config.constants import SCREEN_COLOR

            game_surface.fill(SCREEN_COLOR)
            for obj in drawable:
                obj.draw(game_surface)
            screen.blit(game_surface, (0, 0))

            # Calculate alpha (0 to 255)
            alpha = int((elapsed / self.duration) * 255)

            # Clear text surface and render sections with alpha
            text_surface.fill((0, 0, 0, 0))

            # Calculate starting y position to center vertically
            total_height = sum(section.get_y_adjustment() for section in sections)
            current_y = (SCREEN_HEIGHT - total_height) // 2

            for section in sections:
                section.update_current_color(color_index)
                section.update_render_text()
                section.update_rectangle(current_y)
                # Set alpha on the rendered text
                section.render_text.set_alpha(alpha)
                text_surface.blit(section.render_text, section.rectangle)
                current_y += section.height + section.gap

            # Blit text surface to screen
            screen.blit(text_surface, (0, 0))
            pygame.display.flip()

    def fade_text_in_out(self, screen, text_surface, position, hold_duration=1.0):
        """
        Fade text in, hold, then fade out while keeping background unchanged.

        Args:
            screen: Display surface
            text_surface: Rendered text surface to fade
            position: (x, y) center position for text
            hold_duration: Time to display text at full opacity
        """
        # Fade in
        elapsed = 0
        snapshot = screen.copy()

        while elapsed < self.duration:
            dt = pygame.time.Clock().tick(60) / 1000
            elapsed += dt

            screen.blit(snapshot, (0, 0))

            alpha = int((elapsed / self.duration) * 255)
            text_surface.set_alpha(alpha)
            text_rect = text_surface.get_rect(center=position)
            screen.blit(text_surface, text_rect)

            pygame.display.flip()

        # Hold at full opacity
        elapsed = 0
        while elapsed < hold_duration:
            dt = pygame.time.Clock().tick(60) / 1000
            elapsed += dt

            screen.blit(snapshot, (0, 0))
            text_surface.set_alpha(255)
            text_rect = text_surface.get_rect(center=position)
            screen.blit(text_surface, text_rect)

            pygame.display.flip()

        # Fade out
        elapsed = 0
        while elapsed < self.duration:
            dt = pygame.time.Clock().tick(60) / 1000
            elapsed += dt

            screen.blit(snapshot, (0, 0))

            alpha = int((1 - elapsed / self.duration) * 255)
            text_surface.set_alpha(alpha)
            text_rect = text_surface.get_rect(center=position)
            screen.blit(text_surface, text_rect)

            pygame.display.flip()
