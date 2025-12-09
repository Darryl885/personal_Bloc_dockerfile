# (Articles, classes de données)
# blog/models.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Article:
    title: str
    content: str
    date: str = datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        """Convertit l'article en dictionnaire (utile pour JSON)."""
        return {
            "title": self.title,
            "content": self.content,
            "date": self.date,
        }

    @staticmethod
    def from_dict(data: dict):
        """Crée un Article à partir d'un dictionnaire JSON."""
        return Article(
            title=data["title"],
            content=data["content"],
            date=data.get("date", datetime.now().strftime("%Y-%m-%d"))
        )
