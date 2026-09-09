from app.services.deduplication import check_duplicate
from app.services.triage import classify_domain, is_routine_grievance
from app.services.ranking import rank_best_university

# Test 1: Citizen B reporting similar water contamination
text_citizen_b = "Hamare gaon ke tube well ka paani lal ho raha hai aur iron bahut zyada hai."
print("--- TEST 1: Citizen B Similar Problem ---")
print("Is Routine Grievance?:", is_routine_grievance(text_citizen_b))
print("Domain Category:", classify_domain(text_citizen_b))
matched, score = check_duplicate(text_citizen_b,threshold=0.30)
print("Duplicate Found?:", matched["title"] if matched else "No", f"(Score: {score})")
print("Recommended HEI:", rank_best_university("Water Resources", "Ranchi"))

# Test 2: Routine municipal issue
text_routine = "Hamare gali ki street light kharab hai aur kachra pada hai."
print("\n--- TEST 2: Routine Complaint ---")
print("Is Routine Grievance?:", is_routine_grievance(text_routine))