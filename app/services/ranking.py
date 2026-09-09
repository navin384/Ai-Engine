from app.data.knowledge_base import INSTITUTIONS

def rank_best_university(category: str, district: str) -> str:
    """
    Weighted Allocation Formula:
    Score = 0.40(Domain) + 0.25(Proximity) + 0.25(PastScore) - 0.10(Load)
    """
    candidates = []
    for inst in INSTITUTIONS:
        domain_match = 1.0 if category in inst["domains"] else 0.15
        proximity = 1.0 if inst["district"].lower() == district.lower() else 0.5
        past_score = inst["pastDeliveryScore"]
        load_penalty = inst["currentLoad"] * 0.05

        score = (0.40 * domain_match) + (0.25 * proximity) + (0.25 * past_score) - load_penalty
        candidates.append((inst["id"], score))
    
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0][0] if candidates else None