from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os

from agent import CustomerSupportAgent
from firewall import ActionFirewall
from attack_generator import AttackGenerator
from chaos_injector import ChaosInjector
from evaluator import AgentEvaluator

app = FastAPI(title="AgentShield API", version="1.0.0")

# CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
firewall = ActionFirewall(mode="enforce")
evaluator = AgentEvaluator()
attack_gen = AttackGenerator(llm_client=None)  # Will use LLM in production
chaos_injector = ChaosInjector()

# Simulate agent (will use real LLM in production)
agent = CustomerSupportAgent(llm_client=None)

# State
test_results = []
current_report = None

class TestRequest(BaseModel):
    count: int = 20

class FixRequest(BaseModel):
    recommendations: List[str]

@app.get("/")
def root():
    return {"message": "AgentShield API", "status": "running"}

@app.get("/tools")
def get_tools():
    """Get the agent's tool definitions."""
    return {"tools": agent.get_tools()}

@app.post("/generate-tests")
def generate_tests(request: TestRequest):
    """Generate adversarial test scenarios."""
    global test_results, current_report
    
    tools = agent.get_tools()
    scenarios = attack_gen.generate_scenarios(tools, request.count)
    
    # Store for later
    test_results = scenarios
    
    return {
        "count": len(scenarios),
        "scenarios": scenarios
    }

@app.post("/run-tests")
def run_tests():
    """Run the test suite against the agent with firewall."""
    global test_results, current_report
    
    if not test_results:
        raise HTTPException(status_code=400, detail="No tests generated. Run /generate-tests first.")
    
    # Run tests
    results = evaluator.run_test_suite(agent, firewall, attack_gen, chaos_injector, test_results)
    
    # Generate report
    current_report = evaluator.generate_report()
    
    return {
        "results_count": len(results),
        "passed": sum(1 for r in results if r.passed),
        "report": current_report
    }

@app.get("/report")
def get_report():
    """Get the latest reliability report."""
    if not current_report:
        raise HTTPException(status_code=404, detail="No report available. Run /run-tests first.")
    return current_report

@app.post("/apply-fix")
def apply_fix(request: FixRequest):
    """Apply recommended fixes and re-run tests."""
    global current_report
    
    # Apply fixes (simulate policy changes)
    for rec in request.recommendations:
        if "confirmation" in rec.lower():
            firewall.risk_threshold = 90  # More lenient after fix
        if "permissions" in rec.lower():
            firewall.mode = "enforce"  # Ensure enforce mode
    
    # Re-run tests
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
    """Toggle chaos injection mode."""
    global chaos_injector
    
    chaos_injector.chaos_enabled = enable
    return {"chaos_enabled": chaos_injector.chaos_enabled}

@app.get("/chaos-history")
def get_chaos_history():
    """Get chaos injection history."""
    return {"history": chaos_injector.failure_history}