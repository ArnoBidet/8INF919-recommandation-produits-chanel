# 📁 Structure du Projet - Refactoring

## Nouvelle Architecture (v2.0)

```
├── main.py                    # 🚀 Point d'entrée principal
├── src/                       # 📦 Code source organisé
│   ├── __init__.py           # Package principal
│   ├── core/                 # ⚙️ Configuration et utilitaires
│   │   ├── __init__.py
│   │   └── config.py         # Configuration centralisée
│   ├── models/               # 🤖 Modèles de recommandation
│   │   ├── __init__.py
│   │   └── recommendation_system.py  # Système principal
│   └── ui/                   # 🎨 Interface utilisateur
│       ├── __init__.py
│       ├── components.py     # Composants Streamlit
│       └── styles.py         # Styles CSS
├── requirements-base.txt     # 📋 Dépendances lourdes (cache Docker)
├── requirements.txt          # 📋 Dépendances applicatives  
├── Dockerfile               # 🐳 Configuration Docker
├── docker-compose.yml       # 🐳 Orchestration
└── .dockerignore           # 🐳 Exclusions Docker
```

## 🔄 Changements apportés

### ✅ Améliorations
- **Séparation des responsabilités** : Code organisé en modules logiques
- **Configuration centralisée** : Un seul fichier de config
- **Components UI réutilisables** : Interface modulaire
- **Type hints** : Meilleure documentation du code
- **Error handling** : Gestion robuste des erreurs
- **Versions modernes** : Python 3.11 + packages récents

### 🗂️ Modules

#### `src/core/config.py`
- Configuration des chemins de modèles
- Paramètres Streamlit
- Configuration des embeddings
- Detection automatique Docker/local

#### `src/models/recommendation_system.py`
- Classe `ChanelRecommendationSystem` 
- Chargement des modèles avec fallback
- Méthodes de recherche (image, texte, combinée)
- Gestion des embeddings pré-calculés

#### `src/ui/components.py`
- Interface de recherche interactive
- Affichage des résultats
- Cartes produits avec scores
- Gestion des erreurs UI

#### `src/ui/styles.py`
- CSS centralisé pour Streamlit
- Styles responsive
- Thème Chanel (noir et blanc)

#### `main.py`
- Point d'entrée simplifié
- Orchestration des composants
- Gestion du state Streamlit

## 🚀 Commandes

### Développement
```bash
# Nouvelle commande
streamlit run main.py
```

### Docker
```bash
# Build avec nouvelle structure
docker compose build --no-cache
docker compose up
```

## 📦 Dépendances mises à jour

### Versions modernes
- `streamlit>=1.39.0` (était 1.28.0)
- `transformers>=4.40.0` (était 4.21.3)  
- `sentence-transformers>=3.0.0` (était 2.2.2)
- `numpy>=1.24.0,<2.0.0` (était 1.17.3)
- `Python 3.11` (était 3.9)

### Résolution des conflits
- ✅ Numpy `_core` error résolu
- ✅ Compatibilité transformer/huggingface
- ✅ Versions cohérentes scikit-learn/matplotlib
