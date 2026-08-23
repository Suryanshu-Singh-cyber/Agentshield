# backend/root_cause.py
# Failure Taxonomy with Root Cause Graph

from typing import List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum

class FailureCategory(Enum):
    """Taxonomy of failure categories."""
    TOOL_SELECTION = "tool_selection"
    CONFIRMATION_MISSING = "confirmation_missing"
    PERMISSION_VIOLATION = "permission_violation"
    IRREVERSIBLE_ACTION = "irreversible_action"
    GOAL_DRIFT = "goal_drift"
    HALLUCINATION = "hallucination"
    CIRCUIT_BREAKER = "circuit_breaker"

@dataclass
class FailureNode:
    """A node in the failure root cause graph."""
    step: int
    event: str
    detail: str
    severity: str = "info"
    children: List['FailureNode'] = field(default_factory=list)

class RootCauseAnalyzer:
    """
    Analyzes failures and generates visual root cause graphs.
    Provides structured failure taxonomy.
    """
    
    def __init__(self):
        self.failure_taxonomy = {
            "tool_selection": {
                "code": "TS-001",
                "description": "Agent selected wrong tool for the task",
                "fix": "Improve tool descriptions and agent reasoning"
            },
            "confirmation_missing": {
                "code": "CM-001",
                "description": "Agent skipped required confirmation step",
                "fix": "Add explicit confirmation gate for the tool"
            },
            "permission_violation": {
                "code": "PV-001",
                "description": "Agent attempted action without proper authorization",
                "fix": "Implement RBAC (Role-Based Access Control)"
            },
            "irreversible_action": {
                "code": "IA-001",
                "description": "Agent attempted irreversible action without approval",
                "fix": "Require human approval for destructive actions"
            },
            "goal_drift": {
                "code": "GD-001",
                "description": "Agent drifted from original goal",
                "fix": "Add goal tracking and validation"
            },
            "hallucination": {
                "code": "HL-001",
                "description": "Agent invented facts not in context",
                "fix": "Improve grounding with RAG (Retrieval-Augmented Generation)"
            },
            "circuit_breaker": {
                "code": "CB-001",
                "description": "Circuit breaker triggered due to repeated failures",
                "fix": "Review failure patterns and reduce risk tolerance"
            }
        }
    
    def trace_failure(self, failure: Dict) -> Dict:
        """
        Trace the root cause of a failure.
        Returns a visual chain of events.
        """
        input_text = failure.get("input", "")
        tool = failure.get("tool", "unknown")
        blocked_by = failure.get("blocked_by", [])
        attack_type = failure.get("attack_type", "unknown")
        
        # Build the failure chain
        chain = [
            FailureNode(step=1, event="USER INPUT", detail=input_text[:100]),
            FailureNode(step=2, event="INTENT", detail=self._extract_intent(input_text)),
            FailureNode(step=3, event="TOOL SELECTED", detail=tool),
        ]
        
        # Identify missing checks
        missing_checks = self._identify_missing_checks(blocked_by, attack_type)
        for check in missing_checks:
            chain.append(FailureNode(
                step=len(chain) + 1,
                event="MISSING CHECK",
                detail=check,
                severity="warning"
            ))
        
        # Determine root cause category
        root_cause = self._classify_root_cause(blocked_by, attack_type)
        
        # Add failure node
        chain.append(FailureNode(
            step=len(chain) + 1,
            event="FAILURE",
            detail=root_cause["description"],
            severity="critical"
        ))
        
        # Build taxonomy mapping
        taxonomy = self._get_taxonomy_for_failure(root_cause["category"])
        
        # Build children relationships
        for i in range(len(chain) - 1):
            chain[i].children.append(chain[i + 1])
        
        return {
            "chain": [vars(node) for node in chain],
            "root_cause": root_cause,
            "taxonomy": taxonomy,
            "fix_recommendation": root_cause.get("fix", "Review agent behavior and policies.")
        }
    
    def _extract_intent(self, text: str) -> str:
        """Extract intent from user input."""
        text_lower = text.lower()
        if "delete" in text_lower or "remove" in text_lower:
            return "Deletion request"
        elif "refund" in text_lower or "return" in text_lower:
            return "Refund request"
        elif "update" in text_lower or "change" in text_lower:
            return "Update request"
        elif "view" in text_lower or "get" in text_lower or "show" in text_lower:
            return "View request"
        else:
            return "General request"
    
    def _identify_missing_checks(self, blocked_by: List[str], attack_type: str) -> List[str]:
        """Identify what checks were missing."""
        checks = []
        
        if "confirmation" in str(blocked_by) or "confirmation" in attack_type:
            checks.append("Missing confirmation step")
        if "irreversible" in str(blocked_by) or "destructive" in attack_type:
            checks.append("No approval for irreversible action")
        if "authorization" in str(blocked_by) or "authority" in attack_type:
            checks.append("Missing authorization check")
        if "tool_misuse" in attack_type:
            checks.append("Tool argument validation missing")
        
        if not checks:
            checks.append("Unknown missing check - review system")
        
        return checks
    
    def _classify_root_cause(self, blocked_by: List[str], attack_type: str) -> Dict:
        """Classify the root cause of failure."""
        if "irreversible" in str(blocked_by) or "destructive" in attack_type:
            return {
                "category": "irreversible_action",
                "description": "Irreversible action attempted without proper approval",
                "severity": "critical",
                "fix": "Add human approval workflow for destructive actions"
            }
        elif "confirmation" in str(blocked_by) or "confirmation" in attack_type:
            return {
                "category": "confirmation_missing",
                "description": "Agent skipped required confirmation step",
                "severity": "high",
                "fix": "Implement explicit confirmation gate"
            }
        elif "authority" in attack_type or "authorization" in str(blocked_by):
            return {
                "category": "permission_violation",
                "description": "Agent attempted action without proper authorization",
                "severity": "high",
                "fix": "Implement RBAC and proper authentication"
            }
        elif "misuse" in attack_type:
            return {
                "category": "tool_selection",
                "description": "Agent misused a tool with incorrect parameters",
                "severity": "medium",
                "fix": "Add parameter validation for tools"
            }
        else:
            return {
                "category": "unknown",
                "description": "Unclassified failure pattern",
                "severity": "medium",
                "fix": "Review agent behavior and add specific policies"
            }
    
    def _get_taxonomy_for_failure(self, category: str) -> Dict:
        """Get taxonomy details for a failure category."""
        return self.failure_taxonomy.get(category, {
            "code": "UNK-001",
            "description": "Unknown failure category",
            "fix": "Review and classify the failure"
        })
    
    def generate_failure_report(self, failures: List[Dict]) -> Dict:
        """
        Generate a comprehensive failure report with taxonomy.
        """
        if not failures:
            return {"message": "No failures to analyze", "taxonomy": []}
        
        report = {
            "total_failures": len(failures),
            "taxonomy_breakdown": {},
            "critical_failures": [],
            "high_failures": [],
            "medium_failures": [],
            "recommendations": [],
            "failure_chains": []
        }
        
        for failure in failures:
            trace = self.trace_failure(failure)
            severity = trace["root_cause"].get("severity", "medium")
            
            # Add to breakdown
            category = trace["root_cause"]["category"]
            if category not in report["taxonomy_breakdown"]:
                report["taxonomy_breakdown"][category] = {
                    "count": 0,
                    "code": trace["taxonomy"]["code"],
                    "description": trace["taxonomy"]["description"]
                }
            report["taxonomy_breakdown"][category]["count"] += 1
            
            # Add to severity lists
            failure_entry = {
                "input": failure.get("input", "")[:100],
                "root_cause": trace["root_cause"]["description"],
                "fix": trace["fix_recommendation"]
            }
            
            if severity == "critical":
                report["critical_failures"].append(failure_entry)
            elif severity == "high":
                report["high_failures"].append(failure_entry)
            else:
                report["medium_failures"].append(failure_entry)
            
            # Add recommendations
            if trace["fix_recommendation"] not in report["recommendations"]:
                report["recommendations"].append(trace["fix_recommendation"])
            
            # Add chain for visualization
            report["failure_chains"].append({
                "input": failure.get("input", ""),
                "chain": trace["chain"],
                "root_cause": trace["root_cause"]["description"]
            })
        
        return report
