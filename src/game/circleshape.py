from .shape import Shape


class CircleShape(Shape):
    """Circular game object with radius-based collision."""

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.radius = radius  # Alias for size

    def collides_with(self, other):
        """Check circle-to-circle collision."""
        if not hasattr(other, "radius"):
            # If other is not a circle, delegate to its collision method
            return other.collides_with(self)
        return self.position.distance_to(other.position) <= self.radius + other.radius
