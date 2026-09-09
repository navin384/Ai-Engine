from app.data.knowledge_base import ROUTINE_COMPLAINTS, DOMAIN_TAXONOMY

def is_routine_grievance(text: str) -> bool:
    """Routine civic complaints ko university research pipeline se bahar nikalta hai."""
    t_lower = text.lower()
    return any(word in t_lower for word in ROUTINE_COMPLAINTS)

def classify_domain(text: str) -> str:
    """Thematic domain tag karta hai."""
    t_lower = text.lower()
    scores = {}
    for domain, keywords in DOMAIN_TAXONOMY.items():
        score = sum(1 for kw in keywords if kw in t_lower)
        scores[domain] = score
    
    best_domain = max(scores, key=scores.get)
    return best_domain if scores[best_domain] > 0 else "General Innovation"