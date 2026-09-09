# app/services/triage.py
import re
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from app.data.knowledge_base import DOMAIN_TAXONOMY, ROUTINE_MUNICIPAL_KEYWORDS

embedder = SentenceTransformer('all-MiniLM-L6-v2')

domain_names = list(DOMAIN_TAXONOMY.keys())
domain_descriptions = [DOMAIN_TAXONOMY[d] for d in domain_names]
domain_vectors = embedder.encode(domain_descriptions, normalize_embeddings=True)

def evaluate_triage_and_domain(text: str):
    """
    Returns: (is_routine, category, confidence)
    """
    text_clean = text.lower().strip()
    if len(text_clean) < 10:
        return False, "Other", 0.30

    # 1. Routine municipal check
    for phrase in ROUTINE_MUNICIPAL_KEYWORDS:
        if phrase in text_clean:
            return True, "Routine Municipal Complaint", 0.95

    # 2. Semantic Domain Similarity
    text_vec = embedder.encode([text_clean], normalize_embeddings=True)
    sims = cosine_similarity(text_vec, domain_vectors)[0]
    
    best_idx = int(sims.argmax())
    confidence = float(sims[best_idx])
    
    best_domain = domain_names[best_idx] if confidence > 0.22 else "Other"
    return False, best_domain, round(min(confidence + 0.35, 0.98), 2)

def analyze_severity_and_impact(text: str, category: str):
    """
    Evaluates Severity, Urgency, Impact level, and estimated population impact.
    """
    text_l = text.lower()
    
    # Critical risk keywords
    critical_triggers = ["death", "die", "poison", "marr gaye", "bimari", "epidemic", "fatal", "hazard", "collapse", "risk to life", "cut off"]
    high_urgency_triggers = ["emergency", "monsoon", "immediately", "urgent", "kal tak", "bachhe", "school band"]
    
    is_critical = any(w in text_l for w in critical_triggers)
    is_urgent = any(w in text_l for w in high_urgency_triggers) or (category in ["Healthcare", "Water & Sanitation", "Public Safety"])

    # Severity computation
    if is_critical or category in ["Healthcare", "Public Safety"]:
        severity = "CRITICAL" if is_critical else "HIGH"
    elif category in ["Water & Sanitation", "Roads & Transport", "Electricity", "Women & Child Safety"]:
        severity = "HIGH"
    elif category in ["Agriculture", "Education", "Waste Management"]:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    # Urgency computation
    urgency = "HIGH" if (is_urgent or severity in ["CRITICAL", "HIGH"]) else "MEDIUM"

    # Impact Level & Population estimation
    if "village" in text_l or "gaon" in text_l or "panchayat" in text_l or severity in ["CRITICAL", "HIGH"]:
        impact_level = "HIGH"
        affected_pop = "500 - 2,500 villagers"
    elif "school" in text_l or "tola" in text_l or "ward" in text_l:
        impact_level = "MEDIUM"
        affected_pop = "100 - 500 individuals"
    else:
        impact_level = "LOW"
        affected_pop = "Under 100 individuals"

    return severity, urgency, impact_level, affected_pop