"""
Système de recommandation principal pour les produits Chanel
"""

import pandas as pd
import numpy as np
import pickle
from PIL import Image
import cv2
from sklearn.metrics.pairwise import cosine_similarity
import torch
import clip
from sentence_transformers import SentenceTransformer
import os
from typing import List, Tuple, Dict, Union
import warnings
import streamlit as st

from ..core.config import get_models_directory, MODEL_CONFIG, EMBEDDING_CONFIG

warnings.filterwarnings('ignore')


class ChanelRecommendationSystem:
    def __init__(self, models_dir: str = None):
        """
        Système de recommandation de produits Chanel
        
        Args:
            models_dir: Répertoire contenant les modèles pré-entraînés
        """
        self.models_dir = models_dir or get_models_directory()
        self.df = None
        self.visual_embeddings = None
        self.textual_embeddings = None
        self.clip_model = None
        self.clip_preprocess = None
        self.text_model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self._load_data_and_models()
    
    def _load_data_and_models(self):
        """Charge les données et modèles pré-entraînés"""
        try:
            # Charger le DataFrame principal
            csv_path = os.path.join(self.models_dir, 'df_clean_indexed.csv')
            if os.path.exists(csv_path):
                self.df = pd.read_csv(csv_path)
                st.success(f"✅ Dataset chargé: {len(self.df)} produits")
            else:
                st.error(f"❌ Fichier dataset non trouvé: {csv_path}")
                return
            
            # Charger les embeddings visuels
            visual_path = os.path.join(self.models_dir, 'embeddings_visuels.npz')
            if os.path.exists(visual_path):
                self.visual_embeddings = np.load(visual_path)
                st.success("✅ Embeddings visuels chargés")
            
            # Charger les embeddings textuels
            textual_path = os.path.join(self.models_dir, 'embeddings_textuels.npz')
            if os.path.exists(textual_path):
                self.textual_embeddings = np.load(textual_path)
                st.success("✅ Embeddings textuels chargés")
            
            # Charger le modèle CLIP pour la recherche par image
            self._load_clip_model()
            
            # Charger le modèle textuel pour la recherche par texte
            self._load_text_model()
                
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement: {e}")
    
    def _load_clip_model(self):
        """Charge le modèle CLIP"""
        try:
            self.clip_model, self.clip_preprocess = clip.load("ViT-B/32", device=self.device)
            st.success(f"✅ Modèle CLIP chargé sur {self.device}")
        except Exception as e:
            st.warning(f"⚠️ Impossible de charger CLIP: {e}")
    
    def _load_text_model(self):
        """Charge le modèle de texte avec fallback"""
        for model_name in MODEL_CONFIG["text_models"]:
            try:
                self.text_model = SentenceTransformer(model_name)
                st.success(f"✅ Modèle textuel chargé: {model_name}")
                break
            except Exception as e:
                st.warning(f"⚠️ Impossible de charger {model_name}: {e}")
                continue
        
        if self.text_model is None:
            st.error("❌ Aucun modèle textuel n'a pu être chargé")
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Préprocesse une image pour extraction d'embeddings
        
        Args:
            image: Image PIL
            
        Returns:
            Image préprocessée en array numpy
        """
        # Redimensionner et normaliser l'image
        image = image.convert('RGB')
        image = image.resize((224, 224))
        img_array = np.array(image) / 255.0
        return img_array
    
    def extract_clip_embedding(self, image: Image.Image) -> np.ndarray:
        """
        Extrait l'embedding CLIP d'une image
        
        Args:
            image: Image PIL
            
        Returns:
            Embedding CLIP (512 dimensions)
        """
        if self.clip_model is None:
            raise ValueError("Modèle CLIP non disponible")
        
        # Préprocessing CLIP
        image_tensor = self.clip_preprocess(image).unsqueeze(0).to(self.device)
        
        # Extraction de l'embedding
        with torch.no_grad():
            embedding = self.clip_model.encode_image(image_tensor)
            embedding = embedding.squeeze().cpu().numpy()
        
        return embedding
    
    def extract_text_embedding(self, text: str) -> np.ndarray:
        """
        Extrait l'embedding textuel d'un texte
        
        Args:
            text: Texte à encoder
            
        Returns:
            Embedding textuel (768 dimensions)
        """
        if self.text_model is None:
            raise ValueError("Modèle textuel non disponible")
        
        try:
            # Encoder le texte et retourner l'embedding
            embedding = self.text_model.encode(text)
            if isinstance(embedding, np.ndarray) and len(embedding.shape) > 1:
                return embedding[0]  # Si c'est un batch, prendre le premier
            return embedding
        except Exception as e:
            st.error(f"Erreur lors de l'extraction de l'embedding : {e}")
            # Retourner un embedding par défaut de la bonne taille
            return np.zeros(768)  # Dimension par défaut pour all-mpnet-base-v2
    
    def search_by_image(self, uploaded_image: Image.Image, top_k: int = 10) -> List[Tuple[int, float]]:
        """
        Recherche par similarité visuelle
        
        Args:
            uploaded_image: Image uploadée par l'utilisateur
            top_k: Nombre de produits à retourner
            
        Returns:
            Liste de tuples (index_produit, score_similarité)
        """
        # Extraire l'embedding de l'image uploadée
        query_embedding = self.extract_clip_embedding(uploaded_image)
        
        # Utiliser les embeddings CLIP pré-calculés
        if self.visual_embeddings and 'clip_embeddings' in self.visual_embeddings:
            product_embeddings = self.visual_embeddings['clip_embeddings']
        else:
            raise ValueError("Embeddings visuels CLIP non disponibles")
        
        # Calculer les similarités
        similarities = cosine_similarity([query_embedding], product_embeddings)[0]
        
        # Trier et retourner les top K
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = [(idx, similarities[idx]) for idx in top_indices]
        
        return results
    
    def search_by_text(self, query_text: str, top_k: int = 10) -> List[Tuple[int, float]]:
        """
        Recherche par similarité textuelle
        
        Args:
            query_text: Texte de recherche
            top_k: Nombre de produits à retourner
            
        Returns:
            Liste de tuples (index_produit, score_similarité)
        """
        # Vérifier que le modèle textuel est disponible
        if self.text_model is None:
            raise ValueError("Modèle textuel non disponible")
        
        # Extraire l'embedding du texte de recherche
        query_embedding = self.extract_text_embedding(query_text)
        
        # Utiliser les embeddings textuels pré-calculés (version améliorée d'abord, puis basique)
        if self.textual_embeddings and 'title_embeddings_improved' in self.textual_embeddings:
            product_embeddings = self.textual_embeddings['title_embeddings_improved']
        elif self.textual_embeddings and 'title_embeddings_basic' in self.textual_embeddings:
            product_embeddings = self.textual_embeddings['title_embeddings_basic']
            st.info("ℹ️ Utilisation des embeddings textuels basiques")
        else:
            raise ValueError("Aucun embedding textuel disponible")
        
        # Calculer les similarités
        similarities = cosine_similarity([query_embedding], product_embeddings)[0]
        
        # Trier et retourner les top K
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = [(idx, similarities[idx]) for idx in top_indices]
        
        return results
    
    def combined_search(self, uploaded_image: Image.Image, query_text: str, 
                       weight_image: float = 0.5, weight_text: float = 0.5, 
                       top_k: int = 10) -> List[Tuple[int, float]]:
        """
        Recherche combinée (image + texte)
        
        Args:
            uploaded_image: Image uploadée
            query_text: Texte de recherche
            weight_image: Poids pour la similarité visuelle
            weight_text: Poids pour la similarité textuelle
            top_k: Nombre de produits à retourner
            
        Returns:
            Liste de tuples (index_produit, score_combiné)
        """
        # Recherche par image
        image_results = self.search_by_image(uploaded_image, len(self.df))
        image_scores = {idx: score for idx, score in image_results}
        
        # Recherche par texte
        text_results = self.search_by_text(query_text, len(self.df))
        text_scores = {idx: score for idx, score in text_results}
        
        # Combinaison des scores
        combined_scores = {}
        all_indices = set(image_scores.keys()).union(set(text_scores.keys()))
        
        for idx in all_indices:
            img_score = image_scores.get(idx, 0)
            txt_score = text_scores.get(idx, 0)
            combined_score = (weight_image * img_score) + (weight_text * txt_score)
            combined_scores[idx] = combined_score
        
        # Trier et retourner les top K
        sorted_results = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results[:top_k]
    
    def get_product_info(self, product_index: int) -> Dict:
        """
        Récupère les informations d'un produit
        
        Args:
            product_index: Index du produit dans le DataFrame
            
        Returns:
            Dictionnaire contenant les informations du produit
        """
        if self.df is None or product_index >= len(self.df):
            return {}
        
        product = self.df.iloc[product_index]
        return {
            'title': product.get('title', 'N/A'),
            'price': product.get('price', 'N/A'),
            'category': product.get('category2_code', 'N/A'),
            'image_url': product.get('imageurl', ''),
            'product_code': product.get('product_code', 'N/A')
        }
