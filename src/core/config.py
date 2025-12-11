"""
Configuration de l'application Chanel
"""

import os
from pathlib import Path

# Configuration des chemins
PROJECT_ROOT = Path(__file__).parent.parent
MODELS_DIR = os.environ.get(
    'MODELS_DIR', 
    str(PROJECT_ROOT / "Chanel_Recommendation_Models-20251211T193057Z-3-001" / "Chanel_Recommendation_Models")
)

# Configuration Docker
DOCKER_MODELS_PATH = "/app/models"

# Configuration des modèles
MODEL_CONFIG = {
    "text_models": [
        "all-mpnet-base-v2",
        "paraphrase-MiniLM-L6-v2", 
        "all-MiniLM-L6-v2"
    ],
    "visual_models": {
        "clip": "ViT-B/32",
        "resnet": "resnet50",
        "vit": "vit_base_patch16_224"
    }
}

# Configuration Streamlit
STREAMLIT_CONFIG = {
    "page_title": "Chanel Product Recommendation Platform",
    "page_icon": "👜",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Configuration des embeddings
EMBEDDING_CONFIG = {
    "visual_embeddings": {
        "cnn_embeddings": 186624,
        "resnet_embeddings": 2048,
        "clip_embeddings": 512,
        "vit_embeddings": 768
    },
    "textual_embeddings": {
        "title_embeddings_basic": 384,
        "title_embeddings_improved": 768
    }
}

def get_models_directory():
    """Retourne le répertoire des modèles selon l'environnement"""
    if os.path.exists(DOCKER_MODELS_PATH):
        return DOCKER_MODELS_PATH
    return MODELS_DIR
