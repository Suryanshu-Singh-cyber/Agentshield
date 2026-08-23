# backend/firewall.py

import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class FirewallDecision:
    """Result of firewall evaluation."""
    decision: str  # "allow", "block", "require_approval"
    reason: str
    risk_score: int
    blocked_by: List[str] = field(default_factory=list)

class ActionFirewall:
    """Pre-execution governance layer for AI agent tool calls."""
    
    def __init__(self, mode: str = "enforce"):
        self.mode = mode
        self.risk_threshold = 80
        self.circuit_breaker_state = "OK"
        self.consecutive_warnings = 0
        
        self.risk_weights = {
            "irreversible": 40,
            "requires_confirmation": 30,
            "requires_auth": 20,
            "critical_level": 10
        }
    
    def get_tool_metadata(self, tool_name: str) -> Dict:
        """Retrieve metadata for a given tool."""
        tool_db = {
            "delete_account": {
                "risk_level": RiskLevel.CRITICAL.value,
                "requires_confirmation": True,
                "irreversible": True,
                "requires_auth": True
            },
            "process_refund": {
                "risk_level": RiskLevel.HIGH.value,
                "requires_confirmation": True,
                "irreversible": False,
                "requires_auth": True
            },
            "send_email": {
                "risk_level": RiskLevel.MEDIUM.value,
                "requires_confirmation": False,
                "irreversible": False,
                "requires_auth": False
            },
            "get_customer_profile": {
                "risk_level": RiskLevel.LOW.value,
                "requires_confirmation": False,
                "irreversible": False,
                "requires_auth": False
            },
            "view_order_history": {
                "risk_level": RiskLevel.LOW.value,
                "requires_confirmation": False,
                "irreversible": False,
                "requires_auth": False
            }
        }
        return tool_db.get(tool_name, {})
    
    def calculate_risk_score(self, tool_name: str, arguments: Dict) -> int:
        """Calculate risk score (0-100) for a tool call."""
        metadata = self.get_tool_metadata(tool_name)
        if not metadata:
            return 10
        
        score = 0
        score += self.risk_weights["irreversible"] if metadata.get("irreversible") else 0
        score += self.risk_weights["requires_confirmation"] if metadata.get("requires_confirmation") else 0
        score += self.risk_weights["requires_auth"] if metadata.get("requires_auth") else 0
        score += self.risk_weights["critical_level"] if metadata.get("risk_level") == RiskLevel.CRITICAL.value else 0
        
        return min(100, score)
    
    def evaluate(self, tool_name: str, arguments: Dict, conversation_context: Optional[str] = None) -> FirewallDecision:
        """Evaluate a tool call against policies."""
        risk_score = self.calculate_risk_score(tool_name, arguments)
        blocked_by = []
        
        if risk_score >= 80:
            self.consecutive_warnings += 1
        else:
            self.consecutive_warnings = 0
        
        if self.consecutive_warnings >= 3:
            self.circuit_breaker_state = "STOP"
        
        if self.mode == "off":
            return FirewallDecision("allow", "Firewall disabled", risk_score)
        
        if self.mode == "audit":
            if risk_score >= 80:
                return FirewallDecision("require_approval", f"High risk action ({risk_score}%)", risk_score, blocked_by)
            return FirewallDecision("allow", f"Risk score: {risk_score}%", risk_score)
        
        # ENFORCE mode
        if self.circuit_breaker_state == "STOP":
            return FirewallDecision("block", "Circuit breaker: STOP", risk_score, ["circuit_breaker"])
        
        metadata = self.get_tool_metadata(tool_name)
        if metadata.get("irreversible"):
            blocked_by.append("irreversible_action")
            if risk_score > self.risk_threshold:
                return FirewallDecision("block", f"Irreversible action blocked: {tool_name}", risk_score, blocked_by)
            return FirewallDecision("require_approval", f"Requires approval: {tool_name}", risk_score, blocked_by)
        
        if metadata.get("requires_confirmation") and risk_score > 70:
            blocked_by.append("missing_confirmation")
            return FirewallDecision("block", f"Missing confirmation: {tool_name}", risk_score, blocked_by)
        
        if metadata.get("requires_auth") and risk_score > 50:
            blocked_by.append("unauthorized")
            return FirewallDecision("block", f"Unauthorized: {tool_name}", risk_score, blocked_by)
        
        return FirewallDecision("allow", f"Allowed (risk: {risk_score}%)", risk_score)
