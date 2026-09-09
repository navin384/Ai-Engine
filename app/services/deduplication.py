# app/services/deduplication.py
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.data.knowledge_base import HISTORICAL_PROBLEMS
from app.models.schemas import SimilarProblemMatch

embedder = SentenceTransformer('all-MiniLM-L6-v2')

kb_texts = [p["description"] for p in HISTORICAL_PROBLEMS]
kb_vectors = embedder.encode(kb_texts, normalize_embeddings=True) if kb_texts else np.array([])

def detect_relationships(text: str, user_lat: float, user_lon: float):
    """
    Returns list of SimilarProblemMatch objects and relationship flag.
    """
    if len(kb_vectors) == 0:
        return [], "NEW_PROBLEM"

    query_vec = embedder.encode([text], normalize_embeddings=True)
    sims = cosine_similarity(query_vec, kb_vectors)[0]
    
    matches = []
    has_exact = False
    has_similar = False

    for idx, score in enumerate(sims):
        score_val = float(score)
        if score_val >= 0.55:  # Relevance cutoff
            prob = HISTORICAL_PROBLEMS[idx]
            
            if score_val >= 0.82:
                rel = "EXACT_DUPLICATE"
                has_exact = True
            elif score_val >= 0.65:
                rel = "SIMILAR_PROBLEM"
                has_similar = True
            else:
                rel = "RELATED_THEME"

            matches.append(SimilarProblemMatch(
                problemId=prob["id"],
                title=prob["title"],
                similarity=round(score_val, 2),
                relationship=rel,
                blueprintUrl=prob.get("blueprintUrl")
            ))

    # Sort matches by similarity score descending
    matches.sort(key=lambda x: x.similarity, reverse=True)

    if has_exact:
        summary_action = "REUSE_EXISTING_SOLUTION"
    elif has_similar:
        summary_action = "ADAPT_SIMILAR_BLUEPRINT"
    else:
        summary_action = "ROUTE_TO_INSTITUTION"

    return matches, summary_action