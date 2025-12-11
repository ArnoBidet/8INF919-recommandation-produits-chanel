# Utiliser une image de base avec Python pré-installé pour optimiser le cache
FROM python:3.11-slim

# Variables d'environnement pour optimiser pip et Python
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Installer les dépendances système (couche mise en cache)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1-mesa-dri \
    libglu1-mesa \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Définir le répertoire de travail
WORKDIR /app

# ÉTAPE 1: Installer d'abord les dépendances lourdes séparément
# Ces packages changent rarement, donc on les met en cache
COPY requirements-base.txt .
RUN pip install --no-cache-dir -r requirements-base.txt

# ÉTAPE 2: Copier et installer les requirements complets
# Cette couche ne se reconstruit que si requirements.txt change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ÉTAPE 3: Copier les modèles pré-entraînés
# Cette couche est relativement stable mais volumineuse
COPY Chanel_Recommendation_Models-20251211T193057Z-3-001/Chanel_Recommendation_Models/ /app/models/

# ÉTAPE 4: Copier le code de l'application (dernière étape pour maximiser le cache)
# Cette couche se reconstruit uniquement si le code change
COPY main.py .
COPY src/ ./src/

# Port d'exposition pour Streamlit
EXPOSE 8501

# Configuration Streamlit
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Commande de démarrage
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
