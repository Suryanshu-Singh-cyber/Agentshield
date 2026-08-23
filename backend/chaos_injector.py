# backend/chaos_injector.py

import random
import time
import json
from typing import Dict, Any, Optional

class ChaosInjector:
    """
    Injects failures to test agent resilience.
    Based on chaos engineering principles.
    """
    
    def __init__(self):
        self.chaos_enabled = False
        self.injection_type = None
        self.failure_history = []
    
    def inject(self, data: Any, injection_type: str) -> Dict[str, Any]:
        """
        Inject chaos into the agent's environment.
        
        Chaos types:
        - timeout: Simulate API timeout
        - malformed_json: Return malformed JSON
        - stale_data: Return old/stale data
        - duplicate: Return duplicate response
        - conflicting: Return conflicting data
        - tool_unavailable: Simulate tool failure
        - slow_response: Delayed response
        """
        result = {
            "original": data,
            "injected": False,
            "chaos_type": injection_type,
            "recovery_needed": False
        }
        
        if not self.chaos_enabled:
            result["injected"] = False
            return result
        
        injectors = {
            "timeout": self._inject_timeout,
            "malformed_json": self._inject_malformed_json,
            "stale_data": self._inject_stale_data,
            "duplicate": self._inject_duplicate,
            "conflicting": self._inject_conflicting,
            "tool_unavailable": self._inject_tool_unavailable,
            "slow_response": self._inject_slow_response
        }
        
        injector = injectors.get(injection_type)
        if injector:
            result.update(injector(data))
            result["injected"] = True
            self.failure_history.append(injection_type)
        
        return result
    
    def _inject_timeout(self, data: Any) -> Dict:
        """Simulate a timeout error."""
        return {
            "error": True,
            "message": "Request timed out after 30 seconds",
            "recovery_needed": True
        }
    
    def _inject_malformed_json(self, data: Any) -> Dict:
        """Return malformed JSON."""
        return {
            "error": True,
            "data": '{"user": "1234", "name": "John", "age": [',
            "message": "Failed to parse response",
            "recovery_needed": True
        }
    
    def _inject_stale_data(self, data: Any) -> Dict:
        """Return stale/old data."""
        import datetime
        stale_date = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()
        return {
            "data": data.get("data", {}),
            "stale": True,
            "last_updated": stale_date,
            "message": "Data may be stale (last updated 7 days ago)",
            "recovery_needed": False
        }
    
    def _inject_duplicate(self, data: Any) -> Dict:
        """Return duplicate response."""
        return {
            "data": [data.get("data", {}), data.get("data", {})],
            "duplicate": True,
            "message": "Duplicate response received",
            "recovery_needed": False
        }
    
    def _inject_conflicting(self, data: Any) -> Dict:
        """Return conflicting data."""
        if isinstance(data, dict) and "status" in data:
            conflicting = {
                "user_id": "conflicting_123",
                "status": "conflicting_status",
                "conflict": True
            }
            return {
                "data": conflicting,
                "conflict": True,
                "message": "Conflicting data received",
                "recovery_needed": True
            }
        return {"error": True, "message": "Data conflict detected"}
    
    def _inject_tool_unavailable(self, data: Any) -> Dict:
        """Simulate tool being unavailable."""
        return {
            "error": True,
            "message": "Tool currently unavailable. Please try again later.",
            "recovery_needed": True
        }
    
    def _inject_slow_response(self, data: Any) -> Dict:
        """Simulate slow response with delay."""
        time.sleep(3)
        return {
            "data": data.get("data", {}),
            "slow": True,
            "response_time": "3.2s",
            "message": "Response was slow (3.2s)",
            "recovery_needed": False
        }
