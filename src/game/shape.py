import pygame


class Shape(pygame.sprite.Sprite):
    """Base class for game objects with position and velocity."""

    def __init__(self, x, y, size):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.size = size  # Generic size property (radius for circles, etc.)

    def draw(self, screen):
        """Render the shape. Override in subclasses."""
        pass

    def update(self, dt):
        """Update shape state. Override in subclasses."""
        pass

    def collides_with(self, other):
        """Check collision with another shape. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement collides_with()")
