# Etape 1: Choisir une image de base
FROM python:3.12-slim

# Définissez le répertoire de travail dans le conteneur
WORKDIR /code

# Copiez les fichiers de dépendances et installez-les

COPY ./api_francetravail/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le reste des fichiers de votre application dans le conteneur

COPY ./api_francetravail/ /code/


# Commande pour lancer l'application FastAPI avec Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]