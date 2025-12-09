FROM python:3.12-alpine

# Définir un répertoire de travail
WORKDIR /app

# Copier tout le projet (y compris blog/, app.py, requirements.txt)
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut
CMD ["python", "app.py"]
