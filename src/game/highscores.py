import json
import os

from src.config.constants import FONT_SCORE, HIGH_SCORES_LIST_COLORS

from .section import Section


class HighScoreManager:
    """Manage top 5 high scores with persistence."""

    def __init__(self, high_scores_file):
        self.high_scores_file = high_scores_file
        self.scores = self.load_scores()

    def load_scores(self):
        """Load scores from JSON file."""
        if os.path.exists(self.high_scores_file):
            try:
                with open(self.high_scores_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_scores(self):
        """Persist scores to JSON file."""
        os.makedirs(os.path.dirname(self.high_scores_file), exist_ok=True)
        with open(self.high_scores_file, "w") as f:
            json.dump(self.scores, f, indent=2)

    def is_high_score(self, score):
        """Check if score qualifies for top 5."""
        if len(self.scores) < 5:
            return True
        return score > self.scores[-1]["score"]

    def get_rank(self, score):
        """Get position in leaderboard (-1 if not qualifying)."""
        if not self.is_high_score(score):
            return -1
        for i, entry in enumerate(self.scores):
            if score > entry["score"]:
                return i
        return len(self.scores)

    def add_score(self, name, score):
        """Insert new score and maintain top 5."""
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
        """Return current high scores list."""
        return self.scores

    def get_high_score_sections(self):
        """Create formatted Section objects for display."""
        high_score_sections = []

        for i, entry in enumerate(self.scores):
            rank = i + 1
            name = entry["name"].upper()
            score = str(entry["score"]).upper()

            # Format: "1. NAME            123456"
            name_padded = name.ljust(16)
            score_padded = score.rjust(6)
            high_score_content = f"{rank}. {name_padded}    {score_padded}"

            new_section = Section(
                text_content=high_score_content,
                font_name=FONT_SCORE,
                font_size=28,
                colors=HIGH_SCORES_LIST_COLORS,
                gap=0,
            )
            high_score_sections.append(new_section)

        return high_score_sections
