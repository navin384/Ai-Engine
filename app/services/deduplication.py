from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.data.knowledge_base import HISTORICAL_PROBLEMS

# Lightweight transformer model (CPU-friendly)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Historical data ke embeddings precompute
kb_texts = [p["description"] for p in HISTORICAL_PROBLEMS]
kb_embeddings = model.encode(kb_texts) if kb_texts else np.array([])

def check_duplicate(new_text: str, threshold: float = 0.30):
    """
    Returns (matched_dict, similarity_score) agar pehle se solved problem se match mile.
    """
    if len(kb_embeddings) == 0:
        return None, 0.0

    new_emb = model.encode([new_text])
    sims = cosine_similarity(new_emb, kb_embeddings)[0]
    
    best_idx = int(np.argmax(sims))
    best_score = float(sims[best_idx])

    if best_score >= threshold:
        return HISTORICAL_PROBLEMS[best_idx], round(best_score, 3)
    return None, round(best_score, 3)