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
class ToolCapability:
    """Risk metadata for a tool."""
    name: str
    risk_level: RiskLevel
    requires_confirmation: bool = False
    irreversible: bool = False
    requires_auth: bool = False

@dataclass
class FirewallDecision:
    """Result of firewall evaluation."""
    decision: str  # "allow", "block", "require_approval"
    reason: str
    risk_score: int  # 0-100
    blocked_by: List[str] = field(default_factory=list)

class ActionFirewall:
    """
    Pre-execution governance layer for AI agent tool calls.
    Based on the Decision Intelligence Core (DIC) pattern. [citation:4]
    """
    
    def __init__(self, mode: str = "enforce"):
        """
        mode: "off", "audit", "enforce"
        """
        self.mode = mode
        self.risk_threshold = 80  # Block actions above this score
        self.circuit_breaker_state = "OK"  # OK → WARN → SLOW → STOP → ESCALATE
        self.consecutive_warnings = 0
        self.consecutive_stops = 0
        
        # Risk scoring matrix
        self.risk_weights = {
            "irreversible": 40,
            "requires_confirmation": 30,
            "requires_auth": 20,
            "critical_level": 10
        }
    
    def get_tool_metadata(self, tool_name: str) -> Dict:
        """Retrieve metadata for a given tool."""
        # In production, this would query a database or policy store
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
            return 10  # Unknown tool: low risk default
        
        score = 0
        score += self.risk_weights["irreversible"] if metadata.get("irreversible") else 0
        score += self.risk_weights["requires_confirmation"] if metadata.get("requires_confirmation") else 0
        score += self.risk_weights["requires_auth"] if metadata.get("requires_auth") else 0
        score += self.risk_weights["critical_level"] if metadata.get("risk_level") == RiskLevel.CRITICAL.value else 0
        
        return min(100, score)
    
    def evaluate(self, tool_name: str, arguments: Dict, conversation_context: Optional[str] = None) -> FirewallDecision:
        """
        Evaluate a tool call against policies.
        Returns: allow, block, or require_approval. [citation:4][citation:8]
        """
        risk_score = self.calculate_risk_score(tool_name, arguments)
        blocked_by = []
        
        # Track risk for circuit breaker logic
        if risk_score >= 80:
            self.consecutive_warnings += 1
        else:
            self.consecutive_warnings = 0
        
        # Circuit breaker escalation
        if self.consecutive_warnings >= 3:
            self.circuit_breaker_state = "STOP"
        elif self.consecutive_warnings >= 2:
            self.circuit_breaker_state = "SLOW"
        
        # Decision logic
        if self.mode == "off":
            return FirewallDecision("allow", "Firewall disabled", risk_score)
        
        if self.mode == "audit":
            if risk_score >= 80:
                return FirewallDecision("require_approval", f"High risk action ({risk_score}%)", risk_score, blocked_by)
            return FirewallDecision("allow", f"Risk score: {risk_score}%", risk_score)
        
        # ENFORCE mode (production)
        if self.circuit_breaker_state == "STOP":
            return FirewallDecision("block", "Circuit breaker: STOP (too many high-risk actions)", risk_score, ["circuit_breaker"])
        
        # Check irreversible actions
        metadata = self.get_tool_metadata(tool_name)
        if metadata.get("irreversible"):
            blocked_by.append("irreversible_action")
            if risk_score > self.risk_threshold:
                return FirewallDecision("block", f"Irreversible action blocked: {tool_name}", risk_score, blocked_by)
            return FirewallDecision("require_approval", f"Requires human approval: {tool_name}", risk_score, blocked_by)
        
        # Check high-risk actions without confirmation
        if metadata.get("requires_confirmation") and risk_score > 70:
            blocked_by.append("missing_confirmation")
            return FirewallDecision("block", f"Missing confirmation for {tool_name}", risk_score, blocked_by)
        
        # Check authorization
        if metadata.get("requires_auth") and risk_score > 50:
            blocked_by.append("unauthorized")
            return FirewallDecision("block", f"Unauthorized action: {tool_name}", risk_score, blocked_by)
        
        return FirewallDecision("allow", f"Action allowed (risk: {risk_score}%)", risk_score)
    
    def get_policy_annotation(self, conversation_id: str) -> str:
        """Get system prompt annotation for flagged conversations.""" 
        # Monotonic flag: once flagged, stays flagged until cleared [citation:8]
        return "⚠️ This conversation is FLAGGED for untrusted content. All destructive actions are BLOCKED."
