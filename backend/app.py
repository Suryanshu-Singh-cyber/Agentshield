# backend/app.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os
import uvicorn

# Import your modules
from agent import CustomerSupportAgent
from firewall import ActionFirewall
from attack_generator import AttackGenerator
from chaos_injector import ChaosInjector
from evaluator import AgentEvaluator

# ============================================
# APP INITIALIZATION
# ============================================
app = FastAPI(
    title="AgentShield API",
    version="1.0.0",
    description="AI Agent Reliability Engineering Platform"
)

# CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://localhost:8000",
        "https://*.streamlit.app",
        "https://*.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# INITIALIZE COMPONENTS
# ============================================
firewall = ActionFirewall(mode="enforce")
evaluator = AgentEvaluator()
attack_gen = AttackGenerator(llm_client=None)
chaos_injector = ChaosInjector()
agent = CustomerSupportAgent(llm_client=None)

# State
test_results = []
current_report = None

# ============================================
# API MODELS
# ============================================
class TestRequest(BaseModel):
    count: int = 20

class FixRequest(BaseModel):
    recommendations: List[str]

# ============================================
# API ENDPOINTS
# ============================================
@app.get("/")
def root():
    return {"message": "AgentShield API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/tools")
def get_tools():
    return {"tools": agent.get_tools()}

@app.post("/generate-tests")
def generate_tests(request: TestRequest):
    global test_results, current_report
    tools = agent.get_tools()
    scenarios = attack_gen.generate_scenarios(tools, request.count)
    test_results = scenarios
    return {
        "count": len(scenarios),
        "scenarios": scenarios
    }

@app.post("/run-tests")
def run_tests():
    global test_results, current_report
    if not test_results:
        raise HTTPException(status_code=400, detail="No tests generated")
    results = evaluator.run_test_suite(agent, firewall, attack_gen, chaos_injector, test_results)
    current_report = evaluator.generate_report()
    return {
        "results_count": len(results),
        "passed": sum(1 for r in results if r.passed),
        "report": current_report
    }

@app.get("/report")
def get_report():
    if not current_report:
        raise HTTPException(status_code=404, detail="No report available")
    return current_report

@app.post("/apply-fix")
def apply_fix(request: FixRequest):
    global current_report, test_results
    for rec in request.recommendations:
        if "confirmation" in rec.lower():
            firewall.risk_threshold = 90
        if "permissions" in rec.lower():
            firewall.mode = "enforce"
    if not test_results:
        raise HTTPException(status_code=400, detail="No tests available")
    results = evaluator.run_test_suite(agent, firewall, attack_gen, chaos_injector, test_results)
    current_report = evaluator.generate_report()
    return {
        "status": "fixes_applied",
        "new_reliability": current_report["overall_reliability"],
        "report": current_report
    }

@app.post("/chaos-mode")
def toggle_chaos(enable: bool):
    global chaos_injector
    chaos_injector.chaos_enabled = enable
    return {"chaos_enabled": chaos_injector.chaos_enabled}

@app.get("/chaos-history")
def get_chaos_history():
    return {"history": chaos_injector.failure_history}
