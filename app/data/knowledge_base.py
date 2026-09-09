# app/data/knowledge_base.py

# 14 Expanded Thematic Domains with semantic anchors
DOMAIN_TAXONOMY = {
    "Water & Sanitation": "drinking water contamination iron arsenic fluoride handpump borewell talab open defecation drainage sewer pipeline leakage",
    "Agriculture": "crop failure kheti pest attack drought fertilizer seeds mandi cold storage soil health paddy yield lac cultivation",
    "Healthcare": "primary health center phc doctor medicine ambulance maternal child hospital malnutrition dengue malaria epidemic disease",
    "Education": "school building teacher shortage digital classroom lab dropout electricity in school midday meal smart education",
    "Roads & Transport": "broken bridge culvert pulia pothole rural connectivity bus stand road safety fatal accident road washed away",
    "Electricity": "power cut transformer blast low voltage load shedding no grid off grid solar power wiring hazard",
    "Waste Management": "garbage dumping plastic waste bio medical waste toxic dump river pollution compost recycling solid waste",
    "Environment": "deforestation forest fire soil erosion mining pollution coal dust river siltation air pollution industrial effluents",
    "Public Safety": "street dark crime prone bridge broken collapse risk flooding river drowning landslide hazard fire hazard",
    "Women & Child Safety": "dark bus stop unlit street school road eve teasing child labor early marriage safety helpline",
    "Infrastructure": "community hall panchayat bhawan market shed dam barrier storage warehouse bus terminal",
    "Digital/Public Services": "pragya kendra csc internet optical fiber land records caste certificate ration biometric failure",
    "Employment & Livelihood": "tussar silk handicraft tribal artisan self help group shg migration unemployment skill center",
    "Other": "general societal challenge grievance administration"
}

ROUTINE_MUNICIPAL_KEYWORDS = [
    "ration card nahi mila", "pension ruka hua hai", "clerk ghus mang raha", 
    "death certificate", "birth certificate", "panchayat bhawan me tala band",
    "garbage truck nahi aaya", "safai karmi absent"
]

# Verified Jharkhand Institutions (AISHE & NAAC Coordinated)
JHARKHAND_INSTITUTIONS = [
    {
        "id": "INST-BIT-MESRA",
        "name": "BIT Mesra, Ranchi",
        "district": "Ranchi",
        "lat": 23.4123, "lon": 85.4399,
        "domains": ["Water & Sanitation", "Electricity", "Infrastructure", "Waste Management", "Digital/Public Services"],
        "pastDeliveryScore": 0.94,
        "currentCapacity": 8
    },
    {
        "id": "INST-IIT-ISM",
        "name": "IIT (ISM) Dhanbad",
        "district": "Dhanbad",
        "lat": 23.8144, "lon": 86.4412,
        "domains": ["Environment", "Electricity", "Roads & Transport", "Waste Management", "Water & Sanitation"],
        "pastDeliveryScore": 0.97,
        "currentCapacity": 9
    },
    {
        "id": "INST-NIT-JSR",
        "name": "NIT Jamshedpur",
        "district": "East Singhbhum",
        "lat": 22.7770, "lon": 86.1441,
        "domains": ["Roads & Transport", "Electricity", "Infrastructure", "Water & Sanitation"],
        "pastDeliveryScore": 0.91,
        "currentCapacity": 7
    },
    {
        "id": "INST-BAU-RANCHI",
        "name": "Birsa Agricultural University (BAU), Ranchi",
        "district": "Ranchi",
        "lat": 23.4432, "lon": 85.3211,
        "domains": ["Agriculture", "Employment & Livelihood", "Environment", "Water & Sanitation"],
        "pastDeliveryScore": 0.95,
        "currentCapacity": 6
    },
    {
        "id": "INST-CUJ-RANCHI",
        "name": "Central University of Jharkhand (CUJ), Ranchi",
        "district": "Ranchi",
        "lat": 23.3441, "lon": 85.3096,
        "domains": ["Education", "Environment", "Public Safety", "Digital/Public Services"],
        "pastDeliveryScore": 0.88,
        "currentCapacity": 5
    },
    {
        "id": "INST-XLRI-JSR",
        "name": "XLRI Jamshedpur",
        "district": "East Singhbhum",
        "lat": 22.8028, "lon": 86.1854,
        "domains": ["Employment & Livelihood", "Education", "Digital/Public Services", "Women & Child Safety"],
        "pastDeliveryScore": 0.93,
        "currentCapacity": 6
    },
    {
        "id": "INST-RANCHI-UNIV",
        "name": "Ranchi University",
        "district": "Ranchi",
        "lat": 23.3700, "lon": 85.3250,
        "domains": ["Healthcare", "Education", "Employment & Livelihood", "Women & Child Safety"],
        "pastDeliveryScore": 0.84,
        "currentCapacity": 6
    },
    {
        "id": "INST-VBU-HAZARIBAGH",
        "name": "Vinoba Bhave University, Hazaribagh",
        "district": "Hazaribagh",
        "lat": 23.9925, "lon": 85.3637,
        "domains": ["Education", "Healthcare", "Environment"],
        "pastDeliveryScore": 0.82,
        "currentCapacity": 5
    },
    {
        "id": "INST-KOLHAN-UNIV",
        "name": "Kolhan University, Chaibasa",
        "district": "West Singhbhum",
        "lat": 22.5564, "lon": 85.8080,
        "domains": ["Education", "Employment & Livelihood", "Healthcare"],
        "pastDeliveryScore": 0.80,
        "currentCapacity": 5
    },
    {
        "id": "INST-SKMU-DUMKA",
        "name": "Sido Kanhu Murmu University (SKMU), Dumka",
        "district": "Dumka",
        "lat": 24.2680, "lon": 87.2480,
        "domains": ["Agriculture", "Education", "Healthcare", "Employment & Livelihood"],
        "pastDeliveryScore": 0.81,
        "currentCapacity": 5
    },
    {
        "id": "INST-JUT-RANCHI",
        "name": "Jharkhand University of Technology (JUT), Ranchi",
        "district": "Ranchi",
        "lat": 23.3600, "lon": 85.3400,
        "domains": ["Infrastructure", "Roads & Transport", "Electricity", "Waste Management"],
        "pastDeliveryScore": 0.86,
        "currentCapacity": 7
    },
    {
        "id": "INST-IIIT-RANCHI",
        "name": "IIIT Ranchi",
        "district": "Ranchi",
        "lat": 23.3441, "lon": 85.3096,
        "domains": ["Digital/Public Services", "Education", "Public Safety", "Healthcare"],
        "pastDeliveryScore": 0.89,
        "currentCapacity": 6
    }
]

# Historical Knowledge Base for Deduplication
HISTORICAL_PROBLEMS = [
    {
        "id": "PROB-JH-001",
        "title": "Groundwater Iron and Arsenic Filtration",
        "description": "Tube well water is reddish with severe iron smell, causing stomach infections and skin rashes in villagers.",
        "category": "Water & Sanitation",
        "lat": 23.3441, "lon": 85.3096,
        "district": "Ranchi",
        "blueprintUrl": "https://jansetu.jharkhand.gov.in/blueprints/low-cost-iron-filter.pdf"
    },
    {
        "id": "PROB-JH-002",
        "title": "Micro Solar Cold Storage for Forest Produce",
        "description": "Mahua flowers, sal seeds, and organic vegetables rot during transit due to complete lack of grid power and cold chains.",
        "category": "Electricity",
        "lat": 22.8046, "lon": 86.2029,
        "district": "East Singhbhum",
        "blueprintUrl": "https://jansetu.jharkhand.gov.in/blueprints/solar-cold-box.pdf"
    },
    {
        "id": "PROB-JH-003",
        "title": "Collapsing Wooden Culvert over Seasonal Nala",
        "description": "Wooden culvert bridge washed away during monsoon, disconnecting three tribal villages from primary school and hospital.",
        "category": "Roads & Transport",
        "lat": 24.2680, "lon": 87.2480,
        "district": "Dumka",
        "blueprintUrl": "https://jansetu.jharkhand.gov.in/blueprints/modular-precast-culvert.pdf"
    }
]