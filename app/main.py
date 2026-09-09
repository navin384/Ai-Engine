from fastapi import FastAPI, BackgroundTasks
import requests
import os
from app.models.schemas import TriageRequest, CallbackPayload
from app.services.triage import is_routine_grievance, classify_domain
from app.services.deduplication import check_duplicate
from app.services.ranking import rank_best_university

app = FastAPI(title="Jharkhand Societal Innovation AI Engine", version="1.0.0")

NODE_BACKEND_URL = os.getenv("NODE_BACKEND_URL", "http://localhost:5000/api/v1/ai/triage-callback")

def execute_ai_pipeline(req: TriageRequest):
    # Step 1: Routine complaint check
    if is_routine_grievance(req.text):
        payload = CallbackPayload(
            problemId=req.problemId,
            category="Routine Municipal Grievance",
            isDuplicate=False,
            action="DIVERT_MUNICIPAL"
        )
    else:
        # Step 2: Domain classification
        category = classify_domain(req.text)

        # Step 3: Semantic deduplication (Citizen B scenario)
        matched_prob, score = check_duplicate(req.text, threshold=0.65)
        is_duplicate = matched_prob is not None

        # Step 4: University ranking
        hei_id = rank_best_university(category, req.district)

        payload = CallbackPayload(
            problemId=req.problemId,
            category=category,
            isDuplicate=is_duplicate,
            parentProblemId=matched_prob["id"] if is_duplicate else None,
            similarityScore=score,
            recommendedHeiId=hei_id,
            action="REUSE_SOLUTION" if is_duplicate else "ROUTE_HEI"
        )

    # Step 5: Webhook callback to Node.js backend
    try:
        res = requests.post(NODE_BACKEND_URL, json=payload.model_dump(), timeout=5)
        print(f"[AI Sync Success] Problem: {req.problemId} -> Status {res.status_code}")
    except Exception as e:
        print(f"[AI Sync Warning] Node.js server unreachable: {e}")

@app.post("/triage")
def trigger_triage(req: TriageRequest, bg: BackgroundTasks):
    bg.add_task(execute_ai_pipeline, req)
    return {"status": "QUEUED", "problemId": req.problemId}

@app.get("/health")
def health():
    return {"status": "ACTIVE", "model": "all-MiniLM-L6-v2"}