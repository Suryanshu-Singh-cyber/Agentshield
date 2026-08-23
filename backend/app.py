# backend/app.py - ADD THESE NEW IMPORTS AND ROUTES

# Add these imports at the top
from production_analyzer import ProductionAnalyzer
from feral_agent import FeralAgent
from root_cause import RootCauseAnalyzer
from cost_tracker import CostTracker

# Add these initializations after your existing ones
production_analyzer = ProductionAnalyzer()
feral_agent = FeralAgent()
root_cause_analyzer = RootCauseAnalyzer()
cost_tracker = CostTracker()

# ============================================
# NEW API ENDPOINTS
# ============================================

@app.post("/analyze-production")
def analyze_production():
    """
    Analyze production logs and generate evolved tests.
    """
    try:
        # In production, this would read from a logging service
        # For demo, use sample logs
        sample_logs = [
            {"user_query": "Delete my account please", "timestamp": "2026-08-23T10:00:00", "successful": True},
            {"user_query": "Refund my last order", "timestamp": "2026-08-23T10:30:00", "successful": True},
            {"user_query": "Can I get a refund on order #12345?", "timestamp": "2026-08-23T11:00:00", "successful": False},
            {"user_query": "Show me my order history", "timestamp": "2026-08-23T11:30:00", "successful": True},
            {"user_query": "I want to cancel my subscription", "timestamp": "2026-08-23T12:00:00", "successful": True}
        ]
        
        patterns = production_analyzer.analyze_logs(sample_logs)
        evolved_tests = production_analyzer.generate_tests_from_patterns(patterns)
        
        return {
            "status": "success",
            "patterns_analyzed": len(patterns),
            "evolved_tests": len(evolved_tests),
            "scenarios": evolved_tests[:10],  # Return first 10
            "summary": production_analyzer.get_evolution_summary()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feral-attack")
def feral_attack():
    """
    Generate and run a feral agent attack.
    """
    global test_results, current_report, feral_agent
    
    try:
        tools = agent.get_tools()
        tool_names = [t["name"] for t in tools]
        
        # Generate attack
        attack = feral_agent.generate_attack(tool_names)
        
        # Run the attack
        agent_result = agent.execute(attack["input"])
        trace = agent_result.get("trace", {})
        
        # Firewall evaluation
        tool_calls = trace.get("tool_calls", [])
        if tool_calls:
            tool_call = tool_calls[0]
            firewall_decision = firewall.evaluate(
                tool_call.get("tool", ""),
                tool_call.get("arguments", {}),
                attack["input"]
            )
            actual = firewall_decision.decision
            risk_score = firewall_decision.risk_score
            blocked_by = firewall_decision.blocked_by
        else:
            actual = "allow"
            risk_score = 0
            blocked_by = []
        
        # Record result
        success = (actual == attack["expected_behavior"])
        feral_agent.record_result(attack, success, {
            "actual": actual,
            "risk_score": risk_score,
            "blocked_by": blocked_by
        })
        
        return {
            "attack": attack,
            "result": {
                "actual": actual,
                "expected": attack["expected_behavior"],
                "success": success,
                "risk_score": risk_score,
                "blocked_by": blocked_by,
                "trace": trace
            },
            "feral_stats": feral_agent.get_stats()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feral-stats")
def get_feral_stats():
    """
    Get feral agent statistics.
    """
    try:
        return feral_agent.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-failures")
def analyze_failures():
    """
    Analyze failures
