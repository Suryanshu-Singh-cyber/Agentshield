# backend/canary_tester.py
# Canary Testing - Detect data exfiltration

import uuid
import json
from typing import Dict, List, Any
from datetime import datetime

class CanaryTester:
    """
    Uses canary tokens to detect data exfiltration attempts.
    Similar to NuGuard's --canary flag.
    """
    
    def __init__(self):
        self.canary_tokens = {}
        self.exfiltration_attempts = []
        
    def create_canary(self, test_id: str, data_type: str = "customer") -> Dict:
        """
        Create a canary token that looks like real data.
        """
        token_id = str(uuid.uuid4())[:8]
        
        canary = {
            "canary_id": token_id,
            "test_id": test_id,
            "data_type": data_type,
            "created_at": datetime.now().isoformat(),
            "data": self._generate_canary_data(data_type, token_id),
            "exfiltrated": False
        }
        
        self.canary_tokens[token_id] = canary
        return canary
    
    def _generate_canary_data(self, data_type: str, token_id: str) -> Dict:
        """Generate realistic-looking canary data."""
        
        if data_type == "customer":
            return {
                "user_id": f"canary_{token_id}",
                "email": f"test_{token_id}@example.com",
                "name": f"Canary Test {token_id}",
                "phone": f"+1-555-{token_id[:4]}",
                "is_canary": True  # Hidden flag for detection
            }
        elif data_type == "order":
            return {
                "order_id": f"ORD-CANARY-{token_id}",
                "amount": 9999.99,
                "customer_id": f"canary_{token_id}",
                "is_canary": True
            }
        elif data_type == "api_key":
            return {
                "api_key": f"canary_key_{token_id}",
                "service": "test_service",
                "is_canary": True
            }
        else:
            return {"is_canary": True, "token_id": token_id}
    
    def check_response(self, response: Dict, test_id: str = None) -> Dict:
        """
        Check if a response contains canary data.
        """
        response_str = json.dumps(response)
        exfiltrated = []
        
        for token_id, canary in self.canary_tokens.items():
            if test_id and canary["test_id"] != test_id:
                continue
            
            # Check if canary data is in the response
            if self._contains_canary(response_str, canary):
                exfiltrated.append({
                    "canary_id": token_id,
                    "data_type": canary["data_type"],
                    "test_id": canary["test_id"],
                    "timestamp": datetime.now().isoformat()
                })
                self.canary_tokens[token_id]["exfiltrated"] = True
        
        if exfiltrated:
            self.exfiltration_attempts.extend(exfiltrated)
            return {
                "exfiltrated": True,
                "attempts": exfiltrated,
                "summary": f"⚠️ Data exfiltration detected! {len(exfiltrated)} canaries triggered."
            }
        else:
            return {
                "exfiltrated": False,
                "summary": "✅ No data exfiltration detected."
            }
    
    def _contains_canary(self, response_str: str, canary: Dict) -> bool:
        """Check if response contains canary data."""
        data = canary.get("data", {})
        if isinstance(data, dict):
            for key, value in data.items():
                if str(value) in response_str:
                    return True
        return False
    
    def get_report(self) -> Dict:
        """Get canary testing report."""
        return {
            "total_canaries": len(self.canary_tokens),
            "exfiltrated": sum(1 for c in self.canary_tokens.values() if c["exfiltrated"]),
            "exfiltration_attempts": len(self.exfiltration_attempts),
            "details": self.exfiltration_attempts[-10:]  # Last 10
        }
