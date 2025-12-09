# blog/storage.py
import os
import json
from blog.models import Article

ARTICLES_DIR = "data/articles"

def save_article(article: Article):
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    filename = os.path.join(ARTICLES_DIR, f"{article.title}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(article.to_dict(), f, ensure_ascii=False, indent=4)

def load_article(title: str) -> Article | None:
    filename = os.path.join(ARTICLES_DIR, f"{title}.json")
    if not os.path.exists(filename):
        return None
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        return Article.from_dict(data)

def load_all_articles() -> list[Article]:
    articles = []
    if not os.path.exists(ARTICLES_DIR):
        return articles
    for file in os.listdir(ARTICLES_DIR):
        if file.endswith(".json"):
            with open(os.path.join(ARTICLES_DIR, file), "r", encoding="utf-8") as f:
                data = json.load(f)
                articles.append(Article.from_dict(data))
    return articles

def delete_article(title: str) -> bool:
    """Supprime un article par son titre."""
    filename = os.path.join(ARTICLES_DIR, f"{title}.json")
    if os.path.exists(filename):
        os.remove(filename)
        return True
    return False


# Concepts appliqués
# Gestion des exceptions : si l’article n’existe pas → 404.

# Manipulation de fichiers : suppression et remplacement des fichiers JSON.

# Fonctions utilitaires : delete_article pour centraliser la logique.

# Form handling : formulaire pré-rempli pour l’édition.