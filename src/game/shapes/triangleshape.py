from .shape import Shape


class TriangleShape(Shape):
    """Triangular game object with polygon-based collision."""

    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        self.rotation = 0

    def get_triangle_points(self):
        """Get triangle vertices. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement get_triangle_points()")

    @staticmethod
    def _point_in_triangle(point, triangle):
        """Check if a point is inside a triangle using barycentric coordinates."""
        x, y = point
        x1, y1 = triangle[0]
        x2, y2 = triangle[1]
        x3, y3 = triangle[2]

        denominator = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        if abs(denominator) < 0.0001:
            return False

        a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denominator
        b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denominator
        c = 1 - a - b

        return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1

    @staticmethod
    def _circle_intersects_triangle(circle_pos, circle_radius, triangle):
        """Check if a circle intersects with a triangle."""
        # Check if circle center is inside triangle
        if TriangleShape._point_in_triangle(circle_pos, triangle):
            return True

        # Check if any triangle vertex is inside the circle
        for vertex in triangle:
            if circle_pos.distance_to(vertex) <= circle_radius:
                return True

        # Check if circle intersects any edge of the triangle
        for i in range(3):
            v1 = triangle[i]
            v2 = triangle[(i + 1) % 3]

            # Find closest point on line segment to circle center
            edge = v2 - v1
            edge_length_sq = edge.length_squared()

            if edge_length_sq == 0:
                # Degenerate edge (point)
                if circle_pos.distance_to(v1) <= circle_radius:
                    return True
                continue

            # Project circle center onto edge
            t = max(0, min(1, (circle_pos - v1).dot(edge) / edge_length_sq))
            closest_point = v1 + edge * t

            if circle_pos.distance_to(closest_point) <= circle_radius:
                return True

        return False

    def collides_with(self, other):
        """Check collision between triangle and another shape."""
        if hasattr(other, "radius"):
            # Colliding with a circle
            return self._circle_intersects_triangle(
                other.position, other.radius, self.get_triangle_points()
            )
        else:
            # Colliding with another triangle (not implemented yet)
            raise NotImplementedError("Triangle-to-triangle collision not implemented")
