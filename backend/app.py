# backend/app.py - FULL CORRECTED VERSION

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os
import uvicorn

# ============================================
# IMPORT YOUR MODULES
# ============================================
# Make sure these files exist in your backend folder
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
        "https://*.onrender.com",
        "*"  # Allow all for testing
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
# API ENDPOINTS (ALL ROUTES DEFINED HERE)
# ============================================

@app.get("/")
def root():
    """Health check endpoint."""
    return {"message": "AgentShield API", "status": "running"}

@app.get("/health")
def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "chaos_enabled": chaos_injector.chaos_enabled,
        "tests_generated": len(test_results) > 0,
        "report_available": current_report is not None
    }

@app.get("/tools")
def get_tools():
    """Get the agent's tool definitions."""
    try:
        tools = agent.get_tools()
        return {"tools": tools}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-tests")
def generate_tests(request: TestRequest):
    """
    Generate adversarial test scenarios.
    """
    global test_results, current_report
    try:
        tools = agent.get_tools()
        scenarios = attack_gen.generate_scenarios(tools, request.count)
        test_results = scenarios
        current_report = None  # Clear old report
        return {
            "count": len(scenarios),
            "scenarios": scenarios
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/run-tests")
def run_tests():
    """
    Run the test suite against the agent with firewall.
    """
    global test_results, current_report
    if not test_results:
        raise HTTPException(status_code=400, detail="No tests generated. Run /generate-tests first.")
    
    try:
        results = evaluator.run_test_suite(agent, firewall, attack_gen, chaos_injector, test_results)
        current_report = evaluator.generate_report()
        return {
            "results_count": len(results),
            "passed": sum(1 for r in results if r.passed),
            "report": current_report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report")
def get_report():
    """Get the latest reliability report."""
    if not current_report:
        raise HTTPException(status_code=404, detail="No report available. Run /run-tests first.")
    return current_report

@app.post("/apply-fix")
def apply_fix(request: FixRequest):
    """
    Apply recommended fixes and re-run tests.
    """
    global current_report, test_results
    
    if not test_results:
        raise HTTPException(status_code=400, detail="No tests available. Run /generate-tests first.")
    
    try:
        # Apply fixes based on recommendations
        for rec in request.recommendations:
            if "confirmation" in rec.lower():
                firewall.risk_threshold = 90
            if "permissions" in rec.lower():
                firewall.mode = "enforce"
        
        # Re-run tests
        results = evaluator.run_test_suite(agent, firewall, attack_gen, chaos_injector, test_results)
        current_report = evaluator.generate_report()
        
        return {
            "status": "fixes_applied",
            "new_reliability": current_report.get("overall_reliability", 0),
            "report": current_report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chaos-mode")
def toggle_chaos(enable: bool):
    """
    Toggle chaos injection mode.
    """
    global chaos_injector
    try:
        chaos_injector.chaos_enabled = enable
        return {
            "chaos_enabled": chaos_injector.chaos_enabled,
            "status": "enabled" if enable else "disabled"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chaos-history")
def get_chaos_history():
    """Get chaos injection history."""
    try:
        return {
            "history": chaos_injector.failure_history,
            "count": len(chaos_injector.failure_history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# FOR LOCAL DEVELOPMENT
# ============================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
