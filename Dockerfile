# 1. Partir d'une image Python légère (slim)
FROM python:3.12-slim

# 2. Définir le dossier de travail dans le conteneur
WORKDIR /app

# 3. Copier d'abord requirements.txt (pour le cache Docker)
COPY requirements.txt .

# 4. Installer les dépendances sans garder le cache (pour réduire la taille)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copier le reste du code
COPY app.py auth.py ./

# 6. Créer un utilisateur non-root pour la sécurité et lui donner les droits sur /app
RUN useradd -m appuser && chown -R appuser /app

# 7. S'exécuter en tant que cet utilisateur
USER appuser

# 8. Exposer le port
EXPOSE 5000

# 9. Lancer l'application avec Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]