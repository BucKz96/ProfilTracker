# Etape 1: Choisir une image de base
FROM python:3.12-slim

# Etape 2: Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Etape 3: Copier le fichier de dépendances et installer les dépendances
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Etape 4: Copier le reste du code source de l'API dans le conteneur
COPY ./app.py /app/app.py

# Etape 5: Exposer le port sur lequel l'API s'exécute
EXPOSE 5000

# Etape 6: Définir la commande pour démarrer l'application
CMD ["python", "app.py"]
