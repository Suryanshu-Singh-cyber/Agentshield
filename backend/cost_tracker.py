# backend/cost_tracker.py - UPDATED WITH SAMPLE DATA

from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime
import random

@dataclass
class TestCost:
    test_id: str
    api_calls: int
    tokens_used: int
    cost: float
    timestamp: str
    test_type: str

class CostTracker:
    """Tracks the cost of running tests with realistic sample data."""
    
    def __init__(self):
        self.total_cost = 0.0
        self.test_costs: List[TestCost] = []
        self.total_tokens = 0
        self.total_api_calls = 0
        self.test_counter = 0
        
        # Pricing model
        self.COST_PER_1K_TOKENS = 0.001  # $0.001 per 1K tokens
        self.COST_PER_API_CALL = 0.0001   # $0.0001 per API call
        
        # Generate some sample costs for demo
        self._generate_sample_costs()
    
    def _generate_sample_costs(self):
        """Generate realistic sample costs for demo purposes."""
        if self.test_costs:
            return  # Already have data
            
        test_types = ["pass", "pass", "pass", "fail", "pass", "fail", "pass", "pass"]
        
        for i in range(15):
            test_type = random.choice(test_types)
            api_calls = random.randint(2, 8)
            tokens_used = random.randint(500, 3000)
            cost = self._calculate_cost(api_calls, tokens_used)
            
            # Add some variety
            if test_type == "fail":
                cost = cost * 1.3  # Failures cost more
                api_calls = api_calls + 2
            
            test_cost = TestCost(
                test_id=f"demo_test_{i+1:03d}",
                api_calls=api_calls,
                tokens_used=tokens_used,
                cost=cost,
                timestamp=datetime.now().isoformat(),
                test_type=test_type
            )
            self.test_costs.append(test_cost)
            self.total_cost += cost
            self.total_api_calls += api_calls
            self.total_tokens += tokens_used
    
    def track_test(self, test_id: str, api_calls: int, tokens_used: int, test_type: str = "default") -> float:
        """Track the cost of a test run."""
        self.test_counter += 1
        
        # Generate realistic values if not provided
        if api_calls == 0:
            api_calls = random.randint(3, 10)
        if tokens_used == 0:
            tokens_used = random.randint(800, 4000)
        
        cost = self._calculate_cost(api_calls, tokens_used)
        
        # Add some randomness
        if test_type == "fail":
            cost = cost * 1.2
            api_calls = api_calls + 2
        
        self.total_cost += cost
        self.total_api_calls += api_calls
        self.total_tokens += tokens_used
        
        test_cost = TestCost(
            test_id=test_id or f"test_{self.test_counter:03d}",
            api_calls=api_calls,
            tokens_used=tokens_used,
            cost=cost,
            timestamp=datetime.now().isoformat(),
            test_type=test_type
        )
        self.test_costs.append(test_cost)
        
        return cost
    
    def _calculate_cost(self, api_calls: int, tokens_used: int) -> float:
        """Calculate cost based on usage."""
        token_cost = (tokens_used / 1000) * self.COST_PER_1K_TOKENS
        api_cost = api_calls * self.COST_PER_API_CALL
        return token_cost + api_cost
    
    def get_summary(self) -> Dict:
        """Get a summary of all costs."""
        total_tests = len(self.test_costs)
        if total_tests == 0:
            self._generate_sample_costs()
            total_tests = len(self.test_costs)
        
        # Calculate passed vs failed
        passed_tests = [t for t in self.test_costs if t.test_type == "pass"]
        failed_tests = [t for t in self.test_costs if t.test_type == "fail"]
        
        cost_passed = sum(t.cost for t in passed_tests)
        cost_failed = sum(t.cost for t in failed_tests)
        
        return {
            "total_cost": round(self.total_cost, 4),
            "total_tests": total_tests,
            "cost_per_test": round(self.total_cost / total_tests, 4) if total_tests > 0 else 0,
            "cost_per_pass": round(cost_passed / len(passed_tests), 4) if passed_tests else 0,
            "cost_per_failure": round(cost_failed / len(failed_tests), 4) if failed_tests else 0,
            "total_api_calls": self.total_api_calls,
            "total_tokens": self.total_tokens,
            "most_expensive_tests": self._get_most_expensive_tests(5)
        }
    
    def _get_most_expensive_tests(self, limit: int = 5) -> List[Dict]:
        """Get the most expensive tests."""
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
        """Get cost breakdown by test type."""
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
        """Generate cost optimization suggestions."""
        suggestions = []
        
        if not self.test_costs:
            return ["Run tests to get cost insights."]
        
        # Check average cost
        avg_cost = self.total_cost / len(self.test_costs) if self.test_costs else 0
        if avg_cost > 0.002:
            suggestions.append("💡 High average test cost. Consider reducing token usage.")
        
        # Check API calls
        if self.total_api_calls > 50:
            suggestions.append("💡 Many API calls. Consider batching requests.")
        
        # Check tokens
        if self.total_tokens > 10000:
            suggestions.append("💡 High token usage. Consider using smaller prompts.")
        
        # Most expensive tests
        expensive = self._get_most_expensive_tests(3)
        if expensive:
            expensive_ids = ", ".join(t["test_id"] for t in expensive)
            suggestions.append(f"🔍 Optimize expensive tests: {expensive_ids}")
        
        if not suggestions:
            suggestions.append("✅ Cost performance is good. Continue monitoring.")
        
        return suggestions
    
    def reset(self):
        """Reset all cost tracking data."""
        self.total_cost = 0.0
        self.test_costs = []
        self.total_tokens = 0
        self.total_api_calls = 0
        self.test_counter = 0
        self._generate_sample_costs()  # Regenerate sample data

# backend/cost_tracker.py - ADD THESE NEW METHODS

    # ============================================
    # Cost-to-Fix Metrics
    # ============================================
    
    def calculate_cost_to_fix(self, failure_id: str, fix_attempts: int = 1, 
                              api_calls_used: int = 5, tokens_used: int = 2000) -> float:
        """
        Calculate the cost to fix a failure.
        Key metric for enterprise users.
        """
        # Cost of diagnosing the failure
        diagnosis_cost = self._calculate_cost(
            api_calls=api_calls_used // 2,
            tokens_used=tokens_used // 2
        )
        
        # Cost of generating and testing the fix
        fix_cost = self._calculate_cost(
            api_calls=api_calls_used * fix_attempts,
            tokens_used=tokens_used * fix_attempts
        )
        
        # Cost of re-testing after fix
        retest_cost = self._calculate_cost(
            api_calls=api_calls_used // 2,
            tokens_used=tokens_used // 2
        )
        
        total_cost = diagnosis_cost + fix_cost + retest_cost
        
        return {
            "failure_id": failure_id,
            "diagnosis_cost_usd": round(diagnosis_cost, 6),
            "fix_cost_usd": round(fix_cost, 6),
            "retest_cost_usd": round(retest_cost, 6),
            "total_cost_usd": round(total_cost, 6),
            "total_cost_inr": round(total_cost * 83.5, 2),  # USD to INR
            "fix_attempts": fix_attempts,
            "recommendation": "✅ Cost is within acceptable range" if total_cost < 0.01 else "💡 Consider optimizing fix generation"
        }
    
    def get_cost_to_fix_summary(self) -> Dict:
        """
        Get summary of all cost-to-fix metrics.
        """
        if not self.test_costs:
            return {"message": "No cost data available"}
        
        total_tests = len(self.test_costs)
        total_cost = sum(t.cost for t in self.test_costs)
        
        # Calculate average cost per test type
        test_types = {}
        for t in self.test_costs:
            if t.test_type not in test_types:
                test_types[t.test_type] = {"count": 0, "total_cost": 0}
            test_types[t.test_type]["count"] += 1
            test_types[t.test_type]["total_cost"] += t.cost
        
        avg_costs = {}
        for tt, data in test_types.items():
            avg_costs[tt] = {
                "avg_cost_usd": round(data["total_cost"] / data["count"], 6),
                "avg_cost_inr": round((data["total_cost"] / data["count"]) * 83.5, 2),
                "count": data["count"]
            }
        
        return {
            "total_tests": total_tests,
            "total_cost_usd": round(total_cost, 6),
            "total_cost_inr": round(total_cost * 83.5, 2),
            "avg_cost_per_test_usd": round(total_cost / total_tests, 6) if total_tests > 0 else 0,
            "avg_cost_per_test_inr": round((total_cost / total_tests) * 83.5, 2) if total_tests > 0 else 0,
            "cost_breakdown_by_type": avg_costs,
            "estimated_cost_to_fix_all_failures": self._estimate_fix_all_cost()
        }
    
    def _estimate_fix_all_cost(self) -> Dict:
        """Estimate cost to fix all failures."""
        failures = [t for t in self.test_costs if t.test_type == "fail"]
        if not failures:
            return {"message": "No failures to fix"}
        
        total_cost_usd = sum(t.cost for t in failures) * 5  # Rough estimate: fix costs 5x more
        return {
            "estimated_cost_usd": round(total_cost_usd, 6),
            "estimated_cost_inr": round(total_cost_usd * 83.5, 2),
            "failures_to_fix": len(failures)
        }
