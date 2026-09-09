# app/services/ranking.py
import math
from app.data.knowledge_base import JHARKHAND_INSTITUTIONS
from app.models.schemas import InstitutionMatch

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2)**2 + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon / 2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def rank_top_institutions(category: str, user_district: str, user_lat: float, user_lon: float, top_k: int = 4):
    """
    Calculates weighted match score and generates natural language reasons.
    Formula: 0.40(Domain) + 0.25(Proximity) + 0.20(PastDelivery) + 0.15(Capacity)
    """
    ranked_list = []

    for inst in JHARKHAND_INSTITUTIONS:
        reasons = []
        
        # 1. Domain Match
        if category in inst["domains"]:
            domain_score = 1.0
            reasons.append(f"Direct active specialization in {category}")
        else:
            domain_score = 0.25
            reasons.append("Interdisciplinary engineering & technical capability")

        # 2. Geographic Proximity
        dist_km = haversine_km(user_lat, user_lon, inst["lat"], inst["lon"])
        if inst["district"].lower() == user_district.lower() or dist_km <= 35.0:
            geo_score = 1.0
            reasons.append(f"Local district proximity ({inst['district']} - within ~{int(dist_km)} km)")
        elif dist_km <= 120.0:
            geo_score = 0.70
            reasons.append(f"Regional proximity (~{int(dist_km)} km from site)")
        else:
            geo_score = 0.40
            reasons.append(f"State-level nodal institution ({inst['district']})")

        # 3. Delivery Score
        past_perf = inst["pastDeliveryScore"]
        if past_perf >= 0.90:
            reasons.append(f"Exceptional past delivery record ({int(past_perf*100)}% project success)")
        else:
            reasons.append(f"Active accredited research faculty ({int(past_perf*100)}% rating)")

        # 4. Capacity
        cap_score = min(inst["currentCapacity"] / 10.0, 1.0)
        if inst["currentCapacity"] >= 7:
            reasons.append(f"High immediate lab & student squad bandwidth ({inst['currentCapacity']}/10)")

        # Composite Score Calculation
        total_score = (
            (0.40 * domain_score) +
            (0.25 * geo_score) +
            (0.20 * past_perf) +
            (0.15 * cap_score)
        )

        ranked_list.append(InstitutionMatch(
            id=inst["id"],
            name=f"Potential Match: {inst['name']}",
            matchScore=round(total_score, 2),
            reasons=reasons[:3]  # Top 3 most pertinent reasons
        ))

    # Sort descending
    ranked_list.sort(key=lambda x: x.matchScore, reverse=True)
    return ranked_list[:top_k]