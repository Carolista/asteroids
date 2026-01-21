import json
import os

from ..config.constants import FONT_REGULAR


class HighScoreManager:
    def __init__(self, high_scores_file):
        self.high_scores_file = high_scores_file
        self.scores = self.load_scores()

    def load_scores(self):
        """Load high scores from file or return empty list if file doesn't exist."""
        if os.path.exists(self.high_scores_file):
            try:
                with open(self.high_scores_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_scores(self):
        """Save high scores to file."""
        os.makedirs(os.path.dirname(self.high_scores_file), exist_ok=True)
        with open(self.high_scores_file, "w") as f:
            json.dump(self.scores, f, indent=2)

    def is_high_score(self, score):
        """Check if a score qualifies for the high score list."""
        if len(self.scores) < 5:
            return True
        return score > self.scores[-1]["score"]

    def get_rank(self, score):
        """Get the rank position for a score (-1 if not in top 5)."""
        if not self.is_high_score(score):
            return -1
        for i, entry in enumerate(self.scores):
            if score > entry["score"]:
                return i
        return len(self.scores)

    def add_score(self, name, score):
        """Add a score to the high score list (assumes it qualifies)."""
        rank = self.get_rank(score)
        if rank == -1:
            return

        new_entry = {"name": name, "score": score}
        self.scores.insert(rank, new_entry)

        # Keep only top 5
        if len(self.scores) > 5:
            self.scores = self.scores[:5]

        self.save_scores()

    def get_scores(self):
        """Return the current high score list."""
        return self.scores


# def draw_high_scores(screen, high_scores, x, y, color):
#     """Draw high scores list on screen with right-justified scores."""
#     font = __import__("pygame").font.Font(FONT_REGULAR, 24)

#     for i, entry in enumerate(high_scores):
#         rank = i + 1
#         name = entry["name"]
#         score = str(entry["score"])

#         # Format: "1. NAME            123456"
#         # Name padded to 16 chars, 4 spaces, score right-justified to 6 chars
#         name_padded = name.ljust(16)
#         score_padded = score.rjust(6)
#         text = f"{rank}. {name_padded}    {score_padded}"

#         score_text = font.render(text, True, color)
#         screen.blit(score_text, (x, y + i * 30))


def draw_high_scores_centered(screen, high_scores, center_x, y, color):
    """Draw high scores list on screen centered horizontally with right-justified scores."""
    font = __import__("pygame").font.Font(FONT_REGULAR, 24)

    for i, entry in enumerate(high_scores):
        rank = i + 1
        name = entry["name"].upper()
        score = str(entry["score"]).upper()

        # Format: "1. NAME            123456"
        # Name padded to 16 chars, 4 spaces, score right-justified to 6 chars
        name_padded = name.ljust(16)
        score_padded = score.rjust(6)
        text = f"{rank}. {name_padded}    {score_padded}"

        score_text = font.render(text, True, color)
        score_rect = score_text.get_rect(center=(center_x, y + i * 30))
        screen.blit(score_text, score_rect)
