# Point d’entrée du serveur Flask

from flask import Flask, render_template, request, redirect, url_for
from blog.models import Article
from blog.storage import save_article, load_all_articles, load_article ,delete_article
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # ⚠️ à remplacer par une vraie clé sécurisée

# ================= ROUTES PUBLIQUES =================
@app.route("/")
def home():
    articles = load_all_articles()
    return render_template("home.html", articles=articles)

@app.route("/article/<title>")
def article(title):
    article = load_article(title)
    if not article:
        return "Article introuvable", 404
    return render_template("article.html", article=article)

# ================= ROUTES ADMIN =================

@app.route("/admin/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    articles = load_all_articles()
    return render_template("dashboard.html", articles=articles)

@app.route("/admin/add", methods=["GET", "POST"])
def add_article():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        date = request.form.get("date")

        if not title or not content:
            error = "Le titre et le contenu sont obligatoires."
            return render_template("add_article.html", error=error)

        article = Article(title=title, content=content, date=date)
        save_article(article)
        return redirect(url_for("dashboard"))

    return render_template("add_article.html")

@app.route("/admin/edit/<title>", methods=["GET", "POST"])
def edit_article(title):

    article = load_article(title)
    if not article:
        return "Article introuvable", 404

    if request.method == "POST":
        new_title = request.form.get("title")
        new_content = request.form.get("content")
        new_date = request.form.get("date")

        if not new_title or not new_content:
            error = "Le titre et le contenu sont obligatoires."
            return render_template("edit_article.html", article=article, error=error)

        # Supprimer l’ancien fichier si le titre change
        if new_title != title:
            delete_article(title)

        updated = Article(title=new_title, content=new_content, date=new_date)
        save_article(updated)
        return redirect(url_for("dashboard"))

    return render_template("edit_article.html", article=article)

@app.route("/admin/delete/<title>", methods=["POST"])
def delete_article_route(title):
    if delete_article(title):
        return redirect(url_for("dashboard"))
    return "Article introuvable", 404


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Vérification simple (hardcodée)
        if username == "admin" and password == "password123":
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "Identifiants incorrects"
            return render_template("login.html", error=error)

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))


# ================= MAIN =================
if __name__ == "__main__":
    # Crée un article de test si aucun n’existe
    if not load_all_articles():
        demo = Article(title="Mon premier article", content="Bienvenue sur mon blog !")
        save_article(demo)

    # Affiche les articles en console
    for a in load_all_articles():
        print(a.title, "-", a.date)

    # Lance le serveur Flask
    app.run(debug=True)

# Concepts appliqués
# Gestion des exceptions : si l’article n’existe pas → 404.

# Manipulation de fichiers : suppression et remplacement des fichiers JSON.

# Fonctions utilitaires : delete_article pour centraliser la logique.

# Form handling : formulaire pré-rempli pour l’édition.

print("Hello, Captain!")