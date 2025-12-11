"""
Application principale Chanel Recommendation Platform
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / "src"))

import streamlit as st
from PIL import Image
import warnings

from src.core.config import STREAMLIT_CONFIG
from src.models.recommendation_system import ChanelRecommendationSystem
from src.ui.styles import MAIN_CSS
from src.ui.components import (
    create_search_interface,
    display_search_results,
    show_search_button,
    show_loading,
    show_error,
    create_sidebar_info
)

warnings.filterwarnings('ignore')


def main():
    """Fonction principale de l'application"""
    
    # Configuration de la page
    st.set_page_config(**STREAMLIT_CONFIG)
    
    # Application des styles CSS
    st.markdown(MAIN_CSS, unsafe_allow_html=True)
    
    # Initialisation du système de recommandation
    if 'recommendation_system' not in st.session_state:
        with st.spinner('🔄 Chargement des modèles...'):
            try:
                st.session_state.recommendation_system = ChanelRecommendationSystem()
            except Exception as e:
                st.error(f"❌ Erreur lors de l'initialisation: {e}")
                st.stop()
    
    # Interface utilisateur
    search_params = create_search_interface()
    create_sidebar_info()
    
    # Traitement de la recherche
    if show_search_button():
        process_search(search_params)


def process_search(params):
    """
    Traite la recherche selon les paramètres fournis
    
    Args:
        params: Dictionnaire contenant les paramètres de recherche
    """
    recommendation_system = st.session_state.recommendation_system
    search_mode = params['search_mode']
    
    try:
        with st.spinner('🔄 Recherche en cours...'):
            if search_mode == "Recherche par image":
                if not params['uploaded_image']:
                    show_error("Veuillez uploader une image.")
                    return
                
                image = Image.open(params['uploaded_image'])
                results = recommendation_system.search_by_image(image, params['top_k'])
                display_search_results(results, recommendation_system, "Résultats par image")
            
            elif search_mode == "Recherche par texte":
                if not params['query_text'].strip():
                    show_error("Veuillez saisir une description.")
                    return
                
                results = recommendation_system.search_by_text(params['query_text'], params['top_k'])
                display_search_results(results, recommendation_system, "Résultats par texte")
            
            else:  # Recherche combinée
                if not params['uploaded_image'] or not params['query_text'].strip():
                    show_error("Veuillez fournir une image ET une description.")
                    return
                
                image = Image.open(params['uploaded_image'])
                results = recommendation_system.combined_search(
                    image, 
                    params['query_text'],
                    params['weight_image'],
                    params['weight_text'],
                    params['top_k']
                )
                display_search_results(results, recommendation_system, "Résultats combinés")
    
    except Exception as e:
        show_error(f"Erreur lors de la recherche: {e}")


if __name__ == "__main__":
    main()
