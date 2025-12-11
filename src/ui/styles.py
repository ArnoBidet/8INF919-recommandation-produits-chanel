"""
Styles CSS pour l'interface Streamlit
"""

MAIN_CSS = """
<style>
.main-header {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    color: #000000;
    padding: 2rem 0;
    border-bottom: 3px solid #000000;
    margin-bottom: 2rem;
}

.recommendation-card {
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem;
    background-color: #f9f9f9;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.similarity-score {
    background-color: #000000;
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: bold;
}

.category-badge {
    background-color: #f0f0f0;
    color: #333;
    padding: 0.2rem 0.5rem;
    border-radius: 10px;
    font-size: 0.7rem;
    margin: 0.2rem;
}

.price-tag {
    color: #d4af37;
    font-weight: bold;
    font-size: 1.1rem;
}

.search-section {
    background-color: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}

.result-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}

.product-image {
    max-width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
}

.loading-spinner {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
}
</style>
"""
