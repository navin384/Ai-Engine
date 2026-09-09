# app/data/knowledge_base.py

# 1. Historical & Verified Problems (Continuous Knowledge Commons)
# Citizen B ke deduplication testing ke liye English + Hinglish keywords included hain
HISTORICAL_PROBLEMS = [
    {
        "id": "PROB-JH-001",
        "title": "Groundwater Iron & Heavy Metal Contamination",
        "description": "Borewell tube well handpump water has high iron content turning water red lal paani kharab kheti paddy crop stomach health issue.",
        "category": "Water Resources",
        "assignedHeiId": "U-0268", # BIT Mesra
        "status": "SOLVED_VERIFIED",
        "blueprintUrl": "https://gov.jharkhand.in/blueprints/low-cost-iron-sand-filter.pdf"
    },
    {
        "id": "PROB-JH-002",
        "title": "Solar Cold Storage for Forest Produce",
        "description": "Mahua flowers sal seeds wild forest produce rot quickly due to no electricity grid power shortage and lack of cold storage.",
        "category": "Clean Energy",
        "assignedHeiId": "U-0272", # NIT Jamshedpur
        "status": "PILOT_TESTING",
        "blueprintUrl": "https://gov.jharkhand.in/blueprints/solar-micro-cold-room.pdf"
    },
    {
        "id": "PROB-JH-003",
        "title": "Lac Host Tree Pest Infection",
        "description": "Insects pests destroying ber and kusum trees impacting tribal lac farming harvesting output yield kharab kheti.",
        "category": "Agriculture",
        "assignedHeiId": "U-0269", # Birsa Agricultural University
        "status": "SOLVED_VERIFIED",
        "blueprintUrl": "https://gov.jharkhand.in/blueprints/bio-pest-spray.pdf"
    }
]

# 2. Jharkhand HEI Capability Matrix (AISHE / NAAC mapped)
INSTITUTIONS = [
    {
        "id": "U-0268",
        "name": "Birla Institute of Technology (BIT) Mesra",
        "district": "Ranchi",
        "domains": ["Water Resources", "Clean Energy", "IoT"],
        "pastDeliveryScore": 0.94,
        "currentLoad": 3
    },
    {
        "id": "U-0272",
        "name": "National Institute of Technology (NIT) Jamshedpur",
        "district": "East Singhbhum",
        "domains": ["Clean Energy", "Urban Infrastructure", "Water Resources"],
        "pastDeliveryScore": 0.89,
        "currentLoad": 2
    },
    {
        "id": "U-0269",
        "name": "Birsa Agricultural University (BAU)",
        "district": "Ranchi",
        "domains": ["Agriculture", "Soil Health", "Rural Livelihoods"],
        "pastDeliveryScore": 0.96,
        "currentLoad": 4
    }
]

# 3. Domain Classification Taxonomy
DOMAIN_TAXONOMY = {
    "Water Resources": [
        "water", "paani", "iron", "arsenic", "fluoride", "borewell", 
        "handpump", "filter", "talab", "irrigation", "drainage", "chapa kal", "tube well"
    ],
    "Agriculture": [
        "crop", "kheti", "soil", "pest", "fertilizer", "seed", 
        "fasal", "mandi", "lac", "yield", "paddy", "kisan"
    ],
    "Clean Energy": [
        "solar", "bijli", "electricity", "battery", "cold storage", 
        "power", "grid", "biogas", "light"
    ],
    "Rural Livelihoods": [
        "tussar", "silk", "handicraft", "forest produce", "bamboo", 
        "mahua", "artisan", "tribal"
    ]
}

# 4. Civic Routine Complaints (For Triage Gatekeeper)
ROUTINE_COMPLAINTS = [
    "street light", "kachra", "garbage", "pothole", "sadak tuti", 
    "ration card", "pension", "bribe", "clerk", "drain blocked", 
    "safai", "nali band"
]