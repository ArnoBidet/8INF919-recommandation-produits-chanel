"""
Composants UI pour l'affichage des résultats de recommandation
"""

import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from typing import List, Dict, Tuple


def display_product_card(product_info: Dict, similarity_score: float):
    """
    Affiche une carte produit avec les informations et le score de similarité
    
    Args:
        product_info: Dictionnaire contenant les informations du produit
        similarity_score: Score de similarité (0-1)
    """
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Afficher l'image du produit
            if product_info.get('image_url'):
                try:
                    response = requests.get(product_info['image_url'], timeout=5)
                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))
                        st.image(img, width=150)
                    else:
                        st.write("🖼️ Image non disponible")
                except Exception:
                    st.write("🖼️ Image non disponible")
            else:
                st.write("🖼️ Pas d'image")
        
        with col2:
            # Informations du produit
            st.write(f"**{product_info.get('title', 'Produit sans nom')}**")
            
            # Score de similarité
            score_percentage = int(similarity_score * 100)
            if score_percentage >= 80:
                score_color = "🟢"
            elif score_percentage >= 60:
                score_color = "🟡"
            else:
                score_color = "🔴"
            
            st.write(f"{score_color} **Similarité:** {score_percentage}%")
            
            # Prix
            if product_info.get('price') and product_info['price'] != 'N/A':
                st.write(f"💰 **Prix:** {product_info['price']}")
            
            # Catégorie
            if product_info.get('category') and product_info['category'] != 'N/A':
                st.write(f"🏷️ **Catégorie:** {product_info['category']}")
            
            # Code produit
            if product_info.get('product_code') and product_info['product_code'] != 'N/A':
                st.write(f"🔢 **Code:** {product_info['product_code']}")
        
        st.divider()


def display_search_results(results: List[Tuple[int, float]], recommendation_system, title: str):
    """
    Affiche les résultats de recherche
    
    Args:
        results: Liste de tuples (index_produit, score_similarité)
        recommendation_system: Instance du système de recommandation
        title: Titre de la section
    """
    if not results:
        st.warning("Aucun résultat trouvé.")
        return
    
    st.subheader(f"🎯 {title}")
    st.write(f"**{len(results)} produits trouvés**")
    
    # Afficher les résultats
    for i, (product_idx, score) in enumerate(results):
        product_info = recommendation_system.get_product_info(product_idx)
        
        with st.expander(f"#{i+1} - {product_info.get('title', 'Produit')} ({int(score*100)}%)", expanded=(i < 3)):
            display_product_card(product_info, score)


def create_search_interface():
    """
    Crée l'interface de recherche principale
    
    Returns:
        Tuple contenant les paramètres de recherche sélectionnés
    """
    st.markdown('<h1 class="main-header">👜 Chanel Product Recommendation Platform</h1>', 
                unsafe_allow_html=True)
    
    # Menu de sélection du mode de recherche
    search_mode = st.sidebar.selectbox(
        "🔍 Mode de recherche",
        ["Recherche par image", "Recherche par texte", "Recherche combinée"],
        help="Sélectionnez le type de recherche que vous souhaitez effectuer"
    )
    
    # Paramètres communs
    top_k = st.sidebar.slider("📊 Nombre de résultats", min_value=5, max_value=20, value=10)
    
    # Interface selon le mode
    uploaded_image = None
    query_text = ""
    weight_image = 0.5
    weight_text = 0.5
    
    if search_mode == "Recherche par image":
        st.header("🖼️ Recherche par image")
        st.write("Uploadez une image pour trouver des produits similaires")
        
        uploaded_image = st.file_uploader(
            "Choisissez une image...", 
            type=['png', 'jpg', 'jpeg'],
            help="Formats supportés: PNG, JPG, JPEG"
        )
        
        if uploaded_image:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write("**Image uploadée:**")
                image = Image.open(uploaded_image)
                st.image(image, width=300)
    
    elif search_mode == "Recherche par texte":
        st.header("📝 Recherche par texte")
        st.write("Décrivez le produit que vous recherchez")
        
        query_text = st.text_input(
            "Description du produit:",
            placeholder="Ex: Rouge à lèvres rouge mat, parfum floral, sac à main noir...",
            help="Soyez aussi précis que possible dans votre description"
        )
    
    else:  # Recherche combinée
        st.header("🎯 Recherche combinée")
        st.write("Combinez une image et une description textuelle")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🖼️ Image")
            uploaded_image = st.file_uploader(
                "Choisissez une image...", 
                type=['png', 'jpg', 'jpeg']
            )
            
            if uploaded_image:
                image = Image.open(uploaded_image)
                st.image(image, width=250)
        
        with col2:
            st.subheader("📝 Description")
            query_text = st.text_area(
                "Description:",
                placeholder="Décrivez ce que vous cherchez...",
                height=100
            )
        
        # Réglage des poids
        st.subheader("⚖️ Pondération")
        weight_image = st.slider(
            "Poids de l'image", 
            min_value=0.0, max_value=1.0, value=0.5, step=0.1
        )
        weight_text = 1.0 - weight_image
        st.write(f"Poids du texte: {weight_text}")
    
    return {
        'search_mode': search_mode,
        'uploaded_image': uploaded_image,
        'query_text': query_text,
        'top_k': top_k,
        'weight_image': weight_image,
        'weight_text': weight_text
    }


def show_search_button():
    """Affiche le bouton de recherche"""
    return st.button("🔍 Lancer la recherche", type="primary", use_container_width=True)


def show_loading():
    """Affiche un indicateur de chargement"""
    with st.spinner('🔄 Recherche en cours...'):
        st.empty()


def show_error(message: str):
    """Affiche un message d'erreur"""
    st.error(f"❌ {message}")


def show_info(message: str):
    """Affiche un message d'information"""
    st.info(f"ℹ️ {message}")


def show_success(message: str):
    """Affiche un message de succès"""
    st.success(f"✅ {message}")


def create_sidebar_info():
    """Crée les informations dans la barre latérale"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ À propos")
    st.sidebar.markdown("""
    Cette plateforme utilise l'intelligence artificielle pour recommander des produits Chanel 
    basés sur la similarité visuelle et textuelle.
    
    **Fonctionnalités:**
    - 🖼️ Recherche par image
    - 📝 Recherche par description
    - 🎯 Recherche combinée
    
    **Technologies:**
    - CLIP (Vision)
    - Sentence Transformers (Texte)
    - Streamlit (Interface)
    """)
