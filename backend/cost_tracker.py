# backend/cost_tracker.py
# Cost-Per-Test Analytics

from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class TestCost:
    test_id: str
    api_calls: int
    tokens_used: int
    cost: float
    timestamp: str
    test_type: str

class CostTracker:
    """
    Tracks the cost of running tests.
    Provides analytics on cost per test, cost per pass, etc.
    """
    
    def __init__(self):
        self.total_cost = 0.0
        self.test_costs: List[TestCost] = []
        self.total_tokens = 0
        self.total_api_calls = 0
        
        # Pricing model (example - adjust based on actual LLM provider)
        self.COST_PER_1K_TOKENS = 0.001  # $0.001 per 1K tokens
        self.COST_PER_API_CALL = 0.0001   # $0.0001 per API call
    
    def track_test(self, test_id: str, api_calls: int, tokens_used: int, test_type: str = "default") -> float:
        """
        Track the cost of a test run.
        """
        cost = self._calculate_cost(api_calls, tokens_used)
        
        self.total_cost += cost
        self.total_api_calls += api_calls
        self.total_tokens += tokens_used
        
        test_cost = TestCost(
            test_id=test_id,
            api_calls=api_calls,
            tokens_used=tokens_used,
            cost=cost,
            timestamp=datetime.now().isoformat(),
            test_type=test_type
        )
        self.test_costs.append(test_cost)
        
        return cost
    
    def _calculate_cost(self, api_calls: int, tokens_used: int) -> float:
        """
        Calculate cost based on usage.
        """
        token_cost = (tokens_used / 1000) * self.COST_PER_1K_TOKENS
        api_cost = api_calls * self.COST_PER_API_CALL
        return token_cost + api_cost
    
    def get_summary(self) -> Dict:
        """
        Get a summary of all costs.
        """
        total_tests = len(self.test_costs)
        if total_tests == 0:
            return {
                "total_cost": 0.0,
                "total_tests": 0,
                "cost_per_test": 0.0,
                "cost_per_pass": 0.0,
                "cost_per_failure": 0.0,
                "total_api_calls": 0,
                "total_tokens": 0
            }
        
        # Calculate passed vs failed (assuming test_type indicates)
        passed_tests = [t for t in self.test_costs if "pass" in t.test_type.lower()]
        failed_tests = [t for t in self.test_costs if "fail" in t.test_type.lower()]
        
        cost_passed = sum(t.cost for t in passed_tests)
        cost_failed = sum(t.cost for t in failed_tests)
        
        return {
            "total_cost": round(self.total_cost, 4),
            "total_tests": total_tests,
            "cost_per_test": round(self.total_cost / total_tests, 4),
            "cost_per_pass": round(cost_passed / len(passed_tests), 4) if passed_tests else 0,
            "cost_per_failure": round(cost_failed / len(failed_tests), 4) if failed_tests else 0,
            "total_api_calls": self.total_api_calls,
            "total_tokens": self.total_tokens,
            "most_expensive_tests": self._get_most_expensive_tests(5)
        }
    
    def _get_most_expensive_tests(self, limit: int = 5) -> List[Dict]:
        """
        Get the most expensive tests.
        """
        sorted_tests = sorted(self.test_costs, key=lambda t: t.cost, reverse=True)
        return [
            {
                "test_id": t.test_id,
                "cost": round(t.cost, 4),
                "api_calls": t.api_calls,
                "tokens_used": t.tokens_used,
                "timestamp": t.timestamp
            }
            for t in sorted_tests[:limit]
        ]
    
    def get_cost_breakdown(self) -> Dict:
        """
        Get cost breakdown by test type.
        """
        breakdown = {}
        for test in self.test_costs:
            if test.test_type not in breakdown:
                breakdown[test.test_type] = {
                    "count": 0,
                    "total_cost": 0.0,
                    "avg_cost": 0.0,
                    "total_tokens": 0,
                    "total_api_calls": 0
                }
            breakdown[test.test_type]["count"] += 1
            breakdown[test.test_type]["total_cost"] += test.cost
            breakdown[test.test_type]["total_tokens"] += test.tokens_used
            breakdown[test.test_type]["total_api_calls"] += test.api_calls
        
        for test_type in breakdown:
            count = breakdown[test_type]["count"]
            if count > 0:
                breakdown[test_type]["avg_cost"] = round(breakdown[test_type]["total_cost"] / count, 4)
        
        return breakdown
    
    def get_optimization_suggestions(self) -> List[str]:
        """
        Generate cost optimization suggestions.
        """
        suggestions = []
        
        if not self.test_costs:
            return ["Run tests to get cost insights."]
        
        expensive_tests = self._get_most_expensive_tests(3)
        if expensive_tests:
            suggestions.append(f"🔍 Optimize these expensive tests: {', '.join(t['test_id'] for t in expensive_tests)}")
        
        avg_cost = self.total_cost / len(self.test_costs) if self.test_costs else 0
        if avg_cost > 0.01:
            suggestions.append("💡 High average test cost. Consider caching or reducing API calls.")
        
        if self.total_api_calls > 100:
            suggestions.append("💡 Many API calls. Consider batching or using more efficient prompts.")
        
        if not suggestions:
            suggestions.append("✅ Cost performance is good. Continue monitoring.")
        
        return suggestions
    
    def reset(self):
        """Reset all cost tracking data."""
        self.total_cost = 0.0
        self.test_costs = []
        self.total_tokens = 0
        self.total_api_calls = 0
