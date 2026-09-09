# app/main.py
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import requests
import os

from app.models.schemas import TriageRequest, TriageResultResponse
from app.services.triage import evaluate_triage_and_domain, analyze_severity_and_impact
from app.services.deduplication import detect_relationships
from app.services.ranking import rank_top_institutions
from app.data.knowledge_base import JHARKHAND_INSTITUTIONS

app = FastAPI(
    title="JanSetu AI Engine v2",
    description="Multilingual Triage, Severity Estimation, Deduplication & Ranked HEI Recommendation",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

NODE_BACKEND_CALLBACK = os.getenv("NODE_BACKEND_CALLBACK", "http://localhost:5000/api/v1/ai/triage-callback")

# In-memory registry for live frontend polling
AI_JOB_REGISTRY = {}

def process_ai_pipeline(req: TriageRequest):
    pid = req.problemId
    try:
        # State 1: ANALYSING
        AI_JOB_REGISTRY[pid]["status"] = "ANALYSING"
        time.sleep(0.3)

        is_routine, category, confidence = evaluate_triage_and_domain(req.text)
        
        if is_routine:
            AI_JOB_REGISTRY[pid] = {
                "problemId": pid,
                "status": "COMPLETED",
                "category": "Routine Municipal Complaint",
                "confidence": confidence,
                "severity": "LOW",
                "urgency": "LOW",
                "impactLevel": "LOW",
                "estimatedAffectedPop": "Individual / Single Household",
                "similarProblems": [],
                "institutionMatches": [],
                "recommendedAction": "DIVERT_MUNICIPAL"
            }
            return

        severity, urgency, impact, pop = analyze_severity_and_impact(req.text, category)

        # State 2: MATCHING
        AI_JOB_REGISTRY[pid]["status"] = "MATCHING"
        time.sleep(0.3)

        similar_probs, relation_action = detect_relationships(req.text, req.latitude, req.longitude)
        ranked_institutions = rank_top_institutions(category, req.district, req.latitude, req.longitude, top_k=4)

        # Determine Final Action
        if relation_action == "REUSE_EXISTING_SOLUTION":
            final_action = "REUSE_EXISTING_SOLUTION"
        elif relation_action == "ADAPT_SIMILAR_BLUEPRINT":
            final_action = "ADAPT_EXISTING_BLUEPRINT"
        else:
            final_action = "ROUTE_TO_INSTITUTION"

        result_payload = {
            "problemId": pid,
            "status": "COMPLETED",
            "category": category,
            "confidence": confidence,
            "severity": severity,
            "urgency": urgency,
            "impactLevel": impact,
            "estimatedAffectedPop": pop,
            "similarProblems": [m.model_dump() for m in similar_probs],
            "institutionMatches": [inst.model_dump() for inst in ranked_institutions],
            "recommendedAction": final_action
        }

        AI_JOB_REGISTRY[pid] = result_payload

        # Optional Webhook callback to Node.js backend
        try:
            requests.post(NODE_BACKEND_CALLBACK, json=result_payload, timeout=2)
        except Exception:
            pass

    except Exception as e:
        AI_JOB_REGISTRY[pid] = {"problemId": pid, "status": "FAILED", "error": str(e)}

@app.post("/triage")
def trigger_triage(req: TriageRequest, bg: BackgroundTasks):
    AI_JOB_REGISTRY[req.problemId] = {
        "problemId": req.problemId,
        "status": "QUEUED"
    }
    bg.add_task(process_ai_pipeline, req)
    return {"status": "QUEUED", "problemId": req.problemId, "message": "Analysis initiated."}

@app.get("/triage/{problem_id}", response_model=TriageResultResponse)
def get_triage_status(problem_id: str):
    if problem_id not in AI_JOB_REGISTRY:
        raise HTTPException(status_code=404, detail="Problem ticket not found in AI engine.")
    return AI_JOB_REGISTRY[problem_id]

@app.get("/health")
def health():
    return {
        "status": "READY",
        "engine": "JanSetu-AI-v2",
        "supported_domains": 14,
        "active_institutions": len(JHARKHAND_INSTITUTIONS)
    }