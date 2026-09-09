# tests/test_matching.py
from app.services.triage import evaluate_triage_and_domain, analyze_severity_and_impact
from app.services.deduplication import detect_relationships
from app.services.ranking import rank_top_institutions

TEST_CASES = [
    {
        "name": "1. Water (Hinglish - Similar to PROB-001)",
        "text": "Gaon ke chapa kal ka paani pura laal nikal raha hai aur iron ka badboo aa raha hai.",
        "district": "Ranchi", "lat": 23.3441, "lon": 85.3096
    },
    {
        "name": "2. Healthcare / Disease (Hindi - High Severity)",
        "text": "Hamare tola me gande paani se baccho ko bhishan diarrhea aur vomiting ho raha hai turant doctor bhejiye.",
        "district": "Khunti", "lat": 23.0700, "lon": 85.2800
    },
    {
        "name": "3. Education (English)",
        "text": "The local primary school has no roof and digital classes cannot be conducted due to complete lack of power.",
        "district": "Dumka", "lat": 24.2680, "lon": 87.2480
    },
    {
        "name": "4. Road & Transport (Monsoon Hazard)",
        "text": "Pulia bridge wash out ho gaya nala me, 4 gaon block ho chuke hain ambulance bhi nahi aa sakti.",
        "district": "Dhanbad", "lat": 23.8144, "lon": 86.4412
    },
    {
        "name": "5. Waste Management",
        "text": "Open biomedical waste dumped near public pond, stray animals eating used syringes.",
        "district": "East Singhbhum", "lat": 22.8028, "lon": 86.1854
    },
    {
        "name": "6. Routine Grievance (Divert Municipal)",
        "text": "Mere gali ki street light kharab hai aur kachra wala dumper nahi aaya.",
        "district": "Ranchi", "lat": 23.3441, "lon": 85.3096
    },
    {
        "name": "7. Short / Invalid Text",
        "text": "paani help",
        "district": "Ranchi", "lat": 23.3441, "lon": 85.3096
    }
]

def run_tests():
    print("="*75)
    print("       JANSETU AI ENGINE V2 - EVALUATION TEST BENCH")
    print("="*75)

    for case in TEST_CASES:
        print(f"\n[SCENARIO] {case['name']}")
        print(f"Input: \"{case['text']}\"")
        
        is_routine, category, conf = evaluate_triage_and_domain(case['text'])
        
        if is_routine:
            print("  >> ACTION: DIVERT_MUNICIPAL (Routine Civic Complaint Detected)")
            continue

        sev, urg, imp, pop = analyze_severity_and_impact(case['text'], category)
        matches, action = detect_relationships(case['text'], case['lat'], case['lon'])
        top_inst = rank_top_institutions(category, case['district'], case['lat'], case['lon'], top_k=2)

        print(f"  >> Category: {category} (Confidence: {conf})")
        print(f"  >> Severity: {sev} | Urgency: {urg} | Impact: {imp} ({pop})")
        print(f"  >> Recommended Action: {action}")
        
        if matches:
            print(f"  >> Similar DB Project Found: {matches[0].title} (Similarity: {matches[0].similarity}, Rel: {matches[0].relationship})")
        
        print("  >> Top Recommended Institutions:")
        for idx, inst in enumerate(top_inst, 1):
            print(f"     {idx}. {inst.name} — {int(inst.matchScore*100)}% Match")
            print(f"        Reason: {', '.join(inst.reasons)}")

    print("\n" + "="*75)
    print("ALL 7 CRITICAL BENCHMARKS EXECUTED SUCCESSFULLY.")
    print("="*75)

if __name__ == "__main__":
    run_tests()