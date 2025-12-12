# Plateforme de Recommandation de Produits Chanel

Une plateforme interactive de recommandation de produits Chanel utilisant l'intelligence artificielle pour proposer des produits similaires basés sur des critères visuels et textuels.

## Fonctionnalités

### 1. Recherche par Image
- Uploadez une image de produit
- IA analyse les caractéristiques visuelles
- Recommande les 10 produits les plus similaires visuellement
- Utilise le modèle CLIP (OpenAI) pour comprendre le contenu visuel

### 2. Recherche par Texte
- Saisissez une description textuelle du produit recherché
- IA analyse le contenu sémantique du texte
- Propose des produits correspondant à la description
- Utilise SentenceTransformers (all-mpnet-base-v2) pour l'analyse textuelle

### 3. Recherche Combinée
- Combinez une image ET une description textuelle
- Système hybride pondérant les similarités visuelles et textuelles
- Curseur ajustable pour équilibrer l'importance image vs texte
- Recommandations ultra-précises

## Architecture Technique

### Modèles d'IA Utilisés

#### Embeddings Visuels
- **CLIP (ViT-B/32)** - 512 dimensions ⭐ *Meilleur modèle visuel*
- **ResNet50** - 2048 dimensions  
- **Vision Transformer (ViT)** - 768 dimensions
- **CNN Personnalisé** - Dimensions variables

#### Embeddings Textuels
- **all-mpnet-base-v2** - 768 dimensions ⭐ *Meilleur modèle textuel*
- **all-MiniLM-L6-v2** - 384 dimensions (version légère)

#### Métriques de Similarité
- **Similarité Cosinus** pour comparer les embeddings
- **Pondération adaptative** pour la recherche combinée
- **Normalisation L2** des vecteurs d'embedding

### Stack Technologique
- **Frontend**: Streamlit (interface web interactive)
- **Backend**: Python + PyTorch + Transformers
- **IA**: OpenAI CLIP + Sentence Transformers
- **Déployement**: Docker + Docker Compose
- **Data**: Pandas + NumPy + Scikit-learn

## Installation et Déployement

### Prérequis
- Docker et Docker Compose installés
- Modèles pré-entraînés dans le dossier `Chanel_Recommendation_Models/`

### 1. Cloner le Projet
```bash
git clone <repository-url>
cd 8INF919-recommandation-produits-chanel
```

### 2. Vérifier les Modèles
Assurez-vous que le dossier `Chanel_Recommendation_Models-20251211T193057Z-3-001/Chanel_Recommendation_Models/` contient :
```
├── cnn_embedding_model.h5
├── cnn_model.h5/
├── df_clean_indexed.csv
├── df_clean_indexed_with_embeddings.pkl
├── embeddings_textuels.npz
├── embeddings_visuels.npz
├── label_encoder.pkl
└── text_models_info.pkl
```

### 3. Déployement Docker
```bash
# Construire et lancer la plateforme
docker-compose up --build

# Ou en mode détaché
docker-compose up -d --build
```

### 4. Accéder à la Plateforme
- **URL**: http://localhost:8501
- **Interface**: Interface web Streamlit interactive

### 5. Tests (Optionnel)
```bash
# Installer les dépendances localement pour les tests
pip install -r requirements.txt

# Exécuter les tests
python test_system.py
```

## 🎮 Guide d'Utilisation

### Interface Principale
1. **Navigation Sidebar** : Choisissez le type de recherche
2. **Paramètres** : Ajustez le nombre de recommandations (5-20)
3. **Zone Principale** : Interface de recherche et résultats

### Mode Recherche par Image
1. Cliquez sur "Recherche par image"
2. Uploadez une image (JPG, PNG, JPEG)
3. Cliquez "🔍 Rechercher des produits similaires"
4. Visualisez les recommandations avec scores de similarité

### Mode Recherche par Texte
1. Sélectionnez "Recherche par texte"
2. Saisissez votre description (ex: "sac noir élégant", "parfum floral")
3. Cliquez "🔍 Rechercher des produits"
4. Explorez les résultats correspondants

### Mode Recherche Combinée
1. Choisissez "Recherche combinée"
2. Uploadez une image de référence
3. Ajoutez une description complémentaire
4. Ajustez le curseur Image/Texte selon vos préférences
5. Lancez la recherche combinée

### Interprétation des Résultats
- **Score de Similarité** : 0.000 à 1.000 (plus élevé = plus similaire)
- **Catégorie** : Type de produit Chanel
- **Prix** : Prix en euros si disponible
- **Code Produit** : Référence unique Chanel

## Configuration Avancée

### Personnaliser les Modèles
Modifiez `config.py` pour ajuster :
- Modèles d'IA utilisés
- Dimensions des embeddings
- Paramètres de recherche
- Interface utilisateur

### Variables d'Environnement Docker
```yaml
environment:
  - STREAMLIT_THEME_PRIMARY_COLOR=#000000
  - STREAMLIT_THEME_BACKGROUND_COLOR=#FFFFFF
  - PYTHONPATH=/app
```

### Optimisation Performance
- **GPU** : Décommentez les configurations CUDA dans le Dockerfile
- **Mémoire** : Ajustez les limits dans docker-compose.yml
- **Cache** : Les embeddings sont pré-calculés pour une performance optimale

## Dataset

### Statistiques
- **~1000+ produits Chanel** (chaussures, sacs, parfums, cosmétiques, etc.)
- **18 catégories principales** (HANDBAGS, SHOES, READY-TO-WEAR, etc.)
- **Images HD** redimensionnées et normalisées
- **Métadonnées riches** (titre, catégorie, prix, code produit)

### Préprocessing Appliqué
1. **Images** : Redimensionnement 224x224, normalisation RGB, padding blanc
2. **Texte** : Enrichissement avec catégories + prix, nettoyage des données
3. **Embeddings** : Pré-calculés et optimisés pour la performance

## Validation et Métriques

### Métriques de Qualité
- **Silhouette Score** : Qualité des clusters par catégorie
- **Cohérence Intra-classe** : Similarité des produits de même catégorie  
- **Séparation Inter-classe** : Distinction entre catégories différentes

### Tests de Validation
- Tests sur cas pratiques réels
- Comparaison multi-méthodes (CNN vs CLIP vs ViT vs BERT)
- Analyse t-SNE des espaces d'embedding

## Évolutions Futures

### Fonctionnalités Envisagées
-  **Authentification utilisateur** avec profils personnalisés
-  **Base de données** PostgreSQL pour persistence
-  **Analytics** et tracking des interactions
-  **Filtres avancés** par prix, couleur, taille
-  **API REST** pour intégration mobile
-  **Fine-tuning** des modèles sur données Chanel spécifiques

### Scalabilité
- Déployement Kubernetes pour haute disponibilité
- Cache Redis pour améliorer les temps de réponse
- CDN pour distribution optimale des images
- Load balancing pour gestion de charge

## Contributeurs

**Équipe de développement :**
- Johanu GANDONOU
- Maxime MARECESCHE  
- Salomon KABONGO
- Arno BIDET

---

## Support Technique

### Problèmes Fréquents

**Erreur de chargement des modèles**
```bash
# Vérifier les permissions
chmod -R 755 Chanel_Recommendation_Models/

# Reconstruire l'image Docker
docker-compose down
docker-compose up --build --force-recreate
```

**Mémoire insuffisante**
```yaml
# Dans docker-compose.yml
services:
  chanel-recommendation:
    deploy:
      resources:
        limits:
          memory: 4G
```

**Port déjà utilisé**
```bash
# Changer le port dans docker-compose.yml
ports:
  - "8502:8501"  # Utiliser 8502 au lieu de 8501
```

### Logs et Debugging
```bash
# Voir les logs de l'application
docker-compose logs -f chanel-recommendation

# Accéder au container pour debugging
docker-compose exec chanel-recommendation bash
```

---

📧 **Contact** : Pour questions techniques ou contributions, contactez l'équipe de développement.

🎯 **Objectif** : Révolutionner l'expérience d'achat Chanel grâce à l'IA et aux technologies de recommendation avancées.
