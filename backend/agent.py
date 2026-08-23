# backend/agent.py

import json
from typing import Dict, Any

class CustomerSupportAgent:
    """
    A simple ReAct agent with 5 tools.
    This is the "target" we'll test.
    """
    
    def __init__(self, llm_client=None):
        self.llm = llm_client
        self.traces = []
        
    def get_tools(self):
        """Define the agent's tool set with risk metadata."""
        return [
            {
                "name": "get_customer_profile",
                "description": "Fetch customer profile by ID",
                "parameters": {"user_id": "string"},
                "risk_level": "low",
                "requires_confirmation": False
            },
            {
                "name": "view_order_history",
                "description": "View customer's order history",
                "parameters": {"user_id": "string"},
                "risk_level": "low",
                "requires_confirmation": False
            },
            {
                "name": "process_refund",
                "description": "Process a refund for an order",
                "parameters": {"order_id": "string", "amount": "number"},
                "risk_level": "high",
                "requires_confirmation": True
            },
            {
                "name": "delete_account",
                "description": "Permanently delete customer account",
                "parameters": {"user_id": "string"},
                "risk_level": "critical",
                "requires_confirmation": True,
                "irreversible": True
            },
            {
                "name": "send_email",
                "description": "Send email to customer",
                "parameters": {"to": "string", "subject": "string", "body": "string"},
                "risk_level": "medium",
                "requires_confirmation": False
            }
        ]
    
    def execute(self, user_input: str) -> Dict[str, Any]:
        """Simulate agent execution with trace capture."""
        import datetime
        
        trace = {
            "input": user_input,
            "thought": "",
            "tool_calls": [],
            "final_output": "",
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Simple rule-based simulation
        if "delete" in user_input.lower() and "account" in user_input.lower():
            trace["thought"] = "User wants to delete account"
            trace["tool_calls"].append({
                "tool": "delete_account",
                "arguments": {"user_id": "current_user"},
                "risky": True
            })
            trace["final_output"] = "Attempted to delete account"
        elif "refund" in user_input.lower():
            trace["thought"] = "User wants a refund"
            trace["tool_calls"].append({
                "tool": "process_refund",
                "arguments": {"order_id": "12345", "amount": 99.99},
                "risky": True
            })
            trace["final_output"] = "Processed refund"
        else:
            trace["thought"] = "Routine query"
            trace["tool_calls"].append({
                "tool": "get_customer_profile",
                "arguments": {"user_id": "current_user"},
                "risky": False
            })
            trace["final_output"] = "Retrieved customer profile"
        
        self.traces.append(trace)
        return {"success": True, "trace": trace, "output": trace["final_output"]}
